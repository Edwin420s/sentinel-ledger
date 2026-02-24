# Sentinel Ledger - Complete Startup Guide

This guide will walk you through setting up and running the complete Sentinel Ledger system.

## 🚀 Quick Start (One Command)

```bash
# Run the setup script
./setup.sh

# Start backend
cd Backend && ./start.sh

# Start frontend (in new terminal)
cd Frontend && ./start.sh
```

## 📋 Detailed Steps

### Step 1: Prerequisites

Ensure you have installed:
- **Python 3.9+**
- **Node.js 16+**
- **Docker & Docker Compose**
- **Git**

### Step 2: Initial Setup

```bash
# Clone and navigate to project
cd /home/skywalker/Projects/prj/sentinel-ledger

# Run the automated setup
./setup.sh
```

This will:
- Create Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Create environment files
- Start databases (PostgreSQL, Neo4j, Redis)
- Run database migrations

### Step 3: Configure Environment

Edit the following files with your settings:

**Backend Configuration** (`Backend/.env`):
```bash
# Add your RPC URLs
BASE_RPC_URL=https://mainnet.base.org
ETH_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# Database settings (should work with defaults)
POSTGRES_HOST=localhost
POSTGRES_DB=sentinel
POSTGRES_USER=sentinel_user
POSTGRES_PASSWORD=strong_password

# Neo4j settings
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=strong_password

# Optional: OpenRouter for AI explanations
OPENROUTER_API_KEY=your_key_here
```

**Frontend Configuration** (`Frontend/.env.development`):
```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
```

### Step 4: Start Services

#### Option A: Using Startup Scripts (Recommended)

**Backend** (Terminal 1):
```bash
cd Backend
./start.sh
```

**Frontend** (Terminal 2):
```bash
cd Frontend
./start.sh
```

#### Option B: Manual Start

**Backend**:
```bash
cd Backend

# Start databases
docker-compose up -d postgres neo4j redis

# Activate virtual environment
source venv/bin/activate

# Run migrations
alembic upgrade head

# Start API server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Start indexer (in another terminal)
python -m indexer.run
```

**Frontend**:
```bash
cd Frontend
npm run dev
```

### Step 5: Seed Sample Data (Optional)

To test with sample data:

```bash
cd Backend
source venv/bin/activate
python seed_data.py
```

### Step 6: Verify Installation

1. **Backend API**: Visit http://localhost:8000/docs
2. **Frontend**: Visit http://localhost:3000
3. **API Test**: Run `python test_api.py`
4. **Neo4j Browser**: Visit http://localhost:7474

## 🔧 Troubleshooting

### Database Connection Issues

```bash
# Check if databases are running
docker-compose ps

# Restart databases
docker-compose restart postgres neo4j redis

# Check logs
docker-compose logs postgres
```

### Port Conflicts

If ports are already in use:
- Backend API: Change port 8000 in start.sh
- Frontend: Change port 3000 in vite.config.js
- PostgreSQL: Change port 5432 in docker-compose.yml

### Python Dependencies

```bash
# If you get import errors
cd Backend
source venv/bin/activate
pip install -r requirements.txt
```

### Node.js Dependencies

```bash
# If frontend fails to start
cd Frontend
rm -rf node_modules package-lock.json
npm install
```

## 📊 Access Points

Once running:

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main application |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| API Base | http://localhost:8000/api/v1 | REST API endpoint |
| Health Check | http://localhost:8000/health | Service status |
| Neo4j Browser | http://localhost:7474 | Graph database interface |

## 🧪 Testing

### Test API Connection
```bash
cd Backend
python test_api.py
```

### Test Frontend Connection
- Open http://localhost:3000
- The API Test component will show connection status
- Check browser console for any errors

## 🏗 Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │     API         │    │   Indexer       │
│   (React)       │◄──►│   (FastAPI)    │◄──►│   (Python)      │
│   Port: 3000   │    │   Port: 8000   │    │   Background    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Databases     │
                       │ PostgreSQL      │
                       │ Neo4j          │
                       │ Redis           │
                       └─────────────────┘
```

## 📝 Development Notes

- The API Test component only shows in development mode
- All services restart automatically on file changes
- Database migrations are handled by Alembic
- Logs are written to `Backend/logs/`

## 🆘 Getting Help

If you encounter issues:

1. Check the logs in each terminal
2. Verify all environment variables are set
3. Ensure Docker containers are running
4. Check that ports are not blocked by firewall
5. Review the troubleshooting section above

## 🎯 Next Steps

Once everything is running:

1. Explore the API documentation at `/docs`
2. Test the frontend dashboard
3. Add your own RPC URLs for real data
4. Configure OpenRouter for AI explanations
5. Deploy to production when ready

Happy building! 🚀
