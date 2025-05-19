import re
from src import utils

def build_basic_path(destination_path, organizing_pattern):
    basic_path = destination_path + "/" + organizing_pattern
    basic_path = basic_path.replace("//", "/")
    basic_path = basic_path.replace("\\", "/")
    return basic_path

def get_destination_path(metadata, basic_path, desired_bitrate):
    organizing_tags = utils.organizing_pattern_regular_expression.findall(basic_path)
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
        elif tag == "year":
            year = metadata.get(tag)
            if isinstance(year, list):
                year = year[0]
            if isinstance(year, str):
                match = re.search(r'\d+', year)
                if match:
                    metadata[tag] = int(match.group(0))
                else:
                    metadata[tag] = None
            
        if tag in metadata and metadata[tag]:
            organizing_tag_value = utils.sanitize_metadata_tag(metadata[tag])
            basic_path = basic_path.replace(organizing_tag, organizing_tag_value)
        else:
            basic_path = basic_path.replace(organizing_tag, "UNKNOWN_" + tag.upper())
    return basic_path
