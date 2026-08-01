import cv2
import numpy as np
from PIL import Image
from rembg import remove
import sys

def process_photo(input_path, output_path="source-prepped.png"):
    with open(input_path, 'rb') as i:
        input_data = i.read()
        subject_rgba = remove(input_data)
    
    nparr = np.frombuffer(subject_rgba, np.uint8)
    img_rgba = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    
    b, g, r, a = cv2.split(img_rgba)
    gray = cv2.cvtColor(cv2.merge([b, g, r]), cv2.COLOR_BGR2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced_gray = clahe.apply(gray)
    
    white_bg = np.ones_like(enhanced_gray) * 255
    alpha = a.astype(float) / 255.0
    final_img = (enhanced_gray * alpha + white_bg * (1 - alpha)).astype(np.uint8)
    
    cv2.imwrite(output_path, final_img)
    print(f"Prepped image saved to {output_path}")

if __name__ == "__main__":
    photo_file = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    process_photo(photo_file)