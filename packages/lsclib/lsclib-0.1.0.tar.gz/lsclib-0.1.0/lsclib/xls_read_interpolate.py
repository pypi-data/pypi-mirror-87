# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:15:45 2019

@author: smithd24
"""
import pandas as pd
import numpy as np
import pkg_resources
from scipy.interpolate import InterpolatedUnivariateSpline

def excel_read():

    # read silicone matrix absorption spectrum data from excel
    # abs_matrix = pd.read_csv('data/absorption_matrix.csv')
    abs_matrix = pkg_resources.resource_stream(__name__,
                                               'data/absorption_matrix.csv')
    abs_matrix = pd.read_csv(abs_matrix)
    # read pv external quantum efficiency spectrum data from excel
    # EQE_pv = pd.read_csv('data/eqe_pv.csv')
    EQE_pv = pkg_resources.resource_stream(__name__,'data/eqe_pv.csv')
    EQE_pv = pd.read_csv(EQE_pv)
    # read pv internal quantum efficiency spectrum data from excel
    # IQE_pv = pd.read_csv('data/iqe_pv.csv')
    IQE_pv = pkg_resources.resource_stream(__name__,'data/iqe_pv.csv')
    IQE_pv = pd.read_csv(IQE_pv)
    # read xenon emission spectrum data from excel
    # emi_source = pd.read_csv('data/emission_source.csv')
    emi_source = pkg_resources.resource_stream(__name__,
                                               'data/emission_source.csv')
    emi_source = pd.read_csv(emi_source)
    # read phosphor absorption spectrum data from excel
    # abs_particle = pd.read_csv('data/absorption_particle.csv')
    abs_particle = pkg_resources.resource_stream(__name__,
                                                'data/absorption_particle.csv')
    abs_particle = pd.read_csv(abs_particle)
    # read phosphor emission spectrum data from excel
    # emi_particle = pd.read_csv('data/emission_particle.csv')
    emi_particle = pkg_resources.resource_stream(__name__,
                                                'data/emission_particle.csv')
    emi_particle = pd.read_csv(emi_particle)
    
    return abs_matrix, EQE_pv, IQE_pv, emi_source, abs_particle, emi_particle

def spline(dataset):
  "Creates a polynomial regression model for the given degree"
  
  num_cols = np.size(dataset,1)
  X = dataset.iloc[:, 0:1].values
  Y = dataset.iloc[:, num_cols - 1].values
  max_value_x = max(X)[0]
  spl = InterpolatedUnivariateSpline(X, Y)
  
  return spl, max_value_x