# ENTRY POINT
from dotenv import load_dotenv
from termcolor import colored
from agents.helper import run_agent

# This is the main entry point for the application.
def main():
    # Load environment variables
    load_dotenv()

    run_agent()
    # Import and run the main function from the agent module
    # from agent import runAgent
    # runAgent()
    # print(colored('hello', 'red'), colored('world', 'green'))

if __name__ == "__main__":
    main()