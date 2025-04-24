import os
from google import genai
from google.genai import types
import json

system_prompt_path = os.path.join(os.path.dirname(__file__), '../utils', 'system_prompt.txt')
with open(system_prompt_path, 'r') as file:
    system_prompt = file.read().replace('\n', '')

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def run_query(self, messages):
        response = self.client.models.generate_content(
            model="gemini-1.5-flash", 
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, 
                response_mime_type="application/json"
            ),
            contents=json.dumps(messages)
        )
        
        return response.text 
