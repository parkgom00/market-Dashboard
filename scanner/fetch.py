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
    lst = lst[lst["Market"].isin(["KOSPI", "KOSDAQ"])]
    return lst[["Code", "Name"]].rename(columns={"Code": "code", "Name": "name"}).reset_index(drop=True)


def kr_prices(codes, workers: int = 4):
    """종목코드별 DataFrame 을 하나씩 내보내는 제너레이터."""
    import FinanceDataReader as fdr
    from concurrent.futures import ThreadPoolExecutor

    start = start_date()

    def one(code):
        for attempt in range(3):
            try:
                return code, _norm(fdr.DataReader(code, start))
            except Exception:
                time.sleep(1 + attempt)
        return code, None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for code, df in ex.map(one, codes):
            if df is not None and len(df):
                yield code, df


def us_universe() -> pd.DataFrame:
    import FinanceDataReader as fdr
    lst = fdr.StockListing("S&P500")
    lst = lst[["Symbol", "Name"]].rename(columns={"Symbol": "code", "Name": "name"})
    lst["code"] = lst["code"].str.replace(".", "-", regex=False)  # BRK.B -> BRK-B (야후 표기)
    return lst.reset_index(drop=True)


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
