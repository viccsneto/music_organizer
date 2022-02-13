#!/bin/env python3
import argparse
import glob
import hashlib
import os
import re
import shutil
import sys
import traceback

#third party
from tinytag import TinyTag


BANNER = """ ____      _   ____   _    ____ _   _ _   _   __  __           _      
|  _ \    | | |  _ \ / \  / ___| | | | | | | |  \/  |_   _ ___(_) ___ 
| | | |_  | | | |_) / _ \| |   | |_| | | | | | |\/| | | | / __| |/ __|
| |_| | |_| | |  __/ ___ \ |___|  _  | |_| | | |  | | |_| \__ \ | (__ 
|____/ \___/  |_| /_/   \_\____|_| |_|\___/  |_|  |_|\__,_|___/_|\___|
                                                                      
  ___                        _              
 / _ \ _ __ __ _  __ _ _ __ (_)_______ _ __ 
| | | | "__/ _` |/ _` | "_ \| |_  / _ \ "__|
| |_| | | | (_| | (_| | | | | |/ /  __/ |   
 \___/|_|  \__, |\__,_|_| |_|_/___\___|_|   
           |___/                            

                                                  Organize music files
"""
HORIZONTAL_RULE = "-" * 140

DEFAULT_DESIRED_BITRATE = 192

parser = argparse.ArgumentParser(description="Organize music files")
parser.add_argument("--source_path", dest="source_path",  type=str, help="The parent folder of the directory tree containing all music files you want to organize.", required=True)
parser.add_argument("--destination_path", dest="destination_path", type=str, help="The parent folder where the music files are going to be organized.", required=True)
parser.add_argument("--organizing_pattern", dest="organizing_pattern", type=str, help="The pattern describing how the directories hierarchy is going to be created. (e.g., \"{genre}/{decade}/{bitrateclass}/\") will derive something like \"Rock/1980/GOOD_BITRATE/\"", default="{genre}/{decade}/{bitrateclass}/")
parser.add_argument("--file_format", dest="file_format", type=str, help="Comma separated file extensions to scan. (e.g., \mp3,m4a\)", default="mp3,m4a")
parser.add_argument("--desired_bitrate", dest="desired_bitrate", type=int, help="Parameter used to calculate {bitratelevel} or to be used as a filter for {bitrateclass} or {bitratefilter}", default=DEFAULT_DESIRED_BITRATE)
args = parser.parse_args()
organizing_pattern_regular_expression = re.compile(r"\{.*?\}")

def sanitize_metadata_tag(value):  
    sanitized_value = str(value).strip()
    sanitized_value = sanitized_value.replace("/","_")
    sanitized_value = sanitized_value.replace("\\","_")
    sanitized_value = sanitized_value.replace("..","_")
    sanitized_value = sanitized_value.replace("\"","_")
    sanitized_value = sanitized_value.replace("\"","_")
    sanitized_value = sanitized_value.replace("|","_")
    sanitized_value = sanitized_value.replace(":","_")
    sanitized_value = sanitized_value.replace(">","_")
    sanitized_value = sanitized_value.replace("<","_")
    sanitized_value = sanitized_value.replace("?","_")
    sanitized_value = sanitized_value.replace("*","_")

    return sanitized_value

def build_basic_path(destination_path, organizing_pattern):
    basic_path = destination_path + "/" + organizing_pattern
    basic_path = basic_path.replace("//", "/")
    basic_path = basic_path.replace("\\", "/")

    return basic_path


def get_destination_path(metadata, basic_path, desired_bitrate):
    organizing_tags = organizing_pattern_regular_expression.findall(basic_path)
    for organizing_tag in organizing_tags:
        organizing_tag = organizing_tag.strip()
        tag = organizing_tag[1:-1].strip()

        if tag == "bitratelevel":
            metadata[tag] = metadata["bitrate"] // desired_bitrate
        elif tag == "bitrateclass":
            if metadata["bitrate"] >= desired_bitrate:
                metadata[tag] = "GOOD_BITRATE"
            else:
                metadata[tag] = "POOR_BITRATE"
        elif tag == "bitratefilter":
            if metadata["bitrate"] < desired_bitrate:
                return None
            else:
                metadata[tag] = "FILTERED_BITRATE"
        elif tag == "bitrate":
            metadata[tag] = int(metadata[tag])
        elif tag == "decade":
            year = str(metadata["year"]).strip()
            if year.isdigit():
                metadata[tag] = year[0:-1] + "0"
            else:
                metadata[tag] = "UNKNOWN_DECADE"

        if metadata[tag]:
            organizing_tag_value = sanitize_metadata_tag(metadata[tag])
            basic_path = basic_path.replace(organizing_tag, organizing_tag_value)
        else:
            basic_path = basic_path.replace(organizing_tag, "UNKNOWN_" + tag.upper())

    return basic_path

def process_file(processed_files, filename, destination_path, organizing_pattern, desired_bitrate):
    metadata = TinyTag.get(filename).as_dict()
    basic_path = build_basic_path(destination_path, organizing_pattern)
    destination_path = get_destination_path(metadata, basic_path, desired_bitrate)
    if destination_path:
        print(f"[+]\"{filename}\" ==> \"{destination_path}\"")
        if not os.path.isdir(destination_path):
            os.makedirs(destination_path)

        shutil.copy2(filename, destination_path)

        if not destination_path in processed_files.keys():
            processed_files[destination_path] = dict()

        size = os.path.getsize(filename)
        if not size in processed_files[destination_path].keys():
            processed_files[destination_path][size] = list()

        processed_files[destination_path][size].append(filename)
    else:
        print(f"[-]\"{filename}\" was filtered out")


def get_digest(filename):
    BLOCKSIZE = 65536
    hasher = hashlib.blake2b()
    with open(filename, "rb") as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


def find_colliding(candidates):
    colliding = []
    candidate_digests = dict()
    for candidate in candidates:
        digest = get_digest(candidate)
        if not digest in candidate_digests.keys():
            candidate_digests[digest] = set()
        filename_only = os.path.basename(candidate)
        candidate_digests[digest].add(filename_only)

    for digests in candidate_digests.keys():
        if len(candidate_digests[digest]) > 1:
            colliding.append(list(candidate_digests[digest]))

    return colliding


def find_duplicates(processed_files):
    for destination_folder in processed_files:
        for size in processed_files[destination_folder]:
            candidates = processed_files[destination_folder][size]
            if len(candidates) > 1:
                colliding = find_colliding(candidates)
                if len(colliding) > 0:
                    print(HORIZONTAL_RULE)
                    print(f"The following files are duplicated in \"{destination_folder}\":")
                    print(HORIZONTAL_RULE)
                    for file_list in colliding:
                        for i in range(len(file_list)):
                            print(f"\t\"{file_list[i]}\"")
                    print("\n")
def main():
    try:
        print(BANNER)    
        processed_files = dict()
        file_extensions = args.file_format.split(",")

        if not os.path.isdir(args.source_path):
            print(f"The source path \"{args.source_path}\" doesn't exist...")
            return
        for extension in file_extensions:
            search_path = args.source_path + "/**/*." + extension
            files = sorted(list(glob.glob(search_path,recursive = True)))
            for file in files:
                process_file(processed_files, file, args.destination_path, args.organizing_pattern, args.desired_bitrate)

        find_duplicates(processed_files)
    except KeyboardInterrupt:
        print("\nBye...\n")
    except Exception as error:
        print("\nSomething went wrong:\n" + str(error))
        print(traceback.format_exc())

if __name__ == "__main__":
    main()