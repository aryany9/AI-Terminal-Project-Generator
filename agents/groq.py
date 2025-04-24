import os
import json
from groq import Groq

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def run_query(self, messages):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            response_format={"type": "json_object"}
        )

        # print(response)
        
        # Assuming the response is in JSON format
        return response.choices[0].message.content