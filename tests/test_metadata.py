import pytest
from src import metadata

@pytest.mark.parametrize(
    "metadata_dict, basic_path, desired_bitrate, expected",
    [
        # Electric Pulse.mp3
        (dict(year="2013", genre="Electronic", artist="Energy Reactor", album="Energy Emission"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/2013/Electronic/Energy Reactor/Energy Emission"),
        # Repeated Songs/Harmony's Call - Harmony Collection.mp3
        (dict(year=None, genre="orchestral", artist="Roberto Owen", album="Uplifting Pearls"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/UNKNOWN_YEAR/orchestral/Roberto Owen/Uplifting Pearls"),
        # Repeated Songs/Rave in the Sky - Remix.mp3
        (dict(year="2013", genre="synth-driven", artist="Ravengar", album="Real Rave Remix"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/2013/synth-driven/Ravengar/Real Rave Remix"),
        # Songs/City Lights Serenade.mp3
        (dict(year="3024", genre="Jazz", artist="Golisea", album="Golisea and the seagulss"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/3024/Jazz/Golisea/Golisea and the seagulss"),
        # Songs/Harmony's Call.mp3
        (dict(year=None, genre=None, artist="Roberto Owen", album="Uplifting Pearls"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/UNKNOWN_YEAR/UNKNOWN_GENRE/Roberto Owen/Uplifting Pearls"),
        # Songs/Neon Steel.mp3
        (dict(year="1999", genre="Electronic", artist="Mega Master Band", album="Neon Steel Strikes Again"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/1999/Electronic/Mega Master Band/Neon Steel Strikes Again"),
        # Songs/Rave in the Sky.mp3
        (dict(year=None, genre=None, artist="Ravengar", album="Real Rave Remix"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/UNKNOWN_YEAR/UNKNOWN_GENRE/Ravengar/Real Rave Remix"),
        # Songs/Shattered Chains.mp3
        (dict(year="2005", genre=None, artist="HypnoScreamer", album="There are things that should be unnamed"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/2005/UNKNOWN_GENRE/HypnoScreamer/There are things that should be unnamed"),
        # Songs/Whispers of the River.mp3
        (dict(year="1352", genre="Folk", artist="Drizzt Do'Barden", album="Tales of Underdark"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/1352/Folk/Drizzt Do'Barden/Tales of Underdark"),
        # Velvet Riff.mp3
        (dict(year="1983", genre="Jazz", artist="Crazy Jazzy", album="Crazy Jazzy"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/1983/Jazz/Crazy Jazzy/Crazy Jazzy"),
        # Wrath of Oblivion.mp3
        (dict(year="1995", genre="Heavy Metal", artist="Machine Michael", album="Machine Code"),
         "tests_output/{year}/{genre}/{artist}/{album}", 192,
         "tests_output/1995/Heavy Metal/Machine Michael/Machine Code"),
    ]
)
def test_get_destination_path_sample_music(metadata_dict, basic_path, desired_bitrate, expected):
    result = metadata.get_destination_path(dict(metadata_dict), basic_path, desired_bitrate)
    assert result == expected

@pytest.mark.parametrize(
    "metadata_dict, basic_path, desired_bitrate, expected",
    [
        # Year as int
        (dict(year=1987, artist="A"), "music/{decade}/{artist}", 192, "music/1980/A"),
        # Year as string
        (dict(year="1974", artist="B"), "music/{decade}/{artist}", 192, "music/1970/B"),
        # Year as string with text
        (dict(year="Year: 1995", artist="C"), "music/{decade}/{artist}", 192, "music/1990/C"),
        # Year as list
        (dict(year=["2003"], artist="D"), "music/{decade}/{artist}", 192, "music/2000/D"),
        # Year missing
        (dict(artist="E"), "music/{decade}/{artist}", 192, "music/UNKNOWN_DECADE/E"),
        # Year as non-numeric string
        (dict(year="unknown", artist="F"), "music/{decade}/{artist}", 192, "music/UNKNOWN_DECADE/F"),
    ]
)
def test_get_destination_path_decade(metadata_dict, basic_path, desired_bitrate, expected):
    result = metadata.get_destination_path(dict(metadata_dict), basic_path, desired_bitrate)
    assert result == expected

@pytest.mark.parametrize(
    "metadata_dict, basic_path, desired_bitrate, expected",
    [
        # Electric Pulse.mp3
        (dict(year="2013", genre="Electronic", artist="Energy Reactor", album="Energy Emission"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/2010/Electronic/Energy Reactor/Energy Emission"),
        # Harmony's Call - Harmony Collection.mp3
        (dict(year=None, genre="orchestral", artist="Roberto Owen", album="Uplifting Pearls"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/UNKNOWN_DECADE/orchestral/Roberto Owen/Uplifting Pearls"),
        # Rave in the Sky - Remix.mp3
        (dict(year="2013", genre="synth-driven", artist="Ravengar", album="Real Rave Remix"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/2010/synth-driven/Ravengar/Real Rave Remix"),
        # City Lights Serenade.mp3
        (dict(year="3024", genre="Jazz", artist="Golisea", album="Golisea and the seagulss"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/3020/Jazz/Golisea/Golisea and the seagulss"),
        # Harmony's Call.mp3
        (dict(year=None, genre=None, artist="Roberto Owen", album="Uplifting Pearls"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/UNKNOWN_DECADE/UNKNOWN_GENRE/Roberto Owen/Uplifting Pearls"),
        # Neon Steel.mp3
        (dict(year="1999", genre="Electronic", artist="Mega Master Band", album="Neon Steel Strikes Again"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/1990/Electronic/Mega Master Band/Neon Steel Strikes Again"),
        # Rave in the Sky.mp3
        (dict(year=None, genre=None, artist="Ravengar", album="Real Rave Remix"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/UNKNOWN_DECADE/UNKNOWN_GENRE/Ravengar/Real Rave Remix"),
        # Shattered Chains.mp3
        (dict(year="2005", genre=None, artist="HypnoScreamer", album="There are things that should be unnamed"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/2000/UNKNOWN_GENRE/HypnoScreamer/There are things that should be unnamed"),
        # Whispers of the River.mp3
        (dict(year="1352", genre="Folk", artist="Drizzt Do'Barden", album="Tales of Underdark"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/1350/Folk/Drizzt Do'Barden/Tales of Underdark"),
        # Velvet Riff.mp3
        (dict(year="1983", genre="Jazz", artist="Crazy Jazzy", album="Crazy Jazzy"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/1980/Jazz/Crazy Jazzy/Crazy Jazzy"),
        # Wrath of Oblivion.mp3
        (dict(year="1995", genre="Heavy Metal", artist="Machine Michael", album="Machine Code"),
         "tests_output/{decade}/{genre}/{artist}/{album}", 192,
         "tests_output/1990/Heavy Metal/Machine Michael/Machine Code"),
    ]
)
def test_get_destination_path_sample_music_decade(metadata_dict, basic_path, desired_bitrate, expected):
    result = metadata.get_destination_path(dict(metadata_dict), basic_path, desired_bitrate)
    assert result == expected
