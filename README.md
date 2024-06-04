# Digital Image Processing Project

{Place the intro of the project here}

## Prerequisites

Before running the project, ensure you have the following installed:

1. **OpenCV for C++** and its dependencies, including FFmpeg.
2. **Conda** package manager.

### Setting up the Environment

1. Install the required packages using the provided environment configuration:

    ```bash
    conda env create -f environment.yml
    ```

2. Activate the environment:

    ```bash
    conda activate dip_proj
    ```

### Preparing the Dataset

- **Database of Descriptors**: Prepare a dataset of images to be used as the database of descriptors. The path to this directory should be denoted by `{path_to_directory_of_images}`.
- **Single Target Image**: Prepare a single image that you intend to construct. This image should be denoted by `{path_to_a_single_target_image}`.

## Executing the Code

### Step 1: Generating the Pickle Files

Use `generate_pickle.py` to generate the database of descriptors and the descriptors of the target image.

1. **Generating the Database of Descriptors**:

    ```bash
    python3 generate_pickle.py --use_directory {path_to_directory_of_images} --output {path_to_database_pickle_file}
    ```

2. **Generating the Pickle File of the Target Image**:

    ```bash
    python3 generate_pickle.py --use_image {path_to_a_single_target_image} --output {path_to_target_image_pickle_file}
    ```

### Step 2: Image Reconstruction

Open `reconstruct.ipynb` in Jupyter Notebook and modify the following lines under "Selecting the Datasets and the Target Image" section to match your data:

```python
target_path = {path_to_a_single_target_image}
target_pickle = {path_to_target_image_pickle_file}
image = cv2.imread(target_path).astype(np.uint8)
target_df = pd.read_pickle(target_pickle)
dataset_images_dir = {path_to_directory_of_images}
dataset_images_pickle = {path_to_database_pickle_file}
dataset_df = pd.read_pickle(dataset_images_pickle)
```

Execute the code blocks one by one in `reconstruct.ipynb`.

### Step 3: Image Inpainting

Open `inpainting.ipynb` in Jupyter Notebook. Prepare the files you wish to interpolate and put them in a directory denoted by `{input_img_dir}`. The output directory for the interpolated images should be `{output_img_dir}`.

Modify the following lines in the "Selecting the Directory of Images You Wish to Inpaint" section:

```python
input_folder = {input_img_dir}
output_folder = {output_img_dir}
```

Execute the code blocks one by one in `inpainting.ipynb`.

## Additional Resources

For more detailed documentation, code, and the progress we made during the project, visit our [GitHub repository](https://github.com/LeoHsuProgrammingLab/2024-Spring-Digital_Image_Processing_Final_Project). Kindly check out the `dev` branch to view all the updates and trial-and-error we have made:

```bash
git clone https://github.com/LeoHsuProgrammingLab/2024-Spring-Digital_Image_Processing_Final_Project.git
git checkout dev
```

## References

{insert some references}