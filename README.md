# bucket-o-bugs
Sort through wild bugs (insects) localized from a specific location in the world to help humans id them hierarchically.

Done as part of the BeetlePalooza 2024 workshop.

Images of bugs were collected in Panama by Andrew Quitmeyer using [Mothbox](https://digital-naturalism-laboratories.github.io/Mothbox/) to take images of the bugs and classify as `creature` or `non-creature`. The taxonomic keys for bugs native to Panama were retrieved from [GBIF](https://www.gbif.org/) search (DOI: [10.15468/dl.xkdm66](https://doi.org/10.15468/dl.xkdm66)). A common error Mothbox makes is to classify holes in the felt target or smudges as creatures, prompting the addition of `hole` and `circle` to the taxonomic key list to help quickly remove these from collected images.

## Development
The project has been tested on the Ohio Supercomputer Center (OSC) HPC with the following.

```bash
module load miniconda3/24.1.2-py310
```

### Set up the virtual environment
```bash
conda env create -f environment.yaml --solver=libmamba -y
```

If there is an issue with the default prefix, you can set the prefix to a custom location. For example, to set the prefix to `/fs/ess/PAS2136/<username>/.conda/envs/bob`, run the following commands:
```bash
mkdir -p /fs/ess/PAS2136/<username>/.conda/envs/bob
conda env create --prefix /fs/ess/PAS2136/<username>/.conda/envs/bob -f environment.yaml --solver=libmamba -y
```

## Acknowledgement

This work was done during [BeetlePalooza 2024](https://github.com/Imageomics/BeetlePalooza-2024/wiki), which was sponsored by the [Imageomics Institute](https://imageomics.org/) and supported by the National Science Foundation under Awards No. [OAC-2118240](https://nsf.gov/awardsearch/showAward?AWD_ID=2118240) and [AWD-111317](https://nsf.gov/awardsearch/showAward?AWD_ID=111317). Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
