from matplotlib import pyplot as plt
import cv2
import numpy as np

def show_img(img):
    print(img.shape)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

def histogram_equalization(image):
    # Convert the image to YCrCb color space
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    
    # Split the channels
    y, cr, cb = cv2.split(ycrcb)
    
    # Equalize the histogram of the Y channel
    y_eq = cv2.equalizeHist(y)
    
    # Merge the channels back
    ycrcb_eq = cv2.merge((y_eq, cr, cb))
    
    # Convert back to BGR color space
    image_eq = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)
    
    return image_eq

# Method 2: CLAHE (Contrast Limited Adaptive Histogram Equalization)
def apply_clahe(image):
    # Convert the image to YCrCb color space
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    
    # Split the channels
    y, cr, cb = cv2.split(ycrcb)
    
    # Apply CLAHE to the Y channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    y_clahe = clahe.apply(y)
    
    # Merge the channels back
    ycrcb_clahe = cv2.merge((y_clahe, cr, cb))
    
    # Convert back to BGR color space
    image_clahe = cv2.cvtColor(ycrcb_clahe, cv2.COLOR_YCrCb2BGR)
    
    return image_clahe

# Method 3: Manual Brightness and Contrast Adjustment
def adjust_brightness_contrast(image, brightness=0, contrast=0):
    # The image should be in BGR format
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)

    return image

# level like photoshop
def adjust_levels(image, in_levels=(0, 255), gamma=1.0, out_levels=(0, 255)):

    if image.dtype != np.float32:
        image = image.astype(np.float32)
    
    image = (image - in_levels[0]) / (in_levels[1] - in_levels[0])
    image = np.clip(image, 0, 1)  
    
    image = np.power(image, gamma)
    
    image = image * (out_levels[1] - out_levels[0]) + out_levels[0]
    image = np.clip(image, out_levels[0], out_levels[1])  
    
    if image.dtype == np.float32:
        image = np.clip(image, 0, 255).astype(np.uint8)
    
    return image

if __name__ == "__main__":
    path = 'output_final/output_7659_anime_1617_img.png'
    img = cv2.imread(path).astype(np.uint8)
    # img = histogram_equalization(img)
    img_clahe = apply_clahe(img)
    img_bc = adjust_brightness_contrast(img, brightness=0, contrast=0)
    img_l = adjust_levels(img, in_levels=(10, 255), gamma=2, out_levels=(0, 200))
    result = cv2.cvtColor(img_clahe, cv2.COLOR_BGR2RGB)
    plt.imshow(result)
    plt.show()