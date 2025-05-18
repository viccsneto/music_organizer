# Music Organizer

Organize your music files into folders based on their metadata (genre, decade, bitrate, etc.).

## Features
- Organizes music files into a directory structure based on customizable patterns
- Supports filtering and classifying by bitrate
- Detects duplicate files
- Supports multiple file formats (e.g., mp3, m4a)

## Requirements
- Python 3.8+
- [tinytag](https://pypi.org/project/tinytag/)
- [Conda Miniforge](https://github.com/conda-forge/miniforge) or Miniconda (for environment setup)

## Setup

1. **Clone the repository and enter the project directory:**
   ```bash
   git clone <your-repo-url>
   cd music_organizer
   ```

2. **Run the environment setup script:**
   ```bash
   bash setup_environment.sh
   ```
   This will create and activate a conda environment and install all dependencies.

3. **Activate the environment (if not already active):**
   ```bash
   conda activate music-organizer-env
   ```

## Usage

Run the script with the required arguments:

```bash
python tagger.py --source_path <source_folder> --destination_path <destination_folder>
```

### Optional Arguments
- `--organizing_pattern`: Pattern for directory structure (default: `{genre}/{decade}/{bitrateclass}/`)
- `--file_format`: Comma-separated file extensions to scan (default: `mp3,m4a`)
- `--desired_bitrate`: Bitrate threshold for classification/filtering (default: `192`)

### Example
```bash
python tagger.py --source_path sample_music --destination_path organized_music --organizing_pattern "{genre}/{decade}/{bitrateclass}/" --file_format "mp3,m4a" --desired_bitrate 192
```

## Notes
- The script will print out the organization process and warn about duplicates.
- Requirements are managed via `pyproject.toml` and `setup_environment.sh`. The old `requirements.txt` is deprecated.

## License
MIT
