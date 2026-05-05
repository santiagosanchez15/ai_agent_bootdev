import os 
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)



def get_files_info(working_directory: str, directory='.') -> str:
    '''Returns files contained in a path through the agent'''

    absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(absolute_path, directory))
    valid_directory = os.path.commonpath([absolute_path, target_path]) == absolute_path
    if not valid_directory: return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path): return f'Error: "{directory}" is not a directory'

    #list contents of directory and iterate trhough them
    contents = os.listdir(target_path)
    string = []
    for item in contents: 
        try: 
            item_path = os.path.join(target_path, item)
            string.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")

        except ValueError:
            return f"{item} value couldn't be taken"
        except Exception:
            return f"Error {item} couldnt be read"
        
    
    return '\n'.join(string)

