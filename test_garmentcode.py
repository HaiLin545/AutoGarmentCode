from datetime import datetime
import shutil
from pathlib import Path
import yaml

from assets.garment_programs.meta_garment import MetaGarment
from assets.bodies.body_params import BodyParameters
from pygarment.data_config import Properties
import argparse
import os


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run garment code test.")
    parser.add_argument("--body_path", type=str, help="Body measurements to use for the test garment.")
    parser.add_argument("--body_name", type=str, default="neutral")
    parser.add_argument("--design_path", type=str, help="Design YAML to use for the test garment.")
    args = parser.parse_args()

    # body_to_use = "smpl"  # CHANGE HERE to use different set of body measurements
    body_to_use = args.body_name
    body_path = args.body_path
    bodies_measurements = {
        # Our model
        "neutral": "./assets/bodies/mean_all.yaml",
        "mean_female": "./assets/bodies/mean_female.yaml",
        "mean_male": "./assets/bodies/mean_male.yaml",
        # SMPL
        "f_smpl": "./assets/bodies/f_smpl_average_A40.yaml",
        "m_smpl": "./assets/bodies/m_smpl_average_A40.yaml",
        # "smpl": "./assets/bodies/smpl_mesh.yaml",
    }
    
    if body_path is not None:
        bodies_measurements[body_to_use] =  body_path
    
    assert body_to_use in bodies_measurements, f"body_to_use should be one of {list(bodies_measurements.keys())}"
    
    body = BodyParameters(bodies_measurements[body_to_use])

    design_files = {
        "t-shirt": "./assets/design_params/t-shirt.yaml",
    }
    designs = {}
    
    if args.design_path is not None:
        with open(args.design_path, "r") as f:
            designs['custom'] = yaml.safe_load(f)["design"]
    else:
        for df in design_files:
            with open(design_files[df], "r") as f:
                designs[df] = yaml.safe_load(f)["design"]

    test_garments = [MetaGarment(df, body, designs[df]) for df in designs]

    for piece in test_garments:
        pattern = piece.assembly()

        if piece.is_self_intersecting():
            print(f"{piece.name} is Self-intersecting")

        # Save as json file
        sys_props = Properties("./system.json")
        folder = pattern.serialize(
            Path(sys_props["output"]),
            tag="_" + datetime.now().strftime("%y%m%d-%H-%M-%S"),
            to_subfolder=True,
            with_3d=False,
            with_text=False,
            view_ids=False,
            with_printable=True,
        )

        body.save(folder)
        if piece.name in design_files:
            shutil.copy(design_files[piece.name], folder)
        
        if args.design_path is not None:
            shutil.copy(args.design_path, folder)

        print(f"Success! {piece.name} saved to {folder}")
