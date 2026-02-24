#!/usr/bin/env python3
"""
Debug endpoint to test database connection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import APIRouter
from sqlalchemy import text
from db.session import get_db

router = APIRouter()

@router.get("/debug")
async def debug_db():
    """Debug database connection"""
    try:
        from db.session import engine
        with engine.connect() as conn:
            # Test basic query
            result = conn.execute(text("SELECT COUNT(*) FROM tokens"))
            count = result.scalar()
            
            # Test table existence
            tables = conn.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_list = [row[0] for row in tables]
            
            return {
                "status": "success",
                "database_url": str(engine.url),
                "token_count": count,
                "tables": table_list,
                "message": "Database connection working"
            }
    except Exception as e:
        return {
            "status": "error", 
            "error": str(e),
            "message": "Database connection failed"
        }
