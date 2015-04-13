# Temperature generator for REMD-simulations

Python library to query the Temperature generator for REMD-simulations web server.

Temperature generator for REMD-simulations is a webserver for generating temperatures for REMD-calculations. 
You submit the number of protein atoms and water molecules in your system, and an upper and lower limit 
for the temperature range, information about constraints and/or virtual sites and a desired exchange 
probability Pdes, and the webserver will predict a temperature series with correspondig energy differences 
and standard deviations which matches the desired probability Pdes. 
You can then use these temperatures in REMD simulations.

See: http://folding.bmc.uu.se/remd/

Reference: Alexandra Patriksson and David van der Spoel, A temperature predictor for parallel tempering 
simulations Phys. Chem. Chem. Phys., 10 pp. 2073-2077 (2008) http://dx.doi.org/10.1039/b716554d.

## Installation

Run the following command:
```
pip install git+https://github.com/mchelem/remd_temperature
```

## Usage

You can retrieve a list containing the temperatures or a table with temperatures or energies.
[remd temperature results](!http://pix.toile-libre.org/?img=1428960434.png)

The variable names are the ones available at http://folding.bmc.uu.se/remd/
You can both use the human readable name (label) or the shorter and less explanatory form input names.
You **cannot mix both formats** in the same input.

For example, here are two valid and equivalent ways to set contraints in water :
```python
# Uses human readable format
params = {'constraints in water': 'bonds to hydrogens only'}  
```
OR
```python
# Uses original web form parameters
params = {'WC': 1} #
```

Here are the mappings between human readable and form variables (the latter in bold):
  * Exchange probability: **Pdes**,
  * Lower temperature limit: **Tlow**,
  * Number of water molecules: **Nw**,
  * Number of protein atoms: **Np**,
  * Hydrogens in protein: **Hff**, Values: **0** (All H), **1** (Polar H),
  * Simulation type: **Alg**,  Values: **0** (NPT), **1** (NVT),
  * Tolerance: **Tol**,
  * Upper temperature limit: **Thigh**,
  * Constraints in water: **WC**, Values: **0** (Fully flexible), **2** (Flexible Angle), **3** (Rigid)
  * Constraints in the protein: **PC**, Values: **0** (Fully flexible), **1** (Bonds to hydrogens only), **2** (All bonds)
  * Virtual sites in protein: **Vs**, Values: **0** (None), **1**(Virtual hydrogen)
 
