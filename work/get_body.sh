img_path=$1
output_dir=$2

if [ -z "$img_path" ] || [ -z "$output_dir" ]; then
  echo "Usage: $0 <img_path> <output_dir>"
  exit 1
fi

if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
fi

echo "Processing image: $img_path"
bash ../smpl_estimate/run_romp.sh $img_path $output_dir
bash ../smpl_estimate/run_hybrik.sh $img_path $output_dir
bash ../smpl_estimate/get_smpl.sh $output_dir/smpl.json $output_dir/smpl.obj

measurement="/home/hailin/code/GarmentMeasurements/build/measurements"
smpl_data_dir="/home/hailin/code/GarmentMeasurements/data_smpl"

mesh_path="$output_dir/smpl.obj"
body_param_path="$output_dir/smpl.yaml"

echo "Running measurement extraction..."
echo "Mesh path: $mesh_path"
echo "Body parameter path: $body_param_path"

$measurement $mesh_path $body_param_path --data_dir $smpl_data_dir
