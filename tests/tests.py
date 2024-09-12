from detectors.gemini_detector import detect_vinyl
from detectors.audio_detector import get_song_info
from models.vinyl_information import VinylInformation
from models.song_information import SongInformation, TimedLyrics, TimedRow

# def test_detect_image():
#     image_path = "tests/resources/Dark_Side_of_the_Moon.jpg"
#     result = detect_vinyl(image_path)
#     dark_side_of_the_moon_tracks = [
#         "Speak to Me",
#         "Breathe",
#         "On the Run",
#         "Time",
#         "The Great Gig in the Sky",
#         "Money",
#         "Us and Them",
#         "Any Colour You Like",
#         "Brain Damage",
#         "Eclipse"
#     ]
#     expected = VinylInformation(artist="Pink Floyd", album_name="The Dark Side of the Moon", genre="Progressive Rock", year=1973, tracklist=dark_side_of_the_moon_tracks)
#     assert result == expected

def test_detect_song():
    song_path = "tests/resources/sister_golden_hair.mp3"
    result = get_song_info(song_path)
    expected_timed_lyrics = TimedLyrics(rows=[TimedRow(start_time=17, text='Well, I tried to make it Sunday, but I got so damn depressed'), TimedRow(start_time=24, text='That I set my sights on Monday and I got myself undressed'), TimedRow(start_time=31, text="I ain't ready for the altar but I do agree there's times"), TimedRow(start_time=38, text='When a woman sure can be a friend of mine'), TimedRow(start_time=45, text="Well, I keep on thinkin' 'bout you, Sister Golden Hair surprise"), TimedRow(start_time=53, text="And I just can't live without you"), TimedRow(start_time=56, text="Can't you see it in my eyes?"), TimedRow(start_time=59, text='I been one poor correspondent, and I been too, too hard to find'), TimedRow(start_time=66, text="But it doesn't mean you ain't been on my mind"), TimedRow(start_time=73, text='Will you meet me in the middle, will you meet me in the air?'), TimedRow(start_time=81, text='Will you love me just a little, just enough to show you care?'), TimedRow(start_time=87, text="Well, I tried to fake it, I don't mind saying, I just can't make it"), TimedRow(start_time=112, text="Well, I keep on thinking 'bout you, Sister Golden Hair surprise"), TimedRow(start_time=119, text="And I just can't live without you, can't you see it in my eyes?"), TimedRow(start_time=126, text='Now I been one poor correspondent, and I been too, too hard to find'), TimedRow(start_time=133, text="But it doesn't mean you ain't been on my mind"), TimedRow(start_time=140, text='Will you meet me in the middle, will you meet me in the air?'), TimedRow(start_time=147, text='Will you love me just a little, just enough to show you care?'), TimedRow(start_time=154, text="Well, I tried to fake it, I don't mind saying, I just can't make it"), TimedRow(start_time=160, text='Doo wop doo wop, doo wop doo wop'), TimedRow(start_time=167, text='Doo wop doo wop, doo wop doo wop'), TimedRow(start_time=169, text='Doo wop doo wop, doo wop doo wop'), TimedRow(start_time=173, text='Doo wop doo wop, doo wop doo wop'), TimedRow(start_time=175, text='Doo wop doo wop, doo wop doo wop'), TimedRow(start_time=178, text='Doo wop doo wop, doo wop doo wop'), TimedRow(start_time=181, text='Doo wop doo wop, doo wop doo wop'), TimedRow(start_time=185, text='Doo wop doo wop, doo wop doo wop')])
    expected = SongInformation(title="Sister Golden Hair", artist= "America", album= "Definitive Pop: America", lyrics="[Verse 1]\nWell I tried to make it Sunday\nBut I got so damn depressed\nThat I set my sights on Monday\nAnd I got myself undressed\nI ain't ready for the altar\nBut I do agree there's times\nWhen a woman sure can be a friend of mine\n\n[Chorus]\nWell, I keep on thinking about you\nSister Golden Hair surprise\nAnd I just can't live without you\nCan't you see it in my eyes?\nI been one poor correspondent\nAnd I've been too, too hard to find\nBut it doesn't mean\nYou ain't been on my mind\n\n[Bridge]\nWill you meet me in the middle\nWill you meet me in the air?\nWill you love me just a little\nJust enough to show you care?\nWell I tried to fake it\nI don't mind sayin'\nI just can't make it\n[Chorus]\nWell, I keep on thinking about you\nSister Golden Hair surprise\nAnd I just can't live without you\nCan't you see it in my eyes?\nI been one poor correspondent\nAnd I've been too, too hard to find\nBut it doesn't mean\nYou ain't been on my mind\n\n[Outro / Bridge]\nWill you meet me in the middle\nWill you meet me in the air?\nWill you love me just a little\nJust enough to show you care?\nWell I tried to fake it\nI don't mind sayin'\nI just can't make it", current_time=115, timed_lyrics=expected_timed_lyrics)

    assert result == expected