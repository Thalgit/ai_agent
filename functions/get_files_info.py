import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    #blijf in je eige map

    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(full_path)

    if not abs_target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    #is het wel een map

    if not os.path.isdir(abs_target_dir):
        return f'Error: "{directory}" is not a directory'
    
    #list en lines bouwen

    try:
        items = os.listdir(abs_target_dir)
        lines = []
        for name in items:
            item_path = os.path.join(abs_target_dir, name)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            line = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            lines.append(line)
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
