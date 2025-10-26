from unittest.mock import MagicMock, Mock, patch

import pytest

from jarvis import Jarvis


class TestJarvisInit:
    """Test Jarvis initialization"""

    @patch("jarvis.pyttsx3.init")
    def test_init_creates_engine(self, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()

        mock_pyttsx3_init.assert_called_once_with("sapi5")
        assert jarvis.engine == mock_engine
        assert jarvis.recognizer is not None


class TestSpeak:
    """Test speak functionality"""

    @patch("jarvis.pyttsx3.init")
    def test_speak_calls_engine_methods(self, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        test_text = "Hello World"
        jarvis.speak(test_text)

        mock_engine.say.assert_called_once_with(test_text)
        mock_engine.runAndWait.assert_called_once()

    @patch("jarvis.pyttsx3.init")
    def test_speak_with_empty_string(self, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.speak("")

        mock_engine.say.assert_called_once_with("")
        mock_engine.runAndWait.assert_called_once()


class TestWishMe:
    """Test wish_me greeting functionality"""

    @patch("jarvis.pyttsx3.init")
    @patch("jarvis.datetime.datetime")
    def test_wish_me_morning(self, mock_datetime, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_now = Mock()
        mock_now.hour = 9
        mock_datetime.now.return_value = mock_now

        jarvis = Jarvis()
        jarvis.speak = Mock()
        jarvis.wish_me()

        assert jarvis.speak.call_count == 2
        jarvis.speak.assert_any_call("Good Morning!")
        jarvis.speak.assert_any_call("I am Jarvis. How can I help you?")

    @patch("jarvis.pyttsx3.init")
    @patch("jarvis.datetime.datetime")
    def test_wish_me_afternoon(self, mock_datetime, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_now = Mock()
        mock_now.hour = 14
        mock_datetime.now.return_value = mock_now

        jarvis = Jarvis()
        jarvis.speak = Mock()
        jarvis.wish_me()

        assert jarvis.speak.call_count == 2
        jarvis.speak.assert_any_call("Good Afternoon!")
        jarvis.speak.assert_any_call("I am Jarvis. How can I help you?")

    @patch("jarvis.pyttsx3.init")
    @patch("jarvis.datetime.datetime")
    def test_wish_me_evening(self, mock_datetime, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_now = Mock()
        mock_now.hour = 20
        mock_datetime.now.return_value = mock_now

        jarvis = Jarvis()
        jarvis.speak = Mock()
        jarvis.wish_me()

        assert jarvis.speak.call_count == 2
        jarvis.speak.assert_any_call("Good Evening!")
        jarvis.speak.assert_any_call("I am Jarvis. How can I help you?")

    @patch("jarvis.pyttsx3.init")
    @patch("jarvis.datetime.datetime")
    def test_wish_me_midnight(self, mock_datetime, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_now = Mock()
        mock_now.hour = 0
        mock_datetime.now.return_value = mock_now

        jarvis = Jarvis()
        jarvis.speak = Mock()
        jarvis.wish_me()

        jarvis.speak.assert_any_call("Good Morning!")


class TestTakeCommand:
    """Test take_command voice recognition"""

    @patch("jarvis.sr.Microphone")
    @patch("jarvis.pyttsx3.init")
    def test_take_command_success(self, mock_pyttsx3_init, mock_microphone):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_mic_instance = MagicMock()
        mock_microphone.return_value.__enter__.return_value = mock_mic_instance

        jarvis = Jarvis()
        mock_audio = Mock()
        jarvis.recognizer.listen = Mock(return_value=mock_audio)
        jarvis.recognizer.recognize_google = Mock(return_value="Open YouTube")

        result = jarvis.take_command()

        assert result == "open youtube"
        jarvis.recognizer.listen.assert_called_once()
        jarvis.recognizer.recognize_google.assert_called_once_with(mock_audio, language="en-US")

    @patch("jarvis.sr.Microphone")
    @patch("jarvis.pyttsx3.init")
    def test_take_command_recognition_error(self, mock_pyttsx3_init, mock_microphone):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_mic_instance = MagicMock()
        mock_microphone.return_value.__enter__.return_value = mock_mic_instance

        jarvis = Jarvis()
        mock_audio = Mock()
        jarvis.recognizer.listen = Mock(return_value=mock_audio)
        jarvis.recognizer.recognize_google = Mock(side_effect=Exception("Recognition error"))

        result = jarvis.take_command()

        assert result == "None"


class TestGetWikipediaSummary:
    """Test Wikipedia summary retrieval"""

    @patch("jarvis.wikipedia.summary")
    @patch("jarvis.pyttsx3.init")
    def test_get_wikipedia_summary_success(self, mock_pyttsx3_init, mock_wikipedia):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_wikipedia.return_value = "Python is a programming language."

        jarvis = Jarvis()
        result = jarvis.get_wikipedia_summary("Python programming")

        assert result == "Python is a programming language."
        mock_wikipedia.assert_called_once_with("Python programming", sentences=2)

    @patch("jarvis.wikipedia.summary")
    @patch("jarvis.pyttsx3.init")
    def test_get_wikipedia_summary_error(self, mock_pyttsx3_init, mock_wikipedia):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_wikipedia.side_effect = Exception("Page not found")

        jarvis = Jarvis()
        result = jarvis.get_wikipedia_summary("NonexistentTopic")

        assert result is None


class TestGetWeather:
    """Test weather retrieval"""

    @patch("jarvis.requests.get")
    @patch("jarvis.pyttsx3.init")
    def test_get_weather_success(self, mock_pyttsx3_init, mock_requests_get):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_response = Mock()
        mock_response.json.return_value = {
            "cod": 200,
            "main": {"temp": 298.15, "pressure": 1013, "humidity": 65},
        }
        mock_requests_get.return_value = mock_response

        jarvis = Jarvis()
        result = jarvis.get_weather("test_api_key", "London")

        assert result is not None
        assert result["temperature"] == 298.15
        assert result["pressure"] == 1013
        assert result["humidity"] == 65

    @patch("jarvis.requests.get")
    @patch("jarvis.pyttsx3.init")
    def test_get_weather_city_not_found(self, mock_pyttsx3_init, mock_requests_get):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_response = Mock()
        mock_response.json.return_value = {"cod": "404"}
        mock_requests_get.return_value = mock_response

        jarvis = Jarvis()
        result = jarvis.get_weather("test_api_key", "InvalidCity")

        assert result is None

    @patch("jarvis.requests.get")
    @patch("jarvis.pyttsx3.init")
    def test_get_weather_request_error(self, mock_pyttsx3_init, mock_requests_get):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_requests_get.side_effect = Exception("Network error")

        jarvis = Jarvis()
        result = jarvis.get_weather("test_api_key", "London")

        assert result is None


class TestProcessCommand:
    """Test command processing"""

    @patch("jarvis.pyttsx3.init")
    def test_process_command_wikipedia(self, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.speak = Mock()
        jarvis.get_wikipedia_summary = Mock(return_value="Python is a language.")

        jarvis.process_command("wikipedia python")

        jarvis.speak.assert_any_call("Searching Wikipedia...")
        jarvis.speak.assert_any_call("According to Wikipedia")
        jarvis.speak.assert_any_call("Python is a language.")
        jarvis.get_wikipedia_summary.assert_called_once_with("python")

    @patch("jarvis.pyttsx3.init")
    def test_process_command_wikipedia_no_results(self, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.speak = Mock()
        jarvis.get_wikipedia_summary = Mock(return_value=None)

        jarvis.process_command("wikipedia unknown topic")

        jarvis.speak.assert_any_call("Searching Wikipedia...")
        jarvis.speak.assert_any_call("Sorry, I couldn't find any information.")

    @patch("jarvis.webbrowser.open")
    @patch("jarvis.pyttsx3.init")
    def test_process_command_open_youtube(self, mock_pyttsx3_init, mock_webbrowser):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.process_command("open youtube")

        mock_webbrowser.assert_called_once_with("youtube.com")

    @patch("jarvis.webbrowser.open")
    @patch("jarvis.pyttsx3.init")
    def test_process_command_open_google(self, mock_pyttsx3_init, mock_webbrowser):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.process_command("open google")

        mock_webbrowser.assert_called_once_with("google.com")

    @patch("jarvis.datetime.datetime")
    @patch("jarvis.pyttsx3.init")
    def test_process_command_time(self, mock_pyttsx3_init, mock_datetime):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_now = Mock()
        mock_now.strftime.return_value = "14:30:45"
        mock_datetime.now.return_value = mock_now

        jarvis = Jarvis()
        jarvis.speak = Mock()
        jarvis.process_command("what time is it")

        jarvis.speak.assert_called_once_with("The time is 14:30:45")

    @patch("jarvis.pyttsx3.init")
    def test_process_command_weather_success(self, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.speak = Mock()
        jarvis.get_weather = Mock(
            return_value={"temperature": 298.15, "pressure": 1013, "humidity": 65}
        )

        jarvis.process_command("what's the weather", weather_api_key="test_key", city="London")

        assert jarvis.speak.call_count == 3
        calls = [call[0][0] for call in jarvis.speak.call_args_list]
        assert any("25.00 degrees Celsius" in call for call in calls)
        assert any("1013 hPa" in call for call in calls)
        assert any("65 percent" in call for call in calls)

    @patch("jarvis.pyttsx3.init")
    def test_process_command_weather_failure(self, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.speak = Mock()
        jarvis.get_weather = Mock(return_value=None)

        jarvis.process_command("what's the weather", weather_api_key="test_key", city="InvalidCity")

        jarvis.speak.assert_called_once_with("City not found")

    @patch("jarvis.pyttsx3.init")
    def test_process_command_exit(self, mock_pyttsx3_init):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.speak = Mock()

        with pytest.raises(SystemExit):
            jarvis.process_command("exit")

        jarvis.speak.assert_called_once_with("Goodbye!")
