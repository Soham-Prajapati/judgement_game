#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: ./build_friend_apk.sh <API_BASE_URL> <WS_BASE_URL>"
  echo "Example: ./build_friend_apk.sh https://judgement-api.example.com wss://judgement-api.example.com"
  exit 1
fi

API_BASE_URL="$1"
WS_BASE_URL="$2"

export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"

flutter pub get
flutter test
flutter build apk --release \
  --dart-define=API_BASE_URL="$API_BASE_URL" \
  --dart-define=WS_BASE_URL="$WS_BASE_URL"

echo "APK generated at: build/app/outputs/flutter-apk/app-release.apk"
