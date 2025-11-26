import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="..."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="..."
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if args is None:
        args = []        

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            ["python", abs_file_path, *args],
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        stdout = completed_process.stdout
        stderr = completed_process.stderr
        code = completed_process.returncode

        if stdout == "" and stderr == "":
            return "No output produced."

        result = f'STDOUT: {stdout}\nSTDERR: {stderr}'
        
        if code != 0:
            result += f"\nProcess exited with code {code}"

        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"
