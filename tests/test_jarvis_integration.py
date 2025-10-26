from unittest.mock import MagicMock, Mock, patch

from jarvis import Jarvis


class TestIntegrationWikipediaFlow:
    """Test full Wikipedia command flow"""

    @patch("jarvis.wikipedia.summary")
    @patch("jarvis.pyttsx3.init")
    def test_full_wikipedia_query_flow(self, mock_pyttsx3_init, mock_wikipedia):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_wikipedia.return_value = "Python is a high-level programming language."

        jarvis = Jarvis()

        result = jarvis.get_wikipedia_summary("Python programming language")
        assert result == "Python is a high-level programming language."

        jarvis.process_command("wikipedia Python programming language")

        assert mock_engine.say.call_count >= 3
        mock_wikipedia.assert_called()


class TestIntegrationWeatherFlow:
    """Test full weather command flow"""

    @patch("jarvis.requests.get")
    @patch("jarvis.pyttsx3.init")
    def test_full_weather_query_flow(self, mock_pyttsx3_init, mock_requests_get):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_response = Mock()
        mock_response.json.return_value = {
            "cod": 200,
            "main": {"temp": 293.15, "pressure": 1015, "humidity": 70},
        }
        mock_requests_get.return_value = mock_response

        jarvis = Jarvis()

        weather_data = jarvis.get_weather("test_api_key", "Paris")
        assert weather_data is not None
        assert weather_data["temperature"] == 293.15

        jarvis.process_command("what's the weather", weather_api_key="test_api_key", city="Paris")

        assert mock_engine.say.call_count >= 3


class TestIntegrationBrowserFlow:
    """Test full browser command flow"""

    @patch("jarvis.webbrowser.open")
    @patch("jarvis.pyttsx3.init")
    def test_full_youtube_command_flow(self, mock_pyttsx3_init, mock_webbrowser):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.process_command("open youtube")

        mock_webbrowser.assert_called_once_with("youtube.com")

    @patch("jarvis.webbrowser.open")
    @patch("jarvis.pyttsx3.init")
    def test_full_google_command_flow(self, mock_pyttsx3_init, mock_webbrowser):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()
        jarvis.process_command("open google")

        mock_webbrowser.assert_called_once_with("google.com")


class TestIntegrationVoiceRecognitionFlow:
    """Test voice recognition to command processing flow"""

    @patch("jarvis.sr.Microphone")
    @patch("jarvis.webbrowser.open")
    @patch("jarvis.pyttsx3.init")
    def test_voice_to_youtube_command(self, mock_pyttsx3_init, mock_webbrowser, mock_microphone):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_mic_instance = MagicMock()
        mock_microphone.return_value.__enter__.return_value = mock_mic_instance

        jarvis = Jarvis()
        mock_audio = Mock()
        jarvis.recognizer.listen = Mock(return_value=mock_audio)
        jarvis.recognizer.recognize_google = Mock(return_value="open youtube")

        command = jarvis.take_command()
        assert command == "open youtube"

        jarvis.process_command(command)
        mock_webbrowser.assert_called_once_with("youtube.com")

    @patch("jarvis.sr.Microphone")
    @patch("jarvis.datetime.datetime")
    @patch("jarvis.pyttsx3.init")
    def test_voice_to_time_command(self, mock_pyttsx3_init, mock_datetime, mock_microphone):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_now = Mock()
        mock_now.strftime.return_value = "16:45:30"
        mock_datetime.now.return_value = mock_now

        mock_mic_instance = MagicMock()
        mock_microphone.return_value.__enter__.return_value = mock_mic_instance

        jarvis = Jarvis()
        mock_audio = Mock()
        jarvis.recognizer.listen = Mock(return_value=mock_audio)
        jarvis.recognizer.recognize_google = Mock(return_value="what is the time")

        command = jarvis.take_command()
        assert command == "what is the time"

        jarvis.process_command(command)

        assert mock_engine.say.call_count >= 1


class TestIntegrationErrorHandling:
    """Test error handling across the full flow"""

    @patch("jarvis.sr.Microphone")
    @patch("jarvis.pyttsx3.init")
    def test_voice_recognition_error_handling(self, mock_pyttsx3_init, mock_microphone):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_mic_instance = MagicMock()
        mock_microphone.return_value.__enter__.return_value = mock_mic_instance

        jarvis = Jarvis()
        jarvis.recognizer.listen = Mock(return_value=Mock())
        jarvis.recognizer.recognize_google = Mock(side_effect=Exception("Recognition failed"))

        command = jarvis.take_command()
        assert command == "None"

    @patch("jarvis.wikipedia.summary")
    @patch("jarvis.pyttsx3.init")
    def test_wikipedia_error_handling(self, mock_pyttsx3_init, mock_wikipedia):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_wikipedia.side_effect = Exception("Wikipedia error")

        jarvis = Jarvis()
        result = jarvis.get_wikipedia_summary("invalid query")

        assert result is None

        jarvis.process_command("wikipedia invalid query")
        assert mock_engine.say.call_count >= 2

    @patch("jarvis.requests.get")
    @patch("jarvis.pyttsx3.init")
    def test_weather_api_error_handling(self, mock_pyttsx3_init, mock_requests_get):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine
        mock_requests_get.side_effect = Exception("API error")

        jarvis = Jarvis()
        result = jarvis.get_weather("test_key", "London")

        assert result is None

        jarvis.process_command("what's the weather", weather_api_key="test_key", city="London")
        assert mock_engine.say.call_count >= 1


class TestIntegrationGreetingFlow:
    """Test the greeting flow"""

    @patch("jarvis.datetime.datetime")
    @patch("jarvis.pyttsx3.init")
    def test_full_greeting_flow_morning(self, mock_pyttsx3_init, mock_datetime):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_now = Mock()
        mock_now.hour = 8
        mock_datetime.now.return_value = mock_now

        jarvis = Jarvis()
        jarvis.wish_me()

        assert mock_engine.say.call_count == 2
        assert mock_engine.runAndWait.call_count == 2

    @patch("jarvis.datetime.datetime")
    @patch("jarvis.pyttsx3.init")
    def test_full_greeting_flow_evening(self, mock_pyttsx3_init, mock_datetime):
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id="voice1")]
        mock_pyttsx3_init.return_value = mock_engine

        mock_now = Mock()
        mock_now.hour = 19
        mock_datetime.now.return_value = mock_now

        jarvis = Jarvis()
        jarvis.wish_me()

        assert mock_engine.say.call_count == 2
        assert mock_engine.runAndWait.call_count == 2
