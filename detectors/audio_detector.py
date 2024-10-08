import requests
from models.song_information import SongInformation, TimedLyrics
from shazamio import Shazam
from syrics.api import Spotify

audd_io_api_token = '49cc751b8e9de310756bbed451098b8f'
def detect_song_audd_io(file_path):
    url = 'https://api.audd.io/'
    data = {
        'api_token': audd_io_api_token,
        'return': 'lyrics',
    }
    
    files = {
        'file': open(file_path, 'rb')
    }
    
    response = requests.post(url, data=data, files=files)
    if response.status_code != 200:
        return None
    response = response.json().get('result')
    if response is None:
        return None
    current_time = response.get('timecode')
    minutes, seconds = map(int, current_time.split(":"))
    current_time = minutes * 60 + seconds
    return SongInformation.from_json({"title": response.get('title'), "lyrics": response.get("lyrics").get("lyrics"), "album": response.get("album"), "artist": response.get("artist"),"current_time": current_time})


shazam = Shazam()
async def detect_song_shazamio(file_path):
    shazam_result = await shazam.recognize(file_path)
    if shazam_result['matches'] == []:
        return None
    track = shazam_result['track']
    offset = shazam_result['matches'][0]['offset']
    artist_id = track['artists'][0]['adamid']
    album_id = track['albumadamid']

    artist_info = await shazam.artist_about(artist_id)
    artist_name = artist_info['data'][0]['attributes']['name']
    album_info = await shazam.search_album(album_id)
    album_name= album_info['data'][0]['attributes']['name']    
    song_info = SongInformation(title=track['title'], lyrics=None, album=album_name, artist=artist_name, current_time=offset)
    return song_info

LRCLIB_BASE_URL = 'https://lrclib.net'

def get_search_query(song_info : SongInformation):
    if song_info is None:
        return None
    return [f'{LRCLIB_BASE_URL}/api/search?q={song_info.title}+{song_info.artist}+{song_info.album}', f'{LRCLIB_BASE_URL}/api/search?q={song_info.title}']

def get_timed_lyrics_lrclib(song_info : SongInformation):
    search_query = get_search_query(song_info)
    if search_query is None:
        return None
    response = None
    for search_query in search_query:
        try:
            response = requests.get(search_query)
            response = response.json()[0]['syncedLyrics']
            timed_lyrics = TimedLyrics.from_raw_data(response)
            return timed_lyrics
        except Exception as e:
            print(e, response)
    return None


sp = Spotify("AQDLe2rrX0Q_vMiaUAjciWTTHHeZi46nlSswgdsPeGDJAOROrYsCiUleBKB3a9buSl9CrT8--4bEvR5Brup56rK8EWJp1d79oCQBLlDiGYJ3eGjiexT--n8Wu6ouoP9XbrBAvVDHvjl8x2jefAMxFlUhO9xpoEE")
def get_timed_lyrics_spotify(song_info : SongInformation):
    if song_info is None:
        return None
    
    # for somw reson the search query is no good when limit is 1
    spotify_track_id = sp.search(q=f'{song_info.title} {song_info.artist}', type='track', limit=10)['tracks']['items'][0]['id']
    response = sp.get_lyrics(spotify_track_id)
    if response is None:
        print('could not get lyrics for track {}'.format(spotify_track_id))
        return None
    lyrics = response['lyrics']
    timed_lyrics = TimedLyrics.from_spotify_lyrics(lyrics)
    return timed_lyrics

    
async def get_song_info(file_path):
    song_info = await detect_song_shazamio(file_path)
    if song_info is None:
        print('None')
        return None
    timed_lyrics = get_timed_lyrics_spotify(song_info)
    if timed_lyrics is None:
        timed_lyrics = get_timed_lyrics_lrclib(song_info)
    song_info.timed_lyrics = timed_lyrics
    return song_info
    