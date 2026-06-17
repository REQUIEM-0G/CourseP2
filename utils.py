import cv2
import numpy as np
from PIL import Image

def center_digit(img):
    M = cv2.moments(img)
    if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        rows, cols = img.shape
        shift_x = np.round(cols / 2.0 - cx).astype(int)
        shift_y = np.round(rows / 2.0 - cy).astype(int)
        M_shift = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        return cv2.warpAffine(img, M_shift, (cols, rows))
    return img

def preprocess_image(img_input):
    if isinstance(img_input, Image.Image):
        img = np.array(img_input.convert('L'))
    else:
        img = img_input

    if np.mean(img) > 127:
        img = 255 - img
        
    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        cnt = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        digit = img[y:y+h, x:x+w]
        size = max(w, h) + 40
        pad_img = np.zeros((size, size), dtype="uint8")
        dx, dy = (size - w) // 2, (size - h) // 2
        pad_img[dy:dy+h, dx:dx+w] = digit
        img = pad_img

    img_28 = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
    img_28 = center_digit(img_28)
    img_28 = cv2.GaussianBlur(img_28, (3, 3), 0)
    _, img_28 = cv2.threshold(img_28, 50, 255, cv2.THRESH_BINARY)
    
    # повертаємо нормалізований тензор (1, 28, 28, 1)
    img_array = img_28.astype('float32') / 255.0
    return np.expand_dims(img_array, axis=(0, -1))