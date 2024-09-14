import argparse

from vinyl_detector import DEFAULT_QUERY_VINYL as DEFAULT_QUERY_VINYL
from vinyl_detector import DEFAULT_INTERVAL as DEFAULT_VINYL_INTERVAL
from song_detector import DEFAULT_INTERVAL as DEFAULT_SONG_INTERVAL

from vinyl_detector import run_main_loop as run_vinyl_detector
from song_detector import run_main_loop as run_song_detector
from colorama import Fore, init
import asyncio
import concurrent.futures


init(autoreset=True)

def run_async_in_thread(loop, coro):
    """
    Runs an async function (coro) in a separate thread.
    """
    asyncio.set_event_loop(loop)  # Set the event loop for this thread
    loop.run_until_complete(coro)

def main(vinyl_dry_run, vinyl_interval, song_interval):
    song_loop = asyncio.new_event_loop()
    vinyl_loop = asyncio.new_event_loop()    

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Schedule both async tasks to run in separate threads
        song_future = executor.submit(run_async_in_thread, song_loop, run_song_detector(song_interval, Fore.BLUE))
        vinyl_future = executor.submit(run_async_in_thread, vinyl_loop, run_vinyl_detector(vinyl_dry_run, vinyl_interval, Fore.CYAN))

        # Wait for both async functions to complete
        song_future.result()
        vinyl_future.result()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect vinyl records using a webcam.')
    parser.add_argument('--query-vinyl', action='store_true', help='Perform a dry run without querying gemini', default=DEFAULT_QUERY_VINYL, required=False)
    parser.add_argument('--vinyl-interval', type=int, help='Interval between image captures in seconds', default=DEFAULT_VINYL_INTERVAL, required=False)
    parser.add_argument('--song-interval', type=int, help='Interval between audio recordings in seconds', default=DEFAULT_SONG_INTERVAL, required=False)
    args = parser.parse_args()

    main(args.query_vinyl, args.vinyl_interval, args.song_interval)
