#!/bin/env python3
import argparse
import glob
import os
import sys
from tinytag import TinyTag

parser = argparse.ArgumentParser(description='Organize music files')
parser.add_argument('--source_path', dest="source_path",  type=str, help='The parent folder of the directory tree containing all music files you want to organize.', required=True)

parser.add_argument('--destination_path', dest="destination_path", type=str, help='The parent folder where the music files are going to be organized.', required=True)

parser.add_argument('--organization_pattern', dest="organization_pattern", type=str, help='The pattern describing how the directories hierarchy is going to be created. (e.g., "{genre}/{year}/{bitrate}/") will derive something like "Rock/1980/320/"', default='{genre}/{year}/{bitrate}/')

parser.add_argument('--file_format', dest="file_format", type=str, help='Comma separated file extensions to scan. (e.g., "mp3,m4a)" will derive something like "Rock/1980/320/"', default='mp3,m4a')

def process_file(filename):
    metadata = TinyTag.get(filename)
    print(filename, metadata.artist)

args = parser.parse_args()

file_extensions = args.file_format.split(',')

for extension in file_extensions:
    search_path = args.source_path + '/**/*.' + extension
    files = glob.glob(search_path,recursive = True)
    for file in files:
        process_file(file)

#os.makedirs("/tmp/Pachu/meudiretorio/querido/e/talz/")
#filename = sys.argv[1]
#metadata = TinyTag.get(filename)
#print(metadata)
#print(metadata.artist)