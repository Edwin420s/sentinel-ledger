#!/bin/bash

# Sentinel Ledger Backend Startup Script

echo "🚀 Starting Sentinel Ledger Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if requirements.txt is newer
if [ requirements.txt -nt venv/pyvenv.cfg ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start database services
echo "Starting database services..."
docker-compose up -d postgres neo4j redis

# Wait for databases to be ready
echo "Waiting for databases..."
sleep 10

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start API server in background
echo "Starting API server..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# Start indexer in background
echo "Starting indexer..."
python -m indexer.run &
INDEXER_PID=$!

echo "✅ Backend started!"
echo "API Server: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Neo4j Browser: http://localhost:7474"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt signal
trap "echo 'Stopping services...'; kill $API_PID $INDEXER_PID; docker-compose stop; exit" INT
wait
