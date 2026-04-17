#!/bin/bash

# Project Judgement - The "Free Forever" Ultimate Runner
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Project Judgement Final Control Center ===${NC}"

# 1. Choose Action
echo -e "\nWhat would you like to do?"
echo "1) Start Local Backend Server (FastAPI)"
echo "2) Run App Locally (WiFi/Simulator)"
echo -e "${GREEN}3) DEPLOY TO HUGGING FACE (Free Forever Hosting)${NC}"
echo "4) Build APK for Phone (Cloud Build)"
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
        cd frontend && npx expo start --lan -c
        ;;
    3)
        read -p "Enter your Hugging Face Space URL (e.g. hf.co/spaces/user/name): " URL
        # Logic to convert URL to sub-domain format if needed
        # Format: user-name.hf.space
        # We can extract it from the URL or just ask the user for the "Direct Link"
        echo -e "${BLUE}[*] Tip: Use the 'Direct Link' from your HF Space settings.${NC}"
        read -p "Enter your HF Direct Domain (e.g. user-name.hf.space): " DOMAIN
        
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'https://$DOMAIN'|g" frontend/src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'wss://$DOMAIN'|g" frontend/src/core/constants.ts
        
        echo -e "${GREEN}[*] Constants updated to Hugging Face URL.${NC}"
        git add .
        git commit -m "deploy: final configuration for hugging face global play"
        git push origin main
        echo -e "\n${GREEN}=== PUSH COMPLETE ===${NC}"
        echo "Hugging Face is now building your game."
        echo "Check your HF Space build logs and app URL."
        ;;
    4)
        cd frontend && eas build -p android --profile preview
        ;;
    q)
        exit 0
        ;;
esac
