#!/usr/bin/env python3
# encoding: utf-8

import os
import sys

import npyscreen
import logging
import datetime
from logging.handlers import RotatingFileHandler
import argparse
import configparser

import django
import pprint

from django.conf import settings
from logging.handlers import RotatingFileHandler
from django.core.management.base import BaseCommand, CommandError

import pickle

# there is some  import module after determining the sys.path

# minimum lines && column ( Termux for android)
MINIMUM_LINES=32
MINIMUM_COLUMNS=55


if __name__=="__main__":

    # retrieve path
    scriptdir = os.path.dirname( os.path.abspath(sys.argv[0]))

    # You launch from directory where manage.py exist or you are using settingpath argument
    launchdir = os.getcwd()
    pathname =os.path.abspath(launchdir)

    print("go to {} directory".format(pathname))

    # go to the directory
    os.chdir(pathname)

    sys.path.insert(0,pathname)

    projectname='backendSideFondation'

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(projectname))
    django.setup()

    #*******************************************************************
    #* create on curency
    #*
    #*******************************************************************
    from a_p_p_l_i_c_a_t_i_o_n_N_a_m_e.models import M_o_d_e_l_C_o_m_p_o_n_e_n_t, FiatCurrency, getDefaultCurrency

    # getDefaultCurrency is a function that create a currency
    getDefaultCurrency()

