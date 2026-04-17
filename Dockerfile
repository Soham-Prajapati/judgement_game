# Stage 1: Build the Frontend
FROM node:20 as build-stage
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps
COPY frontend/ .
# Build for web
RUN npx expo export --platform web

# Stage 2: Serve with FastAPI
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
# Copy the built frontend from Stage 1 into a 'static' folder in backend
COPY --from=build-stage /frontend/dist ./static

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
