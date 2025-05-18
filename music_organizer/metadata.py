import re
import utils

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
        elif tag == "decade":
            year = str(metadata["year"]).strip()
            if year.isdigit():
                metadata[tag] = year[0:-1] + "0"
            else:
                metadata[tag] = "UNKNOWN_DECADE"
        if tag in metadata and metadata[tag]:
            organizing_tag_value = utils.sanitize_metadata_tag(metadata[tag])
            basic_path = basic_path.replace(organizing_tag, organizing_tag_value)
        else:
            basic_path = basic_path.replace(organizing_tag, "UNKNOWN_" + tag.upper())
    return basic_path
