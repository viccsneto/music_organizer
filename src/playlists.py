import os
from collections import defaultdict
from tinytag import TinyTag

def generate_playlists(destination_path, file_formats):
    genre_map = defaultdict(list)

    for root, _, files in os.walk(destination_path):
        for file in files:
            
            if any(file.lower().endswith(ext) for ext in file_formats):
                full_path = os.path.join(root, file)
            
                try:
                    tag = TinyTag.get(full_path)
                    genre = (tag.genre or "Unknown").strip().replace(" ", "_")
                    genre_map[genre].append(full_path)
            
                except Exception as e:
                    print(f"Skipping {full_path}: {e}")

    for genre, tracks in genre_map.items():
        playlist_filename = f"genre_{genre}.m3u"
        playlist_path = os.path.join(destination_path, playlist_filename)
        
        with open(playlist_path, "w", encoding="utf-8") as f:
            for track in tracks:
                f.write(f"{track}\n")
        
        print(f"Generated playlist: {playlist_path}")
