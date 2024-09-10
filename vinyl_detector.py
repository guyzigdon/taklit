import cv2
import numpy as np
from PIL import Image
import time
from skimage.metrics import structural_similarity as ssim
from gemini_detector.gemini_detector import detect_vinyl

def image_has_changed(img1_array, img2_array, threshold=0.90):
    """Check if the new image is different from the saved image with a tolerance threshold."""
    if img1_array is None:
        return True

    # Convert images to grayscale for SSIM comparison
    img1_gray = cv2.cvtColor(img1_array, cv2.COLOR_RGB2GRAY)
    img2_gray = cv2.cvtColor(img2_array, cv2.COLOR_RGB2GRAY)
    
    # Compute SSIM between two images
    ssim_index, _ = ssim(img1_gray, img2_gray, full=True)
    
    return ssim_index < threshold

def main():
    # TODO: figure out why fps is so slow
    capture_interval = 0.5  # Time between captures in seconds
    save_path = "captured_image.jpg"  # Path where the image will be saved
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    last_image_array = None
    
    try:
        while True:
            # messure iteration time
            start = time.time()

            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            
            # Convert frame to RGB and store as numpy array
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if last_image_array is None or image_has_changed(last_image_array, frame_rgb):
                # Save the new image
                pil_image = Image.fromarray(frame_rgb)
                pil_image.save(save_path)
                print(f"Image changed. Saving image to {save_path}")
                result = detect_vinyl(save_path)
                print(result)

            
            last_image_array = frame_rgb
            end = time.time()
            # print(f"Time elapsed: {end - start}")
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
