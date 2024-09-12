import requests
from models.song_information import SongInformation, TimedLyrics

api_token = '49cc751b8e9de310756bbed451098b8f'
def detect_song(file_path):
    url = 'https://api.audd.io/'
    data = {
        'api_token': api_token,
        'return': 'lyrics',
    }
    
    files = {
        'file': open(file_path, 'rb')
    }
    
    response = requests.post(url, data=data, files=files)
    try:
        response = response.json().get('result')
        current_time = response.get('timecode')
        minutes, seconds = map(int, current_time.split(":"))
        current_time = minutes * 60 + seconds
        return SongInformation.from_json({"title": response.get('title'), "lyrics": response.get("lyrics").get("lyrics"), "album": response.get("album"), "artist": response.get("artist"),"current_time": current_time})
    except Exception as e:
        print(e, response)
        return None


LRCLIB_BASE_URL = 'https://lrclib.net'

def get_search_query(song_info : SongInformation):
    try:
        return f'{LRCLIB_BASE_URL}/api/search?q={song_info.title}+{song_info.artist}+{song_info.album}'
    except Exception as e:
        print(e)
        return None

def get_timed_lyrics(song_info : SongInformation):
    search_query = get_search_query(song_info)
    if search_query is None:
        return None
    response = requests.get(search_query)
    try:
        response = response.json()[0]['syncedLyrics']
        timed_lyrics = TimedLyrics.from_raw_data(response)
        return timed_lyrics
    except Exception as e:
        print(e, response)
        return None
    
def get_song_info(file_path):
    song_info = detect_song(file_path)
    timed_lyrics = get_timed_lyrics(song_info)
    song_info.timed_lyrics = timed_lyrics
    return song_info
    