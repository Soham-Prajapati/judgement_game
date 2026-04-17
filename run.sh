#!/bin/bash

# Project Judgement - The "Simulator-Ready" Runner
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Project Judgement Control Center ===${NC}"

# 1. Choose Action
echo -e "\nWhat would you like to do?"
echo "1) Start Local Backend Server (FastAPI)"
echo "2) Run Locally (Best for SIMULATOR/WiFi)"
echo "3) Run Global (Connect to Railway)"
echo "q) Quit"
read -p "Selection: " choice

case $choice in
    1)
        cd backend && source venv/bin/activate && python3 main.py
        ;;
    2)
        # Use localhost for Simulator, fallback to IP for WiFi
        echo -e "${GREEN}[*] Configuring for Local Simulator/WiFi...${NC}"
        # We set it to localhost because iPhone simulator shares Mac network
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'http://localhost:8000'|g" frontend/src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'ws://localhost:8000'|g" frontend/src/core/constants.ts
        cd frontend && npx expo start --lan -c
        ;;
    3)
        echo -e "${GREEN}[*] Connecting to RAILWAY Server...${NC}"
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'https://judgementgame-production.up.railway.app'|g" frontend/src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'wss://judgementgame-production.up.railway.app'|g" frontend/src/core/constants.ts
        cd frontend && npx expo start --tunnel -c
        ;;
    q)
        exit 0
        ;;
esac
