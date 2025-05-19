# Tests for the music organizer CLI and sample_music repository
# Moved from test_music_organizer.py
import os
import shutil
import pytest
import filecmp
from pathlib import Path
import subprocess

SAMPLE_MUSIC = Path(__file__).parent.parent / "sample_music"
OUTPUT = Path(__file__).parent.parent / "tests_output"
SCRIPT = Path(__file__).parent.parent / "music_organizer.py"

EXPECTED_OUTPUTS = [
    ("Electric Pulse.mp3", "2013/Electronic/Energy Reactor/Energy Emission/Electric Pulse.mp3"),
    ("Repeated Songs/Harmony's Call - Harmony Collection.mp3", "UNKNOWN_YEAR/orchestral/Roberto Owen/Uplifting Pearls/Harmony's Call - Harmony Collection.mp3"),
    ("Repeated Songs/Rave in the Sky - Remix.mp3", "2013/synth-driven/Ravengar/Real Rave Remix/Rave in the Sky - Remix.mp3"),
    ("Songs/City Lights Serenade.mp3", "3024/Jazz/Golisea/Golisea and the seagulss/City Lights Serenade.mp3"),
    ("Songs/Harmony's Call.mp3", "UNKNOWN_YEAR/UNKNOWN_GENRE/Roberto Owen/Uplifting Pearls/Harmony's Call.mp3"),
    ("Songs/Neon Steel.mp3", "1999/Electronic/Mega Master Band/Neon Steel Strikes Again/Neon Steel.mp3"),
    ("Songs/Rave in the Sky.mp3", "UNKNOWN_YEAR/UNKNOWN_GENRE/Ravengar/Real Rave Remix/Rave in the Sky.mp3"),
    ("Songs/Shattered Chains.mp3", "2005/UNKNOWN_GENRE/HypnoScreamer/There are things that should be unnamed/Shattered Chains.mp3"),
    ("Songs/Whispers of the River.mp3", "1352/Folk/Drizzt Do'Barden/Tales of Underdark/Whispers of the River.mp3"),
    ("Velvet Riff.mp3", "1983/Jazz/Crazy Jazzy/Crazy Jazzy/Velvet Riff.mp3"),
    ("Wrath of Oblivion.mp3", "1995/Heavy Metal/Machine Michael/Machine Code/Wrath of Oblivion.mp3"),
]

def clean_output():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(exist_ok=True)

def run_organizer():
    subprocess.run([
        "python3", str(SCRIPT),
        "--source_path", str(SAMPLE_MUSIC),
        "--destination_path", str(OUTPUT),
        "--organizing_pattern", "{year}/{genre}/{artist}/{album}"
    ], check=True)

def test_music_organizer_full_run():
    clean_output()
    run_organizer()
    for src_rel, dst_rel in EXPECTED_OUTPUTS:
        dst_path = OUTPUT / dst_rel
        assert dst_path.exists(), f"Expected file not found: {dst_path}"
        src_path = SAMPLE_MUSIC / src_rel
        # Only compare if file exists in sample_music
        if src_path.exists():
            assert filecmp.cmp(src_path, dst_path, shallow=False), f"File content mismatch: {src_path} vs {dst_path}"

def test_no_extra_files():
    clean_output()
    run_organizer()
    # Collect all expected output files
    expected_files = set((OUTPUT / dst_rel).resolve() for _, dst_rel in EXPECTED_OUTPUTS)
    # Walk output dir and check for unexpected files
    for root, _, files in os.walk(OUTPUT):
        for f in files:
            fpath = Path(root) / f
            assert fpath.resolve() in expected_files, f"Unexpected file in output: {fpath}"

def test_music_organizer_decade_pattern():
    import shutil
    from pathlib import Path
    import filecmp
    import subprocess
    OUTPUT = Path("tests_output/decade_test_run")
    SAMPLE_MUSIC = Path("sample_music")
    SCRIPT = Path("music_organizer.py")
    # Clean output subfolder
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    # Run organizer with {decade} pattern
    subprocess.run([
        "python3", str(SCRIPT),
        "--source_path", str(SAMPLE_MUSIC),
        "--destination_path", str(OUTPUT),
        "--organizing_pattern", "{decade}/{genre}/{artist}/{album}"
    ], check=True)
    # Expected outputs (from previous ground truth)
    expected_outputs = [
        ("Electric Pulse.mp3", "2010/Electronic/Energy Reactor/Energy Emission/Electric Pulse.mp3"),
        ("Repeated Songs/Harmony's Call - Harmony Collection.mp3", "UNKNOWN_DECADE/orchestral/Roberto Owen/Uplifting Pearls/Harmony's Call - Harmony Collection.mp3"),
        ("Repeated Songs/Rave in the Sky - Remix.mp3", "2010/synth-driven/Ravengar/Real Rave Remix/Rave in the Sky - Remix.mp3"),
        ("Songs/City Lights Serenade.mp3", "3020/Jazz/Golisea/Golisea and the seagulss/City Lights Serenade.mp3"),
        ("Songs/Harmony's Call.mp3", "UNKNOWN_DECADE/UNKNOWN_GENRE/Roberto Owen/Uplifting Pearls/Harmony's Call.mp3"),
        ("Songs/Neon Steel.mp3", "1990/Electronic/Mega Master Band/Neon Steel Strikes Again/Neon Steel.mp3"),
        ("Songs/Rave in the Sky.mp3", "UNKNOWN_DECADE/UNKNOWN_GENRE/Ravengar/Real Rave Remix/Rave in the Sky.mp3"),
        ("Songs/Shattered Chains.mp3", "2000/UNKNOWN_GENRE/HypnoScreamer/There are things that should be unnamed/Shattered Chains.mp3"),
        ("Songs/Whispers of the River.mp3", "1350/Folk/Drizzt Do'Barden/Tales of Underdark/Whispers of the River.mp3"),
        ("Velvet Riff.mp3", "1980/Jazz/Crazy Jazzy/Crazy Jazzy/Velvet Riff.mp3"),
        ("Wrath of Oblivion.mp3", "1990/Heavy Metal/Machine Michael/Machine Code/Wrath of Oblivion.mp3"),
    ]
    for src_rel, dst_rel in expected_outputs:
        dst_path = OUTPUT / dst_rel
        assert dst_path.exists(), f"Expected file not found: {dst_path}"
        src_path = SAMPLE_MUSIC / src_rel
        if src_path.exists():
            assert filecmp.cmp(src_path, dst_path, shallow=False), f"File content mismatch: {src_path} vs {dst_path}"
    # Check for no extra files
    expected_files = set((OUTPUT / dst_rel).resolve() for _, dst_rel in expected_outputs)
    for root, _, files in os.walk(OUTPUT):
        for f in files:
            fpath = Path(root) / f
            assert fpath.resolve() in expected_files, f"Unexpected file in output: {fpath}"
