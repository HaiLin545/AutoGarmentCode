
img_path="./assets/test_img/ubc_1.png"
out_folder="./output"

img_basename=$(basename "$img_path" | cut -f 1 -d '.')
img_name=$(basename "$img_path")
output_dir="$out_folder/$img_basename"
mkdir -p "$output_dir"
echo "Created output directory: $output_dir"

new_img_path="$output_dir/$img_name"
cp "$img_path" "$new_img_path"

bash ./work/get_body.sh $img_name $output_dir
bash ./work/agent.sh $img_name $output_dir 
bash ./work/garmentcode.sh $output_dir sim