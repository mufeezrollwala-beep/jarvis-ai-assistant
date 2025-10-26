import speech_recognition as sr
import pyttsx3
import datetime
from typing import Optional
from .config import Config
from .services import OpenAIService, AzureOpenAIService, LocalModelService, LLMService
from .agents import AgentManager
from .skills import WikipediaSkill, WebBrowserSkill, TimeSkill, WeatherSkill
from .utils import setup_logger


class Jarvis:
    def __init__(self, config: Config):
        self.config = config
        
        self._setup_logging()
        self._setup_tts()
        self._setup_recognizer()
        self._setup_llm()
        self._setup_agent()
        
        self.logger.info("Jarvis initialized successfully")
    
    def _setup_logging(self):
        conversation_log = self.config.get("logging.conversation_log", "logs/conversations.log")
        decision_log = self.config.get("logging.decision_log", "logs/decisions.log")
        log_level = self.config.get("logging.level", "INFO")
        mask_sensitive = self.config.get("logging.mask_sensitive", True)
        sensitive_patterns = self.config.get("logging.sensitive_patterns", [])
        
        self.logger = setup_logger(
            "jarvis",
            conversation_log,
            level=log_level,
            mask_sensitive=mask_sensitive,
            sensitive_patterns=sensitive_patterns,
        )
        
        self.decision_logger = setup_logger(
            "jarvis.decisions",
            decision_log,
            level=log_level,
            mask_sensitive=mask_sensitive,
            sensitive_patterns=sensitive_patterns,
        )
    
    def _setup_tts(self):
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        voice_id = self.config.get("jarvis.voice_id", 0)
        if voice_id < len(voices):
            self.engine.setProperty('voice', voices[voice_id].id)
    
    def _setup_recognizer(self):
        self.recognizer = sr.Recognizer()
    
    def _setup_llm(self):
        provider = self.config.get("llm.provider", "openai")
        
        if provider == "openai":
            api_key = self.config.get("llm.openai.api_key")
            model = self.config.get("llm.openai.model", "gpt-4o")
            temperature = self.config.get("llm.openai.temperature", 0.7)
            max_tokens = self.config.get("llm.openai.max_tokens", 2000)
            
            self.llm_service: LLMService = OpenAIService(
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif provider == "azure":
            api_key = self.config.get("llm.azure.api_key")
            endpoint = self.config.get("llm.azure.endpoint")
            deployment = self.config.get("llm.azure.deployment_name")
            api_version = self.config.get("llm.azure.api_version", "2024-02-15-preview")
            temperature = self.config.get("llm.azure.temperature", 0.7)
            max_tokens = self.config.get("llm.azure.max_tokens", 2000)
            
            self.llm_service: LLMService = AzureOpenAIService(
                api_key=api_key,
                endpoint=endpoint,
                deployment_name=deployment,
                api_version=api_version,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif provider == "local":
            model_path = self.config.get("llm.local.model_path")
            context_size = self.config.get("llm.local.context_size", 4096)
            temperature = self.config.get("llm.local.temperature", 0.7)
            max_tokens = self.config.get("llm.local.max_tokens", 2000)
            gpu_layers = self.config.get("llm.local.gpu_layers", 35)
            
            self.llm_service: LLMService = LocalModelService(
                model_path=model_path,
                context_size=context_size,
                temperature=temperature,
                max_tokens=max_tokens,
                gpu_layers=gpu_layers,
            )
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
        
        self.logger.info(f"LLM service initialized: {self.llm_service.get_provider_name()}")
    
    def _setup_agent(self):
        weather_api_key = self.config.get("weather.api_key", "")
        default_city = self.config.get("weather.default_city", "London")
        
        skills = [
            WikipediaSkill(),
            WebBrowserSkill(),
            TimeSkill(),
            WeatherSkill(api_key=weather_api_key, default_city=default_city),
        ]
        
        self.agent = AgentManager(
            llm_service=self.llm_service,
            skills=skills,
            logger=self.decision_logger,
        )
    
    def speak(self, text: str):
        self.logger.info(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def wish_me(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        
        name = self.config.get("jarvis.name", "Jarvis")
        self.speak(f"I am {name}. How can I help you?")
    
    def take_command(self) -> Optional[str]:
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 1
            try:
                audio = self.recognizer.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                return None
        
        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}\n")
            self.logger.info(f"User command: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error in speech recognition: {str(e)}")
            return None
    
    def process_command(self, query: str):
        if 'exit' in query or 'quit' in query or 'goodbye' in query:
            self.speak("Goodbye!")
            return False
        
        response = self.agent.process_message(query)
        self.speak(response)
        return True
    
    def run(self):
        self.wish_me()
        
        while True:
            query = self.take_command()
            if query:
                should_continue = self.process_command(query)
                if not should_continue:
                    break
