
import google.generativeai as genai
import os
import json
from vinyl_information import VinylInformation


api_key = "AIzaSyDRoHdj88R67pXpPWfP-Ij4EXR52pFellw"
propmt = "Can you tell me info about the vinyl in the photo? format answer in JSON with the following structure: {\"artist\": \"artist name\", \"album\": \"album name\", \"year\": \"year\", \"genre\": \"genre\", \"tracklist\": [\"track1\", \"track2\", \"track3\"...]}"

genai.configure(api_key=api_key)

def detect_vinyl(image_path: str) -> str:
    print("querying gemini for vinyl information")
    myfile = genai.upload_file(image_path)
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content([myfile, "\n\n", propmt])
    try:
        return VinylInformation.from_raw_information(json.loads(result.text))
    except Exception as e:
        print(f"Failed to parse response from gemini: {e}")
        return None