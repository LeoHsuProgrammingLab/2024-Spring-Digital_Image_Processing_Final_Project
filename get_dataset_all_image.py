import argparse
import numpy as np
import pandas as pd
import os
from tqdm.auto import tqdm

def load_data_from_file(filename):
    keypoints = []
    descriptors = []

    with open(filename, 'r') as file:
        lines = file.readlines()[2:]

    for line in lines:
        numbers = list(map(float, line.split()))
        keypoints.append(numbers[0:5])
        descriptors.append(numbers[5:])

    keypoints = np.array(keypoints)
    descriptors = np.array(descriptors)

    return keypoints, descriptors

def get_ellipse_properties(keypoints):
    coord = []
    s = []
    o = []
    As = []
    eigenvalues_lst = []
    eigenvectors_lst = []
    semi_major_lst = []
    semi_minor_lst = []
    size_lst = []
    angle_lst = []

    for keypoint in keypoints:
        u, v, a, b, c = keypoint[:5]

        A = np.array([[a, b], [b, c]])

        eigenvalues, eigenvectors = np.linalg.eig(A)

        sorted_indices = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]

        scale_si = np.sqrt(1/eigenvalues[0])
        orientation_oi = np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]) * (180 / np.pi)

        semi_major_axis = 1 / np.sqrt(eigenvalues[0])
        semi_minor_axis = 1 / np.sqrt(eigenvalues[1])

        coord.append((u, v))
        s.append(scale_si)
        o.append(orientation_oi)
        As.append(A)
        eigenvalues_lst.append(eigenvalues)
        eigenvectors_lst.append(eigenvectors)
        semi_major_lst.append(semi_major_axis)
        semi_minor_lst.append(semi_minor_axis)
        size_lst.append(np.pi * semi_major_axis * semi_minor_axis)
        angle_lst.append(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))

    return coord, s, o, As, eigenvalues_lst, eigenvectors_lst, semi_major_lst, semi_minor_lst, size_lst, angle_lst

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--descriptors_dir_path", type=str)
    parser.add_argument("--images_dir_path", type=str)
    parser.add_argument("--save_df_path", type=str)
    args = parser.parse_args()

    # Get the paths from the arguments
    descriptors_dir = args.descriptors_dir_path
    images_dir = args.images_dir_path
    save_dir = args.save_df_path

    # List and sort files in the directories
    descriptors_path_lst = []
    images_path_lst = []

    for file in os.listdir(descriptors_dir):
        if os.path.isdir(os.path.join(descriptors_dir, file)):
            for f in os.listdir(os.path.join(descriptors_dir, file)):
                if f.endswith(".hesaff.sift"):
                    desc_path = os.path.join(file, f)
                    descriptors_path_lst.append(desc_path)
                    images_path_lst.append(desc_path[:-12])
        elif file.endswith(".hesaff.sift"):
            descriptors_path_lst.append(file)
            images_path_lst.append(file[:-12])

        print(descriptors_path_lst[-1])
        print(images_path_lst[-1])

    # Initialize lists to store data for all images
    image_names = []
    coordinates = []
    scales = []
    orientations = []
    matrices = []
    eigenvalues = []
    eigenvectors = []
    semi_major_axes = []
    semi_minor_axes = []
    sizes = []
    angles = []
    descriptors_list = []

    # Process all descriptor files
    for i in tqdm(range(len(descriptors_path_lst))):
        path = os.path.join(descriptors_dir, descriptors_path_lst[i])
        keypoints, descriptors = load_data_from_file(path)
        
        coord, s, o, A, eigenvalues_lst, eigenvectors_lst, semi_major_lst, semi_minor_lst, size_lst, angle_lst = get_ellipse_properties(keypoints)
        
        img_id = images_path_lst[i]
        
        A = [array.tolist() for array in A]
        eigenvalues_lst = [array.tolist() for array in eigenvalues_lst]
        eigenvectors_lst = [array.tolist() for array in eigenvectors_lst]
        
        # Append data to the lists
        image_names += [img_id] * len(keypoints)
        coordinates += coord
        scales += s
        orientations += o
        matrices += A
        eigenvalues += eigenvalues_lst
        eigenvectors += eigenvectors_lst
        semi_major_axes += semi_major_lst
        semi_minor_axes += semi_minor_lst
        sizes += size_lst
        angles += angle_lst
        descriptors_list += descriptors.tolist()
        
    # Create the DataFrame
    df = pd.DataFrame({
        'image_name': image_names,
        'coordinate': coordinates,
        'scale': scales,
        'orientation': orientations,
        'matrix': matrices,
        'eigenvalues': eigenvalues,
        'eigenvectors': eigenvectors,
        'semi_major_axis': semi_major_axes,
        'semi_minor_axis': semi_minor_axes,
        'size': sizes,
        'angle': angles,
        'descriptor': descriptors_list
    })
    print(df.shape)

    # Save the DataFrame to a pickle file
    df.to_pickle(save_dir)

if __name__ == "__main__":
    main()