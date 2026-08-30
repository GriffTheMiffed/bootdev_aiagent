import os.path

max_chars = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:    
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_path_valid_bool = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    except Exception as e:
        return f'Error: os.path functions failed in get_file_content when checking if "{file_path}" is in "{working_directory}"'
    if target_path_valid_bool == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory: "{working_directory}"'
    if os.path.isfile(target_file_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}'
    try: # Library file reading method for laoding n characters from file_path
        with open(target_file_path, "r") as file:
            max_file_content = file.read(max_chars) # TODO: add config file and limit
            if file.read(1):
                max_file_content += f'\n[... File "{file_path}" truncated at {max_chars} characters]'
        return max_file_content
    except Exception as e:
        return f'Error: get_file_content failed to read "{file_path}" inside "{working_directory}"'


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Opens a file in a specified path relative to the working directory, reading characters up to a defined maximum",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to read files from, relative to the working directory",
                }
            },
        },
    },
}
