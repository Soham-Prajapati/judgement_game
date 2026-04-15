#!/bin/bash

# Project Judgement - APK Builder
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Project Judgement APK Builder ===${NC}"

echo "1) Build for LOCAL (My WiFi only)"
echo "2) Build for PRODUCTION (Public Server)"
read -p "Selection: " build_type

CONST_FILE="frontend/src/core/constants.ts"

if [ "$build_type" == "1" ]; then
    IP=$(ipconfig getifaddr en0)
    echo -e "[*] Detected Local IP: ${GREEN}$IP${NC}"
    API_URL="http://$IP:8000"
    WS_URL="ws://$IP:8000"
else
    read -p "Enter your Production URL (e.g., https://your-app.up.railway.app): " PROD_URL
    # Remove trailing slash if any
    PROD_URL=${PROD_URL%/}
    # Extract domain for WS
    DOMAIN=${PROD_URL#*//}
    
    API_URL="$PROD_URL"
    # If https, use wss. If http, use ws.
    if [[ $PROD_URL == https* ]]; then
        WS_URL="wss://$DOMAIN"
    else
        WS_URL="ws://$DOMAIN"
    fi
fi

echo -e "[*] Setting API: ${GREEN}$API_URL${NC}"
echo -e "[*] Setting WS:  ${GREEN}$WS_URL${NC}"

# Update the file
# Using | as delimiter to avoid issues with / in URLs
sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: '$API_URL'|g" $CONST_FILE
sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: '$WS_URL'|g" $CONST_FILE

# 3. Build APK
echo -e "[*] Starting Android Build (this may take a few minutes)..."
cd frontend/android
./gradlew assembleDebug

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}=== BUILD SUCCESSFUL ===${NC}"
    echo -e "APK Location: ${BLUE}frontend/android/app/build/outputs/apk/debug/app-debug.apk${NC}"
    echo -e "Share this file with your friends!"
else
    echo -e "\n${RED}=== BUILD FAILED ===${NC}"
fi
