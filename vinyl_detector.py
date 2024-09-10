import cv2
import numpy as np
from PIL import Image
import time
import os

def image_has_changed(img1_path, img2):
    """Check if the new image is different from the saved image."""
    if not os.path.exists(img1_path):
        return True

    img1 = Image.open(img1_path)
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")
    
    img1_array = np.array(img1)
    img2_array = np.array(img2)
    
    return not np.array_equal(img1_array, img2_array)

def main():
    capture_interval = 10  # Time between captures in seconds
    save_path = "captured_image.jpg"  # Path where the image will be saved
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    last_image = None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            
            # Convert to PIL image
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if last_image is None or image_has_changed(save_path, pil_image):
                # Save the new image
                pil_image.save(save_path)
                print(f"Image saved to {save_path}")
            
            last_image = pil_image
            
            # Wait before capturing the next image
            time.sleep(capture_interval)
    
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    
    finally:
        # Release the webcam and close any windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()