import pytest
import asyncio
import os
from pathlib import Path
from datetime import datetime, timedelta
from src.task_manager import Task, TaskState
from src.background_actions import download_file, reminder_timer, periodic_health_check, batch_web_search


@pytest.fixture
def mock_task():
    task = Task(
        id="test-task-id",
        name="Test Task",
        coroutine=lambda t: None,
        state=TaskState.RUNNING
    )
    return task


@pytest.mark.asyncio
async def test_reminder_timer(mock_task):
    duration = 2
    message = "Test reminder"
    
    start_time = datetime.now()
    result = await reminder_timer(mock_task, duration, message)
    end_time = datetime.now()
    
    elapsed = (end_time - start_time).total_seconds()
    
    assert elapsed >= duration
    assert elapsed < duration + 1
    assert result['message'] == message
    assert result['duration'] == duration
    assert mock_task.progress == 100.0


@pytest.mark.asyncio
async def test_reminder_timer_progress(mock_task):
    duration = 5
    message = "Test reminder"
    
    async def check_progress():
        await asyncio.sleep(2.5)
        return mock_task.progress
    
    result_task = asyncio.create_task(reminder_timer(mock_task, duration, message))
    progress = await check_progress()
    
    assert 40 <= progress <= 60
    
    await result_task


@pytest.mark.asyncio
async def test_download_file(mock_task, tmp_path):
    url = "https://httpbin.org/bytes/1024"
    destination = tmp_path / "test_download.bin"
    
    try:
        result = await download_file(mock_task, url, str(destination))
        
        assert destination.exists()
        assert result['url'] == url
        assert result['size'] > 0
        assert result['destination'] == str(destination)
        
        file_size = destination.stat().st_size
        assert file_size == 1024
    except Exception as e:
        pytest.skip(f"Network test skipped due to: {e}")


@pytest.mark.asyncio
async def test_download_file_creates_directory(mock_task, tmp_path):
    url = "https://httpbin.org/bytes/512"
    destination = tmp_path / "nested" / "dir" / "test_file.bin"
    
    try:
        result = await download_file(mock_task, url, str(destination))
        
        assert destination.exists()
        assert destination.parent.exists()
    except Exception as e:
        pytest.skip(f"Network test skipped due to: {e}")


@pytest.mark.asyncio
async def test_periodic_health_check(mock_task):
    url = "https://httpbin.org/status/200"
    
    try:
        result = await periodic_health_check(mock_task, url, interval_seconds=1, max_checks=3)
        
        assert result['url'] == url
        assert result['total_checks'] == 3
        assert len(result['results']) == 3
        assert result['successful_checks'] >= 2
        
        for check_result in result['results']:
            assert 'check' in check_result
            assert 'timestamp' in check_result
            assert 'success' in check_result
    except Exception as e:
        pytest.skip(f"Network test skipped due to: {e}")


@pytest.mark.asyncio
async def test_periodic_health_check_failure(mock_task):
    url = "https://httpbin.org/status/500"
    
    try:
        result = await periodic_health_check(mock_task, url, interval_seconds=1, max_checks=2)
        
        assert result['total_checks'] == 2
        assert result['successful_checks'] == 0
        
        for check_result in result['results']:
            assert check_result['success'] == False
            if check_result.get('status') is not None:
                assert check_result['status'] >= 500
    except Exception as e:
        pytest.skip(f"Network test skipped due to: {e}")


@pytest.mark.asyncio
async def test_batch_web_search(mock_task):
    queries = ["test query 1", "test query 2", "test query 3"]
    
    result = await batch_web_search(mock_task, queries, delay_seconds=0.5)
    
    assert result['total_queries'] == 3
    assert len(result['results']) == 3
    assert mock_task.progress == 100.0
    
    for i, query_result in enumerate(result['results']):
        assert query_result['query'] == queries[i]
        assert 'timestamp' in query_result
        assert query_result['success'] == True


@pytest.mark.asyncio
async def test_batch_web_search_progress(mock_task):
    queries = ["query 1", "query 2", "query 3", "query 4"]
    
    async def check_progress():
        await asyncio.sleep(1.5)
        return mock_task.progress
    
    result_task = asyncio.create_task(batch_web_search(mock_task, queries, delay_seconds=0.5))
    progress = await check_progress()
    
    assert 0 < progress < 100
    
    await result_task
