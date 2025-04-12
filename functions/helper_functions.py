import json
import os
import requests

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


def process_query(llm_client, user_query, system_prompt):
    """
    Processes the user query using the chosen LLM client.

    Args:
        user_query (str): The user's query.

    Returns:
        str: The response from the LLM.
    """
    
    messages = [{ "role": "system", "content": system_prompt }]
    messages.append({ "role": "user", "content": user_query })
    
    
    while True:
        # Assuming llm_client is already defined and initialized
        response = llm_client.run_query(messages)
        parsed_output = json.loads(response)
        
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get('content')}")
            continue

        if parsed_output.get("step") == "action":
            print(f"🔨: {parsed_output.get('function')}: {parsed_output.get('input')}")
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if avaiable_tools.get(tool_name):
                output = avaiable_tools[tool_name]["fn"](tool_input)
                messages.append({
                    "role": "assistant",
                    "content": json.dumps({ "step": "observe", "output": output })
                })
                continue

        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get('content')}")
            return parsed_output.get('content')