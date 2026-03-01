import os
import sys
sys.path.append(os.getcwd()) 
# os.environ['EGL_DEVICE_ID'] = ''
import argparse
from pathlib import Path

import yaml

from assets.garment_programs.meta_garment import MetaGarment
from assets.bodies.body_params import BodyParameters
from pygarment.data_config import Properties


def get_args():
	parser = argparse.ArgumentParser(description='Generate garmentcode and run simulation in one step.')
	parser.add_argument('--design_path', type=str, required=True, help='Path to design YAML file.')
	parser.add_argument('--body_path', type=str, default="./assets/bodies/mean_all.yaml", help='Path to custom body YAML file.')
	parser.add_argument('--sim_config', '-s', type=str, default='./assets/Sim_props/default_sim_props.yaml', help='Simulation config YAML path.')
	parser.add_argument('--sim', type=str, default='false', help='Whether to run simulation after generating garment code.')
	return parser.parse_args()


if __name__ == '__main__':
	args = get_args()	
	body = BodyParameters(args.body_path)
	with open(args.design_path, 'r') as f:
		design = yaml.safe_load(f)['design']

	piece_name = Path(args.design_path).stem
	piece = MetaGarment(piece_name, body, design)
	pattern = piece.assembly()

	if piece.is_self_intersecting():
		print(f'{piece.name} is self-intersecting')

	sys_props = Properties('./system.json')
	sys_props['output'] = os.path.dirname(args.design_path)
	folder = Path(pattern.serialize(
        sys_props['output'],
        tag='',
        to_subfolder=False,
        with_3d=False,
        with_text=False,
        view_ids=False,
        with_printable=True,
	))
	body.save(folder)

	print(f'Successfully generated garment code for {piece.name} at {folder}')
	if not args.sim or args.sim.lower() == 'false':
		print('Simulation skipped.')
		exit(0)

	spec_path = folder / f'{piece.name}_specification.json'
	if not spec_path.exists():
		raise FileNotFoundError(f'Cannot find generated specification: {spec_path}')

	from pygarment.meshgen.boxmeshgen import BoxMesh
	from pygarment.meshgen.simulation import run_sim
	from pygarment.meshgen.sim_config import PathCofig

	props = Properties(args.sim_config)
	props.set_section_stats('sim', fails={}, sim_time={}, spf={}, fin_frame={}, body_collisions={}, self_collisions={})
	props.set_section_stats('render', render_time={})
	body_yaml = Path(args.body_path)
	body_path_for_sim = str(body_yaml.parent) if args.body_path is not None else None

	garment_name, _, _ = spec_path.stem.rpartition('_')
	paths = PathCofig(
		in_element_path=spec_path.parent,
		out_path=sys_props['output'],
		in_name=garment_name,
		body_name='smpl',
		body_path=body_path_for_sim,
		smpl_body=True,
		add_timestamp=False,
	)

	print(f'Generate box mesh of {garment_name} with resolution {props["sim"]["config"]["resolution_scale"]}...')
	print(f'Garment load: {paths.in_g_spec}')

	garment_box_mesh = BoxMesh(paths.in_g_spec, props['sim']['config']['resolution_scale'])
	garment_box_mesh.load()
	garment_box_mesh.serialize(paths, store_panels=False, uv_config=props['render']['config']['uv_texture'])

	props.serialize(paths.element_sim_props)
	run_sim(
		garment_box_mesh.name,
		props,
		paths,
		save_v_norms=False,
		store_usd=False,
		optimize_storage=False,
		verbose=False,
	)
	props.serialize(paths.element_sim_props)

	print(f'Success! Generated and simulated garment: {paths.out_el}')
