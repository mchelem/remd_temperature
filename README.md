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

```
pip install git+https://github.com/mchelem/remd_temperature
```

