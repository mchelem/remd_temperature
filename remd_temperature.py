#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Client for the Temperature generator for REMD-simulations web server

You submit the number of protein atoms and water molecules in your system,
and an upper and lower limit for the temperature range, information about
constraints and/or virtual sites and a desired exchange probability Pdes,
and the webserver will predict a temperature series with correspondig energy
differences and standard deviations which matches the desired probability Pdes.

See http://folding.bmc.uu.se/remd/
"""
import requests
import BeautifulSoup

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


def _read_table(table):
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


def get_temperature_list(params=default_params):
    """
    Retrieve the temperatures (K) as a list
    Example: [300.0, 332.18, 366.98, 404.54, 445.26, 489.27, 536.92]
    """
    temperatures = []
    res = requests.post(TGENERATOR_URL, data=params)
    soup = BeautifulSoup.BeautifulSoup(res.text)
    heading = soup.findAll(
        lambda x: 'we also give the temperatures below' in x.text)
    # First sibling is a <br>
    temperatures = heading[0].nextSibling.nextSibling.text
    return [float(x) for x in temperatures.split(',')]


def get_temperature_table(params=default_params):
    """
    Get a table contaning the following parameters
        Temperature (K)
        μ (kJ/mol)
        σ (kJ/mol)
        μ12 (kJ/mol)
        σ12 (kJ/mol)
        P12
    """
    res = requests.post(TGENERATOR_URL, data=params)
    soup = BeautifulSoup.BeautifulSoup(res.text)
    table = soup.findAll('table')[1]
    return _read_table(table)
