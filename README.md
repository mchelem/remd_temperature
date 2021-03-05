# Temperature generator for REMD-simulations

Python library to obtain temperatures for replica exchange molecular dynamics simulations. This library queries the Temperature generator for [REMD-simulations web server](http://folding.bmc.uu.se/remd/).

Temperature generator for REMD-simulations is a web server for generating temperatures for REMD-calculations. 
You submit the number of protein atoms and water molecules in your system, and an upper and lower limit 
for the temperature range, information about constraints and/or virtual sites and a desired exchange 
probability Pdes, and the webserver will predict a temperature series with correspondig energy differences 
and standard deviations which matches the desired probability Pdes. 

Reference: Alexandra Patriksson and David van der Spoel, A temperature predictor for parallel tempering 
simulations Phys. Chem. Chem. Phys., 10 pp. 2073-2077 (2008) http://dx.doi.org/10.1039/b716554d.

As of 2021, the remd server is no longer online, but its source code is available at https://github.com/dspoel/remd-temperature-generator
In order to run it, you may install php-cli (`apt install php7.4-cli`), go to its directory, and run `php -S localhost:8000`. You can then access the server on your browser going to http://localhost:8000, fill in the parameters and click submit to get the temperatures.

If you prefer using the python code instead, update the TGENERATOR constant at https://github.com/mchelem/remd_temperature/blob/master/remd_temperature.py#L25 to `TGENERATOR_URL = 'http://localhost:8000/tgenerator.php'` and then run the examples below.

## Installation

Run the following command:
```
pip install git+https://github.com/mchelem/remd_temperature
```

## Usage

Get temperatures and energies (table on the image below):

```python
from remd_temperature import get_temperatures_energies
params = {'number of protein atoms': 200}
print(get_temperatures_energies(params))
```

Get temperatures only (last line on the image below):

```python
from remd_temperature import get_temperatures
params = {'number of protein atoms': 200}
print(get_temperatures(params))
```

![remd temperature results](http://pix.toile-libre.org/upload/original/1428960434.png)

See also the [examples](https://github.com/mchelem/remd_temperature/blob/master/example.py), for details on how to handle the output. The parameters are the ones available at http://folding.bmc.uu.se/remd/

You can use either human readable names (label) or shorter and less explanatory form input names. You **cannot mix both formats** in the same input.

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
 
