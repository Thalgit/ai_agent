import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

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
