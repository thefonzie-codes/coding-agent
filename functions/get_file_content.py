import os
from google.genai import types

MAX_CHARS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of the specified file as a string, constrained to the working directory.",
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
            )
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        workdir_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.abspath(os.path.join(working_directory, file_path))
        if not file_abspath.startswith(workdir_abspath):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            f'Error: File not found or is not a regular file: "{file_path}"'
        file_obj = open(file_abspath, "r")
        file_str = file_obj.read()
        if len(file_str):
            return f'{file_str[:MAX_CHARS]}[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_str
    except Exception as e:
        print(f"Error: {e}")