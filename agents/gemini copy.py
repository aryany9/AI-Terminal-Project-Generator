from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import requests
import json

load_dotenv()

system_prompt_path = os.path.join(os.path.dirname(__file__), '../utils', 'system_prompt.txt')
with open(system_prompt_path, 'r') as file:
    system_prompt = file.read().replace('\n', '')

avaiable_tools = {
    "get_weather": {
        "fn": lambda city: get_weather(city),
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "add": {
        "fn": lambda input: add(input),
        "description": "Takes two numbers as input and returns the sum of the two numbers"
    },
    "run_command": {
        "fn": lambda command: run_command(command),
        "description": "Takes a command as input to execute on system and returns output"
    }
}

def run_command(command):
    result = os.system(command)
    return result

def get_weather(city: str):
    print("🔨 Tool Called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    return f"The weather in {city} is {response.text}." if response.status_code == 200 else "Something went wrong"

def add(input: str):
    x, y = map(int, input.split(","))
    print("🔨 Tool Called: add", x, y)
    return x + y

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.messages = [{ "role": "system", "content": system_prompt }]

    def process_query(self, user_query):
        self.messages.append({ "role": "user", "content": user_query })

        counter = 0
        while True:
            counter += 1
            print("Step: " + str(counter))

            response = self.client.models.generate_content(
                model="gemini-1.5-flash", 
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt, 
                    response_mime_type="application/json"
                ),
                contents=json.dumps(self.messages)
            )

            parsed_output = json.loads(response.text)
            self.messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

            if parsed_output.get("step") == "plan":
                print(f"🧠: {parsed_output.get('content')}")
                continue

            if parsed_output.get("step") == "action":
                print(f"🔨: {parsed_output.get('function')}: {parsed_output.get('input')}")
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")

                if avaiable_tools.get(tool_name):
                    output = avaiable_tools[tool_name]["fn"](tool_input)
                    self.messages.append({
                        "role": "assistant",
                        "content": json.dumps({ "step": "observe", "output": output })
                    })
                    continue

            if parsed_output.get("step") == "output":
                print(f"🤖: {parsed_output.get('content')}")
                return parsed_output.get('content')
