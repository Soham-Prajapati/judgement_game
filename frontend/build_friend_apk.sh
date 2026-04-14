#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: ./build_friend_apk.sh <API_BASE_URL> <WS_BASE_URL>"
  echo "Example: ./build_friend_apk.sh https://judgement-api.example.com wss://judgement-api.example.com"
  exit 1
fi

API_BASE_URL="$1"
WS_BASE_URL="$2"

if [[ -z "${JAVA_HOME:-}" ]]; then
  if [[ -d "/Applications/Android Studio.app/Contents/jbr/Contents/Home" ]]; then
    export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
  elif command -v /usr/libexec/java_home >/dev/null 2>&1; then
    JAVA_CANDIDATE="$(/usr/libexec/java_home 2>/dev/null || true)"
    if [[ -n "$JAVA_CANDIDATE" ]]; then
      export JAVA_HOME="$JAVA_CANDIDATE"
    fi
  fi
fi

if [[ -n "${JAVA_HOME:-}" ]]; then
  export PATH="$JAVA_HOME/bin:$PATH"
fi

if ! command -v java >/dev/null 2>&1; then
  echo "Java runtime not found in this shell."
  echo "Open Android Studio once or set JAVA_HOME, then run again."
  exit 1
fi

flutter pub get
flutter test
flutter build apk --release \
  --dart-define=API_BASE_URL="$API_BASE_URL" \
  --dart-define=WS_BASE_URL="$WS_BASE_URL"

echo "APK generated at: build/app/outputs/flutter-apk/app-release.apk"
