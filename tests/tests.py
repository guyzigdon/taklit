from detectors.gemini_detector import detect_vinyl
from detectors.audio_detection import get_song_info
from models.vinyl_information import VinylInformation
from models.song_information import SongInformation

def test_detect_image():
    image_path = "tests/resources/Dark_Side_of_the_Moon.jpg"
    result = detect_vinyl(image_path)
    dark_side_of_the_moon_tracks = [
        "Speak to Me",
        "Breathe",
        "On the Run",
        "Time",
        "The Great Gig in the Sky",
        "Money",
        "Us and Them",
        "Any Colour You Like",
        "Brain Damage",
        "Eclipse"
    ]
    expected = VinylInformation(artist="Pink Floyd", album_name="The Dark Side of the Moon", genre="Progressive Rock", year=1973, tracklist=dark_side_of_the_moon_tracks)
    assert result == expected

def test_detect_song():
    song_path = "tests/resources/sister_golden_hair.mp3"
    result = get_song_info(song_path)
    expected = SongInformation(title="Sister Golden Hair", lyrics="[Verse 1]\nWell I tried to make it Sunday\nBut I got so damn depressed\nThat I set my sights on Monday\nAnd I got myself undressed\nI ain't ready for the altar\nBut I do agree there's times\nWhen a woman sure can be a friend of mine\n\n[Chorus]\nWell, I keep on thinking about you\nSister Golden Hair surprise\nAnd I just can't live without you\nCan't you see it in my eyes?\nI been one poor correspondent\nAnd I've been too, too hard to find\nBut it doesn't mean\nYou ain't been on my mind\n\n[Bridge]\nWill you meet me in the middle\nWill you meet me in the air?\nWill you love me just a little\nJust enough to show you care?\nWell I tried to fake it\nI don't mind sayin'\nI just can't make it\n[Chorus]\nWell, I keep on thinking about you\nSister Golden Hair surprise\nAnd I just can't live without you\nCan't you see it in my eyes?\nI been one poor correspondent\nAnd I've been too, too hard to find\nBut it doesn't mean\nYou ain't been on my mind\n\n[Outro / Bridge]\nWill you meet me in the middle\nWill you meet me in the air?\nWill you love me just a little\nJust enough to show you care?\nWell I tried to fake it\nI don't mind sayin'\nI just can't make it", current_time="01:55")
    assert result == expected