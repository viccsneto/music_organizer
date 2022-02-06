#!/bin/env python3

# native
import glob
import hashlib
import re
import os
import shutil
import sys

# 3rparty
import click
from tinytag import TinyTag


BANNER = """ ____      _   ____   _    ____ _   _ _   _   __  __           _      
|  _ \    | | |  _ \ / \  / ___| | | | | | | |  \/  |_   _ ___(_) ___ 
| | | |_  | | | |_) / _ \| |   | |_| | | | | | |\/| | | | / __| |/ __|
| |_| | |_| | |  __/ ___ \ |___|  _  | |_| | | |  | | |_| \__ \ | (__ 
|____/ \___/  |_| /_/   \_\____|_| |_|\___/  |_|  |_|\__,_|___/_|\___|
                                                                      
  ___                        _              
 / _ \ _ __ __ _  __ _ _ __ (_)_______ _ __ 
| | | | '__/ _` |/ _` | '_ \| |_  / _ \ '__|
| |_| | | | (_| | (_| | | | | |/ /  __/ |   
 \___/|_|  \__, |\__,_|_| |_|_/___\___|_|   
           |___/                            

                                                  Organize music files
"""
HORIZONTAL_RULE = "-" * 140


@click.command()
@click.option(
    "--source_path",
    help="The parent folder of the directory tree containing all music files you want to organize",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    required=True,
)
@click.option(
    "--destination_path",
    help="The parent folder where the music files are going to be organized",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    required=True,
)
@click.option(
    "--organizing_pattern",
    help='The pattern describing how the directories hierarchy is going to be created. (e.g., "{genre}/{decade}/{bitrateclass}/") will derive something like "Rock/1980/GOOD_BITRATE/',
    type=str,
    default="{genre}/{decade}/{bitrateclass}/",
)
@click.option(
    "--file_format",
    help='Comma separated file extensions to scan. (e.g., "mp3,m4a")',
    type=str,
    default="mp3,m4a",
)
@click.option(
    "--desired_bitrate",
    help="Parameter used to calculate {bitratelevel} or to be used as a filter for {bitrateclass} or {bitratefilter}",
    type=int,
    default=100,
)
def cmd(
    source_path, destination_path, organizing_pattern, file_format, desired_bitrate
):
    """Ad-hoc helper tool for organize music files"""

    try:
        print(BANNER)
        file_extensions = file_format.split(",")

        for extension in file_extensions:
            search_path = source_path + "/**/*." + extension
            files = sorted(list(glob.glob(search_path, recursive=True)))
            for filename in files:
                process_file(
                    filename, destination_path, organizing_pattern, desired_bitrate
                )

        find_duplicated()
    except KeyboardInterrupt:
        print("\nBye...\n")
    except Exception as error:
        print("\nSomething went wrong:\n" + str(error))


organizing_pattern_regular_expression = re.compile(r"\{.*?\}")


def sanitize_metadata_tag(value):
    sanitized_value = str(value).strip()
    sanitized_value = sanitized_value.replace("/", "_")
    sanitized_value = sanitized_value.replace("\\", "_")
    sanitized_value = sanitized_value.replace("..", "_")
    sanitized_value = sanitized_value.replace("'", "_")
    sanitized_value = sanitized_value.replace('"', "_")
    sanitized_value = sanitized_value.replace("|", "_")
    sanitized_value = sanitized_value.replace(":", "_")
    sanitized_value = sanitized_value.replace(">", "_")
    sanitized_value = sanitized_value.replace("<", "_")
    sanitized_value = sanitized_value.replace("?", "_")
    sanitized_value = sanitized_value.replace("*", "_")

    return sanitized_value


def build_basic_path(destination_path, organizing_pattern):

    basic_path = destination_path + "/" + organizing_pattern
    basic_path = basic_path.replace("//", "/")
    basic_path = basic_path.replace("\\", "/")
    return basic_path


def get_destination_path(metadata, basic_path, desired_bitrate):

    organizing_tags = organizing_pattern_regular_expression.findall(basic_path)
    for organizing_tag in organizing_tags:
        tag = organizing_tag[1:-1]

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
            metadata[tag] = str(metadata["year"]).strip()[0:-1] + "0"

        if metadata[tag]:
            organizing_tag_value = sanitize_metadata_tag(metadata[tag])
            basic_path = basic_path.replace(organizing_tag, organizing_tag_value)
        else:
            basic_path = basic_path.replace(organizing_tag, "UNKNOWN")

    return basic_path


processed_files = dict()


def process_file(filename, destination_path, organizing_pattern, desired_bitrate):
    metadata = TinyTag.get(filename).as_dict()
    baic_path = build_basic_path(destination_path, organizing_pattern)
    destination_path = get_destination_path(metadata, baic_path, desired_bitrate)
    if destination_path:
        print(f'[+]"{filename}" ==> "{destination_path}"')
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
        print(f'[-]"{filename}" was filtered out')


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
            candidate_digests[digest] = list()
        candidate_digests[digest].append(candidate)

    for digests in candidate_digests.keys():
        if len(candidate_digests[digest]) > 1:
            colliding.append(candidate_digests[digest])

    return colliding


def find_duplicated():
    for destination_folder in processed_files:
        for size in processed_files[destination_folder]:
            candidates = processed_files[destination_folder][size]
            if len(candidates) > 1:
                colliding = find_colliding(candidates)
                if len(colliding) > 0:
                    print(HORIZONTAL_RULE)
                    print(
                        f'The following files are duplicated in "{destination_folder}":'
                    )
                    print(HORIZONTAL_RULE)
                    for file_list in colliding:
                        for i in range(len(file_list)):
                            print(f"\t{i+1} {file_list[i]}")
                        print("\n\n")
                    print("###")


if __name__ == "__main__":
    cmd()
