import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites the specified file with the contents provided in the arguments.  If a file does not exist, this function can also create and write to it. Limited to the working directory.",
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
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string containing the new contents that will be written to the file.  The old file contents will be overwritten."
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        workdir_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.abspath(os.path.join(working_directory, file_path))
        if not file_abspath.startswith(workdir_abspath):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(file_abspath):
            os.makedirs(file_abspath[len(file_path.split("/")[-1])])
        with open(file_abspath, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f"Error: {e}")