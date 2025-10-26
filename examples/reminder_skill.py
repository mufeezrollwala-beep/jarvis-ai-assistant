"""
Reminder Skill
==============
Set, view, and manage reminders with JARVIS.

Features:
    - Set time-based reminders
    - List active reminders
    - Mark reminders as complete
    - Persistent storage using JSON

Usage:
    - "Remind me to call mom at 3 PM"
    - "Set a reminder for tomorrow"
    - "Show my reminders"
    - "Complete reminder 1"
"""

import json
import os
from datetime import datetime, timedelta
import re

class ReminderSkill:
    """Manage reminders with persistent storage"""
    
    def __init__(self, jarvis_instance, storage_file='reminders.json'):
        self.jarvis = jarvis_instance
        self.storage_file = storage_file
        self.reminders = self._load_reminders()
    
    def can_handle(self, query):
        """Check if this skill can handle the query"""
        triggers = [
            'remind me', 'set reminder', 'show reminder', 
            'list reminder', 'complete reminder', 'delete reminder'
        ]
        return any(trigger in query for trigger in triggers)
    
    def handle(self, query):
        """Execute the reminder skill"""
        try:
            if 'show' in query or 'list' in query:
                self._show_reminders()
            
            elif 'complete' in query or 'done' in query or 'delete' in query:
                self._complete_reminder(query)
            
            elif 'remind me' in query or 'set reminder' in query:
                self._set_reminder(query)
            
            else:
                self.jarvis.speak("I'm not sure what you want to do with reminders")
        
        except Exception as e:
            self.jarvis.speak("Sorry, I couldn't handle that reminder")
            print(f"Reminder error: {e}")
    
    def _set_reminder(self, query):
        """Set a new reminder"""
        # Extract reminder text
        reminder_text = query.replace('remind me to', '')
        reminder_text = reminder_text.replace('remind me', '')
        reminder_text = reminder_text.replace('set reminder', '')
        reminder_text = reminder_text.strip()
        
        # Extract time if present
        due_time = self._extract_time(reminder_text)
        
        if not reminder_text:
            self.jarvis.speak("What would you like me to remind you about?")
            return
        
        # Create reminder
        reminder = {
            'id': len(self.reminders) + 1,
            'text': reminder_text,
            'due_time': due_time.isoformat() if due_time else None,
            'created_at': datetime.now().isoformat(),
            'completed': False
        }
        
        self.reminders.append(reminder)
        self._save_reminders()
        
        # Confirm to user
        if due_time:
            time_str = due_time.strftime("%I:%M %p on %B %d")
            self.jarvis.speak(f"Reminder set for {time_str}: {reminder_text}")
        else:
            self.jarvis.speak(f"Reminder set: {reminder_text}")
        
        print(f"✓ Reminder #{reminder['id']} created")
    
    def _show_reminders(self):
        """Show all active reminders"""
        active_reminders = [r for r in self.reminders if not r['completed']]
        
        if not active_reminders:
            self.jarvis.speak("You don't have any active reminders")
            return
        
        count = len(active_reminders)
        self.jarvis.speak(f"You have {count} active reminder{'s' if count > 1 else ''}")
        
        for reminder in active_reminders:
            text = reminder['text']
            reminder_id = reminder['id']
            
            if reminder['due_time']:
                due_time = datetime.fromisoformat(reminder['due_time'])
                time_str = due_time.strftime("%I:%M %p on %B %d")
                self.jarvis.speak(f"Reminder {reminder_id}: {text}, due {time_str}")
                print(f"{reminder_id}. {text} (due: {time_str})")
            else:
                self.jarvis.speak(f"Reminder {reminder_id}: {text}")
                print(f"{reminder_id}. {text}")
    
    def _complete_reminder(self, query):
        """Mark a reminder as complete"""
        # Extract reminder ID
        reminder_id = self._extract_number(query)
        
        if reminder_id is None:
            self.jarvis.speak("Which reminder number should I mark as complete?")
            return
        
        # Find and complete reminder
        for reminder in self.reminders:
            if reminder['id'] == reminder_id and not reminder['completed']:
                reminder['completed'] = True
                reminder['completed_at'] = datetime.now().isoformat()
                self._save_reminders()
                
                self.jarvis.speak(f"Reminder {reminder_id} marked as complete")
                print(f"✓ Completed: {reminder['text']}")
                return
        
        self.jarvis.speak(f"Reminder {reminder_id} not found")
    
    def _extract_time(self, text):
        """Extract time from text"""
        now = datetime.now()
        
        # Check for specific times (e.g., "3 PM", "15:00")
        time_patterns = [
            (r'(\d{1,2})\s*(am|pm)', 'hour_ampm'),
            (r'(\d{1,2}):(\d{2})\s*(am|pm)?', 'hour_minute'),
            (r'at\s+(\d{1,2})', 'hour_only')
        ]
        
        for pattern, type_ in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if type_ == 'hour_ampm':
                    hour = int(match.group(1))
                    ampm = match.group(2).lower()
                    if ampm == 'pm' and hour != 12:
                        hour += 12
                    elif ampm == 'am' and hour == 12:
                        hour = 0
                    return now.replace(hour=hour, minute=0, second=0, microsecond=0)
                
                elif type_ == 'hour_minute':
                    hour = int(match.group(1))
                    minute = int(match.group(2))
                    ampm = match.group(3)
                    if ampm:
                        ampm = ampm.lower()
                        if ampm == 'pm' and hour != 12:
                            hour += 12
                        elif ampm == 'am' and hour == 12:
                            hour = 0
                    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Check for relative times
        if 'tomorrow' in text.lower():
            return now + timedelta(days=1)
        
        if 'next week' in text.lower():
            return now + timedelta(weeks=1)
        
        if 'in' in text:
            # "in 2 hours", "in 30 minutes"
            match = re.search(r'in\s+(\d+)\s+(hour|minute|day)', text, re.IGNORECASE)
            if match:
                amount = int(match.group(1))
                unit = match.group(2).lower()
                
                if unit == 'hour':
                    return now + timedelta(hours=amount)
                elif unit == 'minute':
                    return now + timedelta(minutes=amount)
                elif unit == 'day':
                    return now + timedelta(days=amount)
        
        return None
    
    def _extract_number(self, text):
        """Extract a number from text"""
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None
    
    def _load_reminders(self):
        """Load reminders from file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_reminders(self):
        """Save reminders to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.reminders, f, indent=2)
        except Exception as e:
            print(f"Failed to save reminders: {e}")
    
    def check_due_reminders(self):
        """Check for due reminders (call periodically)"""
        now = datetime.now()
        due_reminders = []
        
        for reminder in self.reminders:
            if reminder['completed']:
                continue
            
            if reminder['due_time']:
                due_time = datetime.fromisoformat(reminder['due_time'])
                if due_time <= now:
                    due_reminders.append(reminder)
        
        return due_reminders


if __name__ == "__main__":
    # Test the reminder skill
    class MockJarvis:
        def __init__(self):
            self.config = {}
        
        def speak(self, text):
            print(f"JARVIS: {text}")
    
    jarvis = MockJarvis()
    reminder_skill = ReminderSkill(jarvis, 'test_reminders.json')
    
    # Test commands
    test_commands = [
        "remind me to call mom at 3 PM",
        "set reminder for tomorrow",
        "remind me to buy groceries",
        "show my reminders",
        "complete reminder 1"
    ]
    
    for cmd in test_commands:
        print(f"\nUser: {cmd}")
        reminder_skill.handle(cmd)
    
    # Cleanup
    if os.path.exists('test_reminders.json'):
        os.remove('test_reminders.json')
