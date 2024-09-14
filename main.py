import time

from display.client import DisplayClient, GlobalData
from display import start_server

def main():
    while True:
        DisplayClient.set_data(GlobalData(album=f"{time.time()}", artist="a"))
        time.sleep(5)


if __name__ == "__main__":
    start_server()
    main()
