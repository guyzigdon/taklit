
import google.generativeai as genai
from typing import Optional
import json
from models.vinyl_information import VinylInformation


api_key = "AIzaSyDRoHdj88R67pXpPWfP-Ij4EXR52pFellw"

# possible prompts
# consider fetching only name first and then fetching the rest of the information (can be good for hebrew)

album_and_artist_prompt = "Can you tell me the artist and album_name of the vinyl in the photo? if it's hebrew please answer in hebrew. {\"artist\": \"artist name\", \"album\": \"album name\"}"
prompt = "Can you tell me info about the vinyl in the photo? format answer in JSON with the following structure: {\"artist\": \"artist name\", \"album\": \"album name\", \"year\": \"year\", \"genre\": \"genre\", \"tracklist\": [\"track1\", \"track2\", \"track3\"...]}"
hebrew_prompt = "מה האלבום והאומן בתמונה? פורמט:{\"artist\": \"artist name\", \"album\": \"album name\"}"
heb = "אפשר מידע על האלבום בתמונה? תשובה בפורמט JSON \n{\"artist\": \"artist name\", \"album\": \"album name\", \"year\": \"year\", \"genre\": \"genre\", \"tracklist\": [\"track1\", \"track2\", \"track3\"...]}"


genai.configure(api_key=api_key)

def detect_vinyl(image_path: str) -> Optional[VinylInformation]:
    print("querying gemini for vinyl information")
    myfile = genai.upload_file("main.jpg")
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content([myfile, "\n\n", heb])
    try:
        return VinylInformation.from_raw_information(json.loads(result.text))
    except Exception as e:
        print(f"Failed to parse response from gemini: {e}")
        return None