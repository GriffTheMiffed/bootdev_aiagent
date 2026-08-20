import os.path


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        target_dir_valid_bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except Exception as e:
        return f'Error: os.path functions failed in get_files_info when checking if "{directory}" is in "{working_directory}"'
    if target_dir_valid_bool == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(target_dir) == False:
        return f'Error: "{directory}" is not a directory'
    if target_dir_valid_bool == True:
        return f'Success: "{directory}" is within the working directory'


