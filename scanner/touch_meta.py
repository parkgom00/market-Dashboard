"""data/meta.js 의 '마지막 갱신' 시각을 지금(한국시간)으로 바꿉니다."""
import os
from datetime import datetime, timedelta, timezone

TARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "meta.js")
KST = timezone(timedelta(hours=9))


def main():
    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write("// 대시보드 공통 정보 (scanner/touch_meta.py 가 갱신 시각을 자동으로 바꿉니다).\n")
        f.write("window.DASH = window.DASH || {};\n")
        f.write('window.DASH.meta = {\n  title: "마켓 대시보드",\n  updatedAt: "%s",\n  isSample: false // 탭별 샘플 표시는 각 data 파일의 sample: true 로 합니다\n};\n' % now)


if __name__ == "__main__":
    main()
    print("meta 갱신")
