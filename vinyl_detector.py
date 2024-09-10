from time import sleep
from gemini_detector.gemini_detector import detect_vinyl

def main() -> None:
    #setup streaming
    while True:
        # save image from stream in a file called "image.jpg"
        # result = detect_vinyl("image.jpg")
        # send result to frontend
        sleep(10)
        pass


if __name__ == '__main__':
    main()
