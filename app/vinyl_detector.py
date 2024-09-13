import cv2
from PIL import Image
import argparse
import time
from skimage.metrics import structural_similarity as ssim
from detectors.gemini_detector import detect_vinyl
from thread_utils import print_in_color
from colorama import Fore

DEFAULT_INTERVAL = 7
DEFAULT_QUERY_VINYL = False


def image_has_changed(img1_array, img2_array, threshold=0.70):
    if img1_array is None:
        return True, -1

    img1_gray = cv2.cvtColor(img1_array, cv2.COLOR_RGB2GRAY)
    img2_gray = cv2.cvtColor(img2_array, cv2.COLOR_RGB2GRAY)
    
    ssim_index, _ = ssim(img1_gray, img2_gray, full=True)
    return (ssim_index < threshold, ssim_index)


def run_main_loop(query_vinyl : bool = DEFAULT_QUERY_VINYL, interval : int = DEFAULT_INTERVAL, color = None):
    if color is not None:
        globals()['print'] = print_in_color(color)
    save_path = "captured_image.jpg"
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    last_image_array = None

    starting_message = "Starting vinyl main loop."
    print(starting_message)

    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            has_changed, ssim_index = image_has_changed(last_image_array, frame_rgb)

            if last_image_array is None or has_changed:
                pil_image = Image.fromarray(frame_rgb)
                pil_image.save(save_path)
                print(f"Image changed. Saving image to {save_path}. {ssim_index=}")
                if query_vinyl:
                    result = detect_vinyl(save_path)
                    if result is not None:
                        print(Fore.GREEN + result.album_name + " " + result.artist)

            
            last_image_array = frame_rgb
            
            print(f"Waiting {interval} seconds before next capture.")
            time.sleep(interval)
            
            # TODO: without this, the webcam saves old frames
            # figure out how to make it work properly without releasing every iteration
            cap.release()
            cap = cv2.VideoCapture(0)

    
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    
    finally:
        # Release the webcam and close any windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect vinyl records using a webcam.')
    parser.add_argument('--query_vinyl', action='store_true', help='Perform a dry run without querying gemini', default=DEFAULT_QUERY_VINYL, required=False)
    parser.add_argument('--interval', type=int, help='Interval between image captures in seconds', default=DEFAULT_INTERVAL, required=False)
    args = parser.parse_args()
    run_main_loop(args.query_vinyl, args.interval)
