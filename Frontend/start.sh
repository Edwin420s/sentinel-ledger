#!/bin/bash

# Sentinel Ledger Frontend Startup Script

echo "🚀 Starting Sentinel Ledger Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Create environment file if it doesn't exist
if [ ! -f ".env.development" ]; then
    echo "Creating environment file..."
    cp .env.example .env.development
fi

# Start development server
echo "Starting development server..."
npm run dev

echo "✅ Frontend started!"
echo "Application: http://localhost:3000"
