import os


def get_files_info(working_directory, directory="."):
  absolute_path_wd = os.path.abspath(working_directory)
  target_dir = os.path.normpath(os.path.join(absolute_path_wd, directory))
  valid_target_dir = os.path.commonpath([absolute_path_wd,target_dir]) == absolute_path_wd
  if not valid_target_dir:
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  if not os.path.isdir(directory):
    return f'Error: "{directory}" is not a directory'
  dir_files = os.listdir(directory)
  
  str_files = "\n".join(list(map(lambda item: f"- {item}: file_size={os.path.getsize(item)} bytes, is_dir={os.path.isdir(item)}",dir_files)))
  print(str_files)

get_files_info("calculator")