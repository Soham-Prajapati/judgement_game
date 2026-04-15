#!/bin/bash

# Project Judgement - Dev Runner (EXPO VERSION)
# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Project Judgement Control Center (Expo) ===${NC}"

# 1. Check Redis
if ! lsof -i:6379 > /dev/null; then
    echo -e "${RED}[!] Redis is not running on port 6379.${NC}"
    echo -e "Please start redis-server in another terminal or run: brew services start redis"
    exit 1
fi
echo -e "${GREEN}[✓] Redis is running${NC}"

# 2. Setup Backend if needed
cd backend
if [ ! -d "venv" ]; then
    echo -e "${BLUE}[*] Creating Python virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 3. Choose Action
echo -e "\nWhat would you like to do?"
echo "1) Start Backend Server (FastAPI)"
echo "2) Start Frontend (Expo / Expo Go)"
echo "3) Start Both (Background)"
echo "q) Quit"
read -p "Selection: " choice

case $choice in
    1)
        echo -e "${GREEN}[*] Starting Backend on http://localhost:8000...${NC}"
        python3 main.py
        ;;
    2)
        echo -e "${GREEN}[*] Starting Expo Frontend...${NC}"
        cd ../frontend
        # Set IP for Local Testing if needed
        IP=$(ipconfig getifaddr en0)
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'http://$IP:8000'|g" src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'ws://$IP:8000'|g" src/core/constants.ts
        npx expo start
        ;;
    3)
        echo -e "${GREEN}[*] Starting Backend in background...${NC}"
        python3 main.py > ../backend.log 2>&1 &
        BACKEND_PID=$!
        echo -e "${GREEN}[*] Backend PID: $BACKEND_PID. Logs at backend.log${NC}"
        
        echo -e "${GREEN}[*] Starting Expo Frontend...${NC}"
        cd ../frontend
        IP=$(ipconfig getifaddr en0)
        sed -i '' "s|apiBaseUrl: '.*'|apiBaseUrl: 'http://$IP:8000'|g" src/core/constants.ts
        sed -i '' "s|wsBaseUrl: '.*'|wsBaseUrl: 'ws://$IP:8000'|g" src/core/constants.ts
        npx expo start
        
        echo -e "${BLUE}Press Ctrl+C to stop the backend when finished.${NC}"
        trap "kill $BACKEND_PID; exit" INT
        wait
        ;;
    q)
        exit 0
        ;;
    *)
        echo "Invalid selection"
        ;;
esac
