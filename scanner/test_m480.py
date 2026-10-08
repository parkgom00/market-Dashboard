"""단기 유형 C(480분선 지지) 판정 검증. 실행: python test_m480.py"""
import datetime as dt
import collect_m480 as m

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

def build(side_price, side_n=25, rise=0.18, wob=5):
    bars = []
    def add(day, closes):
        t = dt.datetime.strptime(day + "0900", "%Y%m%d%H%M")
        for i, c in enumerate(closes):
            tt = t + dt.timedelta(minutes=i)
            bars.append((day, tt.strftime("%H%M"), c, c * 1.001, c * 0.999, c, 1000.0))
    add("20261006", [10000] * 391); add("20261007", [10000] * 391)
    up = [10000 * (1 + rise * i / 10) for i in range(1, 11)]
    top = up[-1]
    down = [top - (top - side_price) * i / 30 for i in range(1, 31)]
    side = [side_price + (wob if i % 2 else -wob) for i in range(side_n)]
    add("20261008", up + down + side)
    return bars

b = build(10150)
d, why = m.judge(b, "20261008")
check("+18% 급등 후 480분선 근처에서 횡보 → 해당", d is not None and d["rise"] >= 15 and d["side"] >= 3)
check("설명 문구", d is not None and "480분선" in m.note(d) and "횡보" in m.note(d))
check("480분선보다 아직 2% 넘게 위 → 비해당", m.judge(build(10400), "20261008")[1] == "480분선보다 아직 높음")
check("480분선 아래로 이탈 → 비해당", m.judge(build(9900), "20261008")[1] == "480분선 이탈")
check("장중 +10%만 올랐던 종목 → 비해당", m.judge(build(10100, rise=0.10), "20261008")[1] == "장중 +15% 미달")
check("내려오는 중(횡보 없음) → 비해당", m.judge(b, "20261008", upto="0935")[0] is None)
check("출렁임이 크면 횡보 아님", m.judge(build(10150, wob=150), "20261008")[0] is None)
K = m.KST
check("회차: 10:02 → 10:00", m.due_slot(dt.datetime(2026, 10, 8, 10, 2, tzinfo=K), "") == "10:00")
check("회차: 이미 한 회차는 다시 안 함", m.due_slot(dt.datetime(2026, 10, 8, 10, 29, tzinfo=K), "10:00") is None)
check("회차: 10:31 → 10:30", m.due_slot(dt.datetime(2026, 10, 8, 10, 31, tzinfo=K), "10:00") == "10:30")
check("회차: 10시 전·14:50 후에는 없음", m.due_slot(dt.datetime(2026, 10, 8, 9, 40, tzinfo=K), "") is None and m.due_slot(dt.datetime(2026, 10, 8, 14, 55, tzinfo=K), "14:00") is None)
check("회차: 오후 14:31 → 14:30", m.due_slot(dt.datetime(2026, 10, 8, 14, 31, tzinfo=K), "14:00") == "14:30")
far = build(10400)                       # 480분선 위 약 +3%: 조건 미충족이지만 '접근 중'
check("접근 중: 480분선 위 5% 이내", m.approaching(far, "20261008") is not None and "남음" in m.note_near(m.approaching(far, "20261008")))
check("접근 중: 조건 충족 종목은 접근 목록에 안 넣음", m.approaching(b, "20261008") is None)
check("접근 중: 8% 위는 제외", m.approaching(build(10900), "20261008") is None)
check("접근 중: 480분선 이탈은 제외", m.approaching(build(9900), "20261008") is None)
uni = {"000010": {"name": "가", "market": "KOSDAQ", "marcap": 1e11, "value": 5e10}, "000030": {"name": "나"}}
rows, near, diag = m.evaluate(["000010", "000020", "000030"], uni, "20261008", fetch=lambda c, t: b if c == "000010" else far if c == "000030" else [])
check("evaluate: 충족 1개 · 접근 중 1개", len(rows) == 1 and rows[0]["name"] == "가" and len(near) == 1 and near[0]["name"] == "나")
print(m.note(d) if d else why)
print(f"{sum(ok)}/{len(ok)}")
raise SystemExit(0 if all(ok) else 1)
