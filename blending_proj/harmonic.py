import cv2
import numpy as np
from scipy.interpolate import griddata
import sys

def harmonic_interpolation(image):
    # Split the image into color channels and the alpha channel
    b, g, r, a = cv2.split(image)

    # Create a mask where alpha is 255 (1 for interpolation, 0 otherwise)
    mask = a == 255

    # Get the coordinates of pixels to interpolate (alpha == 0)
    points_to_interpolate = np.column_stack(np.where(a == 0))

    # Get the coordinates of known points (alpha == 255)
    known_points = np.column_stack(np.where(a == 255))

    # Interpolating each color channel separately
    for channel in [b, g, r]:
        known_values = channel[mask]
        interpolated_values = griddata(known_points, known_values, points_to_interpolate, method='linear')
        channel[a == 0] = interpolated_values

    # Set all alpha values to 255
    a[:] = 255

    # Merge the channels back
    interpolated_image = cv2.merge([b, g, r, a])

    return interpolated_image

if __name__ == "__main__":
    # Check for the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python3 harmonic.py <input_image> <output_image>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]

    # Load the input image
    image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Error: Unable to load image '{input_image_path}'")
        sys.exit(1)

    # Perform harmonic interpolation
    result_image = harmonic_interpolation(image)

    # Save the result
    cv2.imwrite(output_image_path, result_image)
    print(f"Interpolated image saved as '{output_image_path}'")
