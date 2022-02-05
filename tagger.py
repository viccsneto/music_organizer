#!/bin/env python3
import argparse
import glob
import hashlib
import re
import os
import shutil
import sys
from tinytag import TinyTag

parser = argparse.ArgumentParser(description='Organize music files')
parser.add_argument('--source_path', dest="source_path",  type=str, help='The parent folder of the directory tree containing all music files you want to organize.', required=True)

parser.add_argument('--destination_path', dest="destination_path", type=str, help='The parent folder where the music files are going to be organized.', required=True)

parser.add_argument('--organization_pattern', dest="organization_pattern", type=str, help='The pattern describing how the directories hierarchy is going to be created. (e.g., "{genre}/{decade}/{bitrate}/") will derive something like "Rock/1980/320/"', default='{genre}/{decade}/{bitrate}/')

parser.add_argument('--file_format', dest="file_format", type=str, help='Comma separated file extensions to scan. (e.g., "mp3,m4a)" will derive something like "Rock/1980/320/"', default='mp3,m4a')

args = parser.parse_args()

organization_pattern_regular_expression = re.compile(r'\{.*?\}')

def get_destination_path(metadata):
    basic_path = args.destination_path +"/" + args.organization_pattern
    basic_path = basic_path.replace("//","/")
    basic_path = basic_path.replace("\\","/")

    organization_tags = organization_pattern_regular_expression.findall(basic_path)
    for organization_tag in organization_tags:
        tag = organization_tag[1:-1]
        if (tag == 'decade'):
            metadata[tag] = str(metadata['year'])[0:-1]+"0"
        
        if (metadata[tag]):
            if (tag == 'bitrate'):
                metadata[tag] = int(metadata[tag])
            basic_path = basic_path.replace(organization_tag, str(metadata[tag]))
        else:
            basic_path = basic_path.replace(organization_tag, "Unknown")

    return basic_path
    

processed_files = dict()

def process_file(filename):
    metadata = TinyTag.get(filename).as_dict()
    destination_path = get_destination_path(metadata)
    print(f'"{filename}" will be copied to "{destination_path}"')    
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)
    
    shutil.copy2(filename, destination_path)
    
    if (not destination_path in processed_files.keys()):
        processed_files[destination_path] = dict()

    size = os.path.getsize(filename)
    if (not size in processed_files[destination_path].keys()):
        processed_files[destination_path][size] = list()
        
    processed_files[destination_path][size].append(filename)


file_extensions = args.file_format.split(',')

for extension in file_extensions:
    search_path = args.source_path + '/**/*.' + extension
    files = sorted(list(glob.glob(search_path,recursive = True)))
    for file in files:
        process_file(file)


def get_digest(filename):
    BLOCKSIZE = 65536
    hasher = hashlib.blake2b()
    with open(filename, 'rb') as afile:
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
            if (len(candidates) > 1):
                colliding = find_colliding(candidates)
                if len(colliding) > 0:
                    print(f'The following files are duplicated in "{destination_folder}" ----------------------')
                    for file_list in colliding:
                        for i in range(len(file_list)):
                            print(f"{i+1} {file_list[i]}")
                        print('\n\n')                        
                    print('---------------------------------------------------------------------------------')

find_duplicated()