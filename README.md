# sakura

This small package `sakura` is just a tiny helper for plotting CMS DQM files. The additional package `simplotter` is for helping plotting distributions for SimDoublets in a much nicer way than the standard DQM plotters.

**Table of content:**

- [Installation](#installation)
- [Usage of `simplotter`](#usage-of--simplotter)
    - [`makeCutPlots`](#makecutplots)

## Installation
To install the package, first down load this repository, and pip install by performing the following commands:
```bash
git clone https://github.com/JanGerritSchulz/sakura.git
cd sakura
pip3 install .
```

*Note: for installing in developer mode do `python3 -m pip install -e .` instead. When installed as editable, a project can be edited in-place without reinstallation:

## Usage of  `simplotter`
At the moment, the package supports plotting the distributions of the cut variables on doublets of the true SimDoublets and some general plots for the SimDoublets. Thi can be done with the command line functions `makeCutPlots` and `makeGeneralPlots`. More on their usage below. There is also the function `makeAllPlots` which essentially runs both.

### `makeCutPlots`
This command line function plots the distributions of doublet cut parameters for the true SimDoublets of TrackingParticles which were produced by the `SimDoubletsAnalyzer` module in CMSSW. You can get a summary of the command options with 
```bash
makeCutPlots --help
```

You have to provide two **required arguments**: 
- first positional argument: **DQM file**. It expects the path to the DQM ROOT file which was produced in the harvesting step and contains all the histograms.
- second positional argument: **config file**. This file contains the information about which were the configured cut values for the doublet cuts. This can either be:
    - a yaml file (`.yml`) with all parameters inside. An example is given in [`currentCuts.yml`](./simplotter/dataconfig/currentCuts.yml).
    - the CMSSW config file you used for the validation step directly (`.py`). The function will read the config, extract the parameters and creates a corresponding yaml file on its own (in the given `--DIR` directory). *Note that if you pass the CMSSW config, you need to be in a `cmsenv` otherwise python cannot interpret the file. Also, if the SimDoubletsAnalyzer in that config is named differently from `simDoubletsAnalyzerPhase2`, you will have to provide the correct name in the argument `--analyzer`.*

Then, you have a couple of optional arguments summarized in the following table.

| Option              | Meaning                                                                                                                                                                                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-d` / `--directory`      | Directory to save the plots in.                                                                                                                                                                                                                                                                   |
| `-c` / `--cut`             | Cut parameter to be plotted (by default, all cut parameters are plotted).                                                                                                                                                                                                                         |
| `-a` / `--analyzer` | If the provided config is a CMSSW config, the function needs to know the name of the SimDoubletsAnalyzer module to read the cut values correctly. You therefore should pass the name here. Default is `SimDoubletsAnalyzerPhase2`.                                                                |
| `-n` / `--nevents`  | Number of events (used for scaling to numbers per event if provided). The function will try to determine the number of events on its own first by looking at the DQM file and then the config file. If nothing is found there, take the given value. Defaults to `-1` meaning no scaling applied. |

#### Example use case
An example application could look like this:
```bash
makeCutPlots DQM_SimDoublets_currentCuts.root simDoublets_currentCuts_TEST.py -d /eos/user/j/jaschulz/www/Plots/NGT/test/sakura_makeCutPlots -n 5000 -a simDoubletsAnalyzerCurrentCuts
```

The result of this call can be found [here](https://jaschulz.web.cern.ch/Plots/NGT/test/sakura_makeCutPlots/cutParameters).


### `makeGeneralPlots`
This command line function plots some general distributions for the true SimDoublets of TrackingParticles which were produced by the `SimDoubletsAnalyzer` module in CMSSW. You can get a summary of the command options with 
```bash
makeGeneralPlots --help
```

You have to provide one **required argument**: 
- positional argument: **DQM file**. It expects the path to the DQM ROOT file which was produced in the harvesting step and contains all the histograms.

Then, you have a couple of optional arguments summarized in the following table.

| Option              | Meaning                                                                                                                                                                                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-d` / `--directory`      | Directory to save the plots in.                                                                                                                                                                                                                                                                   |
| `-n` / `--nevents`  | Number of events (used for scaling to numbers per event if provided). The function will try to determine the number of events on its own first by looking at the DQM file. If nothing is found there, take the given value. Defaults to `-1` meaning no scaling applied. |

#### Example use case
An example application could look like this:
```bash
makeGeneralPlots DQM_SimDoublets_currentCuts.root -d /eos/user/j/jaschulz/www/Plots/NGT/test/sakura_makeCutPlots -n 5000
```

The result of this call can be found [here](https://jaschulz.web.cern.ch/Plots/NGT/test/sakura_makeCutPlots/general).