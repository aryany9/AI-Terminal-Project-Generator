# utils/tools.py

# Export all tools
from functions.command_functions import is_npm_package_installed, run_command
from functions.create_functions import create_directory_in_output, create_file_in_directory
from functions.read_functions import list_output_directories, list_output_structure, read_file_content


tools = {
    "create_directory_in_output": {
        "fn": create_directory_in_output,
        "description": " Creates a directory in the output folder if it doesn't already exist."
    },
    "is_npm_package_installed": {
        "fn": is_npm_package_installed,
        "description": "Check if a package is installed using npm."
    },
    "create_file_in_directory": {
        "fn": create_file_in_directory,
        "description": "Creates a file in the specified directory with the given content."
    },
    "list_output_directories": {
        "fn": list_output_directories,
        "description": "Lists all directories in the output folder."
    },
    "list_output_structure": {
        "fn": list_output_structure,
        "description": "Gives context about the output folder structure."
    },
    "read_file_content": {
        "fn": read_file_content,
        "description": "Reads the content of a file."
    },
    "run_command": {
        "fn": run_command,
        "description": "Runs a shell command and returns the result."
    }
}