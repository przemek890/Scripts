import os
import shutil
import re
""""""""""""""
def clear_subdirectory(path):
    if os.path.exists(path):
        for dir_name in os.listdir(path):
            dir_path = os.path.join(path, dir_name)
            if re.match(r'\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}', dir_name) and os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
    else:
        print(f"Subdirectory {path} does not exist.")


