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
    # Define the full path for the new file
    file_path = os.path.join(directory_path, file_name)
    
    # Create and write to the file
    with open(file_path, "w") as file:
        file.write(content)
    
    print(f"File '{file_name}' created in '{directory_path}'.")
    return {"status": "success", "message": f"File '{file_name}' created in '{directory_path}'."}