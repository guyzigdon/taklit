from gemini_detector.gemini_detector import detect_vinyl
from vinyl_information import VinylInformation

def test_detect_image():
    image_path = "tests/Dark_Side_of_the_Moon.jpg"
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