import requests

from .models import GlobalData

class DisplayClient():
    @classmethod
    def set_data(cls, data: GlobalData):
        try:
            response = requests.post("http://localhost:5000/data", json=data.model_dump())
            
            # Check if the response status code indicates success (200-299)
            return response.ok
        except requests.RequestException as e:
            # Handle any exceptions that occur during the request
            print(f"An error occurred: {e}")
            return False
