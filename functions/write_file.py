import os
from google.genai import types


def write_file(working_directory, file_path, content):
  try:
    absolute_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_target_file = os.path.commonpath([absolute_path,target_file_path]) == absolute_path
    if not valid_target_file:
      return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file_path):
      return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(os.path.dirname(target_file_path),exist_ok=True)
    with open(target_file_path, "w") as w:
      w.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f"Error: {e}"
   
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes content in a given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to be written",
            ),
            "content": types.Schema(
              type=types.Type.STRING,
              description="Content to be written in the given file"
            )
        },
        required=["file_path", "content"]
    ),
)