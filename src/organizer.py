import os
import shutil
from tinytag import TinyTag
from src import metadata

def process_file(processed_files, filename, destination_path, organizing_pattern, desired_bitrate):
    metadata_dict = TinyTag.get(filename).as_dict()
    basic_path = metadata.build_basic_path(destination_path, organizing_pattern)
    destination_path = metadata.get_destination_path(metadata_dict, basic_path, desired_bitrate)
    if destination_path:
        print(f"[+]\"{filename}\" ==> \"{destination_path}\"")
        if not os.path.isdir(destination_path):
            os.makedirs(destination_path)
        shutil.copy2(filename, destination_path)
        if destination_path not in processed_files.keys():
            processed_files[destination_path] = dict()
        size = os.path.getsize(filename)
        if size not in processed_files[destination_path].keys():
            processed_files[destination_path][size] = list()
        processed_files[destination_path][size].append(filename)
    else:
        print(f"[-]\"{filename}\" was filtered out")
