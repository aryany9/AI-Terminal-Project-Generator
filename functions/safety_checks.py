import os

def is_safe_path(path):
    """
    Validates if the path is within current working directory.
    
    Args:
        path (str): Path to validate
        
    Returns:
        bool: True if path is safe, False otherwise
    """
    # Get absolute paths for comparison
    path = os.path.abspath(path)
    cwd = os.path.abspath(os.getcwd())
    
    # Check if the path is within the current working directory
    return path.startswith(cwd)

def is_safe_command(command):
    """
    Checks if a command is safe to execute (no sudo).
    
    Args:
        command (str): Command to check
        
    Returns:
        bool: True if command is safe, False otherwise
    """
    # Check if command contains sudo
    if "sudo" in command.lower().split():
        return False
    return True