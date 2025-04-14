import os
def generate_tree(directory, prefix=""):
    """
    Recursively generate a tree structure string for a given directory.
    """
    tree = ""
    entries = sorted(os.listdir(directory))
    for index, entry in enumerate(entries):
        entry_path = os.path.join(directory, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        tree += prefix + connector + entry + "\n"
        if os.path.isdir(entry_path):
            extension = "    " if index == len(entries) - 1 else "│   "
            tree += generate_tree(entry_path, prefix + extension)
    return tree


def list_output_structure():
    """
    Lists the structure of the output folder in a tree format.

    Returns:
        dict: A dictionary containing the structure of the output folder.
    """
    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, "output")

    if not os.path.exists(output_directory):
        return {"status": "error", "message": "Output directory does not exist."}

    tree_structure = generate_tree(output_directory)

    return {
        "status": "success",
        "message": f"Output folder structure:\n{tree_structure}"
    }

def list_output_directories():
    """
    Lists all directories in the output folder.
    
    Returns:
        list: A list of directory names in the output folder.
    """
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Define the output directory path
    output_directory = os.path.join(current_directory, "output")
    
    # List all directories in the output folder
    directories = [d for d in os.listdir(output_directory) if os.path.isdir(os.path.join(output_directory, d))]

    # Return the list of directories
    return {"status": "success", "message": directories}

def read_file_content(file_path: str):
    """
    Reads the content of a file.
    
    Args:
        file_path (str): The path to the file to read.
        
    Returns:
        str: The content of the file.
    """
    with open(file_path, "r") as file:
        content = file.read()
    
    # Return the list of directories
    return {"status": "success", "message": content}