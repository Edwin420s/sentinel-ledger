import asyncio
import logging
from typing import Dict, Any
from datetime import datetime, timedelta

from tasks.job_runner import JobRunner

logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self):
        self.jobs = {}
        self.running = False
        self.job_runner = JobRunner()
    
    def add_job(self, name: str, interval_seconds: int, func, *args, **kwargs):
        """Add a scheduled job"""
        self.jobs[name] = {
            "interval": interval_seconds,
            "func": func,
            "args": args,
            "kwargs": kwargs,
            "last_run": None
        }
        logger.info(f"Added job: {name} (every {interval_seconds}s)")
    
    async def run_job(self, name: str, job_config: Dict):
        """Run a single job"""
        try:
            logger.info(f"Running job: {name}")
            await job_config["func"](*job_config["args"], **job_config["kwargs"])
            job_config["last_run"] = datetime.utcnow()
            logger.info(f"Completed job: {name}")
        except Exception as e:
            logger.error(f"Job {name} failed: {e}")
    
    async def run_forever(self):
        """Run scheduler forever"""
        self.running = True
        
        # Initialize jobs
        for name, config in self.jobs.items():
            config["last_run"] = datetime.utcnow()
        
        logger.info("Scheduler started")
        
        while self.running:
            now = datetime.utcnow()
            
            for name, config in self.jobs.items():
                last_run = config["last_run"]
                interval = config["interval"]
                
                if not last_run or (now - last_run).total_seconds() >= interval:
                    asyncio.create_task(self.run_job(name, config))
            
            await asyncio.sleep(1)
    
    def stop(self):
        """Stop scheduler"""
        self.running = False
        logger.info("Scheduler stopped")