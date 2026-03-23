# GarmentCode: Programming Parametric Sewing Patterns

![Examples of garments sampled from GarmentCode configurator](https://github.com/maria-korosteleva/GarmentCode/raw/main/assets/img/header.png)

Official Implementation of [GarmentCode: Programming Parametric Sewing Patterns](https://igl.ethz.ch/projects/garmentcode/) and [GarmentCodeData: A Dataset of 3D Made-to-Measure Garments With Sewing Patterns](https://igl.ethz.ch/projects/GarmentCodeData/).

> You can find the body measurements part of the project here: https://github.com/mbotsch/GarmentMeasurements 

## News

**[June 3, 2025]** GarmentCode online configurator demo is back online 🥳

**[April, 2025]** GarmentCode online configurator demo is temporarily unavailable. We are working on bringing it back online!

**[Nov 20, 2024]** GarmentCode configurator demo is now ONLINE 🥳 Check it out: https://garmentcode.ethz.ch/ (not for mobile) 

**[Sept 4, 2024]** We release a new version of the dataset with a few fixes and updates: [GarmentCodeData (v2)](https://doi.org/10.3929/ethz-b-000690432). See documentation for new data version for more details.

**[Aug 30, 2024]** Major release -- implementation of [GarmentCodeData](https://igl.ethz.ch/projects/GarmentCodeData/) in `pygarment v2.0.0`, new GUI, and other updates and improvements. Basic JSON representation classes are now part of PyGarment library! See CHANGELOG for more details

**[July 1, 2024]** [GarmentCodeData](https://igl.ethz.ch/projects/GarmentCodeData/) is accepted to ECCV!

**[May 29, 2024]** First release of [GarmentCodeData](https://doi.org/10.3929/ethz-b-000673889) dataset!

**[Oct 18, 2023]** First release of GarmentCode!

## Documents

1. [Installation](https://github.com/maria-korosteleva/GarmentCode/blob/main/docs/Installation.md)
2. [Running Configurator](https://github.com/maria-korosteleva/GarmentCode/blob/main/docs/Running_garmentcode.md) 
3. [Running Data Generation (warp)](https://github.com/maria-korosteleva/GarmentCode/blob/main/docs/Running_data_generation.md) 
3. [Body measurements](https://github.com/maria-korosteleva/GarmentCode/blob/main/docs/Body%20Measurements%20GarmentCode.pdf)
4. [Dataset documentation](https://www.research-collection.ethz.ch/handle/20.500.11850/673889)
3. [Running Old Maya+Qualoth tools](https://github.com/maria-korosteleva/GarmentCode/blob/main/docs/Running_Maya_Qualoth.md) 

## AutoGarmentCode Extension (`work/`)

This repository also contains an AI extension in [work/](https://github.com/maria-korosteleva/GarmentCode/tree/main/work), which performs:

`garment image -> body estimation -> LLM design params -> GarmentCode pattern generation (optional simulation)`

The key scripts are:

- `work/get_body.sh`: estimate SMPL + extract body measurements (`smpl.yaml`)
- `work/agent.sh`: run VLM/LLM pipeline and generate `design.yaml`
- `work/garmentcode.sh`: build garment patterns from `design.yaml` + `smpl.yaml`, and optionally run simulation
- `work/run.sh`: single-image end-to-end pipeline
- `work/run_batch.sh`: batch processing pipeline

### Environment Setup for `work/`

1. Install and verify the base GarmentCode environment first (see Installation docs above).
2. Install Python dependencies used by `work/`:

```bash
pip install openai pyyaml
```

3. Ensure body-estimation scripts are available in the sibling directory:

```text
../smpl_estimate/run_romp.sh
../smpl_estimate/run_hybrik.sh
../smpl_estimate/get_smpl.sh
```

4. Build and prepare [GarmentMeasurements](https://github.com/mbotsch/GarmentMeasurements), then make sure these paths are valid in `work/get_body.sh`:

```text
measurement=/home/hailin/code/GarmentMeasurements/build/measurements
smpl_data_dir=/home/hailin/code/GarmentMeasurements/data_smpl
```

5. Set your OpenAI-compatible API configuration in `work/agent.py` before running.

### Run Instructions (`work/`)

Run from repository root.

Single image:

```bash
bash ./work/run.sh
```

Batch images:

```bash
bash ./work/run_batch.sh
```

Or run step by step:

```bash
bash ./work/get_body.sh <img_path> <output_dir>
bash ./work/agent.sh <img_name> <output_dir>
bash ./work/garmentcode.sh <output_dir> [sim]
```

Default output files in `<output_dir>`:

- `smpl.json`, `smpl.obj`, `smpl.yaml`
- `design.yaml`
- generated garment pattern files (and simulation outputs if `sim` is enabled)

### Important Notes

- Update hard-coded local paths in `work/agent.sh`, `work/garmentcode.sh`, and `work/get_body.sh` to match your machine.
- Keep image path handling consistent across scripts. `get_body.sh` expects `<img_path>`; if you customize `run.sh`, pass a full image path.
- `work/garmentcode.sh` requires both `<output_dir>/design.yaml` and `<output_dir>/smpl.yaml`.
- The LLM output is expected to be fenced YAML and then converted into full GarmentCode design schema.

## Navigation

### Library

[PyGarment](https://github.com/maria-korosteleva/GarmentCode/tree/main/pygarment) is the core library described in the GarmentCode paper. It contains the base types (Edge, Panel, Component, Interface, etc.), as well as edge factory and various helpers and operators that help you design sewing patterns.  

See [Installation instructions](https://github.com/maria-korosteleva/GarmentCode/tree/main/docs/Installation.md) before use.

### Examples

* [assets/garment_programs/](https://github.com/maria-korosteleva/GarmentCode/tree/main/assets/garment_programs/) contains the code of garment components designed using PyGarment. 
* [assets/design_params/](https://github.com/maria-korosteleva/GarmentCode/tree/main/assets/design_params/), [assets/bodies/](https://github.com/maria-korosteleva/GarmentCode/tree/main/assets/bodies/) contain examples of design and body measurements presets. They can be used in both GarmentCode GUI and `test_garmentcode.py` script.

> NOTE: [assets/design_params/default.yaml](https://github.com/maria-korosteleva/GarmentCode/blob/main/assets/design_params/default.yaml) is the setup used by GUI on load. Changing this file results in changes in the GUI initial state =) 


## Citation

If you are using our system in your research, please cite our papers:

```bibtex
@inproceedings{GarmentCodeData:2024,
  author = {Korosteleva, Maria and Kesdogan, Timur Levent and Kemper, Fabian and Wenninger, Stephan and Koller, Jasmin and Zhang, Yuhan and Botsch, Mario and Sorkine-Hornung, Olga},
  title = {{GarmentCodeData}: A Dataset of 3{D} Made-to-Measure Garments With Sewing Patterns},
  booktitle={Computer Vision -- ECCV 2024},
  year = {2024},
  keywords = {sewing patterns, garment reconstruction, dataset},
}
```

```bibtex
@article{GarmentCode2023,
  author = {Korosteleva, Maria and Sorkine-Hornung, Olga},
  title = {{GarmentCode}: Programming Parametric Sewing Patterns},
  year = {2023},
  issue_date = {December 2023},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  volume = {42},
  number = {6},
  doi = {10.1145/3618351},
  journal = {ACM Transaction on Graphics},
  note = {SIGGRAPH ASIA 2023 issue},
  numpages = {16},
  keywords = {sewing patterns, garment modeling}
}
```

## Issues, questions, suggestions

Please post your issues and questions to [GitHub Issues](https://github.com/maria-korosteleva/GarmentCode/issues).

For other requests you can find my info on https://korosteleva.com/.  

## Contributors

This project is brought to life by these people:

* [Maria Korosteleva](https://github.com/maria-korosteleva)
* [Jasmin Koller](https://github.com/JasminKoller)
* [Yuhan Zhang](https://github.com/yuhan-zh)
* [Yuhan Liu](https://github.com/yuhanliu-tech)
* [Ami Beuret](https://github.com/amibeuret)
* [Olga Sorkine-Hornung](https://igl.ethz.ch/people/sorkine/index.php)

The body measurements team developed [GarmentMeasurements](https://github.com/mbotsch/GarmentMeasurements): 
* [Fabian Kemper](https://github.com/fabiankemper)
* [Stephan Wenninger](https://github.com/stephan-wenninger)
* [Mario Botsch](https://github.com/mbotsch)
