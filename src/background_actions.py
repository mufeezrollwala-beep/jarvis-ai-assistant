import asyncio
import aiohttp
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta


async def download_file(task, url: str, destination: str, chunk_size: int = 8192):
    dest_path = Path(destination)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(dest_path, 'wb') as f:
                async for chunk in response.content.iter_chunked(chunk_size):
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        from src.task_manager import TaskManager
                        task.progress = progress
    
    return {
        "url": url,
        "destination": str(dest_path),
        "size": downloaded,
        "completed_at": datetime.now()
    }


async def reminder_timer(task, duration_seconds: int, message: str):
    total_seconds = duration_seconds
    elapsed = 0
    
    while elapsed < total_seconds:
        await asyncio.sleep(1)
        elapsed += 1
        task.progress = (elapsed / total_seconds) * 100
    
    return {
        "message": message,
        "duration": duration_seconds,
        "triggered_at": datetime.now()
    }


async def periodic_health_check(task, url: str, interval_seconds: int = 60, max_checks: int = 10):
    results = []
    
    for i in range(max_checks):
        try:
            start_time = datetime.now()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    status = response.status
                    response_time = (datetime.now() - start_time).total_seconds()
                    
                    results.append({
                        "check": i + 1,
                        "status": status,
                        "response_time": response_time,
                        "timestamp": datetime.now(),
                        "success": 200 <= status < 300
                    })
        except Exception as e:
            results.append({
                "check": i + 1,
                "status": None,
                "error": str(e),
                "timestamp": datetime.now(),
                "success": False
            })
        
        task.progress = ((i + 1) / max_checks) * 100
        
        if i < max_checks - 1:
            await asyncio.sleep(interval_seconds)
    
    success_count = sum(1 for r in results if r.get("success", False))
    
    return {
        "url": url,
        "total_checks": max_checks,
        "successful_checks": success_count,
        "results": results
    }


async def batch_web_search(task, queries: list, delay_seconds: float = 1.0):
    results = []
    total = len(queries)
    
    for i, query in enumerate(queries):
        try:
            await asyncio.sleep(delay_seconds)
            
            result = {
                "query": query,
                "timestamp": datetime.now(),
                "success": True
            }
            results.append(result)
            
        except Exception as e:
            results.append({
                "query": query,
                "error": str(e),
                "success": False
            })
        
        task.progress = ((i + 1) / total) * 100
    
    return {
        "total_queries": total,
        "successful": sum(1 for r in results if r.get("success", False)),
        "results": results
    }


async def scheduled_task(task, target_time: datetime, action: callable):
    now = datetime.now()
    
    if target_time > now:
        delay = (target_time - now).total_seconds()
        await asyncio.sleep(delay)
    
    task.progress = 50.0
    
    result = await action(task)
    
    task.progress = 100.0
    
    return {
        "scheduled_for": target_time,
        "executed_at": datetime.now(),
        "action_result": result
    }
