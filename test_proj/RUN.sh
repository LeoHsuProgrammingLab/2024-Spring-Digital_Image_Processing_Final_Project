dataset_images_dir="data/holiday_images"
dataset_descriptors_dir="data/holiday_descriptors" 
dataset_pickle_path="data/holiday_df.pkl"

target_image_path="data/target_image/215100.jpg"
target_descriptor_save_dir="data/target_desc"
target_pickle_path="data/target_df.pkl"

rm -rf hesaff
rm -rf image_dummy
rm -rf descriptor_dummy
rm -rf "$dataset_descriptors_dir"
rm -rf "$dataset_pickle_path"
rm -rf "$target_pickle_path"

# compile for hesaff 
cd hesaff_c++
make clean
make
mv hesaff ..
make clean
cd ..

# =========
#  dataset
# =========

# generate descriptors for dataset
for file in "$dataset_images_dir"/*.jpg
do
    if [ -f "$file" ]
    then
        ./hesaff "$file" 20
    fi
done

# move .hesaff.sift to $dataset_descriptors_dir
mkdir "$dataset_descriptors_dir"
for file in "$dataset_images_dir"/*.hesaff.sift
do
    mv "$file" "$dataset_descriptors_dir"
done

# generate the pickle for dataset
python3 get_dataset.py \
    --descriptors_dir_path "$dataset_descriptors_dir" \
    --images_dir_path "$dataset_images_dir" \
    --save_df_path "$dataset_pickle_path"

# =========
#  target 
# =========

# generate descriptors for target
./hesaff "$target_image_path" 10

mkdir image_dummy
cp "$target_image_path" image_dummy

mkdir descriptor_dummy
cp "$target_image_path".hesaff.sift descriptor_dummy

# generate the pickle for target image
python3 get_dataset.py \
    --descriptors_dir_path descriptor_dummy \
    --images_dir_path image_dummy \
    --save_df_path "$target_pickle_path"


rm -rf image_dummy
rm -rf descriptor_dummy
rm -rf hesaff

echo "finished!"