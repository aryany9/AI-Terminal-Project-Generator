import subprocess

def run_command(command: str, cwd: str = None, timeout: int = 30) -> dict:
    """
    Runs a shell command and returns the result.

    Args:
        command (str): The command to run (e.g., 'npm install').
        cwd (str, optional): The working directory to run the command in.
        timeout (int, optional): The maximum time in seconds to allow the command to run.

    Returns:
        dict: {
            'success': bool,
            'stdout': str,
            'stderr': str,
            'return_code': int
        }
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout
        )
        return {
            'status': 'Success' if result.returncode == 0 else 'Failure',
            'message': result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
        }
    except subprocess.TimeoutExpired:
        return {
            'status': "error",
            'message': "Command timed out"
        }
    except Exception as e:
        return {
            'status': "error",
            'message': str(e)
        }
