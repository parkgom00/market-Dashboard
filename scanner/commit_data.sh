#!/usr/bin/env bash
# 수집 결과(data/, scanner/out/)가 바뀌었으면 main 에 저장합니다. 바뀐 게 없으면 아무것도 하지 않습니다.
# 다른 작업이 그 사이에 같은 파일을 바꿨어도 실패하지 않도록, 최신 main 위에 "이 작업이 만든 파일"을 통째로 다시 올립니다.
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
MSG="데이터 갱신 $(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')"
git commit -q -m "$MSG"
OURS=$(git rev-parse HEAD)
FILES=$(git diff --name-only --diff-filter=AM "$OURS~1" "$OURS")
for i in 1 2 3 4 5 6; do
  git fetch -q origin main
  git reset -q --hard origin/main
  for f in $FILES; do
    git checkout -q "$OURS" -- "$f"
  done
  git add data scanner/out
  if git diff --cached --quiet; then
    echo "최신 main 과 같음"
    exit 0
  fi
  git commit -q -m "$MSG"
  if git push -q origin HEAD:main; then
    echo "저장 완료 (시도 $i)"
    exit 0
  fi
  sleep $((i * 4))
done
echo "푸시 실패" >&2
exit 1
