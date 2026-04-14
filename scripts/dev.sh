#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Starting Judgement backend..."

cd "$REPO_ROOT/backend"
if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!

cleanup() {
  echo "Stopping backend..."
  kill "$API_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Backend: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo ""
echo "Run Flutter now:"
echo "cd $REPO_ROOT/frontend"
echo "flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000 --dart-define=WS_BASE_URL=ws://10.0.2.2:8000"
echo ""
echo "Press Ctrl+C to stop backend"
wait "$API_PID"
