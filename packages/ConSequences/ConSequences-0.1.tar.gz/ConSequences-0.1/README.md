# ConSequences

![](https://github.com/broadinstitute/ConSequences/blob/master/images/Logo.png)

Suite to delineate contiguous and conserved sequences from assemblies and search for their presence in raw sequencing data.

Developed by Rauf Salamzade in the Earl Bacterial Genomics Group at the Broad Institute.

### Documentation

For documentaion on how to use ConSequences and information on its underlying assumptions, please check out the wiki: https://github.com/broadinstitute/ConSequences/wiki

### Installation

To install ConSequences, please take the following steps:

1. Clone this git repository:

`git clone git@github.com:broadinstitute/ConSequences.git`

2. Setup the conda environment using the yml file. 

`conda env create -f ConSequences_Environment.yml -p /path/to/conda_environment/`

3. Activate the environment and perform setup and pip installation in the git repository:

```
source activate /path/to/conda_environment/
python setup.py install
pip install -e .
```

### Acknowledgments:

Development of the suite had valuable input from several folks including:

Abigail Manson, Terrance Shea, Colin Worby, Bruce Walker, Alejandro Pironti, and Ashlee Earl.

This project has been funded in whole or in part with Federal funds from the National Institute of Allergy and Infectious Diseases, National Institutes of Health, Department of Health and Human Services,under Grant Number U19AI110818 to the Broad Institute.
