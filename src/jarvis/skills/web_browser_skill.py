from typing import Dict, Any
import webbrowser
from .base_skill import BaseSkill, SkillResult


class WebBrowserSkill(BaseSkill):
    def get_name(self) -> str:
        return "open_website"
    
    def get_description(self) -> str:
        return "Open a website in the default web browser. Supports popular sites like YouTube, Google, etc."
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "site": {
                    "type": "string",
                    "description": "The website to open. Can be a common name (youtube, google) or a full URL",
                }
            },
            "required": ["site"],
        }
    
    def execute(self, site: str, **kwargs) -> SkillResult:
        try:
            site_lower = site.lower()
            
            site_map = {
                "youtube": "https://www.youtube.com",
                "google": "https://www.google.com",
                "github": "https://www.github.com",
                "reddit": "https://www.reddit.com",
                "twitter": "https://www.twitter.com",
                "facebook": "https://www.facebook.com",
            }
            
            if site_lower in site_map:
                url = site_map[site_lower]
            elif site.startswith("http://") or site.startswith("https://"):
                url = site
            else:
                url = f"https://{site}"
            
            webbrowser.open(url)
            return SkillResult(success=True, result=f"Opened {url} in browser")
        except Exception as e:
            return SkillResult(
                success=False,
                result=None,
                error=f"Error opening website: {str(e)}"
            )
