import sounddevice as sd
from detectors.audio_detector import get_song_info
from thread_utils import print_in_color
import wavio
import soundfile as sf
import asyncio
import argparse
import time
from colorama import Fore
from display.client import DisplayClient

# Configuration
SAMPLE_RATE = 44100  # Sample rate in Hz
DURATION = 5  # Duration of each recording in seconds
DEFAULT_INTERVAL = 10  # Interval between recordings in seconds
OUTPUT_FILE_PREFIX = "recording_"


def process_audio(data, filename):
    print(f"Processing audio data. Saving to {filename}.wav and {filename}.ogg.")

    # Save as WAV using wavio
    wavio.write(f"{filename}.wav", data, SAMPLE_RATE, sampwidth=2)

    # Save as OGG using soundfile
    sf.write(f"{filename}.ogg", data, SAMPLE_RATE, format='OGG')


def record_audio():
    """
    Record audio for a specified duration and save it to a file.
    """
    global SAMPLE_RATE, DURATION, OUTPUT_FILE_PREFIX

    print("Recording...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished

    # timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_FILE_PREFIX}"
    process_audio(recording, filename)
    return filename


async def run_main_loop(interval: int = DEFAULT_INTERVAL, color=None):
    """
    Main loop to record audio at specified intervals.
    """
    if color is not None:
        globals()['print'] = print_in_color(color)

    print("Starting main loop.")

    while True:
        filename = record_audio()
        result = await get_song_info(f"{filename}.ogg")
        if result is not None:
            print(Fore.GREEN + result.title + ", lyrics:")
            result.set_current_and_next_lines()
            live_lyrics = result.live_lyrics
            if live_lyrics is not None:
                lyrics = "\n".join([row for row in result.live_lyrics])
            else:
                lyrics = "\u266C"
            print(Fore.GREEN + lyrics)
            DisplayClient.set_data(result)
        print(f"Waiting {interval} seconds before next recording.")
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect vinyl records using a webcam.')
    parser.add_argument('--interval', type=int, help='Interval between image captures in seconds', default=DEFAULT_INTERVAL, required=False)
    args = parser.parse_args()
    asyncio.run(run_main_loop(args.interval))