#!/bin/bash

# Project Judgement - Dev Runner (EXPO VERSION)
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Project Judgement Control Center (Expo) ===${NC}"

# Function to check local Redis
check_redis() {
    if ! lsof -i:6379 > /dev/null; then
        echo -e "${RED}[!] Local Redis is not running.${NC}"
        echo -e "Required for local testing. Run: brew services start redis"
        exit 1
    fi
}

# 1. Setup Backend environment (needed for local server only)
if [ -d "backend/venv" ]; then
    source backend/venv/bin/activate
fi

# 2. Choose Action
echo -e "\nWhat would you like to do?"
echo "1) Start Backend Server (FastAPI - LOCAL)"
echo "2) Start Frontend (LOCAL WiFi - Connects to local Mac)"
echo "3) Start Frontend (TUNNEL - Connects to local Mac via public link)"
echo "4) Start Frontend (TUNNEL - Connects to RAILWAY Global Server)"
echo "q) Quit"
read -p "Selection: " choice

CONST_FILE="frontend/src/core/constants.ts"

case $choice in
    1)
        check_redis
        cd backend && python3 main.py
        ;;
    2)
        cd frontend
        IP=$(ipconfig getifaddr en0)
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'http://$IP:8000'|g" src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'ws://$IP:8000'|g" src/core/constants.ts
        npx expo start -c
        ;;
    3)
        echo -e "${BLUE}[*] Using Tunnel for Frontend. Ensure local backend is running!${NC}"
        cd frontend
        IP=$(ipconfig getifaddr en0)
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'http://$IP:8000'|g" src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'ws://$IP:8000'|g" src/core/constants.ts
        npx expo start --tunnel -c
        ;;
    4)
        read -p "Enter your Railway Backend URL: " RAILWAY_URL
        RAILWAY_URL=${RAILWAY_URL%/}
        DOMAIN=${RAILWAY_URL#*//}
        
        # Set URLs in constants
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: '$RAILWAY_URL'|g" $CONST_FILE
        if [[ $RAILWAY_URL == https* ]]; then
            sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'wss://$DOMAIN'|g" $CONST_FILE
        else
            sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'ws://$DOMAIN'|g" $CONST_FILE
        fi
        
        echo -e "${GREEN}[*] Constants updated to Railway URL: $RAILWAY_URL${NC}"
        cd frontend && npx expo start --tunnel -c
        ;;
    q)
        exit 0
        ;;
esac
