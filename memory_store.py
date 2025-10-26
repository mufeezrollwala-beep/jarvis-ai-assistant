import json
import sqlite3
import time
from collections import deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class ShortTermMemory:
    def __init__(self, max_size: int = 50, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.memory = deque(maxlen=max_size)
    
    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        timestamp = time.time()
        entry = {
            'text': text,
            'timestamp': timestamp,
            'metadata': metadata or {}
        }
        self.memory.append(entry)
    
    def get_recent(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        current_time = time.time()
        cutoff_time = current_time - self.ttl_seconds
        
        valid_memories = [
            entry for entry in self.memory 
            if entry['timestamp'] >= cutoff_time
        ]
        
        if limit:
            return list(valid_memories[-limit:])
        return list(valid_memories)
    
    def clear_expired(self):
        current_time = time.time()
        cutoff_time = current_time - self.ttl_seconds
        
        self.memory = deque(
            (entry for entry in self.memory if entry['timestamp'] >= cutoff_time),
            maxlen=self.max_size
        )
    
    def get_context_string(self, limit: Optional[int] = None) -> str:
        recent_memories = self.get_recent(limit)
        if not recent_memories:
            return ""
        
        context_parts = []
        for entry in recent_memories:
            timestamp_str = datetime.fromtimestamp(entry['timestamp']).strftime('%H:%M:%S')
            context_parts.append(f"[{timestamp_str}] {entry['text']}")
        
        return "\n".join(context_parts)
    
    def clear(self):
        self.memory.clear()


class LongTermMemory:
    def __init__(self, persist_directory: str = "./memory_data/chroma"):
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        try:
            self.collection = self.client.get_collection(name="jarvis_memories")
        except:
            self.collection = self.client.create_collection(
                name="jarvis_memories",
                metadata={"hnsw:space": "cosine"}
            )
        
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        doc_id = f"mem_{int(time.time() * 1000000)}"
        
        metadata = metadata or {}
        metadata['timestamp'] = time.time()
        metadata['created_at'] = datetime.now().isoformat()
        
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
    
    def search(self, query: str, limit: int = 5, filter_dict: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        where = filter_dict if filter_dict else None
        
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where=where
        )
        
        memories = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                memory = {
                    'text': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                }
                memories.append(memory)
        
        return memories
    
    def get_all(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        results = self.collection.get()
        
        memories = []
        if results['documents']:
            for i, doc in enumerate(results['documents']):
                memory = {
                    'id': results['ids'][i],
                    'text': doc,
                    'metadata': results['metadatas'][i] if results['metadatas'] else {}
                }
                memories.append(memory)
        
        if limit:
            memories = memories[:limit]
        
        return memories
    
    def prune_old(self, days: int = 30, category: Optional[str] = None):
        cutoff_timestamp = time.time() - (days * 24 * 3600)
        
        all_memories = self.get_all()
        ids_to_delete = []
        
        for memory in all_memories:
            metadata = memory.get('metadata', {})
            timestamp = metadata.get('timestamp', 0)
            mem_category = metadata.get('category', '')
            
            if timestamp < cutoff_timestamp:
                if category is None or mem_category == category:
                    ids_to_delete.append(memory['id'])
        
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
        
        return len(ids_to_delete)
    
    def delete_by_category(self, category: str):
        all_memories = self.get_all()
        ids_to_delete = []
        
        for memory in all_memories:
            metadata = memory.get('metadata', {})
            if metadata.get('category') == category:
                ids_to_delete.append(memory['id'])
        
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
        
        return len(ids_to_delete)
    
    def clear(self):
        self.client.delete_collection(name="jarvis_memories")
        self.collection = self.client.create_collection(
            name="jarvis_memories",
            metadata={"hnsw:space": "cosine"}
        )


class MemoryStore:
    def __init__(self, persist_directory: str = "./memory_data"):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(persist_directory=str(self.persist_directory / "chroma"))
        
        self.db_path = self.persist_directory / "metadata.db"
        self._init_metadata_db()
    
    def _init_metadata_db(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at REAL NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_sessions (
                session_id TEXT PRIMARY KEY,
                started_at REAL NOT NULL,
                ended_at REAL,
                summary TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completed_tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                completed_at REAL NOT NULL,
                result TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_conversation(self, user_text: str, assistant_text: str, metadata: Optional[Dict[str, Any]] = None):
        self.short_term.add(f"User: {user_text}", metadata)
        self.short_term.add(f"Assistant: {assistant_text}", metadata)
        
        conversation_entry = f"User: {user_text}\nAssistant: {assistant_text}"
        conv_metadata = metadata or {}
        conv_metadata['type'] = 'conversation'
        self.long_term.add(conversation_entry, conv_metadata)
    
    def add_user_preference(self, key: str, value: str):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, value, time.time()))
        
        conn.commit()
        conn.close()
        
        self.long_term.add(
            f"User preference: {key} = {value}",
            {'category': 'preference', 'key': key}
        )
    
    def get_user_preference(self, key: str) -> Optional[str]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM user_preferences WHERE key = ?', (key,))
        result = cursor.fetchone()
        
        conn.close()
        
        return result[0] if result else None
    
    def get_all_preferences(self) -> Dict[str, str]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('SELECT key, value FROM user_preferences')
        results = cursor.fetchall()
        
        conn.close()
        
        return {key: value for key, value in results}
    
    def add_task(self, description: str, result: Optional[str] = None):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO completed_tasks (description, completed_at, result)
            VALUES (?, ?, ?)
        ''', (description, time.time(), result))
        
        conn.commit()
        conn.close()
        
        task_text = f"Completed task: {description}"
        if result:
            task_text += f" - Result: {result}"
        
        self.long_term.add(task_text, {'category': 'task', 'description': description})
    
    def get_recent_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT task_id, description, completed_at, result
            FROM completed_tasks
            ORDER BY completed_at DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        tasks = []
        for row in results:
            tasks.append({
                'task_id': row[0],
                'description': row[1],
                'completed_at': datetime.fromtimestamp(row[2]).isoformat(),
                'result': row[3]
            })
        
        return tasks
    
    def retrieve_context(self, query: str, include_short_term: bool = True, 
                        long_term_limit: int = 5) -> Dict[str, Any]:
        context = {}
        
        if include_short_term:
            context['recent_conversation'] = self.short_term.get_context_string(limit=10)
        
        context['relevant_memories'] = self.long_term.search(query, limit=long_term_limit)
        
        context['preferences'] = self.get_all_preferences()
        
        return context
    
    def prune_memories(self, days: int = 30):
        deleted_count = self.long_term.prune_old(days=days)
        self.short_term.clear_expired()
        return deleted_count
    
    def export_memories(self, output_path: str):
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'short_term_memories': self.short_term.get_recent(),
            'long_term_memories': self.long_term.get_all(),
            'preferences': self.get_all_preferences(),
            'recent_tasks': self.get_recent_tasks(limit=100)
        }
        
        output_file = Path(output_path)
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return str(output_file)
    
    def import_memories(self, input_path: str, clear_existing: bool = False):
        with open(input_path, 'r') as f:
            import_data = json.load(f)
        
        if clear_existing:
            self.short_term.clear()
            self.long_term.clear()
        
        for memory in import_data.get('long_term_memories', []):
            self.long_term.add(memory['text'], memory.get('metadata'))
        
        for key, value in import_data.get('preferences', {}).items():
            self.add_user_preference(key, value)
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM user_preferences')
        pref_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM completed_tasks')
        task_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'short_term_count': len(self.short_term.get_recent()),
            'long_term_count': len(self.long_term.get_all()),
            'preferences_count': pref_count,
            'tasks_count': task_count,
            'persist_directory': str(self.persist_directory)
        }
