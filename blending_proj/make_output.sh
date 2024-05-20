original_image="data/house.png"
remove_background_image="data/image_with_alpha.png"
interpolated_image="data/result.png"
threshold=64

rm -rf "$remove_background_image"
rm -rf "$interpolated_image"

python3 remove_background.py "$original_image" "$remove_background_image" "$threshold"
python3 harmonic.py "$remove_background_image" "$interpolated_image"