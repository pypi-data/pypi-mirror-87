#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 20:08:55 2020

@author: WildTuan
"""
from setuptools import setup
 
setup(
     name='my-awesome-firstAppPipInstallable-script',    # This is the name of your PyPI-package.
     version='0.2',                          # Update the version number for new releases
     scripts=['FirstAppPipInst']             # The name of your scipt, and also the command you'll be using for calling it
 )