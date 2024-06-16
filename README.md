# Top FCNC analysis

## How to run

First run
```
. setup.sh 
```

It will load the key4hep software stack.

The lhe files generated with Madgraph have to be in the `MG5_aMCatNLO` folder. Run

```
python run_edm4hep.py
``` 

It will run the `DelphesPythia8_EDM4HEP` for the IDEA detector and separate by name the processes. The output will be stored in the `gen` folder.

The fccanalyses code for flattening the edm4hep file is in `analysis/analysis_stage1`. The proccessList variable needs to be updated with the processes to run.
```
processList = {
    'ee2tt_bWbW': { # key is the name of the process in the gen folder
        "fraction": 1, # fraction of files to run
    },
    'ee2tt_cHbW_h2bb': {
        "fraction": 1,
    },
    ...
}
```

Run the analysis with

```
fccanalysis run analysis/analysis_stage1.py
```

The output will be in the `outputs/stage1` folder