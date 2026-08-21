import os.path


def get_files_info(working_directory: str, directory: str = ".") -> str:
    dir_content_str = f'Result for "{directory}" directory: \n' 
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        target_dir_valid_bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except Exception as e:
        return dir_content_str + f'    Error: os.path functions failed in get_files_info when checking if "{directory}" is in "{working_directory}"'
    if target_dir_valid_bool == False:
        return dir_content_str + f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(target_dir) == False:
        return dir_content_str + f'    Error: "{directory}" is not a directory'
    if target_dir_valid_bool == True:
        dir_list = []
        try:
            for item in os.listdir(target_dir): # Pre validated target_dir exists
                item_name = item
                item_size = os.path.getsize(os.path.join(target_dir, item))
                item_is_dir = os.path.isdir(os.path.join(target_dir, item))
                dir_list.append((item_name, item_size, item_is_dir))
        except Exception as e:
            return dir_content_str + f'    Error: os functions failed in get_file_info when listing working_dir contents and stats'
        str_add = []
        for item in dir_list:
            str_add.append(f"  - {item[0]}: file_size={item[1]}, is_dir={item[2]}")
        dir_content_str_add = "\n".join(str_add)
        return dir_content_str + dir_content_str_add 
    


