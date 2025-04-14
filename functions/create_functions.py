import os

def create_directory_in_output(directory_name: str):
    """
    Creates a directory in the output folder if it doesn't already exist.

    Args:
        directory_name (str): The name of the directory to create.
    """
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Define the output directory path
    output_directory = os.path.join(current_directory, "output", directory_name)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Directory '{directory_name}' created in 'output' folder.")
    else:
        print(f"Directory '{directory_name}' already exists in 'output' folder.")
    return {"status": "success", "message": f"Directory '{directory_name}' created in 'output' folder."}


def create_file_in_directory(directory_path: str, file_name: str, content: str):
    """
    Creates a file in the specified directory with the given content.

    Args:
        directory_path (str): The path to the directory where the file will be created.
        file_name (str): The name of the file to create.
        content (str): The content to write to the file.
    """
    
     # Get the current working directory
    current_directory = os.getcwd()

    # Check if 'output' is already in the directory_path
    if "output" in os.path.normpath(directory_path).split(os.sep):
        output_directory = os.path.join(current_directory, directory_path)
    else:
        output_directory = os.path.join(current_directory, "output", directory_path)

    # Make sure the directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Define the full path for the new file
    file_path = os.path.join(output_directory, file_name)
    
     # Clean up content
    if isinstance(content, str):
        content = content.encode().decode('unicode_escape')  # convert \\n to \n
    
    # Create and write to the file
    with open(file_path, "w") as file:
        file.write(content)
    
    print(f"File '{file_name}' created in '{directory_path}'.")
    return {"status": "success", "message": f"File '{file_name}' created in '{directory_path}'."}