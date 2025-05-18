import os
import hashlib
from src import utils

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
        if digest not in candidate_digests:
            candidate_digests[digest] = set()
        candidate_digests[digest].add(candidate)  # Use full path, not just basename
    for digest, files in candidate_digests.items():
        if len(files) > 1:
            colliding.append(list(files))
    return colliding

def find_duplicates(processed_files):
    for destination_folder in processed_files:
        for size in processed_files[destination_folder]:
            candidates = processed_files[destination_folder][size]
            if len(candidates) > 1:
                colliding = find_colliding(candidates)
                if len(colliding) > 0:
                    print(utils.HORIZONTAL_RULE)
                    print(f"The following files are duplicated in \"{destination_folder}\":")
                    print(utils.HORIZONTAL_RULE)
                    for file_list in colliding:
                        for i in range(len(file_list)):
                            print(f"\t\"{file_list[i]}\"")
                    print("\n")
