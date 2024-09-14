import requests
from typing import Union
from models.vinyl_information import VinylInformation
from models.song_information import SongInformation


class DisplayClient():
    @classmethod
    def set_data(cls, data_model: Union[VinylInformation, SongInformation]):
        try:
            response = requests.post(
                "http://localhost:5000/data",
                json=data_model.model_dump()
            )
            
            # Check if the response status code indicates success (200-299)
            return response.ok
        except requests.RequestException as e:
            # Handle any exceptions that occur during the request
            print(f"An error occurred: {e}")
            return False
