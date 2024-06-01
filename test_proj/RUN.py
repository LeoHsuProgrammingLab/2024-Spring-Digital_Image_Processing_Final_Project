import os
import subprocess
import shutil

def process_dataset(dataset_images_dir, dataset_descriptors_dir, dataset_pickle_path):
    # Remove existing directories and files
    if os.path.exists(dataset_descriptors_dir):
        shutil.rmtree(dataset_descriptors_dir)
    if os.path.exists(dataset_pickle_path):
        os.remove(dataset_pickle_path)

    # Generate descriptors for the dataset
    for file in os.listdir(dataset_images_dir):
        if file.endswith(".jpg"):
            file_path = os.path.join(dataset_images_dir, file)
            subprocess.run(["./hesaff", file_path, "20"])

    # Move .hesaff.sift files to the descriptors directory
    os.makedirs(dataset_descriptors_dir, exist_ok=True)
    for file in os.listdir(dataset_images_dir):
        if file.endswith(".hesaff.sift"):
            src_path = os.path.join(dataset_images_dir, file)
            dst_path = os.path.join(dataset_descriptors_dir, file)
            shutil.move(src_path, dst_path)

    # Generate the pickle for the dataset
    subprocess.run(["python3", "get_dataset.py",
                    "--descriptors_dir_path", dataset_descriptors_dir,
                    "--images_dir_path", dataset_images_dir,
                    "--save_df_path", dataset_pickle_path])

def rename_dir(dataset_images_dir):
    for dir in os.listdir(dataset_images_dir):
        if os.path.isdir(os.path.join(dataset_images_dir, dir)):
            new_dirname = dir.replace(" ", "_")
            os.rename(os.path.join(dataset_images_dir, dir), os.path.join(dataset_images_dir, new_dirname))

def rename_files(dataset_images_dir):
    for dir in os.listdir(dataset_images_dir):
        if os.path.isdir(os.path.join(dataset_images_dir, dir)):
            for file in os.listdir(os.path.join(dataset_images_dir, dir)):
                new_filename = file.replace(" ", "_")
                os.rename(os.path.join(dataset_images_dir, dir, file), os.path.join(dataset_images_dir, dir, new_filename))
        else:
            new_filename = dir.replace(" ", "_")
            os.rename(os.path.join(dataset_images_dir, dir), os.path.join(dataset_images_dir, new_filename))

def process_dataset_with_dir(dataset_images_dir, dataset_descriptors_dir, dataset_pickle_path, max_num_each_dir=7):
    # Remove existing directories and files
    if os.path.exists(dataset_descriptors_dir):
        shutil.rmtree(dataset_descriptors_dir)
    if os.path.exists(dataset_pickle_path):
        os.remove(dataset_pickle_path)

    # Generate descriptors for the dataset
    for dir in os.listdir(dataset_images_dir):
        if os.path.isdir(os.path.join(dataset_images_dir, dir)):
            count = 0
            for file in os.listdir(os.path.join(dataset_images_dir, dir)):
                if file.endswith(".jpg"):
                    file_path = os.path.join(dataset_images_dir, dir, file)
                    subprocess.run(["./hesaff", file_path, "20"])
                    count += 1
                    if count == max_num_each_dir:
                        break

    # Move .hesaff.sift files to the descriptors directory
    os.makedirs(dataset_descriptors_dir, exist_ok=True)
    for dir in os.listdir(dataset_images_dir):
        if os.path.isdir(os.path.join(dataset_images_dir, dir)):
            for file in os.listdir(os.path.join(dataset_images_dir, dir)):
                if file.endswith(".hesaff.sift"):
                    src_path = os.path.join(dataset_images_dir, dir, file)
                    dst_path = os.path.join(dataset_descriptors_dir, file)
                    shutil.move(src_path, dst_path)

    # Generate the pickle for the dataset
    subprocess.run(["python3", "get_dataset.py",
                    "--descriptors_dir_path", dataset_descriptors_dir,
                    "--images_dir_path", dataset_images_dir,
                    "--save_df_path", dataset_pickle_path])


### Function to Process the Target Image
def process_target(target_image_dir, target_descriptor_save_dir, target_pickle_path):
    # Remove existing directories and files
    if os.path.exists(target_pickle_path):
        os.remove(target_pickle_path)

    # Generate descriptors for the target image
    for file in os.listdir(target_image_dir):
        if file.endswith(".jpg"):
            target_image_path = os.path.join(target_image_dir, file)
            subprocess.run(["./hesaff", target_image_path, "10"])

    os.makedirs(target_descriptor_save_dir, exist_ok=True)
    for file in os.listdir("."):
        if file.endswith(".hesaff.sift"):
            descriptor_file = f"{target_image_path}.hesaff.sift"
            shutil.move(descriptor_file, target_descriptor_save_dir)

    # Generate the pickle for the target image
    subprocess.run(["python3", "get_dataset.py",
                    "--descriptors_dir_path", target_descriptor_save_dir,
                    "--images_dir_path", target_image_dir,
                    "--save_df_path", target_pickle_path])

# Example usage
if __name__ == "__main__":
    # Set variables
    dataset = "anime"
    dataset_images_dir = f"data/{dataset}_images"
    dataset_descriptors_dir = f"data/{dataset}_desc"
    dataset_pickle_path = f"data/{dataset}_df.pkl"

    target_image_path = "data/target_image"
    target_descriptor_save_dir = "data/target_desc"
    target_pickle_path = "data/target_df.pkl"

    # Remove old hesaff executable if it exists
    if os.path.exists("hesaff"):
        os.remove("hesaff")

    # Compile hesaff feature extractor
    os.chdir("hesaff_c++")
    subprocess.run(["make", "clean"])
    subprocess.run(["make"])
    shutil.move("hesaff", "..")
    subprocess.run(["make", "clean"])
    os.chdir("..")
    
    # Rename directories and files
    rename_files(dataset_images_dir)
    rename_files(dataset_descriptors_dir)

    # Process dataset and target
    # process_dataset(dataset_images_dir, dataset_descriptors_dir, dataset_pickle_path)
    # process_target(target_image_path, target_descriptor_save_dir, target_pickle_path)
    # process_dataset_with_dir(dataset_images_dir, dataset_descriptors_dir, dataset_pickle_path, max_num_each_dir=10)

    print("Finished!")
