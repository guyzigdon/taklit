from openai import OpenAI
from base64 import b64encode

from vinyl_information import VinylInformation

class ImageDetector:
    GPT_TEXT_PROMPT = (
        "What vinyl record is in this image? Return in format:\n\n"
        "Artist: artist\n"
        "Album Name: name"
    )
    GPT_IMAGE_URL_PREAMBLE = "data:image/jpeg;base64,"

    def __init__(self) -> None:
        self.client = OpenAI()
    
    def detect_image(self, image_data: bytes) -> VinylInformation:
        raw_information = ImageDetector._get_raw_vinyl_information(image_data)
        return VinylInformation.from_raw_information(raw_information)


    def _get_raw_vinyl_information(self, image_data: bytes) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": ImageDetector.GPT_TEXT_PROMPT,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"{ImageDetector.GPT_IMAGE_URL_PREAMBLE}{b64encode(image_data).decode('utf-8')}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content
