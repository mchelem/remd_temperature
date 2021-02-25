# -*- coding: utf-8 -*-
"""
Client for the Temperature generator for REMD-simulations web server

You submit the number of protein atoms and water molecules in your system,
and an upper and lower limit for the temperature range, information about
constraints and/or virtual sites and a desired exchange probability Pdes,
and the webserver will predict a temperature series with correspondig energy
differences and standard deviations which matches the desired probability Pdes.

See: http://folding.bmc.uu.se/remd/


Author: michele.silva@gmail.com
License: GPLv2
"""

import logging
import requests
import BeautifulSoup


logger = logging.getLogger(__name__)

TGENERATOR_URL = 'http://folding.bmc.uu.se/remd/tgenerator.php'

default_params = dict(
    Pdes=0.25,
    Tol=1e-4,
    Tlow=300,
    Thigh=500,
    Nw=0,
    WC=3,
    Np=200,
    PC=1,
    Hff=0,
    Vs=0,
    Alg=0,
)

# --- Mappings for human readable variables and values to server format ---

constraints_water = {
    'fully flexible': 0,
    'flexible angle': 2,
    'rigid': 3,
}

constraints_protein = {
    'fully flexible': 0,
    'bonds to hydrogens only': 1,
    'all bonds': 2,
}

params_mapping = {
    'exchange probability': 'Pdes',
    'lower temperature limit': 'Tlow',
    'number of water molecules': 'Nw',
    'number of protein atoms': 'Np',
    'hydrogens in protein': ('Hff', {'all h': 0, 'polar h': 1}),
    'simulation type': ('Alg',  {'npt': 0, 'nvt': 1}),
    'tolerance': 'Tol',
    'upper temperature limit': 'Thigh',
    'constraints in water': ('WC', constraints_water),
    'constraints in the protein': ('PC', constraints_protein),
    'virtual sites in protein': ('Vs', {'none': 0, 'virtual hydrogen': 1}),
}


def load_parameters(input_params):
    """
    Load parameters from a dictionary

    The parameters can be specified both as the original form parameters
    on the server or as the labels for these parameters

    Original form parameters:
        param['PC'] = 2  # Constraints in the protein: All bonds
    Human readable parameters:
        param['constraints in the protein'] = 'all bonds'

    :params params: Input parameters to the remd temperature server
        as dictionary of variable, value

    :return: Parameters in the original form parameter format, filled with
        default values when the variable was in the input.
    """
    keys = [key.lower() for key in input_params.keys()]
    if not ('np' in keys or 'number of protein atoms' in keys):
        raise AttributeError('You must specify the number of protein atoms')

    params = default_params.copy()
    if 'Np' in input_params:
        params.update(input_params)
    else:
        for key, value in input_params.items():
            try:
                # Remove spaces and make everything lower case
                key = ' '.join(key.lower().split())
                mapping = params_mapping[key]
                if isinstance(value, str):
                    value = ' '.join(value.lower().split())
                if isinstance(mapping, tuple):
                    params[mapping[0]] = mapping[1][value]
                else:
                    params[mapping] = value
            except KeyError as e:
                logger.warn('Invalid variable: ' + str(e))
    return params


def _read_table(table):
    """
    Read an HTML table filled with numbers to a list

    :param table: HTML table found by BeautifulSoup

    :return: The values in the table: list(list(float)
    """
    result = []
    for row in table.findAll('tr'):
        cols = row.findAll('td')
        if cols and len(cols) > 1:
            result.append([])
            for col in cols[1:]:
                text = ''.join(col.findAll(text=True))
                text = 'nan' if not text else text
                result[-1].append(float(text))
    return result


# --- Public methods ---

def get_temperatures(params):
    """
    Retrieve the temperatures (K) as a list

    Sample Output: [300.0, 332.18, 366.98, 404.54, 445.26, 489.27, 536.92]

    :params params: Dictionary of parameters using the server form
        variables or the human readable format. See: load_parameters

    :return: List of temperatures in K - list(float)
    """
    params = load_parameters(params)
    temperatures = []
    res = requests.post(TGENERATOR_URL, data=params)
    soup = BeautifulSoup.BeautifulSoup(res.text)
    heading = soup.findAll(
        lambda x: 'we also give the temperatures below' in x.text)
    # First sibling is a <br>
    temperatures = heading[0].nextSibling.nextSibling.text
    return [float(x) for x in temperatures.split(',')]


def get_temperatures_energies(params):
    """
    Get a table contaning the following parameters

    The parameters, from left to right are the following:
        Temperature (K)
        μ (kJ/mol)
        σ (kJ/mol)
        μ12 (kJ/mol)
        σ12 (kJ/mol)
        P12

    :params params: Dictionary of parameters using the server form
        variables or the human readable format. See: load_parameters

    :return list with temperatures and energies - list(list(float))
    """
    params = load_parameters(params)
    res = requests.post(TGENERATOR_URL, data=params)
    soup = BeautifulSoup.BeautifulSoup(res.text)
    table = soup.findAll('table')[1]
    return _read_table(table)
