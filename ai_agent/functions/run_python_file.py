import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="function to run any python code from given document all of this performed by given arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to where we the content of the file can be retrieved, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description='By defaul given value is 0, but this is used to pass extra argument to given function, in case it more than usual arguments'
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    '''Let the llm run/code python files'''

    absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_file = os.path.commonpath([absolute_path, target_path]) == absolute_path
    if not valid_file: return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path): return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith('.py'): return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_path]
    if args != None: command.extend(args)
    
    try:
        completed = subprocess.run(command, cwd=working_directory, stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True, timeout=30)

        if completed.returncode != 0: return f"Procces exited with code {completed.returncode}"
        elif not completed.stdout and not completed.stderr: return 'No output produced'
        else: return f"STDOUT: {completed.stdout}\n STDERR: {completed.stderr}"
    except Exception as e: return f"Error: executing Python file: {e}"