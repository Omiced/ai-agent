import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
  try:
    absolute_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_target_file = os.path.commonpath([absolute_path,target_file_path]) == absolute_path
    if not valid_target_file:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
      return f'Error: "{file_path}" does not exist or is not a regular file'
    if file_path[len(file_path) - 3:] != ".py":
      return f'Error: "{file_path}" is not a Python file' 
    command = ["python", target_file_path]
    if args :
      command.extend(args)
    subprocess_objt = subprocess.run(command, text=True, timeout=30,cwd=working_directory,capture_output=True)
    output = []
    if subprocess_objt.returncode > 0:
      output =  [f"Process exited with code {subprocess_objt.returncode}"]
    if not subprocess_objt.stdout and not subprocess_objt.stderr :
      output.append("No output produced")
    if subprocess_objt.stdout:
      output.append(f"STDOUT: {subprocess_objt.stdout}")
    if subprocess_objt.stderr:
      output.append(f"STDERR: {subprocess_objt.stderr}")
    return "\n".join(output)
   




  except Exception as e:
    return f"Error: executing Python file: {e}"