from matplotlib import pyplot as plt
import cv2

def show_img(img):
    print(img.shape)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()