import cv2
import numpy as np
import sys
import argparse
np.set_printoptions(threshold=sys.maxsize)

parser = argparse.ArgumentParser(description="Process some input and output paths with a threshold value.")
parser.add_argument('input_path', type=str, help='The path to the input file.')
parser.add_argument('output_path', type=str, help='The path to the output file.')
parser.add_argument('threshold', type=int, choices=range(0, 256), help='An integer threshold value between 0 and 255.')

args = parser.parse_args()

input_path = args.input_path
output_path = args.output_path
threshold = args.threshold

image_with_alpha = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

if image_with_alpha.ndim == 2:
    image_with_alpha = cv2.cvtColor(image_with_alpha, cv2.COLOR_GRAY2RGBA)
elif image_with_alpha.shape[2] == 3:
    alpha_channel = np.ones((image_with_alpha.shape[0], image_with_alpha.shape[1]), dtype=image_with_alpha.dtype) * 255
    image_with_alpha = np.dstack((image_with_alpha, alpha_channel))
elif image_with_alpha.shape[2] == 4:
    image_with_alpha = cv2.cvtColor(image_with_alpha, cv2.COLOR_BGRA2RGBA)

# Create a mask where all RGB values are zero (black pixels)
black_mask = (image_with_alpha[:, :, 0] == 0) & (image_with_alpha[:, :, 1] == 0) & (image_with_alpha[:, :, 2] == 0)

# Set alpha values to 0 where the mask is True (where pixels are black)
image_with_alpha[black_mask, 3] = 0

gray_image = cv2.cvtColor(image_with_alpha[:, :, :3], cv2.COLOR_BGR2GRAY)

image_with_alpha[:, :, 3] = np.where(gray_image <= threshold, 0, 255)

cv2.imwrite(output_path, image_with_alpha)