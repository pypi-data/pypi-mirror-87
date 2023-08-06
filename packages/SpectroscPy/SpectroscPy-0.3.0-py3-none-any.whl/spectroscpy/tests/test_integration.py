# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

# Integration tests for SpectroscPy

import os
import numpy as np
from spectroscpy import SpectroscPy_run

def test_SpectroscPy_run():

    spectral_boundaries = 'Keep all'
    ticker_distance = 250
    data_dir = '{0}/'.format(os.path.dirname(__file__))

    ###############################################
    # Testing various combinations of spectra
    ###############################################

    # IR with SSDG a.u., outproj, single snapshot, 'Vib modes: 1/m'
    ref_harmonic_frequencies = [414847.68302357, 414104.28285256, 178148.02217701, \
                                158913.50380254, 148697.90566093, 18299.94565116]
    ref_fundamental = []
    ref_overtones = []
    ref_combotones = []
    ref_harmonic_ir = [1.70424946e-05, 7.11347711e-06, 1.16235812e-06, \
                       2.59612870e-05, 9.52361364e-09, 7.56689106e-05]
    ref_fundamental_ir = []
    ref_overtone_ir = []
    ref_combotone_ir = []

    ref_input_raman = ['You did not ask for Raman intensities']
    ref_harmonic_raman = []
    ref_fundamental_raman = []
    ref_overtone_raman = []
    ref_combotone_raman = []

    ref_ih = ['You did not ask for Hyper-Raman intensities']
    ref_harmonic_hR_vv = []
    ref_fundamental_hR_vv = []
    ref_overtone_hR_vv = []
    ref_combotone_hR_vv = []
    ref_harmonic_hR_hv = []
    ref_fundamental_hR_hv = []
    ref_overtone_hR_hv = []
    ref_combotone_hR_hv = []

    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, a.u.']
    names = [data_dir,'hf_H2O2.rsp_tensor', 'H2O2.mol']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # With Raman, 'Raman: CPG 45+4, a.u.'
    ref_harmonic_frequencies = [414847.68302357, 414104.28285256, 178148.02217701, \
                                158913.50380254, 148697.90566093, 18299.94565116]
    ref_harmonic_ir = [1.70424946e-05, 7.11347711e-06, 1.16235812e-06, \
                       2.59612870e-05, 9.52361364e-09, 7.56689106e-05]
    ref_input_raman = [0.0, 2194746.0394200613]
    ref_harmonic_raman = [[0.07930255, 0.45635755, 0.0458494 ,\
                           0.01015121, 0.07769959, 0.03215856], \
                          [0.08495927, 0.49572019, 0.04674917, \
                           0.0103366 , 0.08624967, 0.03293001]]

    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['IR', 'Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, a.u.', 'Raman: CPG 45+4, a.u.']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # Also with Hyper-Raman
    ref_harmonic_ir = [1.70424946e-05, 7.11347711e-06, 1.16235812e-06, \
                       2.59612870e-05, 9.52361364e-09, 7.56689106e-05]
    ref_harmonic_raman = [[0.07930255, 0.45635755, 0.0458494 , \
                           0.01015121, 0.07769959, 0.03215856], \
                          [0.08495927, 0.49572019, 0.04674917, \
                           0.0103366 , 0.08624967, 0.03293001]]
    ref_harmonic_hR_vv = [[5.31275323e-42, 1.63731429e-42, 4.38462803e-43,
                           2.74009360e-42, 6.76023854e-44, 2.97702629e-41],
                          [4.04902604e-46, 1.31612249e-46, 1.26646968e-48,
                           4.77616251e-48, 8.16225856e-50, 7.27144463e-51]]
    ref_ih = [2194746.0394200613, 0.0]
    ref_harmonic_hR_hv = [[7.03927756e-43, 5.22978431e-43, 2.73830629e-43,
                           1.05652253e-42, 1.15579372e-44, 6.26610333e-42],
                          [5.13529085e-47, 4.26925953e-47, 7.97713412e-49,
                           1.79640060e-48, 1.95696552e-50, 1.48825197e-51]]

    spectroscopy_type = ['IR', 'Raman', 'Hyper-Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, a.u.', 'Raman: CPG 45+4, a.u.', \
                                  'Hyper-Raman: SI complete']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(np.multiply(ref_harmonic_hR_vv, 1.0e51), \
                       np.multiply(properties.hyper_raman_vv.harmonic, 1.0e51))
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(np.multiply(ref_harmonic_hR_hv, 1.0e51), \
                       np.multiply(properties.hyper_raman_hv.harmonic, 1.0e51))
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # With boundaries
    harmonic_frequency_limits = [20000, 200000]
    ref_harmonic_frequencies = [178148.02217701, 158913.50380254, 148697.90566093]
    ref_harmonic_ir = [1.16235812e-06, 2.59612870e-05, 9.52361364e-09]
    ref_harmonic_raman = [[0.0458494 , 0.01015121, 0.07769959], \
                          [0.04674917, 0.0103366 , 0.08624967]]
    ref_ih = [2194746.0394200613, 0.0]
    ref_harmonic_hR_vv = [[4.38462803e-43, 2.74009360e-42, 6.76023854e-44],
                          [1.26646968e-48, 4.77616251e-48, 8.16225856e-50]]
    ref_harmonic_hR_hv = [[2.73830629e-43, 1.05652253e-42, 1.15579372e-44],
                          [7.97713412e-49, 1.79640060e-48, 1.95696552e-50]]

    spectroscopy_type = ['IR', 'Raman', 'Hyper-Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, a.u.', 'Raman: CPG 45+4, a.u.', \
                                  'Hyper-Raman: SI complete']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, harmonic_frequency_limits, spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(np.multiply(ref_harmonic_hR_vv, 1.0e51), \
                       np.multiply(properties.hyper_raman_vv.harmonic, 1.0e51))
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(np.multiply(ref_harmonic_hR_hv, 1.0e51), \
                       np.multiply(properties.hyper_raman_hv.harmonic, 1.0e51))
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    #####################################
    # Multiple IR snapshots
    #####################################
    data_dir = '{0}/snap_combo_test/'.format(os.path.dirname(__file__))
    run_specification = ['Multiple snapshots', 'No outproj', 'FraME']
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/cm', 'IR: NIMAC, km/mol', 'Raman: CPG 45+4, a.u.']
    names = [data_dir, 1, 10, 'ir_raman_hf', 'opt', 'trjout', []]

    ref_harmonic_frequencies = [3.33078114e+03, 3.32158536e+03, 3.29228022e+03, 3.28194549e+03,
                                3.20776855e+03, 3.19761998e+03, 1.92917363e+03, 1.61277454e+03,
                                1.59622670e+03, 1.58442665e+03, 1.57799919e+03, 1.54559059e+03,
                                1.52559898e+03, 1.37816741e+03, 1.23799082e+03, 1.19014362e+03,
                                1.01341530e+03, 9.68188256e+02, 8.62645250e+02, 6.09233078e+02,
                                5.45659043e+02, 4.19803875e+02, 1.71337329e+02, 1.40899461e+02,
                                1.22066920e+02, 9.41093315e+01, 6.55948158e+01, 1.99624528e+01,
                                4.48189727e+00, 5.64144241e-15]
    ref_harmonic_ir = [5.60177482e+00, 8.76300875e+00, 4.43962691e+00, 4.89804133e+00,
                       2.77869445e+00, 4.74816503e+00, 4.16442196e+02, 2.85626104e+01,
                       1.70492603e+01, 2.86844236e+01, 2.33283697e+01, 7.62134211e+01,
                       1.31892291e+01, 6.08451702e+01, 1.34805808e+01, 6.33563381e+00,
                       2.02586950e+00, 1.28400989e+00, 6.82871011e-01, 3.98663831e+01,
                       4.54839060e+00, 3.83943417e+00, 3.44440417e+00, 5.47707190e+00,
                       4.82938698e+00, 2.08633073e+00, 2.77679902e+00, 9.46017663e-01,
                       3.06349179e-01, 7.82142529e-17]
    ref_input_raman = ['You did not ask for Raman intensities']
    ref_harmonic_raman = []

    ref_ih = ['You did not ask for Hyper-Raman intensities']
    ref_harmonic_hR_vv = []
    ref_harmonic_hR_hv = []

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # Skip snapshot 3
    names = [data_dir, 1, 10, 'ir_raman_hf', 'opt', 'trjout', [3]]

    ref_harmonic_frequencies = [3.33106580e+03, 3.32174914e+03, 3.29235498e+03, 3.28243743e+03,
                                3.20760092e+03, 3.19715558e+03, 1.92828228e+03, 1.61293055e+03,
                                1.59658884e+03, 1.58465969e+03, 1.57808758e+03, 1.54544889e+03,
                                1.52579398e+03, 1.37871364e+03, 1.23785090e+03, 1.19000455e+03,
                                1.01457251e+03, 9.67029242e+02, 8.62756045e+02, 6.09357913e+02,
                                5.45551889e+02, 4.19831825e+02, 1.71098648e+02, 1.40287291e+02,
                                1.21083429e+02, 9.14602123e+01, 6.06554280e+01, 1.90287044e+01,
                                4.97988585e+00, 5.87424838e-15]
    ref_harmonic_ir = [5.41756152e+00, 8.82082372e+00, 4.72075070e+00, 5.05296719e+00,
                       3.08555269e+00, 4.94016221e+00, 4.16693178e+02, 2.86942346e+01,
                       1.83557977e+01, 2.60575007e+01, 2.54746775e+01, 7.60626000e+01,
                       1.35534696e+01, 6.08382063e+01, 1.35485785e+01, 6.54423322e+00,
                       1.97560023e+00, 1.34249757e+00, 7.06441926e-01, 4.00434954e+01,
                       4.62407815e+00, 3.85007260e+00, 3.57064324e+00, 5.29449646e+00,
                       5.35989143e+00, 1.92016383e+00, 2.60461748e+00, 9.24235884e-01,
                       3.40387977e-01, 7.32301105e-17]

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # Skip snapshot 3 and with spectral boundaries
    names = [data_dir, 1, 10, 'ir_raman_hf', 'opt', 'trjout', [3]]
    harmonic_frequency_limits = [750, 2500]

    ref_harmonic_frequencies = [1928.28228082, 1612.93054675, 1596.5888359 , 1584.65968965,
                                1578.08757736, 1545.44889491, 1525.79397837, 1378.71364202,
                                1237.85090302, 1190.00455   , 1014.57251102,  967.02924156,
                                862.75604487]

    ref_harmonic_ir = [416.6931785 ,  28.69423459,  18.35579774,  26.05750075,  25.4746775,
                        76.0626    ,  13.55346961,  60.83820625,  13.54857855,   6.54423322,
                         1.97560023,   1.34249757,   0.70644193]

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, harmonic_frequency_limits, spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    #############################################
    # Testing other frequency units
    #############################################

    data_dir = '{0}/'.format(os.path.dirname(__file__))
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    # Only IR with SSDG a.u., outproj, single snapshot, 'Vib modes: 1/cm'
    ref_harmonic_frequencies = [4148.47683024, 4141.04282853, 1781.48022177, 1589.13503803, \
                                1486.97905661, 182.99945651]
    ref_harmonic_ir = [1.70424946e-05, 7.11347711e-06, 1.16235812e-06, 2.59612870e-05, 9.52361364e-09, \
                       7.56689106e-05]
    ref_harmonic_raman = []
    ref_ih = ['You did not ask for Hyper-Raman intensities']
    ref_harmonic_hR_vv = []
    ref_harmonic_hR_hv = []
    spectroscopy_type = ['IR']
    names = [data_dir,'hf_H2O2.rsp_tensor', 'H2O2.mol']
    spectroscopy_specification = ['Vib modes: 1/cm', 'IR: SSDG, a.u.']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # Only IR with SSDG a.u., outproj, single snapshot, 'Vib modes: 1/s'
    ref_harmonic_frequencies = [1.24368207e+14, 1.24145341e+14, 5.34074335e+13, 4.76410699e+13, \
                                4.45785106e+13, 5.48618569e+12]
    spectroscopy_specification = ['Vib modes: 1/s', 'IR: SSDG, a.u.']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # Only IR with SSDG a.u., outproj, single snapshot, 'Vib modes: ang. 1/s'
    ref_harmonic_frequencies = [7.81428488e+14, 7.80028181e+14, 3.35568801e+14, 2.99337671e+14, \
                                2.80095043e+14, 3.44707213e+13]
    spectroscopy_specification = ['Vib modes: ang. 1/s', 'IR: SSDG, a.u.']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # Only IR with SSDG a.u., outproj, single snapshot, 'Vib modes: Eh'
    ref_harmonic_frequencies = [0.01890185, 0.01886798, 0.00811702, 0.00724063, 0.00677518, 0.00083381]
    spectroscopy_specification = ['Vib modes: Eh', 'IR: SSDG, a.u.']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    #############################################
    # Testing anharmonic frequencies
    #############################################

    # 'Vib modes: 1/m'
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: MDAC, m**2/(s*mol)']
    names = [data_dir,'hf_anharm_H2O2.rsp_tensor', 'H2O2.mol']

    # GVPT2 frequencies, DVTP2 intensities, w/ 1-1 checks.  This is default.
    ref_harmonic_frequencies = [414847.6830235662, 414104.2828525629, 178148.02217701354, \
                                158913.5038025385, 148697.90566093015, 18299.94565115991]
    ref_fundamental = [396057.43586589, 404798.68025287, 181622.38677956,
                    145526.50449582, 147425.41271963, -35751.88302422]
    ref_overtones = [ 785763.7904302,   803683.37589429,  348760.7362605,
                      280130.8044133,   293772.40096096, -133966.9388231 ]
    ref_combotones = [[     0.        , 789532.03985542, 571337.7795644,  542945.85920111,
                       543137.76510721, 345048.23894016],
                      [789532.03985542,      0.        , 581047.24654331, 550884.16599507,
                       551929.17084098, 371669.13263512],
                      [571337.7795644 , 581047.24654331,      0.        , 328411.46648376,
                       324992.05211235, 156838.92199932],
                      [542945.85920111, 550884.16599507, 328411.46648376,      0.,
                       291836.56645761,  83339.75275562],
                      [543137.76510721, 551929.17084098, 324992.05211235, 291836.56645761,
                            0.        , 110068.23014444],
                      [345048.23894016, 371669.13263512, 156838.92199932,  83339.75275562,
                       110068.23014444,      0.        ]]
    ref_harmonic_ir = [2.47758950e+13, 1.03413711e+13, 1.68980326e+12, \
                       3.77417826e+13, 1.38451583e+10, 1.10005317e+14]
    ref_fundamental_ir = [ 2.30619415e+13,  3.26466951e+12,  3.61011365e+11,
                           4.08975052e+13,  3.44932309e+09, -7.63359156e+14]
    ref_overtone_ir = [ 8.58392415e+10,  4.23865536e+10,  1.84918690e+11, \
                        2.05189755e+10,  1.70427797e+09, -1.48001366e+14]
    ref_combotone_ir = [[0.00000000e+00, 1.64118417e+12, 1.71857707e+11,
                         4.42260746e+09, 2.94685593e+11, 3.07793407e+12],
                        [1.64118417e+12, 0.00000000e+00, 1.07872034e+10,
                         4.42508342e+11, 2.63620441e+09, 1.76135047e+12],
                        [1.71857707e+11, 1.07872034e+10, 0.00000000e+00,
                         3.56424083e+11, 2.43212365e+10, 1.87416123e+11],
                        [4.42260746e+09, 4.42508342e+11, 3.56424083e+11,
                         0.00000000e+00, 1.13326043e+11, 2.77976060e+11],
                        [2.94685593e+11, 2.63620441e+09, 2.43212365e+10,
                         1.13326043e+11, 0.00000000e+00, 2.19788277e+10],
                        [3.07793407e+12, 1.76135047e+12, 1.87416123e+11,
                         2.77976060e+11, 2.19788277e+10, 0.00000000e+00]]

    run_specification = ['Single snapshot',  'No FraME', 'Outproj', \
                         'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # Same, just default setting
    run_specification = ['Single snapshot',  'No FraME', 'Outproj', 'Anharmonic']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # 'Vib modes: 1/cm'
    ref_harmonic_frequencies = [4148.47683024, 4141.04282853, 1781.48022177, 1589.13503803, \
                                1486.97905661, 182.99945651]
    ref_fundamental = [3960.57435866, 4047.98680253, 1816.2238678,
                    1455.26504496, 1474.2541272, -357.51883024]
    ref_overtones = [ 7857.6379043,   8036.83375894,  3487.6073626,
                      2801.30804413,  2937.72400961, -1339.66938823]
    ref_combotones = [[   0.        , 7895.32039855, 5713.37779564, 5429.45859201, 5431.37765107,
                       3450.4823894 ],
                      [7895.32039855,    0.        , 5810.47246543, 5508.84165995, 5519.29170841,
                       3716.69132635],
                      [5713.37779564, 5810.47246543,    0.        , 3284.11466484, 3249.92052112,
                       1568.38921999],
                      [5429.45859201, 5508.84165995, 3284.11466484,    0.        , 2918.36566458,
                       833.39752756],
                      [5431.37765107, 5519.29170841, 3249.92052112, 2918.36566458,    0.,
                       1100.68230144],
                      [3450.4823894,  3716.69132635, 1568.38921999,  833.39752756, 1100.68230144,
                       0.        ]]

    run_specification = ['Single snapshot',  'No FraME', 'Outproj', 'Anharmonic']
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/cm', 'IR: MDAC, m**2/(s*mol)']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # 'Vib modes: 1/s'
    ref_harmonic_frequencies = [1.24368207e+14, 1.24145341e+14, 5.34074335e+13, 4.76410699e+13, \
                                4.45785106e+13, 5.48618569e+12]
    ref_fundamental = [ 1.18735032e+14,  1.21355591e+14,  5.44490218e+13,
                     4.36277485e+13,  4.41970269e+13, -1.07181449e+13]
    ref_overtones = [ 2.35566058e+14,  2.40938215e+14,  1.04555838e+14,
                      8.39811024e+13,  8.80707502e+13, -4.01622779e+13]
    ref_combotones = [[0.00000000e+00, 2.36695751e+14, 1.71282757e+14, 1.62771074e+14,
                       1.62828606e+14, 1.03442860e+14],
                      [2.36695751e+14, 0.00000000e+00, 1.74193582e+14, 1.65150918e+14,
                       1.65464203e+14, 1.11423603e+14],
                      [1.71282757e+14, 1.74193582e+14, 0.00000000e+00, 9.84552808e+13,
                       9.74301661e+13, 4.70191259e+13],
                      [1.62771074e+14, 1.65150918e+14, 9.84552808e+13, 0.00000000e+00,
                       8.74904016e+13, 2.49846293e+13],
                      [1.62828606e+14, 1.65464203e+14, 9.74301661e+13, 8.74904016e+13,
                       0.00000000e+00, 3.29976253e+13],
                      [1.03442860e+14, 1.11423603e+14, 4.70191259e+13, 2.49846293e+13,
                       3.29976253e+13, 0.00000000e+00]]

    spectroscopy_specification = ['Vib modes: 1/s', 'IR: MDAC, m**2/(s*mol)']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # 'Vib modes: ang. 1/s'
    ref_harmonic_frequencies = [7.81428488e+14, 7.80028181e+14, 3.35568801e+14, 2.99337671e+14, \
                                2.80095043e+14, 3.44707206e+13]
    ref_fundamental = [ 7.46034210e+14,  7.62499669e+14,  3.42113294e+14,
                     2.74121228e+14,  2.77698110e+14, -6.73440905e+13]
    ref_overtones = [ 1.48010520e+15,  1.51385945e+15,  6.56943707e+14,
                      5.27668829e+14,  5.53364844e+14, -2.52347034e+14]
    ref_combotones = [[0.00000000e+00, 1.48720326e+15, 1.07620130e+15, 1.02272082e+15,
                       1.02308230e+15, 6.49950656e+14],
                      [1.48720326e+15, 0.00000000e+00, 1.09449056e+15, 1.03767382e+15,
                       1.03964225e+15, 7.00095144e+14],
                      [1.07620130e+15, 1.09449056e+15, 0.00000000e+00, 6.18612774e+14,
                       6.12171788e+14, 2.95429881e+14],
                      [1.02272082e+15, 1.03767382e+15, 6.18612774e+14, 0.00000000e+00,
                       5.49718406e+14, 1.56983056e+14],
                      [1.02308230e+15, 1.03964225e+15, 6.12171788e+14, 5.49718406e+14,
                       0.00000000e+00, 2.07330194e+14],
                      [6.49950656e+14, 7.00095144e+14, 2.95429881e+14, 1.56983056e+14,
                       2.07330194e+14, 0.00000000e+00]]

    spectroscopy_specification = ['Vib modes: ang. 1/s', 'IR: MDAC, m**2/(s*mol)']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # 'Vib modes: Eh'
    ref_harmonic_frequencies = [0.01890185, 0.01886798, 0.00811702, 0.00724063, 0.00677518, 0.00083381]
    ref_fundamental = [ 0.01804571,  0.01844399,  0.00827533,  0.00663068,  0.0067172,  -0.00162898]
    ref_overtones = [ 0.03580204,  0.03661851,  0.01589071,  0.0127637,   0.01338526, -0.00610398]
    ref_combotones = [[0.        , 0.03597373, 0.02603207, 0.02473844, 0.02474718, 0.01572156],
                      [0.03597373, 0.        , 0.02647446, 0.02510013, 0.02514775, 0.01693449],
                      [0.02603207, 0.02647446, 0.        , 0.01496353, 0.01480773, 0.00714611],
                      [0.02473844, 0.02510013, 0.01496353, 0.        , 0.01329705, 0.00379724],
                      [0.02474718, 0.02514775, 0.01480773, 0.01329705, 0.        , 0.00501508],
                      [0.01572156, 0.01693449, 0.00714611, 0.00379724, 0.00501508, 0.        ]]

    spectroscopy_specification = ['Vib modes: Eh', 'IR: MDAC, m**2/(s*mol)']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # With spectral boundaries
    harmonic_frequency_limits = [750, 2500]
    spectroscopy_specification = ['Vib modes: 1/cm', 'IR: MDAC, m**2/(s*mol)']

    ref_harmonic_frequencies = [1781.48022177, 1589.13503803, 1486.97905661]
    ref_fundamental = [1806.70732912, 1629.54316495, 1471.06917007]
    ref_overtones = [3622.78863395, 3282.85794395, 2931.84462103]
    ref_combotones = [[   0.      ,   3474.35630648, 3271.37695375],
                      [3474.35630648,    0.        , 3095.77954416],
                      [3271.37695375, 3095.77954416,    0.        ]]
    ref_harmonic_ir = [1.68980326e+12, 3.77417826e+13, 1.38451583e+10]
    ref_fundamental_ir = [1.45931433e+12, 3.61187177e+13, 1.26087920e+10]
    ref_overtone_ir = [1.26594775e+08, 1.38126143e+11, 1.51533061e+09]
    ref_combotone_ir = [[0.00000000e+00, 2.96196421e+11, 1.25060998e+10],
                        [2.96196421e+11, 0.00000000e+00, 1.18105584e+11],
                        [1.25060998e+10, 1.18105584e+11, 0.00000000e+00]]

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, harmonic_frequency_limits, spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # New molecule, CO2
    # Default, GVPT2 frequencies, DVPT2 intensities, w/ 1-1 checks
    ref_harmonic_frequencies = [256437.00659636, 151124.33230516,  77296.77672684,  77296.64946092]
    ref_fundamental = [251541.01307331, 145222.64954562,  76854.85245673,  76854.70570159]
    ref_overtones = [500606.12530794, 297503.0186331,  154143.18970647, 157941.75784598]
    ref_combotones = [[     0.        , 398506.11685921, 327003.83987687, 327003.67295073],
                      [398506.11685921,      0.        , 225340.43060746, 225340.28098378],
                      [327003.83987687, 225340.43060746,      0.        , 153886.10372417],
                      [327003.67295073, 225340.28098378, 153886.10372417,      0.        ]]
    ref_harmonic_ir = [8.54625832e+14, 3.17635369e+03, 5.19429527e+13, 5.19426496e+13]
    ref_fundamental_ir = [8.19474208e+14, 2.84260765e+03, 5.11382110e+13, 5.11379038e+13]
    ref_overtone_ir = [  25.40036256,  218.31910831, 2636.89009248,   58.22707756]
    ref_combotone_ir = [[0.00000000e+00, 1.66393085e+13, 1.85592250e+03, 4.67037802e+02],
                        [1.66393085e+13, 0.00000000e+00, 1.40798509e+10, 1.40806092e+10],
                        [1.85592250e+03, 1.40798509e+10, 0.00000000e+00, 5.32281245e+00],
                        [4.67037802e+02, 1.40806092e+10, 5.32281245e+00, 0.00000000e+00]]

    spectroscopy_specification = ['Vib modes: 1/m', 'IR: MDAC, m**2/(s*mol)']
    names = [data_dir,'anharm_ir_opt_CO2.rsp_tensor', 'opt_CO2.mol']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # VPT2
    ref_fundamental = [251541.01307331, 139253.45676694,  76854.85245673,  76854.70570159]
    ref_overtones = [500606.12530794, 277967.49681247, 159027.0578499,  159027.08248123]
    ref_combotones = [[     0.        , 388738.35594889, 327003.83987687, 327003.67295073],
                      [388738.35594889,      0.        , 205805.23489789, 205804.43305208],
                      [327003.83987687, 205805.23489789,      0.        , 153886.10372417],
                      [327003.67295073, 205804.43305208, 153886.10372417,      0.        ]]
    ref_harmonic_ir = [1.04469889e+03, 3.88279063e-09, 6.34953251e+01, 6.34949545e+01]
    ref_fundamental_ir = [1.00172937e+03, 6.67988353e-09, 6.25116048e+01, 6.25112293e+01]
    ref_overtone_ir = [3.10495302e-11, 2.49350076e-10, 1.33029629e-08, 5.29699937e-09]
    ref_combotone_ir = [[0.00000000e+00, 1.98414220e+01, 2.26868894e-09, 5.70909344e-10],
                                    [1.98414220e+01, 0.00000000e+00, 1.57192012e-02, 1.57199969e-02],
                                    [2.26868894e-09, 1.57192012e-02, 0.00000000e+00, 6.50663255e-12],
                                    [5.70909344e-10, 1.57199969e-02, 6.50663255e-12, 0.00000000e+00]]

    run_specification = ['Single snapshot',  'No FraME', 'Outproj', 'Anharmonic: VPT2']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: NIMAC, km/mol']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # DVPT2 frequencies, VPT2 intensities
    ref_fundamental = [251541.01307331, 149021.21767726,  76854.85245673,  76854.70570159]
    ref_overtones = [500606.12530794, 297503.0186331,  154143.34045028, 154143.03897053]
    ref_combotones = [[     0.        , 398506.11685921, 327003.83987687, 327003.67295073],
                      [398506.11685921,      0.        , 225340.43060746, 225340.28098378],
                      [327003.83987687, 225340.43060746,      0.        , 153886.10372417],
                      [327003.67295073, 225340.28098378, 153886.10372417,      0.        ]]
    ref_fundamental_ir = [1.00172937e+03, 7.14843567e-09, 6.25116048e+01, 6.25112293e+01]
    ref_overtone_ir = [3.10495302e-11, 2.66874369e-10, 1.28944292e-08, 5.13431780e-09]
    ref_combotone_ir = [[0.00000000e+00, 2.03399740e+01, 2.26868894e-09, 5.70909344e-10],
                                    [2.03399740e+01, 0.00000000e+00, 1.72112802e-02, 1.72122071e-02],
                                    [2.26868894e-09, 1.72112802e-02, 0.00000000e+00, 6.50663255e-12],
                                    [5.70909344e-10, 1.72122071e-02, 6.50663255e-12, 0.00000000e+00]]

    run_specification = ['Single snapshot',  'No FraME', 'Outproj', 'Anharmonic: Freq DVPT2, Int VPT2']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # DVPT2
    ref_overtone_ir = [3.10495302e-11, 2.66874369e-10, 3.22335078e-09, 6.94651632e-11]
    ref_combotone_ir = [[0.00000000e+00, 2.03399740e+01, 2.26868894e-09, 5.70909344e-10],
                                    [2.03399740e+01, 0.00000000e+00, 1.72112802e-02, 1.72122071e-02],
                                    [2.26868894e-09, 1.72112802e-02, 0.00000000e+00, 6.50663255e-12],
                                    [5.70909344e-10, 1.72122071e-02, 6.50663255e-12, 0.00000000e+00]]

    run_specification = ['Single snapshot',  'No FraME', 'Outproj', 'Anharmonic: DVPT2']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: NIMAC, km/mol']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # DVPT2 with 1-1 checks
    run_specification = ['Single snapshot',  'No FraME', 'Outproj', 'Anharmonic: DVPT2, w/ 1-1 checks']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # GVPT2 frequencies, DVPT2 intensities
    ref_fundamental = [251541.01307331, 145222.64954562,  76854.85245673,  76854.70570159]
    ref_overtones = [500606.12530794, 297503.0186331,  154143.18970647, 157941.75784598]
    ref_combotones = [[     0.        , 398506.11685921, 327003.83987687, 327003.67295073],
                      [398506.11685921,      0.        , 225340.43060746, 225340.28098378],
                      [327003.83987687, 225340.43060746,      0.        , 153886.10372417],
                      [327003.67295073, 225340.28098378, 153886.10372417,      0.        ]]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj', 'Anharmonic: Freq GVPT2, Int DVPT2']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # GVPT2 frequencies, DVPT2 intensities, w/ 1-1 checks and forced removal of i,j
    run_specification = ['Single snapshot',  'No FraME', 'Outproj', \
                         'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks and forced removal']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    ################################
    # Raman anharmonic
    ################################
    spectroscopy_type = ['Raman']

    # Default
    ref_harmonic_frequencies = [256437.00659612, 151124.33230492,  77296.77672635,  77296.64946049]
    ref_fundamental = [251541.03004926, 145222.60989632,  76854.85877896,  76854.70747309]
    ref_overtones = [500606.17121029, 297503.00613437, 154143.19654364, 157941.80080274]
    ref_combotones = [[     0.        , 398506.12815512, 327003.87448365, 327003.69258875],
                      [398506.12815512,      0.        , 225340.43664436, 225340.28192791],
                      [327003.87448365, 225340.43664436,      0.       ,  153886.1133476 ],
                      [327003.69258875, 225340.28192791, 153886.1133476,       0.        ]]

    ref_harmonic_ir = []
    ref_fundamental_ir = []
    ref_overtone_ir = []
    ref_combotone_ir = []

    ref_input_raman = [0.0, 219474.60394200613]
    ref_harmonic_raman = [[4.53263491e-12, 9.26005295e-02, 3.17855256e-11, 3.24475018e-12],
                          [4.53936045e-12, 9.26966048e-02, 3.18050950e-11, 3.24599800e-12]]
    ref_fundamental_raman = [[4.80799128e-12, 8.88403378e-02, 3.16489362e-11, 3.26558293e-12],
                             [4.87633186e-12, 8.90586079e-02, 3.17364560e-11, 3.26775105e-12]]
    ref_overtone_raman = [[1.82913516e-03, 6.82920887e-05, 9.39258683e-04, 9.62426439e-04],
                          [1.97633183e-03, 5.49728045e-05, 1.12084414e-03, 1.14848731e-03]]
    ref_combotone_raman = [[[0.00000000e+00, 6.68051330e-15, 5.36442562e-04, 5.36458689e-04],
                            [6.68051330e-15, 0.00000000e+00, 1.93304594e-13, 2.36882808e-13],
                            [5.36442562e-04, 1.93304594e-13, 0.00000000e+00, 2.72619337e-04],
                            [5.36458689e-04, 2.36882808e-13, 2.72619337e-04, 0.00000000e+00]],
                           [[0.00000000e+00, 4.78453649e-15, 6.39682834e-04, 6.39713789e-04],
                            [4.78453649e-15, 0.00000000e+00, 2.07142407e-13, 2.45106722e-13],
                            [6.39682834e-04, 2.07142407e-13, 0.00000000e+00, 2.93236803e-04],
                            [6.39713789e-04, 2.45106722e-13, 2.93236803e-04, 0.00000000e+00]]]

    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: CPG 45+7, a.u.']
    names = [data_dir,'anharm_raman_opt_CO2.rsp_tensor', 'opt_CO2.mol']
    run_specification = ['Single snapshot',  'No FraME', 'Outproj', \
                         'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # With spectral boundaries
    harmonic_frequency_limits = [100000, 300000]
    ref_harmonic_frequencies = [256437.00659612, 151124.33230492]
    ref_fundamental = [252933.05968835, 149556.85212988]
    ref_overtones = [503390.23048852, 298574.28210431]
    ref_combotones = [[     0.       ,  400433.79577907],
                      [400433.79577907,      0.        ]]
    ref_harmonic_raman = [[4.53263491e-12, 9.26005295e-02], [4.53936045e-12, 9.26966048e-02]]
    ref_fundamental_raman = [[4.71114182e-12, 9.19978672e-02],
                             [4.74070823e-12, 9.21620270e-02]]
    ref_overtone_raman = [[1.83930767e-03, 6.85380010e-05],
                          [1.98732296e-03, 5.51707556e-05]]
    ref_combotone_raman = [[[0.00000000e+00, 6.71282861e-15],
                            [6.71282861e-15, 0.00000000e+00]],
                           [[0.00000000e+00, 4.80768058e-15],
                            [4.80768058e-15, 0.00000000e+00]]]

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, harmonic_frequency_limits, spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    ##########################################
    # Testing IR without outprojection
    ##########################################
    ref_harmonic_frequencies = [4.14848132e+05, 4.14105192e+05, 1.78147036e+05, 1.58912905e+05, \
                                1.48698110e+05, 1.83061036e+04, 4.66792909e+02, 2.28608186e+02, \
                                3.76592066e+00, 1.78308846e+00, 2.00676340e-16, 6.82319818e-14]
    ref_fundamental = []
    ref_overtones = []
    ref_combotones = []
    ref_harmonic_ir = [1.70425815e-05, 7.11360916e-06, 1.16243696e-06, 2.59611627e-05,
                       9.52928458e-09, 7.56686604e-05, 4.15214594e-06, 1.41336245e-09,
                       1.03022827e-14, 6.28763989e-14, 2.10884638e-30, 6.41679479e-22]
    ref_fundamental_ir = []
    ref_overtone_ir = []
    ref_combotone_ir = []

    ref_input_raman = ['You did not ask for Raman intensities']
    ref_harmonic_raman = []
    ref_fundamental_raman = []
    ref_overtone_raman = []
    ref_combotone_raman = []
    run_specification = ['Single snapshot',  'No FraME', 'No outproj']
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, a.u.']
    names = [data_dir,'hf_H2O2.rsp_tensor', 'H2O2.mol']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    #########################################
    # Testing various IR units
    #########################################

    # IR 'IR: SSDG, C**2/kg'
    ref_harmonic_frequencies = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, \
                                148697.90566093, 18299.94565116]
    ref_harmonic_ir = [4.80247329e-13, 2.00453540e-13, 3.27545582e-14, 7.31573576e-13, \
                       2.68369749e-16, 2.13230475e-12]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, C**2/kg']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # IR 'IR: SSDG, D2A2/amu'
    ref_harmonic_ir = [7.16729788e-01, 2.99160484e-01, 4.88834942e-02, 1.09181362e+00, \
                       4.00519861e-04, 3.18229012e+00]

    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, D2A2/amu']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # IR 'IR: MDAC, m**2/(s*mol)'
    ref_harmonic_ir = [2.47758955e+13, 1.03413714e+13, 1.68980328e+12, 3.77417830e+13, \
                       1.38451595e+10, 1.10005317e+14]

    spectroscopy_specification = ['Vib modes: 1/m', 'IR: MDAC, m**2/(s*mol)']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # IR 'IR: MDAC, L/(cm*s*mol)'
    ref_harmonic_ir = [2.47758955e+14, 1.03413714e+14, 1.68980328e+13, 3.77417830e+14, \
                       1.38451595e+11, 1.10005317e+15]

    spectroscopy_specification = ['Vib modes: 1/m', 'IR: MDAC, L/(cm*s*mol)']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # IR 'IR: NIMAC, m/mol'
    ref_harmonic_ir = [3.02861786e+04, 1.26413440e+04, 2.06562397e+03, 4.61357442e+04, \
                       1.69243922e+01, 1.34471049e+05]

    spectroscopy_specification = ['Vib modes: 1/m', 'IR: NIMAC, m/mol']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # IR 'IR: NIMAC, km/mol'
    ref_harmonic_ir = [3.02861786e+01, 1.26413440e+01, 2.06562397e+00, 4.61357442e+01, \
                       1.69243922e-02, 1.34471049e+02]

    spectroscopy_specification = ['Vib modes: 1/m', 'IR: NIMAC, km/mol']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    ##########################################
    # Testing Raman without outprojection
    ##########################################
    # 'Raman: CPG 45+4, a.u.'
    ref_harmonic_frequencies = [4.14848132e+05, 4.14105192e+05, 1.78147036e+05, 1.58912905e+05, \
                                1.48698110e+05, 1.83061036e+04, 4.66792909e+02, 2.28608186e+02, \
                                3.76592066e+00, 1.78308846e+00, 2.00676340e-16, 6.82319818e-14]
    ref_harmonic_ir = []
    ref_harmonic_raman = [[7.93028424e-02, 4.56357234e-01, 4.58507534e-02, 1.01512626e-02,
                           7.76989345e-02, 3.21671155e-02, 1.60659179e-02, 5.49605023e-03,
                           6.02922285e-10, 1.06834364e-09, 7.75710579e-11, 5.23731418e-03],
                          [8.49595795e-02, 4.95719846e-01, 4.67506291e-02, 1.03366556e-02,
                           8.62489799e-02, 3.29389362e-02, 1.68834189e-02, 5.83206659e-03,
                           6.39431311e-10, 1.13117595e-09, 8.16618156e-11, 5.45999671e-03]]

    run_specification = ['Single snapshot',  'No FraME', 'No outproj']
    spectroscopy_type = ['Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: CPG 45+4, a.u.']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    ###########################################
    # Testing Raman with different temperature
    ###########################################
    # 'Raman: CPG 45+4, a.u.'
    ref_harmonic_frequencies = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, \
                                148697.90566093, 18299.94565116]
    ref_input_raman = [0.0, 2194746.0394200613]
    ref_harmonic_raman = [[0.07930255, 0.45635755, 0.0458494 , 0.01015121, 0.07769959, 0.03215856], \
                 [0.08495927, 0.49572019, 0.04674917, 0.0103366 , 0.08624967, 0.03293001]]

    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: CPG 45+4, a.u.']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all',  spectral_boundaries, 0, 500, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    #########################################
    # Testing various Raman units
    #########################################

    # 'Raman: CPG 45+7, a.u.'
    ref_harmonic_frequencies = [414847.68302357, 414104.28285256, 178148.02217701,
                                158913.50380254, 148697.90566093, 18299.94565116]
    ref_harmonic_raman = \
        [[0.13877932, 0.56428613, 0.07978227, 0.01776461, 0.10018108, 0.05627554], \
         [0.14867857, 0.61365418, 0.08134747, 0.01808905, 0.11121732, 0.05762325]]

    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: CPG 45+7, a.u.']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # 'Raman: PCPG 45+4, Å^4/amu'
    ref_harmonic_raman = [[11.33579065, 65.23338327,  6.55387684,
                            1.45104975, 11.10665772, 4.59686046],
                          [12.14438241, 70.86002056,  6.68249426,
                           1.47755042, 12.32883741, 4.70713297]]

    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: PCPG 45+4, Å^4/amu']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # 'Raman: PCPG 45+7, Å^4/amu'
    ref_harmonic_raman = [[19.83761352, 80.66108141, 11.40436285,
                            2.53933706, 14.32024325, 8.04422734],
                          [21.25264742, 87.71792697, 11.6280985 ,
                            2.58571323, 15.89780238, 8.236874  ]]

    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: PCPG 45+7, Å^4/amu']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # 'Raman: SCS 45+4, SI units'
    ref_harmonic_raman = [[1.68900739e-59, 9.66746918e-59, 7.73454705e-61,
                           1.21585175e-61, 7.62680802e-61, 1.00212177e-63],
                          [6.13170567e-57, 3.59014089e-56, 1.29487703e-56,
                           3.33476796e-57, 3.03476824e-56, 2.05309056e-55]]
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: SCS 45+4, SI units']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(np.multiply(ref_harmonic_raman, 1.0e57), \
                       np.multiply(properties.raman.harmonic, 1.0e57))
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    # 'Raman: SCS 45+7, SI units'
    ref_harmonic_raman = [[2.95575993e-59, 1.19538261e-58, 1.34588402e-60,
                           2.12774056e-61, 9.83353848e-61, 1.75365240e-63],
                          [1.07304739e-56, 4.44425099e-56, 2.25319425e-56,
                           5.83584392e-57, 3.91327617e-56, 3.59264298e-55]]

    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: SCS 45+7, SI units']

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(np.multiply(ref_harmonic_raman, 1.0e57), \
                       np.multiply(properties.raman.harmonic, 1.0e57))
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    #############################################
    # Testing Hyper-Raman with relative units
    #############################################

    ref_harmonic_frequencies = [414847.68302357, 414104.28285256, 178148.02217701, 
                                158913.50380254, 148697.90566093, 18299.94565116]
    ref_input_raman = ['You did not ask for Raman intensities']
    ref_harmonic_raman = []
    ref_ih = [2194746.0394200613, 0.0]
    ref_harmonic_hR_vv = [[1.32930196e-01, 4.09671782e-02, 1.09707611e-02,
                          6.85597773e-02, 1.69147670e-03, 7.44880611e-01],
                         [7.46162915e-01, 2.42537782e-01, 2.33387660e-03,
                          8.80161132e-03, 1.50415793e-04, 1.33999690e-05]]
    ref_harmonic_hR_hv = [[7.96756176e-02, 5.91944687e-02, 3.09941244e-02,
                          1.19584836e-01, 1.30821064e-03, 7.09242743e-01],
                         [5.31269910e-01, 4.41674910e-01, 8.25271918e-03,
                          1.85846063e-02, 2.02457256e-04, 1.53966642e-05]]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['Hyper-Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'Hyper-Raman: Relative']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    #############################################
    # Testing Hyper-Raman without outprojection
    #############################################

    ref_harmonic_frequencies = [4.14848132e+05, 4.14105192e+05, 1.78147036e+05, 1.58912905e+05, \
                                1.48698110e+05, 1.83061036e+04, 4.66792909e+02, 2.28608186e+02, \
                                3.76592066e+00, 1.78308846e+00, 2.00676340e-16, 6.82319818e-14]
    ref_harmonic_raman = []
    ref_harmonic_hR_vv = [[5.31273995e-42, 1.63730356e-42, 4.38473895e-43,
                           2.74010236e-42, 6.76044647e-44, 2.97550125e-41,
                           6.80552913e-39, 3.32424797e-39, 1.45857352e-42,
                           1.50750449e-41,         0.0,         0.0],
                          [4.04903478e-46, 1.31612617e-46, 1.26647019e-48,
                           4.77610258e-48, 8.16255824e-50, 7.27754427e-51,
                           7.18664080e-55, 2.04810522e-56, 6.60058384e-67,
                           3.41426816e-67,         0.0,         0.0]]
    ref_harmonic_hR_hv = [[7.03925589e-43, 5.22975464e-43, 2.73834897e-43,
                           1.05652542e-42, 1.15574097e-44, 6.26338275e-42,
                           3.85813147e-39, 2.21622586e-39, 9.47159688e-43,
                           9.35558514e-42,         0.0,         0.0],
                          [5.13529829e-47, 4.26927492e-47, 7.97707447e-49,
                           1.79637731e-48, 1.95694983e-50, 1.48962076e-51,
                           4.10208004e-55, 1.36484221e-56, 4.29033384e-67,
                           2.12564065e-67,         0.0,         0.0]]
    run_specification = ['Single snapshot',  'No FraME', 'No outproj']
    spectroscopy_specification = ['Vib modes: 1/m', 'Hyper-Raman: SI complete']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(np.multiply(ref_harmonic_hR_vv, 1.0e68), \
                       np.multiply(properties.hyper_raman_vv.harmonic, 1.0e68))
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(np.multiply(ref_harmonic_hR_hv, 1.0e68), \
                       np.multiply(properties.hyper_raman_hv.harmonic, 1.0e68))
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    #################################################
    # Testing Hyper-Raman with different temperature
    #################################################

    ref_harmonic_frequencies = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, \
                                148697.90566093, 18299.94565116]
    ref_harmonic_hR_vv = [[1.00449121e-01, 3.09569817e-02, 8.33802650e-03,
                          5.23233957e-02, 1.29513564e-03, 8.06637339e-01],
                         [7.46081599e-01, 2.42511384e-01, 2.34711611e-03,
                          8.88830357e-03, 1.52395746e-04, 1.92010781e-05]]
    ref_harmonic_hR_hv = [[6.08887819e-02, 4.52369208e-02, 2.38229334e-02,
                          9.22979347e-02, 1.01301590e-03, 7.76740413e-01],
                         [5.31141250e-01, 4.41568010e-01, 8.29842925e-03,
                          1.87651570e-02, 2.05094915e-04, 2.20592430e-05]]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['Hyper-Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'Hyper-Raman: Relative']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all',  spectral_boundaries, 0, 500, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    #################################################
    # Testing Hyper-Raman acetonitrile and PBE0
    #################################################

    ref_harmonic_frequencies = [317856.39743121, 317853.74787773, 311438.99096985, 243343.46125899, \
                                160281.82059371, 160280.65824062, 155928.11021045, 115925.32030771, \
                                115924.61054995,  98390.40505199, 57141.73061079,  57138.76702502]
    ref_ih = [0.0]
    ref_harmonic_hR_vv = [[3.62227706e-01, 3.62234035e-01, 2.66531636e-01, 2.63531818e-03,
                          1.11360609e-03, 1.11345743e-03, 1.32406438e-03, 1.15347880e-03,
                          1.15319171e-03, 9.90449800e-05, 2.07226152e-04, 2.07235145e-04]]
    ref_harmonic_hR_hv = [[3.17571204e-01, 3.17588532e-01, 3.49798202e-01, 4.33810095e-03,
                          2.33136208e-03, 2.33126776e-03, 1.93772093e-03, 1.91050463e-03,
                          1.90967547e-03, 4.72823392e-05, 1.18089718e-04, 1.18058415e-04]]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    names = [data_dir,'ir_raman_hyper_raman_opt_pcseg-2_PBE0_acetonitrile.rsp_tensor', \
             'opt_pcseg-2_PBE0_acetonitrile.mol']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert ref_ih == properties.input_hyperraman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)

    ######################################
    # Anharmonic Hyper-Raman
    ######################################

    names = [data_dir,'anharm_hR_opt_CO2.rsp_tensor', 'opt_CO2.mol']
    ref_harmonic_frequencies = [256437.00659612, 151124.33230492,  77296.77672635,  77296.64946049]
    ref_fundamental = [251541.03004926, 145222.60989632,  76854.85877896,  76854.70747309]
    ref_overtones = [500606.17121029, 297503.00613437, 154143.19654364, 157941.80080274]
    ref_combotones = [[     0.        , 398506.12815512, 327003.87448365, 327003.69258875],
                      [398506.12815512,      0.        , 225340.43664436, 225340.28192791],
                      [327003.87448365, 225340.43664436,      0.        , 153886.1133476 ],
                      [327003.69258875, 225340.28192791, 153886.1133476 ,      0.        ]]

    ref_input_raman = ['You did not ask for Raman intensities']
    ref_ih = [0.0, 2194746.0394200613]
    ref_harmonic_hR_vv = [[9.90788525e-01, 6.99024602e-12, 4.60571029e-03, 4.60576436e-03],
                          [4.36934142e-01, 2.95139325e-11, 2.81530072e-01, 2.81535786e-01]]
    ref_fundamental_hR_vv = [[9.90017134e-01, 6.48909276e-12, 4.99140794e-03, 4.99145809e-03],
                             [4.31811936e-01, 3.03823007e-11, 2.84091301e-01, 2.84096763e-01]]
    ref_overtone_hR_vv = [[0.38437107, 0.22640362, 0.37506885, 0.01415645],
                          [0.02660268, 0.03278811, 0.85395224, 0.08665698]]
    ref_combotone_hR_vv = [[[0.00000000e+00, 8.66078715e-01, 3.38917659e-09, 4.32500315e-10],
                            [1.00000000e+00, 0.00000000e+00, 9.99999997e-01, 1.00000000e+00],
                            [2.62033993e-10, 6.69608257e-02, 0.00000000e+00, 1.39100821e-11],
                            [3.34385538e-11, 6.69604591e-02, 1.39100059e-11, 0.00000000e+00]],
                           [[0.00000000e+00, 1.96812827e-01, 5.06472242e-10, 3.93178580e-10],
                            [9.99999998e-01, 0.00000000e+00, 9.99999999e-01, 1.00000000e+00],
                            [1.03345130e-09, 4.01594510e-01, 0.00000000e+00, 8.93400541e-11],
                            [8.02273076e-10, 4.01592662e-01, 8.93396430e-11, 0.00000000e+00]]]
    ref_harmonic_hR_hv = [[9.89172560e-01, 9.13516264e-12, 5.41373105e-03, 5.41370927e-03],
                          [4.23346143e-01, 3.26349593e-11, 2.88325584e-01, 2.88328273e-01]]
    ref_fundamental_hR_hv = [[9.88061890e-01, 8.72560181e-12, 5.96907193e-03, 5.96903847e-03],
                             [4.11657247e-01, 3.44030721e-11, 2.94170131e-01, 2.94172622e-01]]
    ref_overtone_hR_hv = [[0.35113417, 0.21135637, 0.42668718, 0.01082228],
                          [0.03157629, 0.02782191, 0.8507255 , 0.0898763 ]]
    ref_combotone_hR_hv = [[[0.00000000e+00, 8.49865153e-01, 3.61956268e-09, 1.07825411e-09],
                            [1.00000000e+00, 0.00000000e+00, 9.99999996e-01, 9.99999999e-01],
                            [3.19713085e-10, 7.50679110e-02, 0.00000000e+00, 4.62549284e-11],
                            [9.52400881e-11, 7.50669360e-02, 4.62543275e-11, 0.00000000e+00]],
                           [[0.00000000e+00, 2.24011676e-01, 6.36352559e-10, 4.91830343e-10],
                            [9.99999998e-01, 0.00000000e+00, 9.99999999e-01, 9.99999999e-01],
                            [1.10218069e-09, 3.87994580e-01, 0.00000000e+00, 2.35760205e-10],
                            [8.51862272e-10, 3.87993743e-01, 2.35759696e-10, 0.00000000e+00]]]

    run_specification = ['Single snapshot',  'No FraME', 'Outproj', \
                         'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks']
    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, 'Keep all', spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_ih, properties.input_hyperraman_frequencies)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)
    
    # With spectral boundaries
    harmonic_frequency_limits = [100000, 300000]
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, a.u.', 'Raman: CPG 45+4, a.u.', \
                                  'Hyper-Raman: SI complete']
    ref_harmonic_frequencies = [256437.00659612, 151124.33230492]
    ref_fundamental = [252933.05968835, 149556.85212988]
    ref_overtones = [503390.23048852, 298574.28210431]
    ref_combotones = [[     0.       ,  400433.79577907],
                      [400433.79577907,      0.        ]]
    ref_harmonic_hR_vv = [[2.29991092e-46, 1.62264124e-57],
                          [2.44012459e-41, 1.64825006e-51]]
    ref_fundamental_hR_vv = [[2.18036508e-46, 1.64622074e-57],
                             [2.48788245e-41, 1.80334217e-51]]
    ref_overtone_hR_vv = [[3.14997378e-58, 1.55046575e-58],
                          [8.40748847e-54, 8.93531686e-54]]
    ref_combotone_hR_vv = [[[0.00000000e+00, 4.60040669e-48],
                            [4.60040669e-48, 0.00000000e+00]],
                           [[0.00000000e+00, 4.04008377e-44],
                            [4.04008377e-44, 0.00000000e+00]]]
    ref_harmonic_hR_hv = [[2.83980954e-47, 2.62260834e-58],
                          [3.11423346e-42, 2.40070410e-52]]
    ref_fundamental_hR_hv = [[2.66299696e-47, 2.67597023e-58],
                             [3.11791160e-42, 2.62826049e-52]]
    ref_overtone_hR_hv = [[4.75240578e-59, 2.37353497e-59],
                          [1.84583808e-54, 1.44455423e-54]]
    ref_combotone_hR_hv = [[[0.00000000e+00, 7.13218710e-49],
                            [7.13218710e-49, 0.00000000e+00]],
                           [[0.00000000e+00, 7.75620501e-45],
                            [7.75620501e-45, 0.00000000e+00]]]

    properties = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                 [], names, harmonic_frequency_limits, spectral_boundaries, 0, 298, ticker_distance)

    assert np.allclose(ref_harmonic_frequencies, properties.frequencies.harmonic)
    assert np.allclose(ref_fundamental, properties.frequencies.fundamental)
    assert np.allclose(ref_overtones, properties.frequencies.overtones)
    assert np.allclose(ref_combotones, properties.frequencies.combotones)
    assert np.allclose(ref_harmonic_ir, properties.ir.harmonic)
    assert np.allclose(ref_fundamental_ir, properties.ir.fundamental)
    assert np.allclose(ref_overtone_ir, properties.ir.overtones)
    assert np.allclose(ref_combotone_ir, properties.ir.combotones)
    assert ref_input_raman == properties.input_raman_frequencies
    assert np.allclose(ref_harmonic_raman, properties.raman.harmonic)
    assert np.allclose(ref_fundamental_raman, properties.raman.fundamental)
    assert np.allclose(ref_overtone_raman, properties.raman.overtones)
    assert np.allclose(ref_combotone_raman, properties.raman.combotones)
    assert np.allclose(ref_ih, properties.input_hyperraman_frequencies)
    assert np.allclose(ref_harmonic_hR_vv, properties.hyper_raman_vv.harmonic)
    assert np.allclose(ref_fundamental_hR_vv, properties.hyper_raman_vv.fundamental)
    assert np.allclose(ref_overtone_hR_vv, properties.hyper_raman_vv.overtones)
    assert np.allclose(ref_combotone_hR_vv, properties.hyper_raman_vv.combotones)
    assert np.allclose(ref_harmonic_hR_hv, properties.hyper_raman_hv.harmonic)
    assert np.allclose(ref_fundamental_hR_hv, properties.hyper_raman_hv.fundamental)
    assert np.allclose(ref_overtone_hR_hv, properties.hyper_raman_hv.overtones)
    assert np.allclose(ref_combotone_hR_hv, properties.hyper_raman_hv.combotones)
    
