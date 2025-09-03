import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified file.  Limited to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The main project folder where the files are located and where commands are executed by default. Also known as the root folder. Use '.' by default.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A string that specifies the location of a file or directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of strings - these will be the arguments (argv) for the file being ran"
            )
        },
    ),
)

# python
def run_python_file(working_directory, file_path, args=None):
    args = args or []
    try:
        file_abspath = os.path.abspath(os.path.join(working_directory, file_path))
        if not file_abspath.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(file_abspath):
            return f'Error: File "{file_path}" not found.'
        if not file_abspath.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Run with cwd so relative behavior matches manual run
        result = subprocess.run(
            ["python3", file_abspath] + args,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Combine outputs; some runners print on stderr
        output = (result.stdout or "") + (result.stderr or "")
        if output.strip():
            return output
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        return "No Output Produced"

    except Exception as e:
        return f"Error: {e}"

# def run_python_file(working_directory, file_path, args=[]):
#     try:
#         file_abspath = os.path.abspath(os.path.join(working_directory, file_path))
#         print(file_abspath)
#         if not file_abspath.startswith(os.path.abspath(working_directory)):
#             return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
#         if not os.path.exists(file_abspath):
#             return f'Error: File "{file_path}" not found.'
#         if not file_abspath.endswith(".py"):
#             return f'Error: "{file_path}" is not a Python file.'
#         result = subprocess.run(
#             ["python3", file_abspath] + args, 
#             cwd=working_directory,
#             capture_output=True, 
#             text=True,  
#             timeout=30)
#         if result.stdout:
#             return f"STDOUT: {result.stdout}"
#         if result.returncode != 0:
#             return f"STDOUT: {result.stdout} \n Process exited with code {result.returncode}"
#         if not result.stdout:
#             return "No Output Produced"
#     except Exception as e:
#         print(f"Error: {e}")