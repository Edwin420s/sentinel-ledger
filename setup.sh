#!/bin/bash

# Sentinel Ledger Complete Setup Script

echo "🔧 Setting up Sentinel Ledger..."

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Backend
echo "Setting up backend..."
cd Backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Create environment file
if [ ! -f ".env" ]; then
    echo "Creating backend environment file..."
    cp .env.example .env
    echo "⚠️  Please edit Backend/.env with your RPC URLs and database credentials"
fi

cd ..

# Setup Frontend
echo "Setting up frontend..."
cd Frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Create environment file
if [ ! -f ".env.development" ]; then
    echo "Creating frontend environment file..."
    cp .env.example .env.development
fi

cd ..

# Start databases
echo "Starting databases..."
cd Backend
docker-compose up -d postgres neo4j redis

echo "⏳ Waiting for databases to start..."
sleep 15

# Run database migrations
echo "Running database migrations..."
source venv/bin/activate
alembic upgrade head

cd ..

echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit Backend/.env with your RPC URLs"
echo "2. Start backend: cd Backend && ./start.sh"
echo "3. Start frontend: cd Frontend && ./start.sh"
echo "4. Open http://localhost:3000"
echo ""
echo "📚 Documentation: README.md"
