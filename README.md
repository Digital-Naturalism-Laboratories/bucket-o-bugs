# bucket-o-bugs
Sort through wild bugs (insects) localized from a specific location in the world to help humans id them hierarchically.

Done as part of the BeetlePalooza 2024 workshop.

## Development
The following has been tested on the Ohio Supercomputer Center (OSC) with the following.

```bash
module load miniconda3/24.1.2-py310
```

### Set up the virtual environment
```bash
conda env create -f environment_osc.yaml --solver=libmamba -y
```

If there is an issue with the default prefix, you can set the prefix to a custom location. For example, to set the prefix to `/fs/ess/PAS2136/<username>/.conda/envs/bob`, run the following commands:
```bash
mkdir -p /fs/ess/PAS2136/<username>/.conda/envs/bob
conda env create --prefix /fs/ess/PAS2136/<username>/.conda/envs/bob -f environment_osc.yaml --solver=libmamba -y
```
