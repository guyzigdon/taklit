import sounddevice as sd
from detectors.audio_detector import get_song_info
import wavio
import time

# Configuration
SAMPLE_RATE = 44100  # Sample rate in Hz
DURATION = 5  # Duration of each recording in seconds
INTERVAL = 15  # Interval between recordings in seconds
OUTPUT_FILE_PREFIX = "recording_"

def process_audio(data, filename):
    """
    A function to process the audio data.
    In this example, it just prints a message and saves the audio data.
    """
    print(f"Processing audio data. Saving to {filename}.")
    # Save the recorded data as a WAV file
    wavio.write(filename, data, SAMPLE_RATE, sampwidth=2)

def record_audio():
    """
    Record audio for a specified duration and save it to a file.
    """
    global SAMPLE_RATE, DURATION, OUTPUT_FILE_PREFIX

    # Record audio
    print("Recording...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished

    # Save to file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_FILE_PREFIX}.wav"
    process_audio(recording, filename)
    return filename

def main():
    """
    Main loop to record audio at specified intervals.
    """
    while True:
        filename = record_audio()
        print(f"Waiting {INTERVAL} seconds before next recording.")
        result = get_song_info(filename)
        print(result)
        print(result.get_current_and_next_lines())
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()