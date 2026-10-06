"""가격 데이터 수집 (사용자 PC에서 실행). 이 작업 환경에서는 외부 사이트가 막혀 있어 직접 시험하지 못했습니다.

- 국내: FinanceDataReader (코스피+코스닥 전 종목, 수정주가)
- 미국: yfinance (기본 S&P 500 구성종목, 수정주가)
"""
import datetime as dt
import time

import pandas as pd

COLS = {"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"}


def _norm(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=COLS)[["open", "high", "low", "close", "volume"]].copy()
    df = df.dropna(subset=["close"])
    df = df[df["volume"] > 0]  # 거래정지일 제거
    df.index = pd.to_datetime(df.index)
    return df.sort_index()


def start_date(years: float = 3.2) -> str:
    return (dt.date.today() - dt.timedelta(days=int(365 * years))).isoformat()


def kr_universe() -> pd.DataFrame:
    import FinanceDataReader as fdr
    lst = fdr.StockListing("KRX")
    lst = lst[lst["Market"].isin(["KOSPI", "KOSDAQ"])].copy()
    lst["Sector"] = ""
    try:   # 업종 정보는 'KRX-DESC' 목록에만 있음 (실패해도 나머지는 정상 동작)
        d = fdr.StockListing("KRX-DESC")
        col = "Industry" if "Industry" in d.columns else ("Sector" if "Sector" in d.columns else None)
        if col:
            lst["Sector"] = lst["Code"].map(dict(zip(d["Code"], d[col].fillna("")))).fillna("")
    except Exception:
        pass
    if "Marcap" not in lst.columns:
        lst["Marcap"] = 0
    out = lst[["Code", "Name", "Market", "Marcap", "Sector"]]
    return out.rename(columns={"Code": "code", "Name": "name", "Market": "market", "Marcap": "marcap", "Sector": "sector"}).reset_index(drop=True)


def kr_prices(codes, workers: int = 4):
    """종목코드별 DataFrame 을 하나씩 내보내는 제너레이터."""
    import FinanceDataReader as fdr
    from concurrent.futures import ThreadPoolExecutor

    start = start_date()
    kst = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    # 장 마감(15:30) 전에 실행하면 오늘 일봉은 아직 진행 중 → 판정에 쓰면 안 되므로 버린다
    drop_today = kst.date() if (kst.hour, kst.minute) < (15, 40) else None

    def one(code):
        for attempt in range(3):
            try:
                df = _norm(fdr.DataReader(code, start))
                if drop_today and len(df) and df.index[-1].date() >= drop_today:
                    df = df[df.index.date < drop_today]
                return code, df
            except Exception:
                time.sleep(1 + attempt)
        return code, None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for code, df in ex.map(one, codes):
            if df is not None and len(df):
                yield code, df


def nasdaq100() -> pd.DataFrame:
    """나스닥 100 구성종목 (code, name). 나스닥 공식 API 우선, 실패하면 위키백과 표. 둘 다 실패하면 빈 표."""
    import json
    import urllib.request
    try:
        req = urllib.request.Request("https://api.nasdaq.com/api/quote/list-type/nasdaq100",
                                     headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125 Safari/537.36",
                                              "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            rows = json.loads(r.read().decode())["data"]["data"]["rows"]
        df = pd.DataFrame([{"code": str(x["symbol"]).strip(), "name": str(x.get("companyName") or x["symbol"]).strip()}
                           for x in rows if x.get("symbol")])
        if len(df) >= 90:
            return df
    except Exception as e:
        print("나스닥 100 (공식 API) 실패:", type(e).__name__, e)
    try:
        for t in pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100"):
            cols = {str(c).lower(): c for c in t.columns}
            sym = cols.get("ticker") or cols.get("symbol")
            if sym is not None and 90 <= len(t) <= 110:
                name = cols.get("company") or sym
                return pd.DataFrame({"code": t[sym].astype(str), "name": t[name].astype(str)})
    except Exception as e:
        print("나스닥 100 (위키백과) 실패:", type(e).__name__, e)
    return pd.DataFrame(columns=["code", "name"])


def merge_us(sp: pd.DataFrame, ndx: pd.DataFrame) -> pd.DataFrame:
    """S&P 500 + 나스닥 100 (겹치는 종목은 한 번만). 야후 표기로 통일."""
    both = pd.concat([sp, ndx], ignore_index=True)
    both["code"] = both["code"].astype(str).str.strip().str.replace(".", "-", regex=False).str.replace("/", "-", regex=False)
    return both.drop_duplicates("code").reset_index(drop=True)


def us_universe() -> pd.DataFrame:
    import FinanceDataReader as fdr
    lst = fdr.StockListing("S&P500")
    lst = lst[["Symbol", "Name"]].rename(columns={"Symbol": "code", "Name": "name"})
    ndx = nasdaq100()
    out = merge_us(lst, ndx)   # BRK.B -> BRK-B (야후 표기)
    print(f"미국 스캔 대상: S&P 500 {len(lst)}개 + 나스닥 100 {len(ndx)}개 → 중복 제외 {len(out)}개")
    return out


def us_prices(codes, batch: int = 50):
    import yfinance as yf

    codes = list(codes)
    for i in range(0, len(codes), batch):
        chunk = codes[i:i + batch]
        try:
            data = yf.download(chunk, period="3y", auto_adjust=True, group_by="ticker",
                               progress=False, threads=True)
        except Exception:
            continue
        for c in chunk:
            try:
                sub = data[c] if len(chunk) > 1 else data
                sub = _norm(sub)
                if len(sub):
                    yield c, sub
            except Exception:
                continue
        time.sleep(1)
