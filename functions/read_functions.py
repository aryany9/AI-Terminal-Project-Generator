import os

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

