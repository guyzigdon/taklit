import cv2
import numpy as np
from PIL import Image
import argparse
import time
from skimage.metrics import structural_similarity as ssim
from detectors.gemini_detector import detect_vinyl

def image_has_changed(img1_array, img2_array, threshold=0.90):
    if img1_array is None:
        return True

    img1_gray = cv2.cvtColor(img1_array, cv2.COLOR_RGB2GRAY)
    img2_gray = cv2.cvtColor(img2_array, cv2.COLOR_RGB2GRAY)
    
    ssim_index, _ = ssim(img1_gray, img2_gray, full=True)
    
    return ssim_index < threshold

def main():
    parser = argparse.ArgumentParser(description='Detect vinyl records using a webcam.')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without querying gemini', default=True, required=False)
    args = parser.parse_args()

    # TODO: figure out why fps is so low
    capture_interval = 3  
    save_path = "captured_image.jpg"
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    time.sleep(4)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    last_image_array = None
    
    try:
        while True:
            # measure iteration time
            start = time.time()

            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if last_image_array is None or image_has_changed(last_image_array, frame_rgb) or True:
                pil_image = Image.fromarray(frame_rgb)
                pil_image.save(save_path)
                print(f"Image changed. Saving image to {save_path}")
                if not args.dry_run:
                    import pdb; pdb.set_trace()
                    result = detect_vinyl(save_path)
                    print(result)

            
            last_image_array = frame_rgb
            end = time.time()
            print(f"Time elapsed: {end - start}")
            time.sleep(capture_interval)
    
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    
    finally:
        # Release the webcam and close any windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
