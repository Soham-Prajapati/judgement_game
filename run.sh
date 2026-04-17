#!/bin/bash

# Project Judgement - The "No-Nonsense" Runner
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Project Judgement Control Center ===${NC}"

# 1. Choose Action
echo -e "\nWhat would you like to do?"
echo "1) Start Local Backend Server (FastAPI)"
echo "2) Run App on Phone (WiFi Mode - FASTEST, no ngrok)"
echo "3) Run App on Phone (Tunnel Mode - Use if WiFi fails)"
echo "4) Build Real Mobile App (APK - To send to friends)"
echo "q) Quit"
read -p "Selection: " choice

case $choice in
    1)
        cd backend && source venv/bin/activate && python3 main.py
        ;;
    2)
        # Use Local IP (Same WiFi)
        IP=$(ipconfig getifaddr en0)
        echo -e "${GREEN}[*] Using Local IP: $IP (Ensure phone is on same WiFi)${NC}"
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'http://$IP:8000'|g" frontend/src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'ws://$IP:8000'|g" frontend/src/core/constants.ts
        cd frontend && npx expo start --lan -c
        ;;
    3)
        # Use Tunnel (ngrok)
        echo -e "${BLUE}[*] Starting Tunnel... (Requires 'npx expo login')${NC}"
        cd frontend && npx expo start --tunnel -c
        ;;
    4)
        cd frontend
        echo -e "${GREEN}[*] Starting Cloud Build for APK...${NC}"
        eas build -p android --profile preview
        ;;
    q)
        exit 0
        ;;
esac
