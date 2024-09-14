import threading
import argparse

from vinyl_detector import DEFAULT_QUERY_VINYL as DEFAULT_QUERY_VINYL
from vinyl_detector import DEFAULT_INTERVAL as DEFAULT_VINYL_INTERVAL
from song_detector import DEFAULT_INTERVAL as DEFAULT_SONG_INTERVAL

from vinyl_detector import run_main_loop as run_vinyl_detector
from song_detector import run_main_loop as run_song_detector
from colorama import Fore, init

init(autoreset=True)

def main(vinyl_dry_run, vinyl_interval, song_interval):
    vinyl_thread = threading.Thread(target=run_vinyl_detector, args=(vinyl_dry_run, vinyl_interval, Fore.CYAN))
    song_thread = threading.Thread(target=run_song_detector, args=(song_interval, Fore.BLUE))
    
    vinyl_thread.start()
    song_thread.start()

    vinyl_thread.join()
    song_thread.join()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect vinyl records using a webcam.')
    parser.add_argument('--query-vinyl', action='store_true', help='Perform a dry run without querying gemini', default=DEFAULT_QUERY_VINYL, required=False)
    parser.add_argument('--vinyl-interval', type=int, help='Interval between image captures in seconds', default=DEFAULT_VINYL_INTERVAL, required=False)
    parser.add_argument('--song-interval', type=int, help='Interval between audio recordings in seconds', default=DEFAULT_SONG_INTERVAL, required=False)
    args = parser.parse_args()

    main(args.query_vinyl, args.vinyl_interval, args.song_interval)
