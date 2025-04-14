# from gemini import GeminiClient
from agents.gemini import GeminiClient
from agents.groq import GroqClient
from functions.helper_functions import process_query
import os

# Get LLM Clients
def get_llm_client(user_choice):
    """
    Returns the client for the specified LLM based on user choice.

    Args:
        user_choice (str): The name of the LLM chosen by the user.

    Returns:
        object: The client instance for the specified LLM.

    Raises:
        ValueError: If the user choice is not recognized.
    """
    llm_clients = {
        "gemini": lambda: GeminiClient(),
        "groq": lambda: GroqClient(),
        "openai": lambda: OpenAIClient(),
        "anthropic": lambda: AnthropicClient(),
        "cohere": lambda: CohereClient(),
    }

    if user_choice.lower() in llm_clients:
        return llm_clients[user_choice.lower()]()
    else:
        raise ValueError(f"Unsupported LLM choice: {user_choice}")

# Gets User's LLM Choice
def get_user_choice():
    """
    Prompts the user to choose an LLM and returns the choice.

    Returns:
        str: The name of the chosen LLM.
    """
    print("Supported LLMs:")
    print("1. Gemini")
    print("2. Groq")

    choice = input("Enter the number of the LLM you want to use: ")

    llm_choices = {
        "1": "gemini",
        "2": "groq"
    }

    return llm_choices.get(choice, None)

# Process the query using the LLM client
def run_agent():
    """
    Main function to run the agent. It prompts the user for input and processes it using the chosen LLM client.
    """
    user_choice = get_user_choice()
    if user_choice is None:
        print("Invalid choice. Exiting.")
        return
    
    system_prompt_path = os.path.join(os.path.dirname(__file__), '../utils', 'system_prompt.txt')

    with open(system_prompt_path, 'r') as file:
        system_prompt = file.read().replace('\n', '')
        
    llm_client = get_llm_client(user_choice)

    while True:
        user_query = input('> What do you want me to create? (type "exit" to quit): ')
        if user_query.lower() == 'exit':
            break

        response = process_query(llm_client, user_query, system_prompt)
        
        print(f"Response: {response}")
