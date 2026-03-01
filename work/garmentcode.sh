
out_dir=$1
sim=$2

if [ -z "$out_dir" ]; then
  echo "Usage: $0 <output_dir>"
  exit 1
fi

if [ -z "$sim" ]; then
  sim="false"
fi

garmentcode_python="/home/hailin/code/GarmentCode/.venv/bin/python"
garmentcode_script="/home/hailin/code/GarmentCode/work/garmentcode.py"

design_path="$out_dir/design.yaml"
body_path="$out_dir/smpl.yaml"
if [ ! -f "$design_path" ]; then
  echo "Design file not found: $design_path"
  exit 1
fi

if [ ! -f "$body_path" ]; then
  echo "Body file not found: $body_path"
  exit 1
fi

$garmentcode_python $garmentcode_script \
    --design_path $design_path \
    --body_path $body_path \
    --sim $sim
