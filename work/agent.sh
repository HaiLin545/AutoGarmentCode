
img_name=$1
out_dir=$2

if [ -z "$img_name" ] || [ -z "$out_dir" ]; then
  echo "Usage: $0 <img_name> <output_dir>"
  exit 1
fi

garmentcode_python="/home/hailin/code/GarmentCode/.venv/bin/python"
garmentcode_script="/home/hailin/code/GarmentCode/work/main.py"

echo "Running agent to generate design parameters..."
$garmentcode_python $garmentcode_script \
    --img $out_dir/$img_name \
    --body $out_dir/smpl.yaml \
    --output $out_dir
    