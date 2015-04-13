#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage examples for the Temperature generator for REMD-simulations web client

Author: michele.silva@gmail.com
License: GPLv2
"""
import logging
from remd_temperature import get_temperatures
from remd_temperature import get_temperatures_energies


def _print_temperatures_table(temperatures_table):
    print 'Temperatures and energies'
    print 'Temperature(K)\tμ(kJ/mol)\tσ(kJ/mol)\tμ12(kJ/mol)\t' + \
        'σ12(kJ/mol)\tP12'
    for line in temperatures_table:
        print '%f\t%f\t%f\t%f\t%f\t%f' % tuple(line)


def example_human_readable_params():
    """
    The human readable parameters are the labels of the inputs
    in the original web page

    See example_original_parameters (below)

    - It doesn't differentiate upper and lowercase
    - Any extraneous space is ignored
    """
    params = {
        'number of protein atoms': 50,
        # Example of case insensitivity and removal of spare spaces
        'constraints in the  PROTEIN  ': 'bonds to hydrogens only',
    }
    print '-' * 20
    print 'Example with 50 protein atoms, bonds to hydrogen only\n'
    print 'Temperatures only\n', get_temperatures(params), '\n'
    _print_temperatures_table(get_temperatures_energies(params))


def example_original_params():
    """
    The original web form parameters are the following

    Exchange probability: Pdes,
    Lower temperature limit: Tlow,
    Number of water molecules: Nw,
    Number of protein atoms: Np,
    Hydrogens in protein: Hff, Values: 0 (All H), 1 (Polar H),
    Simulation type: Alg,  Values: 0 (NPT), 1 (NVT),
    Tolerance: Tol,
    Upper temperature limit: Thigh,
    Constraints in water: WC, Values: 0 (Fully flexible), 2 (Flexible Angle),
        3 (Rigid)
    Constraints in the protein: PC, Values: 0 (Fully flexible),
        1 (Bonds to hydrogens only), 2 (All bonds)
    Virtual sites in protein: Vs, Values: 0 (None), 1( Virtual hydrogen)
    """
    # Use original variables interface
    params = {'Np': 20}  # Set number of protein atoms
    print '-' * 20
    print 'Example with  Np=20 (number of protein atoms)\n'
    print 'Temperatures only\n', get_temperatures(params), '\n'
    _print_temperatures_table(get_temperatures_energies(params))


if __name__ == '__main__':
    logging.basicConfig()
    # Write variable names in natural language
    example_human_readable_params()
    # Wtie variable names in the original variables used in the page
    example_original_params()
