"""4장 규칙의 숫자 기준을 모아 둔 파일입니다.
사용자님이 말로 알려주신 규칙에서 '숫자로 정해지지 않은 부분'은 아래 기본값으로 제가 임의로 정한 것입니다.
기준을 바꾸고 싶으면 이 파일의 숫자만 고치면 됩니다.
"""
from dataclasses import dataclass

MA_LIST = (5, 10, 20, 60, 120, 240, 480)


@dataclass(frozen=True)
class Params:
    # ── 규칙 1: 정배열 + 이평선 지지 상승 ─────────────────────────────
    slope_days: int = 10          # 20일선·60일선이 '10거래일 전보다 높아야' 상승 중으로 본다
    support_lookback: int = 20    # 최근 20거래일 안에
    touch_tol: float = 0.01       # 저가가 20일선 또는 60일선의 +1% 이내까지 내려왔고(터치). 2%로 넓히면 꾸준히 오르기만 한 종목도 다 걸립니다
    break_tol: float = 0.01       # 종가는 그 이평선 아래로 1% 넘게 이탈하지 않았으면 '지지'

    # ── 규칙 2: 급등 후 60일선 조정·지지 ──────────────────────────────
    surge_pct: float = 0.30       # 20거래일 안에 +30% 이상 오른 급등 구간이 있었고
    surge_window: int = 20
    search_days: int = 90         # 그 급등은 최근 90거래일 안에 있었고
    min_days_since_peak: int = 5  # 고점 이후 최소 5거래일은 지났고
    min_drawdown: float = 0.10    # 고점 대비 10% 이상 조정을 받았고
    ma60_touch_days: int = 3      # 최근 3거래일 안에 저가가 60일선 +3% 이내까지 내려왔고
    ma60_touch_tol: float = 0.03
    ma60_break_tol: float = 0.01  # 종가는 60일선 아래로 1% 넘게 이탈하지 않았고
    ma60_slope_days: int = 10     # 60일선 자체는 10거래일 전보다 높아야 한다

    # ── 규칙 3: 거래량 동반 240일선 / 480일선 돌파 ────────────────────
    breakout_days: int = 3        # 최근 3거래일 안에 아래→위로 돌파했고, 지금도 선 위에 있어야 한다
    vol_mult: float = 2.0         # 돌파한 날 거래량이 직전 20일 평균의 2배 이상
    prior_window: int = 20        # 돌파 전 20거래일 중
    prior_below_days: int = 10    # 10일 이상 선 아래에 있었어야 '돌파'로 인정 (선 근처 왔다갔다 제외)

    # ── 공통 필터: 거래가 너무 적은 종목 제외 ─────────────────────────
    min_value_kr: float = 5e8     # 최근 20일 평균 거래대금 5억 원 이상
    min_value_us: float = 5e6     # 최근 20일 평균 거래대금 500만 달러 이상


P = Params()


@dataclass(frozen=True)
class ClosingParams:
    """5장 유형 A '종가배팅주' 기준. 말씀하신 문장에서 숫자가 정해지지 않은 부분은 제가 정한 기본값이니 여기서 고치세요."""
    # 공통 체급 (거래대금은 당일 누적)
    min_value: float = 5e9          # 당일 거래대금 50억 원 이상
    min_price: float = 1000
    # A1: 장 마감 직전 대형 수급 + 당일 고가 마감
    a1_min_pct: float = 2.0         # 전일 대비 +2% 이상
    a1_high_gap: float = 0.005      # 현재가가 당일 고가의 0.5% 이내 (고가 마감 근접)
    a1_late_from: str = "15:00"     # '마감 직전' 구간 시작 (분봉 기준)
    a1_late_share: float = 0.10     # 마감 직전 구간 거래량이 당일 거래량의 10% 이상
    a1_flow_share: float = 0.03     # 외국인+기관 순매수 대금이 당일 거래대금의 3% 이상 (수급 자료가 있을 때)
    # A2: 전일 급등 후 거래량 반토막 + 도지 + 10/20일선 사수
    a2_prev_pct: float = 10.0       # 전일 +10% 이상
    a2_vol_ratio: float = 0.5       # 오늘 거래량이 전일의 50% 이하
    a2_doji_body: float = 0.30      # 도지: 몸통이 (고가-저가)의 30% 이하
    a2_min_range: float = 0.01      # 고가-저가가 시가의 1% 이상 (움직임이 아예 없는 종목 제외)
    # A3: 바닥권 거래대금 폭발 장대양봉 + 240/480일선 돌파
    a3_pos_max: float = 0.45        # 바닥권: 최근 250일 저가~고가 범위의 하단 45% 이하에서 출발 (전일 종가 기준)
    a3_value_mult: float = 3.0      # 거래대금이 최근 20일 평균의 3배 이상
    a3_min_value: float = 1e10      # 그리고 100억 원 이상
    a3_body_pct: float = 6.0        # 장대양봉: 시가 대비 종가 +6% 이상
    a3_body_ratio: float = 0.7      # 몸통이 (고가-저가)의 70% 이상
    a3_cross_margin: float = 0.01   # '강하게' 돌파 = 종가가 240·480일선 위로 1% 이상
    top_n: int = 5


CP = ClosingParams()
