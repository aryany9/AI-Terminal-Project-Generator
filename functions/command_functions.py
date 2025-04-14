import subprocess

from termcolor import colored

def run_command(command: str, cwd: str = None, timeout: int = 10) -> dict:
    """
    Runs a shell command and prints logs in real-time.

    Args:
        command (str): The command to run.
        cwd (str, optional): Directory to run the command in.
        timeout (int, optional): Maximum duration to run the command.

    Returns:
        dict: {
            'status': 'Success' or 'Failure' or 'error',
            'message': Combined stdout and stderr output
        }
    """
    print(colored(f'Running command: {command}', 'yellow'))
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        output = []

        # Real-time output reading
        for line in iter(process.stdout.readline, ''):
            print(line, end='')  # print to console in real-time
            output.append(line)

        process.stdout.close()
        process.wait(timeout=timeout)

        return {
            'status': 'success' if process.returncode == 0 else 'error',
            'message': ''.join(output).strip()
        }
    
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            'status': 'error',
            'message': 'Command timed out'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
