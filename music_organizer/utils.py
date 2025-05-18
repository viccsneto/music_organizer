import re

BANNER = '''
 __  __           _         ___                        _              
|  \/  |_   _ ___(_) ___   / _ \ _ __ __ _  __ _ _ __ (_)_______ _ __ 
| |\/| | | | / __| |/ __| | | | | '__/ _` |/ _` | '_ \| |_  / _ \ '__|
| |  | | |_| \__ \ | (__  | |_| | | | (_| | (_| | | | | |/ /  __/ |   
|_|  |_|\__,_|___/_|\___|  \___/|_|  \__, |\__,_|_| |_|_/___\___|_|
                                     |___/                            
                                                  Organize music files
'''
HORIZONTAL_RULE = "-" * 140
DEFAULT_DESIRED_BITRATE = 192
organizing_pattern_regular_expression = re.compile(r"\{.*?\}")

def sanitize_metadata_tag(value):
    if isinstance(value, list):
        value = " ".join(value)
    sanitized_value = str(value).strip()
    sanitized_value = sanitized_value.replace("/", "_")
    sanitized_value = sanitized_value.replace("\\", "_")
    sanitized_value = sanitized_value.replace("..", "_")
    sanitized_value = sanitized_value.replace("\"", "_")
    sanitized_value = sanitized_value.replace("|", "_")
    sanitized_value = sanitized_value.replace(":", "_")
    sanitized_value = sanitized_value.replace(">", "_")
    sanitized_value = sanitized_value.replace("<", "_")
    sanitized_value = sanitized_value.replace("?", "_")
    sanitized_value = sanitized_value.replace("*", "_")
    return sanitized_value
