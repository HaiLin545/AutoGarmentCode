# img_paths=(
#     "./assets/test_img/ubc_1.png"
#     "./assets/test_img/ubc_2.png"
#     "./assets/test_img/ubc_3.png"
#     "./assets/test_img/ubc_4.png"
# )

img_folder="./assets/test_img/ubc_2"

# all images in the folder(png, jpg ,jpeg)
img_paths=($(find "$img_folder" -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \)))
out_folder="./output_3"

for img_path in "${img_paths[@]}"; do

    echo "-------------------------------"
    echo "Processing image: $img_path"

    img_basename=$(basename "$img_path" | cut -f 1 -d '.')
    img_name=$(basename "$img_path")
    output_dir="$out_folder/$img_basename"
    mkdir -p "$output_dir"
    echo "Created output directory: $output_dir"

    new_img_path="$output_dir/$img_name"
    cp "$img_path" "$new_img_path"

    bash ./work/get_body.sh $img_path $output_dir
    bash ./work/agent.sh $img_name $output_dir
    bash ./work/garmentcode.sh $output_dir sim

    echo "Finished processing image: $img_path"
    echo "-------------------------------"
done
