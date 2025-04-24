# ENTRY POINT
from dotenv import load_dotenv
from termcolor import colored
import os
from agents.helper import run_agent
import time


def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear terminal for better experience
    print(colored("Welcome to the AI Terminal Project Generator ⚙️", 'green'))
    print(colored("--------------------------------------------------", 'yellow'))
    time.sleep(0.5)

# This is the main entry point for the application.
def main():
    load_dotenv()

    print_banner()
    run_agent()

if __name__ == "__main__":
    main()