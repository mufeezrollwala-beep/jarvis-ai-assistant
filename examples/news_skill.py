"""
News Headlines Skill
====================
Fetch and read top news headlines from NewsAPI.

Setup:
    1. Get API key from https://newsapi.org/
    2. Add to config.json:
       {
         "apis": {
           "news": {
             "api_key": "your_api_key_here",
             "country": "us",
             "category": "technology"
           }
         }
       }

Usage:
    - "Get news headlines"
    - "What's in the news?"
    - "Tell me the news"
"""

import requests

class NewsSkill:
    """Fetch and read news headlines"""
    
    # Available categories
    CATEGORIES = ['business', 'entertainment', 'general', 'health', 
                  'science', 'sports', 'technology']
    
    # Available countries
    COUNTRIES = ['us', 'gb', 'ca', 'au', 'in', 'de', 'fr', 'jp']
    
    def __init__(self, jarvis_instance):
        self.jarvis = jarvis_instance
        self.api_key = self._get_api_key()
        self.base_url = "https://newsapi.org/v2/top-headlines"
    
    def _get_api_key(self):
        """Get API key from config"""
        return self.jarvis.config.get('apis', {}).get('news', {}).get('api_key')
    
    def can_handle(self, query):
        """Check if this skill can handle the query"""
        triggers = ['news', 'headlines', "what's happening", 'current events']
        return any(trigger in query for trigger in triggers)
    
    def handle(self, query):
        """Execute the news skill"""
        if not self.api_key:
            self.jarvis.speak("News API key is not configured")
            print("Get your API key from https://newsapi.org/")
            return
        
        try:
            # Extract parameters
            category = self._extract_category(query)
            country = self._extract_country(query)
            
            # Fetch news
            self.jarvis.speak("Fetching latest news headlines")
            articles = self._fetch_news(country, category)
            
            if articles:
                self._read_headlines(articles)
            else:
                self.jarvis.speak("No news articles found")
        
        except Exception as e:
            self.jarvis.speak("Could not fetch news")
            print(f"News fetch error: {e}")
    
    def _extract_category(self, query):
        """Extract news category from query"""
        for category in self.CATEGORIES:
            if category in query:
                return category
        
        # Default from config
        return self.jarvis.config.get('apis', {}).get('news', {}).get('category', 'general')
    
    def _extract_country(self, query):
        """Extract country code from query"""
        # Country name mappings
        country_names = {
            'america': 'us', 'usa': 'us', 'united states': 'us',
            'britain': 'gb', 'uk': 'gb', 'england': 'gb',
            'canada': 'ca',
            'australia': 'au',
            'india': 'in',
            'germany': 'de',
            'france': 'fr',
            'japan': 'jp'
        }
        
        for name, code in country_names.items():
            if name in query:
                return code
        
        # Default from config
        return self.jarvis.config.get('apis', {}).get('news', {}).get('country', 'us')
    
    def _fetch_news(self, country='us', category='general', limit=5):
        """Fetch news from NewsAPI"""
        params = {
            'apiKey': self.api_key,
            'country': country,
            'category': category,
            'pageSize': limit
        }
        
        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] == 'ok':
            return data['articles']
        else:
            return []
    
    def _read_headlines(self, articles):
        """Read headlines to user"""
        count = len(articles)
        self.jarvis.speak(f"Here are the top {count} headlines")
        
        for i, article in enumerate(articles, 1):
            title = article['title']
            source = article['source']['name']
            
            # Read headline
            self.jarvis.speak(f"Headline {i} from {source}: {title}")
            
            print(f"\n{i}. {title}")
            print(f"   Source: {source}")
            if article.get('description'):
                print(f"   {article['description']}")


# Integration example
def add_news_to_jarvis():
    """
    How to integrate this skill:
    
    1. In jarvis.txt, add after imports:
       from examples.news_skill import NewsSkill
    
    2. In Jarvis.__init__(), add:
       self.news_skill = NewsSkill(self)
    
    3. In process_command(), add:
       if self.news_skill.can_handle(query):
           self.news_skill.handle(query)
           return
    """
    pass


if __name__ == "__main__":
    # Test the news skill
    class MockJarvis:
        def __init__(self):
            self.config = {
                'apis': {
                    'news': {
                        'api_key': 'test_key',
                        'country': 'us',
                        'category': 'technology'
                    }
                }
            }
        
        def speak(self, text):
            print(f"JARVIS: {text}")
    
    jarvis = MockJarvis()
    news = NewsSkill(jarvis)
    
    print("Testing news skill...")
    print("\nUser: Get technology news")
    news.handle("get technology news")
