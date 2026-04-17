#!/bin/bash

# Project Judgement - The Final Runner
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Project Judgement Control Center ===${NC}"

# 1. Choose Action
echo -e "\nWhat would you like to do?"
echo "1) Start Local Backend Server (FastAPI)"
echo "2) Run App Locally (WiFi/WiFi - Best for dev)"
echo -e "${GREEN}3) GO LIVE (Push all changes to your friends)${NC}"
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
        echo -e "${GREEN}[*] Pushing latest game code to Global Server...${NC}"
        git add .
        git commit -m "chore: update live game"
        git push origin main
        echo -e "\n${GREEN}=== PUSH COMPLETE ===${NC}"
        echo "Railway is now building your game."
        echo "In 2 minutes, open: https://judgementgame-production.up.railway.app"
        ;;
    q)
        exit 0
        ;;
esac
