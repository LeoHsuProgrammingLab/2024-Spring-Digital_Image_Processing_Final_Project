dataset_descriptors_dir="data/holiday_descriptors"
dataset_images_dir="data/holiday_images"
dataset_pickle_path="data/holiday_df.pkl"

python3 get_dataset_all_image.py \
    --descriptors_dir_path "$dataset_descriptors_dir" \
    --images_dir_path "$dataset_images_dir" \
    --save_df_path "$dataset_pickle_path"

target_image_path="data/target_image/"
target_descriptor_save_dir="data/target_desc"
target_pickle_path="data/target_df.pkl"

python3 get_dataset_all_image.py \
    --images_dir_path "$target_image_path" \
    --descriptors_dir_path "$target_descriptor_save_dir" \
    --save_df_path "$target_pickle_path"