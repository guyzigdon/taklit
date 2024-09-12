import requests
from models.song_information import SongInformation

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
    import pdb; pdb.set_trace()
    response = response.json().get('result')
    return SongInformation.from_json({"title": response.get('title'), "lyrics": response.get('lyrics').get('lyrics'), "current_time": response.get('timecode')})