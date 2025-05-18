import argparse
from src import utils

def parse_args():
    parser = argparse.ArgumentParser(description="Organize music files")
    parser.add_argument("--source_path", dest="source_path",  type=str, help="The parent folder of the directory tree containing all music files you want to organize.", required=True)
    parser.add_argument("--destination_path", dest="destination_path", type=str, help="The parent folder where the music files are going to be organized.", required=True)
    parser.add_argument("--organizing_pattern", dest="organizing_pattern", type=str, help="The pattern describing how the directories hierarchy is going to be created. (e.g., '{genre}/{decade}/{bitrateclass}/') will derive something like 'Rock/1980/GOOD_BITRATE/'", default="{genre}/{decade}/{bitrateclass}/")
    parser.add_argument("--file_format", dest="file_format", type=str, help="Comma separated file extensions to scan. (e.g., mp3,m4a)", default="mp3,m4a")
    parser.add_argument("--desired_bitrate", dest="desired_bitrate", type=int, help="Parameter used to calculate {bitratelevel} or to be used as a filter for {bitrateclass} or {bitratefilter}", default=utils.DEFAULT_DESIRED_BITRATE)
    return parser.parse_args()
