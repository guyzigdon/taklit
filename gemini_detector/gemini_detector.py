
import google.generativeai as genai
import os
from vinyl_information import VinylInformation


api_key = "AIzaSyDRoHdj88R67pXpPWfP-Ij4EXR52pFellw"
propmt = "Can you tell me the names of the album and the artist of the vinyl in the photo? format answer in the following way: \n\nArtist: artist\nAlbum Name: name\nGenre: genre\nYear: year\n\n"#Tracklist: \nSide A\n<tracks>\nSide B\n<tracks>"

genai.configure(api_key=api_key)

def detect_vinyl(image_path: str) -> str:
    print("querying gemini for vinyl information")
    myfile = genai.upload_file(image_path)
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content([myfile, "\n\n", propmt])
    return VinylInformation.from_raw_information(result.text)