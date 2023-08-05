# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:14:00 2019

@author: smithd24
"""

import math
import time
from lsclib import xls_read_interpolate as xlsread
from lsclib import lsc_classes as lsccls
import cProfile, pstats
from lsclib import external_equations as eqn
import pandas as pd

def wedge(trials, Einc = 451.313, light_form = 'direct',
                   results = 'single', theta_o = .000001, phi_o = .000001):
    """Set up geometry to run trials for a wedge-shaped LSC. Specify
    vertices that make up the LSC. Each vertice will belong to a boundary and
    each boundary will belong to a volume. Using the LSC classes that have
    been defined, attribute characteristics to each boundary and volume.

    Parameters
    ----------
    trials : int
        Indicate number of bundles that will be used for the program
    Einc : float
        Indicates incident irradiance on the LSC. Default is 451.313 based upon
        the irradiance of the Newport Solar Simulator used for experiments.
    light_form : string
        Determines distribution of light entering the LSC.
        'direct'  - light enters at a fixed angle
        'diffuse' - light enters with a Lambertian distribution
        'ground'  - light enters with a modified Lambertian distribution due to
                    the relative angle up from the ground
    results : string
        Determines if one result or if a matrix of incidence angle
        combinations is desired
    theta_o : float, optional
        Initial polar incidence angle. Default is zero. This is the polar angle
        relative to the LSC normal.
    phi_o : float, optional
        Initial azimuthal incidence angle. Default is zero. This is the azimuth
        angle relative to the LSC normal.
    
    Returns
    -------
    LSC : object
        LSC object is returned after program has run. The LSC object will have
        the optical efficiency, short circuit current (for a cell within an
        LSC and a bare solar cell), and spectral mismatch factor available as
        attributes among a variety of other simulation results.
    
    Notes
    -----
    Having this written as one large script might not be the best. There are
    a large variety of inputs, so, instead of inputting them all here, these
    could be inputs to particular functions that make up "lsc_main". This would
    also demonstrate that a user is not limited to only the configuration
    detailed in the main script shown here.
    
    Phosphor particle should be added before iterating through incidence angle
    combinations.
    
    Starting volume/boundary process shoud be improved.
    
    errorcounts should be replaced by a for loop that runs automatically
    """

    
    # Initialize wedge-shaped geometry. Coordinates of individual vertices are
    # determined before they are assigned to individual boundaries.
    Height = .007
    Film_height = .001
    Short_side_pos = 0  # distance up from zero to the bottom point of the
                              # short side of a wedge-shaped LSC
    Top_length = .05
    Mirror_gap_length = .000001
    W = .022
    precision = 16 
    hypotenuse = math.sqrt(Short_side_pos**2 + Top_length**2)
    angle = math.acos(Top_length/hypotenuse)
    
    L0 = 0
    H0_0 = 0
    H0_1 = Film_height
    H0_2 = Height
    
    L1 = Mirror_gap_length*math.cos(angle)
    H1_0 = Mirror_gap_length*math.sin(angle)
    H1_1 = H1_0 + Film_height
    
    L2 = Top_length
    H2_0 = Short_side_pos
    H2_1 = H2_0 + Film_height
    H2_2 = Height
    
    L1 = round(L1, precision)
    H1_0 = round(H1_0, precision)
    H1_1 = round(H1_1, precision)
    H2_1 = round(H2_1, precision)
    
    L = Top_length
    H = Height
    
    # read in various excel data tables
    [abs_matrix, EQE_pv, IQE_pv, emi_source,
     abs_particle, emi_particle] = xlsread.excel_read()
    EQE_pv, EQE_pv_max = xlsread.spline(EQE_pv)
    IQE_pv, IQE_pv_max = xlsread.spline(IQE_pv)
    emi_source, emi_source_max = xlsread.spline(emi_source)
    abs_particle, abs_particle_max = xlsread.spline(abs_particle)
    emi_particle, emi_particle_max = xlsread.spline(emi_particle)
    
    # establish particle characteristics
    wave_len_min = 270  # minimum wavelength that can be absorbed by a particle
    wave_len_max = 500  # maximum wavelength that can be absorbed by a particle
    qe = 0.75           # quantum efficiency of a particle
    poa = .2            # probability of particle absorption (exp. value)
    extinction = 4240   # extinction coefficient (42.4 cm^-1)
    
    
    # establish matrix characteristics
    IoR = eqn.IoR_Sellmeier    # set index of refraction as constant or eqn
    abs_matrix, abs_matrix_max = xlsread.spline(abs_matrix)
    wave_len_min_matrix = 229   # minimum wavelength absorbed by matrix
    wave_len_max_matrix = 1100  # maximum wavelength absorbed by matrix
    
    
    # establish solar cell characteristics
    wave_len_min_pv = 350   # minimum wavelength absorbed by pv
    wave_len_max_pv = 1100  # maximum wavelength absorbed by pv
    
    # if running a combination of many theta_o and phi_o
    if light_form == 'direct' and results == 'matrix':
        
        data = {'':  [0.001, 15, 30, 45, 60, 75],
                 0:  [0, 0, 0, 0, 0, 0],
                15:  [0, 0, 0, 0, 0, 0],
                30:  [0, 0, 0, 0, 0, 0],
                45:  [0, 0, 0, 0, 0, 0],
                60:  [0, 0, 0, 0, 0, 0],
                75:  [0, 0, 0, 0, 0, 0],
                89.999:  [0, 0, 0, 0, 0, 0]} 
        
        # Convert the dictionary into DataFrame 
        df = pd.DataFrame(data)
        df.set_index('', inplace = True)
        theta_loop_count = len(df.index)
        phi_loop_count = len(df.columns)
    
    # if expecting just one combination of inputs
    if results == 'single':
        
        theta_loop_count = 1
        phi_loop_count = 1
    
    for j in range(phi_loop_count):
        for i in range(theta_loop_count):
            start_time = time.time()
            lsc = lsccls.LSC()  # initialize LSC class
            
            # add phosphor particle
            particle = lsccls.Particle(poa, extinction, wave_len_min,
                                       wave_len_max, qe, abs_particle,
                                       emi_particle, emi_particle_max)
            
            # define dimensions/characteristics of Volume 0 - mirror gap
                        
            # input boundaries by setting boundary points of each
            bdy0a = [[0, L0, H0_0], [0, L1, H1_0], [W, L1, H1_0], [W, L0, H0_0]]
            bdy0b = [[0, L1, H1_0], [0, L1, H1_1], [W, L1, H1_1], [W, L1, H1_0]]
            bdy0c = [[0, L0, H0_1], [0, L1, H1_1], [W, L1, H1_1], [W, L0, H0_1]]
            bdy0d = [[0, L0, H0_0], [0, L0, H0_1], [W, L0, H0_1], [W, L0, H0_0]]
            bdy0e = [[0, L0, H0_0], [0, L1, H1_0], [0, L1, H1_1], [0, L0, H0_1]]
            bdy0f = [[W, L0, H0_0], [W, L1, H1_0], [W, L1, H1_1], [W, L0, H0_1]]
            bdys0 = [bdy0a, bdy0b, bdy0c, bdy0d, bdy0e, bdy0f]
             
            lsc.vol_list.append(lsccls.AbsorbingVolume(bdys0, 0, lsc, IoR,
                                                       abs_matrix,
                                                       wave_len_min_matrix,
                                                       wave_len_max_matrix))
            # add bottom surface
            lsc[0].bdy_list.append(lsccls.OpaqueBoundary(bdys0[0], lsc[0],
                                                         'specular', .05))
            # add right interface with film
            lsc[0].bdy_list.append(lsccls.TransparentBoundary(bdys0[1],
                                                              lsc[0]))
            # add interface with rest of matrix
            lsc[0].bdy_list.append(lsccls.TransparentBoundary(bdys0[2],
                                                              lsc[0]))
            # add left solar cell
            lsc[0].bdy_list.append(lsccls.PVBoundary(bdys0[3], lsc[0],
                                                     'diffuse', EQE_pv ,
                                                     0, wave_len_min_pv,
                                                     wave_len_max_pv))
            # add front mirror
            lsc[0].bdy_list.append(lsccls.OpaqueBoundary(bdys0[4], lsc[0],
                                                         'specular', .05))
            # add back mirror
            lsc[0].bdy_list.append(lsccls.OpaqueBoundary(bdys0[5], lsc[0],
                                                         'specular', .05))
            
            # define dimensions/characteristics of Volume 1 - phosphor film
            
            # input boundaries by setting boundary points of each
            bdy1a = [[0, L1, H1_0], [0, L2, H2_0], [W, L2, H2_0], [W, L1, H1_0]]
            bdy1b = [[0, L2, H2_0], [0, L2, H2_1], [W, L2, H2_1], [W, L2, H2_0]]
            bdy1c = [[0, L1, H1_1], [0, L2, H2_1], [W, L2, H2_1], [W, L1, H1_1]]
            bdy1d = [[0, L1, H1_0], [0, L1, H1_1], [W, L1, H1_1], [W, L1, H1_0]]
            bdy1e = [[0, L1, H1_0], [0, L2, H2_0], [0, L2, H2_1], [0, L1, H1_1]]
            bdy1f = [[W, L1, H1_0], [W, L2, H2_0], [W, L2, H2_1], [W, L1, H1_1]]
            bdys1 = [bdy1a, bdy1b, bdy1c, bdy1d, bdy1e, bdy1f]
            
            lsc.vol_list.append(lsccls.ParticleVolume(bdys1, 1, lsc, IoR,
                                                      abs_matrix, particle,
                                                      wave_len_min_matrix,
                                                      wave_len_max_matrix))
            # add bottom surface
            lsc[1].bdy_list.append(lsccls.OpaqueBoundary(bdys1[0], lsc[1],
                                                         'specular', .05))
            # add right mirror
            lsc[1].bdy_list.append(lsccls.OpaqueBoundary(bdys1[1], lsc[1],
                                                         'specular', .05))
            # add top surface
            lsc[1].bdy_list.append(lsccls.TransparentBoundary(bdys1[2], lsc[1]))
            # add left interface with mirror gap
            lsc[1].bdy_list.append(lsccls.TransparentBoundary(bdys1[3], lsc[1]))
            # add front mirror
            lsc[1].bdy_list.append(lsccls.OpaqueBoundary(bdys1[4], lsc[1],
                                                         'specular', .05))
            # add back mirror
            lsc[1].bdy_list.append(lsccls.OpaqueBoundary(bdys1[5], lsc[1],
                                                         'specular', .05))
            
            # define dimensions/characteristics of Volume 2 - rest of matrix
            
            # input boundaries by setting boundary points of each
            bdy2a = [[0, L0, H0_1], [0, L2, H2_1], [W, L2, H2_1], [W, L0, H0_1]]
            bdy2b = [[0, L2, H2_1], [0, L2, H2_2], [W, L2, H2_2], [W, L2, H2_1]]
            bdy2c = [[0, L0, H0_2], [0, L2, H2_2], [W, L2, H2_2], [W, L0, H0_2]]
            bdy2d = [[0, L0, H0_1], [0, L0, H0_2], [W, L0, H0_2], [W, L0, H0_1]]
            bdy2e = [[0, L0, H0_1], [0, L2, H2_1], [0, L2, H2_2], [0, L0, H0_2]]
            bdy2f = [[W, L0, H0_1], [W, L2, H2_1], [W, L2, H2_2], [W, L0, H0_2]]
            bdys2 = [bdy2a, bdy2b, bdy2c, bdy2d, bdy2e, bdy2f]
            
            # define volume
            lsc.vol_list.append(lsccls.AbsorbingVolume(bdys2, 2, lsc, IoR,
                                                       abs_matrix,
                                                       wave_len_min_matrix,
                                                       wave_len_max_matrix))
            # add interface with mirror gap and phosphor film
            lsc[2].bdy_list.append(lsccls.TransparentBoundary(bdys2[0],
                                                              lsc[2]))
            # add right mirror
            lsc[2].bdy_list.append(lsccls.OpaqueBoundary(bdys2[1], lsc[2],
                                                         'specular', .05))
            # add top surface
            lsc[2].bdy_list.append(lsccls.TransparentBoundary(bdys2[2],
                                                              lsc[2]))
            # add solar cell
            lsc[2].bdy_list.append(
                    lsccls.PVBoundary(bdys2[3], lsc[2], 'diffuse', EQE_pv , 0,
                                      wave_len_min_pv, wave_len_max_pv))
            # add front mirror
            lsc[2].bdy_list.append(lsccls.OpaqueBoundary(bdys2[4], lsc[2],
                                                         'specular', .05))
            # add back mirror
            lsc[2].bdy_list.append(lsccls.OpaqueBoundary(bdys2[5], lsc[2],
                                                         'specular', .05))
             
            # Prepare data inputs for LSC simulation
            if light_form == 'direct' and results == 'matrix':
                theta_o = df.index[i]
                phi_o = df.columns[j]
                
            lsc.matching_pairs()    
            I = Einc*math.cos(math.radians(theta_o))*(L*W)
            theta_o = math.radians(theta_o + 180)  # adjust theta to head down
            phi_o = math.radians(phi_o + 90)       # adjust phi
            
            # Run LSC trials, determining fate of every bundle
            starting_vol = len(lsc) - 1
            starting_bdy = 2
            
            lsc.main(trials, L, W, H, light_form, theta_o,
                     phi_o, starting_vol, starting_bdy, I,
                     emi_source, emi_source_max, particle)
            
            # Process data outputs from all LSC trials
            
            # determine if all bundles in volume 0 are accounted for
            errorcount0 = (lsc[0].bundles_absorbed +
                           lsc[0][0].bundles_absorbed +
                           lsc[0][1].bundles_reflected +
                           lsc[0][1].bundles_refracted +
                           lsc[0][2].bundles_reflected +
                           lsc[0][2].bundles_refracted +
                           lsc[0][3].bundles_absorbed +
                           lsc[0][4].bundles_absorbed + 
                           lsc[0][5].bundles_absorbed)
            
            # determine if all bundles in volume 1 are accounted for
            errorcount1 = (lsc[1].bundles_absorbed +
                           lsc[1][0].bundles_absorbed +
                           lsc[1][1].bundles_absorbed +
                           lsc[1][2].bundles_reflected +
                           lsc[1][2].bundles_refracted +
                           lsc[1][3].bundles_reflected +
                           lsc[1][3].bundles_refracted +
                           lsc[1][4].bundles_absorbed +
                           lsc[1][5].bundles_absorbed + 
                           particle.bundles_absorbed)
            
            # determine if all bundles in volume 2 are accounted for
            errorcount2 = (lsc[2].bundles_absorbed +
                           lsc[2][0].bundles_reflected +
                           lsc[2][0].bundles_refracted +
                           lsc[2][1].bundles_absorbed +
                           lsc[2][2].bundles_reflected +
                           lsc[2][2].bundles_refracted +
                           lsc[2][3].bundles_absorbed +
                           lsc[2][4].bundles_absorbed +
                           lsc[2][5].bundles_absorbed)
        
            error = (errorcount0 + errorcount1 + errorcount2)/trials
        
            if error != 1:
                print("\nENERGY IS NOT CONSERVED!!!!!")

            if results == 'matrix':
                df.iloc[i,j] = lsc
    
    if results == 'matrix':
        writer = pd.ExcelWriter('LSC_data.xlsx')
        df.to_excel(writer,'Sheet1')
        writer.save()
        lsc = df
    else:
        print(time.time() - start_time)
        print(light_form)
        print(lsc.optical_efficiency)
    
    return lsc

# if __name__ == '__main__':
#     LSC_wedge_main(1000)

# pr = cProfile.Profile()
# pr.enable()
# LSC_wedge_main(1000)
# pr.disable()
# pr.dump_stats('prof_data')

# ps = pstats.Stats('prof_data')
# ps.sort_stats(pstats.SortKey.CUMULATIVE)
              
# ps.print_stats()