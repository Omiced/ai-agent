import os
from config import MAX_CHARS
from google.genai import types



def get_file_content(working_directory, file_path):
  try:
    absolute_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_target_file = os.path.commonpath([absolute_path,target_file_path]) == absolute_path
    if not valid_target_file:
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
      return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file_path, "r") as f:
      file_content_string = f.read(MAX_CHARS)
      # After reading the first MAX_CHARS...
      if f.read(1):
          file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    return file_content_string
  except Exception as e:
    return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Shows content of a specific file in the current working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to be displayed",
            ),
        },
        required=["file_path"]
    ),
)