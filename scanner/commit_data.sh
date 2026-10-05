#!/usr/bin/env bash
# 수집 결과(data/, scanner/out/)가 바뀌었으면 main 에 저장합니다. 바뀐 게 없으면 아무것도 하지 않습니다.
set -e
cd "$(dirname "$0")/.."
python scanner/touch_meta.py
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add data scanner/out
if git diff --cached --quiet; then
  echo "변경 없음"
  exit 0
fi
git commit -m "데이터 갱신 $(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')"
for i in 1 2 3 4; do
  if git pull --rebase origin main && git push origin HEAD:main; then
    exit 0
  fi
  sleep $((i * 5))
done
echo "푸시 실패" >&2
exit 1
