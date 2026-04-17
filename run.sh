#!/bin/bash

# Project Judgement - The "No More Questions" Runner
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Project Judgement Control Center ===${NC}"

# 1. Choose Action
echo -e "\nWhat would you like to do?"
echo "1) Start Local Backend Server (FastAPI)"
echo "2) Run App Locally (WiFi Mode)"
echo "3) Run App Locally (Tunnel Mode)"
echo -e "${GREEN}4) RUN GLOBAL GAME (Connects to your Railway Server)${NC}"
echo "5) Build Web Link (To play in browser)"
echo "q) Quit"
read -p "Selection: " choice

case $choice in
    1)
        cd backend && source venv/bin/activate && python3 main.py
        ;;
    2)
        IP=$(ipconfig getifaddr en0)
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'http://$IP:8000'|g" frontend/src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'ws://$IP:8000'|g" frontend/src/core/constants.ts
        cd frontend && npx expo start -c
        ;;
    3)
        IP=$(ipconfig getifaddr en0)
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'http://$IP:8000'|g" frontend/src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'ws://$IP:8000'|g" frontend/src/core/constants.ts
        cd frontend && npx expo start --tunnel -c
        ;;
    4)
        echo -e "${GREEN}[*] Connecting to: https://judgementgame-production.up.railway.app${NC}"
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'https://judgementgame-production.up.railway.app'|g" frontend/src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'wss://judgementgame-production.up.railway.app'|g" frontend/src/core/constants.ts
        cd frontend && npx expo start --tunnel -c
        ;;
    5)
        echo -e "${GREEN}[*] Building Global Web Version...${NC}"
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'https://judgementgame-production.up.railway.app'|g" frontend/src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'wss://judgementgame-production.up.railway.app'|g" frontend/src/core/constants.ts
        cd frontend && npx expo export --platform web
        echo -e "\n${GREEN}=== BUILD COMPLETE ===${NC}"
        echo "Drag the 'frontend/dist' folder into https://app.netlify.com/drop"
        echo "You will get a website link that works for everyone!"
        ;;
    q)
        exit 0
        ;;
esac
