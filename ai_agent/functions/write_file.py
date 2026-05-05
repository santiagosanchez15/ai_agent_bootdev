import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write a file by given provided arguments, where the working directory is given and the file_path is relative to the working directory, and content is added to given file, if file doesnt exist, it is handled by creating a new file with respective directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to where we the content of the file can be retrieved, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="contents to be added to the given file, at given directory, this contents will be fully added"
            )
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    '''Write a file by given arguments 
    working_directory: where the file is located
    file_path: file path to the file inside the working directory
    content: content wanted to be added

    updates the file with given content
    '''
    
    absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_file = os.path.commonpath([absolute_path, target_path]) == absolute_path
    if not valid_file: return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path): return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    #open file and write 
    with open(target_path, "w") as file:
        try: 
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except ValueError: return 'Error: given value is not taken'
        except Exception: return 'Error: given data broke the code, please try again'