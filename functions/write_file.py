import os

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