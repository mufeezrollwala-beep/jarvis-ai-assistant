from unittest.mock import MagicMock, Mock

import pytest


@pytest.fixture
def mock_pyttsx3_engine():
    """Mock pyttsx3 engine for TTS testing"""
    mock_engine = MagicMock()
    mock_engine.getProperty.return_value = [Mock(id="voice1")]
    mock_engine.setProperty.return_value = None
    mock_engine.say.return_value = None
    mock_engine.runAndWait.return_value = None
    return mock_engine


@pytest.fixture
def mock_speech_recognizer():
    """Mock speech recognizer for microphone testing"""
    mock_recognizer = MagicMock()
    mock_recognizer.pause_threshold = 1
    mock_recognizer.listen.return_value = Mock()
    mock_recognizer.recognize_google.return_value = "test command"
    return mock_recognizer


@pytest.fixture
def mock_microphone():
    """Mock microphone context manager"""
    mock_mic = MagicMock()
    mock_mic.__enter__ = Mock(return_value=mock_mic)
    mock_mic.__exit__ = Mock(return_value=False)
    return mock_mic


@pytest.fixture
def mock_wikipedia_summary():
    """Mock wikipedia summary function"""
    return Mock(return_value="Test Wikipedia summary about the topic.")


@pytest.fixture
def mock_requests_get():
    """Mock requests.get for weather API testing"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "cod": 200,
        "main": {"temp": 298.15, "pressure": 1013, "humidity": 65},
    }
    return Mock(return_value=mock_response)


@pytest.fixture
def mock_webbrowser_open():
    """Mock webbrowser.open for browser testing"""
    return Mock()
