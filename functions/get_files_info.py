import os


def get_files_info(working_directory, directory="."):
  try:
    absolute_path_wd = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path_wd, directory))
    valid_target_dir = os.path.commonpath([absolute_path_wd,target_dir]) == absolute_path_wd
    if not valid_target_dir:
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
      return f'Error: "{directory}" is not a directory'
    dir_files = os.listdir(target_dir)
    
    str_files = "\n".join(list(map(lambda item:f"- {item}: file_size={os.path.getsize(os.path.join(target_dir,item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir,item))}",dir_files)))
    return str_files
  except Exception as e:
    return f"Error: {e}"
    
