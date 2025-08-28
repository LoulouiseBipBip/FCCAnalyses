#!/usr/bin/env python3

import os
import glob

# Directory where ROOT files are located
directory = "/eos/user/l/lberiet/Histmaker/ttZ_differential/3l"

# Find all ROOT files in the directory
root_files = glob.glob(os.path.join(directory, "*.root"))

# Rename each ROOT file by adding _4l before the extension
for file_path in root_files:
    file_name = os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)
    new_name = f"{name}_3l{ext}"
    new_path = os.path.join(directory, new_name)
    
    if os.path.exists(new_path):
        print(f"File {new_path} already exists, skipping {file_name}")
        continue
    
    try:
        os.rename(file_path, new_path)
        print(f"Renamed {file_name} to {new_name}")
    except Exception as e:
        print(f"Error renaming {file_name} to {new_name}: {e}")

print("Renaming process completed.") 