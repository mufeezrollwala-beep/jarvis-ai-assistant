import asyncio
import uuid
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Any, Optional, Dict, List
from threading import Lock
import traceback


class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    id: str
    name: str
    coroutine: Callable
    state: TaskState = TaskState.PENDING
    priority: int = 0
    progress: float = 0.0
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    asyncio_task: Optional[asyncio.Task] = None
    
    def __lt__(self, other):
        return self.priority > other.priority


class TaskManager:
    def __init__(self, max_concurrent_tasks: int = 5):
        self.tasks: Dict[str, Task] = {}
        self.max_concurrent_tasks = max_concurrent_tasks
        self.lock = Lock()
        self.event_callbacks: List[Callable] = []
        self.running = False
        self.task_group: Optional[asyncio.TaskGroup] = None
        
    def add_event_callback(self, callback: Callable):
        self.event_callbacks.append(callback)
        
    def remove_event_callback(self, callback: Callable):
        if callback in self.event_callbacks:
            self.event_callbacks.remove(callback)
            
    async def _notify_event(self, task: Task, event_type: str):
        for callback in self.event_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(task, event_type)
                else:
                    callback(task, event_type)
            except Exception as e:
                print(f"Error in event callback: {e}")
    
    def create_task(self, name: str, coroutine: Callable, priority: int = 0) -> str:
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=name,
            coroutine=coroutine,
            priority=priority
        )
        
        with self.lock:
            self.tasks[task_id] = task
            
        return task_id
    
    async def _execute_task(self, task_id: str):
        with self.lock:
            if task_id not in self.tasks:
                return
            task = self.tasks[task_id]
            task.state = TaskState.RUNNING
            task.started_at = datetime.now()
        
        await self._notify_event(task, "started")
        
        try:
            result = await task.coroutine(task)
            
            with self.lock:
                task.state = TaskState.COMPLETED
                task.result = result
                task.progress = 100.0
                task.completed_at = datetime.now()
                
            await self._notify_event(task, "completed")
            
        except asyncio.CancelledError:
            with self.lock:
                task.state = TaskState.CANCELLED
                task.completed_at = datetime.now()
            await self._notify_event(task, "cancelled")
            
        except Exception as e:
            with self.lock:
                task.state = TaskState.FAILED
                task.error = str(e)
                task.completed_at = datetime.now()
                
            print(f"Task {task.name} failed: {e}")
            traceback.print_exc()
            await self._notify_event(task, "failed")
    
    def get_task(self, task_id: str) -> Optional[Task]:
        with self.lock:
            return self.tasks.get(task_id)
    
    def list_tasks(self, state: Optional[TaskState] = None) -> List[Task]:
        with self.lock:
            tasks = list(self.tasks.values())
            if state:
                tasks = [t for t in tasks if t.state == state]
            return sorted(tasks, key=lambda t: t.created_at, reverse=True)
    
    def cancel_task(self, task_id: str) -> bool:
        with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
                
            if task.state in [TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED]:
                return False
                
            if task.asyncio_task and not task.asyncio_task.done():
                task.asyncio_task.cancel()
                return True
                
            task.state = TaskState.CANCELLED
            return True
    
    def set_priority(self, task_id: str, priority: int) -> bool:
        with self.lock:
            task = self.tasks.get(task_id)
            if task and task.state == TaskState.PENDING:
                task.priority = priority
                return True
            return False
    
    def update_progress(self, task_id: str, progress: float):
        with self.lock:
            task = self.tasks.get(task_id)
            if task:
                task.progress = min(100.0, max(0.0, progress))
    
    async def run_tasks(self):
        self.running = True
        
        while self.running:
            pending_tasks = self.list_tasks(TaskState.PENDING)
            running_tasks = self.list_tasks(TaskState.RUNNING)
            
            available_slots = self.max_concurrent_tasks - len(running_tasks)
            
            if available_slots > 0 and pending_tasks:
                tasks_to_start = sorted(pending_tasks, key=lambda t: t.priority, reverse=True)[:available_slots]
                
                for task in tasks_to_start:
                    asyncio_task = asyncio.create_task(self._execute_task(task.id))
                    with self.lock:
                        task.asyncio_task = asyncio_task
            
            await asyncio.sleep(0.1)
    
    def stop(self):
        self.running = False
        
        with self.lock:
            for task in self.tasks.values():
                if task.state == TaskState.RUNNING and task.asyncio_task:
                    task.asyncio_task.cancel()
    
    def get_stats(self) -> Dict[str, int]:
        with self.lock:
            return {
                "total": len(self.tasks),
                "pending": len([t for t in self.tasks.values() if t.state == TaskState.PENDING]),
                "running": len([t for t in self.tasks.values() if t.state == TaskState.RUNNING]),
                "completed": len([t for t in self.tasks.values() if t.state == TaskState.COMPLETED]),
                "failed": len([t for t in self.tasks.values() if t.state == TaskState.FAILED]),
                "cancelled": len([t for t in self.tasks.values() if t.state == TaskState.CANCELLED])
            }
