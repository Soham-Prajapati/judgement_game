#!/bin/bash

# Project Judgement - APK Builder
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Project Judgement APK Builder ===${NC}"

# 1. Get Local IP
IP=$(ipconfig getifaddr en0)
echo -e "[*] Detected Local IP: ${GREEN}$IP${NC}"

# 2. Update Constants
CONST_FILE="frontend/src/core/constants.ts"
echo -e "[*] Updating $CONST_FILE to use your local IP..."
sed -i '' "s/10.0.2.2/$IP/g" $CONST_FILE

# 3. Build APK
echo -e "[*] Starting Android Build (this may take a few minutes)..."
cd frontend/android
./gradlew assembleDebug

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}=== BUILD SUCCESSFUL ===${NC}"
    echo -e "APK Location: ${BLUE}frontend/android/app/build/outputs/apk/debug/app-debug.apk${NC}"
    echo -e "Transfer this file to your phone to play!"
else
    echo -e "\n${RED}=== BUILD FAILED ===${NC}"
    echo -e "Check the logs above for errors."
fi
