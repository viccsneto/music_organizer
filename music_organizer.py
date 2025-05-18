#!/usr/bin/env python3
import glob
import os
import sys
import traceback

# Ensure src is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import cli, utils, organizer, duplicates

def main():
    try:
        print(utils.BANNER)
        processed_files = dict()
        args = cli.parse_args()
        file_extensions = args.file_format.split(",")
        if not os.path.isdir(args.source_path):
            print(f"The source path '{args.source_path}' doesn't exist...")
            return
        for extension in file_extensions:
            search_path = os.path.join(args.source_path, f"**/*.{extension}")
            files = sorted(list(glob.glob(search_path, recursive=True)))
            for file in files:
                organizer.process_file(processed_files, file, args.destination_path, args.organizing_pattern, args.desired_bitrate)
        duplicates.find_duplicates(processed_files)
    except KeyboardInterrupt:
        print("\nBye...\n")
    except Exception as error:
        print("\nSomething went wrong:\n" + str(error))
        print(traceback.format_exc())

if __name__ == "__main__":
    main()