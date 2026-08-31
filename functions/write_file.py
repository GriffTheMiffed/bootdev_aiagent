import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:    
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_path_valid_bool = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if target_path_valid_bool == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: os.path functions failed in write_file when checking if "{file_path}" is in "{working_directory}"'
    if os.path.isdir(target_file_path) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    try:
        writeable_file = os.makedirs(os.path.dirname(target_file_path), exist_ok=True) # Presumed returns None 
        with open(target_file_path, "w") as file:
            written_file_content = file.write(content)
    except Exception as e:
        return f'Error: failed to make "{target_file_path}" or write contents in write_file'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Creates or overwrites a file at a path specified relative to the working directory wtih specified content",
        "parameters": {
            "type": "object",
            "required": [
                    "file_path",
                    "content"
                ],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory file path to write content to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content string to write to the file at the specified relative path",
                }
            },
        },
    },
}
