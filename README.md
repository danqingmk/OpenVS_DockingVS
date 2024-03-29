# How to use DockingVS ?

###  Requirements

This software has been tested on Linux. We think it should work with other linux-based setups quite easily.
 
Prerequisites include:
* OpenBabel (https://open-babel.readthedocs.io/en/latest/index.html)
* UCSF Chimera (https://www.cgl.ucsf.edu/chimera/)
* Mgltools (https://ccsb.scripps.edu/mgltools/)
* AutoDock Vina (https://vina.scripps.edu/)

## General Usage

Step 1: Prepare input files, including parameter configuration file（config.conf）, ligand file (ligand.mol2), and protein file (protein.pdbqt).<br>
Step 2: Run the code to perform docking operations.<br>
```
python autodock.py
```
