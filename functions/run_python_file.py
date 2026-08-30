import os.path
import subprocess


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:    
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_path_valid_bool = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    except Exception as e:
        return f'Error: os.path functions failed in get_file_content when checking if "{file_path}" is in "{working_directory}"'
    if target_path_valid_bool == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory: "{working_directory}"'
    if os.path.isfile(target_file_path) == False:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
    try: #
        command = ["python", target_file_path]
        if args != None:
            command.extend(args)
        completed_command = subprocess.run(
            command, 
            capture_output=True, 
            check=True, 
            cwd=os.path.dirname(target_file_path), 
            timeout=30,
            text=True
        )
    except Exception as e:
        return f'Error: executing Python file: {e}'
    try:
        # Begin capturing CompletedProcess object attributes and returning as a string
        output_string_args = str(completed_command.args)
        if completed_command.returncode != 0:
            output_string_args += f"\nProcess exited with code {completed_command.returncode}"
        if completed_command.stdout and completed_command.stderr == None:
            output_string_args += f"No output produced"
        else:
            output_string_args += f"\nSTDOUT: {completed_command.stdout}"
            output_string_args += f"\nSTDERR: {completed_command.stderr}"
        return output_string_args + "\n\n ---------------- END PYTHON FILE -------------- \n\n"
    except Exception as e:
        return f'Error: failed to construct return string for CompletedProcess in run_python_file'

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a specified python file relative to a working directory using provided arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to read files from, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "description": "List of arguments to pass to the called python file",
                },
            },
        },
    },
}
