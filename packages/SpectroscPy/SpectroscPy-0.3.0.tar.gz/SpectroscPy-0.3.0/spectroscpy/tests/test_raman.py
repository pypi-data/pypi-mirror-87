# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

from spectroscpy import get_a2_term, get_b2_term, get_exp_denominator, \
                        raman_scattering_cross_section, get_combined_polarizabilites, \
                        requested_unit_incident_mode, get_raman_intensities, anharmonicProperty, \
                        get_rscattering_cross_section
import numpy as np

# Global test-variables
au_polarizability_gradient = [[[ 6.24435728e-02, -3.63042281e-02,  2.14401949e-02], \
                               [-3.63042281e-02, -6.26361513e-02, -3.72962095e-02], \
                               [ 2.14401949e-02, -3.72962095e-02, -9.06369159e-06]], \
                              [[ 1.25458452e-01,  5.20423355e-02,  8.34157410e-02], \
                               [ 5.20423355e-02,  6.50703815e-02,  4.80299100e-02], \
                               [ 8.34157410e-02,  4.80299100e-02,  6.96537639e-02]], \
                              [[-2.37970681e-02, -7.93763435e-03,  4.05413246e-02], \
                               [-7.93763435e-03, -1.45319888e-02,  2.33876187e-02], \
                               [ 4.05413246e-02,  2.33876187e-02,  4.94476269e-02]], \
                              [[-1.59236762e-02,  9.24345862e-03,  1.14034737e-02], \
                               [ 9.24345862e-03,  1.58998007e-02, -1.98171323e-02], \
                               [ 1.14034737e-02, -1.98171323e-02,  2.33747801e-05]], \
                              [[ 4.60303578e-03,  4.14936993e-04,  7.97344578e-03], \
                               [ 4.14936993e-04,  4.13298957e-03,  4.64696392e-03], \
                               [ 7.97344578e-03,  4.64696392e-03,  9.41809158e-02]], \
                              [[-2.45703253e-02, -4.36328512e-02, -1.21236513e-02], \
                               [-4.36328512e-02,  2.60312669e-02, -7.01564880e-03], \
                               [-1.21236513e-02, -7.01564880e-03, -2.52655827e-03]]]

au_input_frequency = 0.1

au_vibrational_energies = [0.018901854754709915, 0.018867982944327566, 0.008117022651510061, \
                           0.007240633346545635, 0.006775176360266165, 0.0008338070305617636]

temperature = 298

harmonic_wavenumbers = [414847.68302357, 414104.28285256, 178148.02217701,
                        158913.50380254, 148697.90566093,  18299.94565116]
fundamental = [396057.43586589, 404798.68025287, 181622.38677956,
               145526.50449582, 147425.41271963, -35751.88302422]
overtones = [ 785763.7904302,   803683.37589429,  348760.7362605,
              280130.8044133,   293772.40096096, -133966.9388231 ]
combotones = [[     0.        , 789532.03985542, 571337.7795644,
               542945.85920111, 543137.76510721, 345048.23894016],
              [789532.03985542,      0.        , 581047.24654331,
               550884.16599507, 551929.17084098, 371669.13263512],
              [571337.7795644 , 581047.24654331,      0.        ,
               328411.46648376, 324992.05211235, 156838.92199932],
              [542945.85920111, 550884.16599507, 328411.46648376,
                     0.,        291836.56645761,  83339.75275562],
              [543137.76510721, 551929.17084098, 324992.05211235,
               291836.56645761,      0.        , 110068.23014444],
              [345048.23894016, 371669.13263512, 156838.92199932,
               83339.75275562,  110068.23014444,      0.        ]]

SI_wavenumbers = anharmonicProperty(harmonic_wavenumbers, fundamental, overtones, combotones)


CO2_harmonic_wavenumbers = [308803.62879803, 169409.60714536,  15856.18156937,  15852.54619014]
CO2_fundamental_wavenumbers = [298437.35928427, 170192.2063791,   26246.64170339,  26247.44867762]
CO2_overtones_wavenumbers = [594112.21291436, 339972.06592672,  61950.8418014,   61957.63980011]
CO2_combotones_wavenumbers = [[     0.        , 466883.50538247, 317954.17644414, 317953.1650671 ],
                                 [466883.50538247,      0.        , 198506.6568093 , 198507.79874123],
                                 [317954.17644414, 198506.6568093 ,      0.        ,  59021.90967648],
                                 [317953.1650671,  198507.79874123,  59021.90967648,      0.        ]]

CO2_wavenumbers = anharmonicProperty(CO2_harmonic_wavenumbers, CO2_fundamental_wavenumbers, \
                                         CO2_overtones_wavenumbers, CO2_combotones_wavenumbers)

harmonic_transition_polarizability_moment = \
[[[ 1.07540845e-47, -3.49221675e-47, -2.58346513e-58],
  [-3.49221675e-47, -2.89941073e-48, -3.36135482e-58],
  [-2.58346513e-58, -3.36135482e-58,  6.39633319e-49]],
 [[-8.24604420e-42, -2.82514925e-43, -1.14566667e-57],
  [-2.82514925e-43, -1.03976382e-42, -8.50921710e-59],
  [-1.14566667e-57, -8.50921710e-59, -1.02871011e-42]],
 [[-1.84283543e-57, -3.08648520e-57,  5.07803185e-46],
  [-3.08648520e-57,  1.83972286e-58, -7.00502040e-47],
  [ 5.07803185e-46, -7.00502040e-47,  3.71048697e-57]],
 [[-1.07484360e-46, -4.76220726e-48,  3.32600412e-57],
  [-4.76220726e-48,  1.97189610e-46, -1.73202643e-57],
  [ 3.32600412e-57, -1.73202643e-57,  1.74748381e-47]]]

fundamental_transition_polarizability_moment = \
[[[ 6.80297965e-48, -1.61310930e-47,  1.45946348e-57],
  [-1.61310930e-47, -4.66115634e-49, -1.89821423e-58],
  [ 1.45946348e-57, -1.89821423e-58,  9.32600150e-48]],
 [[-8.11300065e-42, -2.67098174e-43, -2.21527560e-56],
  [-2.67098174e-43, -1.29954508e-42,  5.14427548e-55],
  [-2.21527560e-56,  5.14427548e-55, -1.28904997e-42]],
 [[-1.17251976e-56, -4.10624473e-57,  3.07492257e-46],
  [-4.10624473e-57,  4.41499306e-57,  8.06354559e-47],
  [ 3.07492257e-46,  8.06354559e-47,  2.92330693e-56]],
 [[ 6.75651238e-47,  2.18945677e-47,  3.27849150e-57],
  [ 2.18945677e-47, -1.86167656e-46, -1.16117625e-56],
  [ 3.27849150e-57, -1.16117625e-56, -5.27392796e-47]]]

overtones_transition_polarizability_moment = \
[[[ 3.82939078e-43,  1.53694980e-44, -4.22738855e-59],
  [ 1.53694980e-44, -9.07564089e-45,  2.89133469e-59],
  [-4.22738855e-59,  2.89133469e-59, -9.67391259e-45]],
 [[ 1.31550401e-43,  4.75095936e-45, -2.70775167e-58],
  [ 4.75095936e-45,  1.03724276e-44,  1.99730842e-60],
  [-2.70775167e-58,  1.99730842e-60,  1.01861373e-44]],
 [[ 1.52452537e-42,  7.31388230e-44, -4.21331319e-55],
  [ 7.31388230e-44, -3.39002915e-43,  1.07187805e-53],
  [-4.21331319e-55,  1.07187805e-53, -3.89423013e-42]],
 [[ 1.51949738e-42,  2.12108751e-43,  2.54451056e-55],
  [ 2.12108751e-43, -3.88693029e-42, -6.47251085e-54],
  [ 2.54451056e-55, -6.47251085e-54, -3.41977453e-43]]]

combotones_transition_polarizability_moment = \
[[[[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00]],
  [[ 2.59006638e-49,  1.79576474e-49,  4.01204307e-59],
   [ 1.79576474e-49,  2.47739029e-49,  8.28184605e-60],
   [ 4.01204307e-59,  8.28184605e-60, -4.14164788e-50]],
  [[-2.00652998e-55,  2.54746447e-54, -8.45646455e-43],
   [ 2.54746447e-54,  1.99586876e-55, -3.30996643e-44],
   [-8.45646455e-43, -3.30996643e-44,  4.22154035e-58]],
  [[-6.62297750e-44,  8.43825962e-43,  1.54186157e-54],
   [ 8.43825962e-43,  6.61605528e-44,  6.00522944e-56],
   [ 1.54186157e-54,  6.00522944e-56, -1.21911831e-47]]],
 [[[ 2.59006638e-49,  1.79576474e-49,  4.01204307e-59],
   [ 1.79576474e-49,  2.47739029e-49,  8.28184605e-60],
   [ 4.01204307e-59,  8.28184605e-60, -4.14164788e-50]],
  [[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00]],
  [[-9.18012937e-58, -1.70984433e-59,  2.94260457e-47],
   [-1.70984433e-59, -1.75087280e-58, -5.17254740e-48],
   [ 2.94260457e-47, -5.17254740e-48,  1.93730029e-59]],
  [[ 6.01634695e-47,  2.77371282e-48, -2.34830823e-59],
   [ 2.77371282e-48,  2.05110122e-47, -1.15509632e-58],
   [-2.34830823e-59, -1.15509632e-58,  9.11863815e-48]]],
 [[[-2.00652998e-55,  2.54746447e-54, -8.45646455e-43],
   [ 2.54746447e-54,  1.99586876e-55, -3.30996643e-44],
   [-8.45646455e-43, -3.30996643e-44,  4.22154035e-58]],
  [[-9.18012937e-58, -1.70984433e-59,  2.94260457e-47],
   [-1.70984433e-59, -1.75087280e-58, -5.17254740e-48],
   [ 2.94260457e-47, -5.17254740e-48,  1.93730029e-59]],
  [[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00]],
  [[ 2.55702919e-54,  7.19116036e-55, -9.83446561e-44],
   [ 7.19116036e-55, -1.57222640e-53,  2.51030196e-42],
   [-9.83446561e-44,  2.51030196e-42,  8.58064266e-54]]],
 [[[-6.62297750e-44,  8.43825962e-43,  1.54186157e-54],
   [ 8.43825962e-43,  6.61605528e-44,  6.00522944e-56],
   [ 1.54186157e-54,  6.00522944e-56, -1.21911831e-47]],
  [[ 6.01634695e-47,  2.77371282e-48, -2.34830823e-59],
   [ 2.77371282e-48,  2.05110122e-47, -1.15509632e-58],
   [-2.34830823e-59, -1.15509632e-58,  9.11863815e-48]],
  [[ 2.55702919e-54,  7.19116036e-55, -9.83446561e-44],
   [ 7.19116036e-55, -1.57222640e-53,  2.51030196e-42],
   [-9.83446561e-44,  2.51030196e-42,  8.58064266e-54]],
  [[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
   [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00]]]]

transition_polarizability_moment = \
        anharmonicProperty(harmonic_transition_polarizability_moment, \
                           fundamental_transition_polarizability_moment, \
                           overtones_transition_polarizability_moment, \
                           combotones_transition_polarizability_moment)


def test_get_rscattering_cross_section():

    exp_denominator = [0.9999999979983836, 0.9999999979252363, 0.9998161124349669, \
                       0.9995345574831861, 0.9992377998978554, 0.5866835980974099]
    SI_incident_wavenumbers = 2194746.0394200613
    au_combined_polarizabilites = [0.14867859, 0.61365425, 0.08134748, \
                                   0.01808905, 0.11121733, 0.05762326]

    ref_intensities = [1.49220758e+24, 6.16921579e+24, 1.34555457e+24,
                       3.10875251e+23, 1.95059450e+24, 2.20386779e+24]

    intensities = get_rscattering_cross_section(exp_denominator, SI_incident_wavenumbers, \
                                                SI_wavenumbers.harmonic, au_combined_polarizabilites)

    assert np.allclose(np.multiply(ref_intensities, 1.0e-23), np.multiply(intensities, 1.0e-23))


def test_get_raman_intensities():

    SI_incident_wavenumbers = 2194746.0394200613

    specifications = ['Raman: CPG 45+4, a.u.']

    # Harmonic
    ref_harmonic_intensities = [1.61462441e-12, 4.20770947e-02, 1.67601953e-11, 1.80243517e-12]
    ref_fundamental_intensities = [0., 0., 0., 0.]
    ref_overtones_intensities = [0., 0., 0., 0.]
    ref_combotones_intensities = [[0., 0., 0., 0.],
                                  [0., 0., 0., 0.],
                                  [0., 0., 0., 0.],
                                  [0., 0., 0., 0.]]

    intensities = get_raman_intensities(specifications, SI_incident_wavenumbers, \
                                        transition_polarizability_moment, \
                                        CO2_wavenumbers, False, 0, temperature)

    assert np.allclose(ref_harmonic_intensities, intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, intensities.fundamental)
    assert np.allclose(ref_overtones_intensities, intensities.overtones)
    assert np.allclose(ref_combotones_intensities, intensities.combotones)

    # Anharmonic
    ref_fundamental_intensities = [4.66123032e-13, 4.33275282e-02, 1.06691111e-11, 3.04301235e-12]
    ref_overtones_intensities = [2.55245633e-04, 1.99188838e-05, 2.65192106e-03, 2.65359582e-03]
    ref_combotones_intensities = [[0.00000000e+00, 2.84466723e-16, 9.16030432e-04, 9.16296799e-04],
                                  [2.84466723e-16, 0.00000000e+00, 7.12783900e-13, 3.26202703e-12],
                                  [9.16030432e-04, 7.12783900e-13, 0.00000000e+00, 1.49842181e-03],
                                  [9.16296799e-04, 3.26202703e-12, 1.49842181e-03, 0.00000000e+00]]

    intensities = get_raman_intensities(specifications, SI_incident_wavenumbers, \
                                        transition_polarizability_moment, \
                                        CO2_wavenumbers, True, 0, temperature)

    assert np.allclose(ref_harmonic_intensities, intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, intensities.fundamental)
    assert np.allclose(ref_overtones_intensities, intensities.overtones)
    assert np.allclose(ref_combotones_intensities, intensities.combotones)

    specifications = ['Raman: CPG 45+7, a.u.']
    ref_harmonic_intensities = [2.79758413e-12, 5.09786254e-02, 2.93303418e-11, 2.92534345e-12]
    ref_fundamental_intensities = [7.23681262e-13, 5.13218462e-02, 1.86709444e-11, 4.35662205e-12]
    ref_overtones_intensities = [3.47624890e-04, 2.49701085e-05, 4.06948273e-03, 4.07205434e-03]
    ref_combotones_intensities = [[0.00000000e+00, 3.70735363e-16, 1.60305326e-03, 1.60351940e-03],
                                  [3.70735363e-16, 0.00000000e+00, 1.24737183e-12, 3.69660012e-12],
                                  [1.60305326e-03, 1.24737183e-12, 0.00000000e+00, 2.62223816e-03],
                                  [1.60351940e-03, 3.69660012e-12, 2.62223816e-03, 0.00000000e+00]]

    intensities = get_raman_intensities(specifications, SI_incident_wavenumbers, \
                                        transition_polarizability_moment, \
                                        CO2_wavenumbers, True, 0, temperature)

    assert np.allclose(ref_harmonic_intensities, intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, intensities.fundamental)
    assert np.allclose(ref_overtones_intensities, intensities.overtones)
    assert np.allclose(ref_combotones_intensities, intensities.combotones)

    specifications = ['Raman: PCPG 45+4, Å^4/amu']
    ref_harmonic_intensities = [2.30800198e-10, 6.01465068e+00, 2.39576237e-09, 2.57646541e-10]
    ref_fundamental_intensities = [6.66292964e-11, 6.19339212e+00, 1.52508097e-09, 4.34979088e-10]
    ref_overtones_intensities = [0.03648573, 0.00284728, 0.3790751,  0.37931449]
    ref_combotones_intensities = [[0.00000000e+00, 4.06626927e-14, 1.30940672e-01, 1.30978748e-01],
                                  [4.06626927e-14, 0.00000000e+00, 1.01887885e-10, 4.66285832e-10],
                                  [1.30940672e-01, 1.01887885e-10, 0.00000000e+00, 2.14189782e-01],
                                  [1.30978748e-01, 4.66285832e-10, 2.14189782e-01, 0.00000000e+00]]

    intensities = get_raman_intensities(specifications, SI_incident_wavenumbers, \
                                        transition_polarizability_moment, \
                                        CO2_wavenumbers, True, 0, temperature)

    assert np.allclose(ref_harmonic_intensities, intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, intensities.fundamental)
    assert np.allclose(ref_overtones_intensities, intensities.overtones)
    assert np.allclose(ref_combotones_intensities, intensities.combotones)

    specifications = ['Raman: PCPG 45+7, Å^4/amu']
    ref_harmonic_intensities = [3.99896700e-10, 7.28706738e+00, 4.19258415e-09, 4.18159075e-10]
    ref_fundamental_intensities = [1.03445593e-10, 7.33612859e+00, 2.66889170e-09, 6.22751166e-10]
    ref_overtones_intensities = [0.04969075, 0.00356932, 0.58170644, 0.58207404]
    ref_combotones_intensities = [[0.00000000e+00, 5.29942413e-14, 2.29146176e-01, 2.29212808e-01],
                                  [5.29942413e-14, 0.00000000e+00, 1.78303798e-10, 5.28405267e-10],
                                  [2.29146176e-01, 1.78303798e-10, 0.00000000e+00, 3.74832119e-01],
                                  [2.29212808e-01, 5.28405267e-10, 3.74832119e-01, 0.00000000e+00]]

    intensities = get_raman_intensities(specifications, SI_incident_wavenumbers, \
                                        transition_polarizability_moment, \
                                        CO2_wavenumbers, True, 0, temperature)

    assert np.allclose(ref_harmonic_intensities, intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, intensities.fundamental)
    assert np.allclose(ref_overtones_intensities, intensities.overtones)
    assert np.allclose(ref_combotones_intensities, intensities.combotones)

    specifications = ['Raman: SCS 45+4, SI units']
    SI_incident_wavenumbers = 2194746.0394200613

    ref_harmonic_intensities = [1.97324659e-67, 1.24708655e-56, 1.32864198e-64, 1.42941164e-65]
    ref_fundamental_intensities = [6.02507054e-68, 1.27625433e-56, 3.73260784e-65, 1.06455281e-65]
    ref_overtones_intensities = [8.41271531e-60, 2.06854112e-60, 2.78209485e-57, 2.78346258e-57]
    ref_combotones_intensities = [[0.00000000e+00, 1.62008604e-71, 1.06632183e-58, 1.06663759e-58],
                                  [1.62008604e-71, 0.00000000e+00, 1.70114589e-67, 7.78516352e-67],
                                  [1.06632183e-58, 1.70114589e-67, 0.00000000e+00, 1.67250206e-57],
                                  [1.06663759e-58, 7.78516352e-67, 1.67250206e-57, 0.00000000e+00]]

    intensities = get_raman_intensities(specifications, SI_incident_wavenumbers, \
                                        transition_polarizability_moment, \
                                        CO2_wavenumbers, True, 0, temperature)

    assert np.allclose(np.multiply(ref_harmonic_intensities, 1.0e57), \
                       np.multiply(intensities.harmonic, 1.0e57))
    assert np.allclose(np.multiply(ref_fundamental_intensities, 1.0e57), \
                       np.multiply(intensities.fundamental, 1.0e57))
    assert np.allclose(np.multiply(ref_overtones_intensities, 1.0e57), \
                       np.multiply(intensities.overtones, 1.0e57))
    assert np.allclose(np.multiply(ref_combotones_intensities, 1.0e57), \
                       np.multiply(intensities.combotones, 1.0e57))

    specifications = ['Raman: SCS 45+7, SI units']
    ref_harmonic_intensities = [3.41895200e-67, 1.51091130e-56, 2.32512347e-64, 2.31992809e-65]
    ref_fundamental_intensities = [9.35424846e-68, 1.51173472e-56, 6.53206372e-65, 1.52409971e-65]
    ref_overtones_intensities = [1.14574702e-59, 2.59310194e-60, 4.26923981e-57, 4.27134034e-57]
    ref_combotones_intensities = [[0.00000000e+00, 2.11140052e-71, 1.86606320e-58, 1.86661577e-58],
                                  [2.11140052e-71, 0.00000000e+00, 2.97700530e-67, 8.82231697e-67],
                                  [1.86606320e-58, 2.97700530e-67, 0.00000000e+00, 2.92687860e-57],
                                  [1.86661577e-58, 8.82231697e-67, 2.92687860e-57, 0.00000000e+00]]

    intensities = get_raman_intensities(specifications, SI_incident_wavenumbers, \
                                        transition_polarizability_moment, \
                                        CO2_wavenumbers, True, 0, temperature)

    assert np.allclose(np.multiply(ref_harmonic_intensities, 1.0e57), \
                       np.multiply(intensities.harmonic, 1.0e57))
    assert np.allclose(np.multiply(ref_fundamental_intensities, 1.0e57), \
                       np.multiply(intensities.fundamental, 1.0e57))
    assert np.allclose(np.multiply(ref_overtones_intensities, 1.0e57), \
                       np.multiply(intensities.overtones, 1.0e57))
    assert np.allclose(np.multiply(ref_combotones_intensities, 1.0e57), \
                       np.multiply(intensities.combotones, 1.0e57))

    # Temperature 400K
    specifications = ['Raman: CPG 45+4, a.u.']
    ref_harmonic_intensities = [1.61462441e-12, 4.20770947e-02, 1.67601953e-11, 1.80243517e-12]
    ref_fundamental_intensities = [4.66123032e-13, 4.33275282e-02, 1.06691111e-11, 3.04301235e-12]
    ref_overtones_intensities = [2.55245633e-04, 1.99188838e-05, 2.65192106e-03, 2.65359582e-03]
    ref_combotones_intensities = [[0.00000000e+00, 2.84466723e-16, 9.16030432e-04, 9.16296799e-04],
                                  [2.84466723e-16, 0.00000000e+00, 7.12783900e-13, 3.26202703e-12],
                                  [9.16030432e-04, 7.12783900e-13, 0.00000000e+00, 1.49842181e-03],
                                  [9.16296799e-04, 3.26202703e-12, 1.49842181e-03, 0.00000000e+00]]

    intensities = get_raman_intensities(specifications, SI_incident_wavenumbers, \
                                        transition_polarizability_moment, \
                                        CO2_wavenumbers, True, 0, 400)

    assert np.allclose(ref_harmonic_intensities, intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, intensities.fundamental)
    assert np.allclose(ref_overtones_intensities, intensities.overtones)
    assert np.allclose(ref_combotones_intensities, intensities.combotones)


def test_get_combined_polarizabilites():

    combination_type = ['45+7']
    ref_cpg = [0.14867859, 0.61365425, 0.08134748, 0.01808905, 0.11121733, 0.05762326]

    cpg = get_combined_polarizabilites(au_polarizability_gradient, combination_type)

    assert np.allclose(ref_cpg, cpg)

    combination_type = ['45+4']
    ref_cpg = [0.08495928, 0.49572025, 0.04674918, 0.0103366,  0.08624968, 0.03293001]

    cpg = get_combined_polarizabilites(au_polarizability_gradient, combination_type)

    assert np.allclose(ref_cpg, cpg)


def test_raman_scattering_cross_section():

    raman_type = ['45+7']

    CO2_harmonic_wavenumbers = [308803.62879803, 169409.60714536,  15856.18156937,  15852.54619014]
    CO2_fundamental_wavenumbers = \
        [298437.35928427, 170192.2063791,   26246.64170339,  26247.44867762]
    CO2_overtones_wavenumbers = [594112.21291436, 339972.06592672,  61950.8418014,   61957.63980011]
    CO2_combotones_wavenumbers = \
        [[     0.        , 466883.50538247, 317954.17644414, 317953.1650671 ],
         [466883.50538247,      0.        , 198506.6568093 , 198507.79874123],
         [317954.17644414, 198506.6568093 ,      0.        ,  59021.90967648],
         [317953.1650671,  198507.79874123,  59021.90967648,      0.        ]]

    SI_incident_wavenumbers = 2194746.0394200613

    ref_harmonic_intensities = [3.41895200e-67, 1.51091130e-56, 2.32512347e-64, 2.31992809e-65]
    ref_fundamental_intensities = [9.35424846e-68, 1.51173472e-56, 6.53206372e-65, 1.52409971e-65]
    ref_overtones_intensities = [1.14574702e-59, 2.59310194e-60, 4.26923981e-57, 4.27134034e-57]
    ref_combotones_intensities = [[           0.0, 2.11140052e-71, 1.86606320e-58, 1.86661577e-58],
                                  [2.11140052e-71,            0.0, 2.97700530e-67, 8.82231697e-67],
                                  [1.86606320e-58, 2.97700530e-67,            0.0, 2.92687860e-57],
                                  [1.86661577e-58, 8.82231697e-67, 2.92687860e-57,            0.0]]

    intensities = raman_scattering_cross_section(transition_polarizability_moment, \
                                                 SI_incident_wavenumbers, \
                                                 CO2_wavenumbers, raman_type, 0, temperature)

    assert np.allclose(np.multiply(ref_harmonic_intensities, 1.0e57), \
                       np.multiply(intensities.harmonic, 1.0e57))
    assert np.allclose(np.multiply(ref_fundamental_intensities, 1.0e57), \
                       np.multiply(intensities.fundamental, 1.0e57))
    assert np.allclose(np.multiply(ref_overtones_intensities, 1.0e57), \
                       np.multiply(intensities.overtones, 1.0e57))
    assert np.allclose(np.multiply(ref_combotones_intensities, 1.0e57), \
                       np.multiply(intensities.combotones, 1.0e57))

    raman_type = ['45+4']

    ref_harmonic_intensities = [1.97324659e-67, 1.24708655e-56, 1.32864198e-64, 1.42941164e-65]
    ref_fundamental_intensities = [6.02507054e-68, 1.27625433e-56, 3.73260784e-65, 1.06455281e-65]
    ref_overtones_intensities = [8.41271531e-60, 2.06854112e-60, 2.78209485e-57, 2.78346258e-57]
    ref_combotones_intensities = [[0.00000000e+00, 1.62008604e-71, 1.06632183e-58, 1.06663759e-58],
                                  [1.62008604e-71, 0.00000000e+00, 1.70114589e-67, 7.78516352e-67],
                                  [1.06632183e-58, 1.70114589e-67, 0.00000000e+00, 1.67250206e-57],
                                  [1.06663759e-58, 7.78516352e-67, 1.67250206e-57, 0.00000000e+00]]

    intensities = raman_scattering_cross_section(transition_polarizability_moment, \
                                                 SI_incident_wavenumbers, \
                                                 CO2_wavenumbers, raman_type, 0, temperature)

    assert np.allclose(np.multiply(ref_harmonic_intensities, 1.0e57), \
                       np.multiply(intensities.harmonic, 1.0e57))
    assert np.allclose(np.multiply(ref_fundamental_intensities, 1.0e57), \
                       np.multiply(intensities.fundamental, 1.0e57))
    assert np.allclose(np.multiply(ref_overtones_intensities, 1.0e57), \
                       np.multiply(intensities.overtones, 1.0e57))
    assert np.allclose(np.multiply(ref_combotones_intensities, 1.0e57), \
                       np.multiply(intensities.combotones, 1.0e57))

def test_get_exp_denominator():

    ref_exp_denominator = [0.9999999979983836, 0.9999999979252363, 0.9998161124349669, \
                           0.9995345574831861, 0.9992377998978554, 0.5866835980974099]

    exp_denominator = get_exp_denominator(harmonic_wavenumbers, temperature)

    assert np.allclose(ref_exp_denominator, exp_denominator)

    exp_denominator = get_exp_denominator(harmonic_wavenumbers, 0)

    assert np.allclose(np.ones(6), exp_denominator)


def test_get_b2_term():

    ref_b2 = [0.021239769179061247, 0.03931133318988317, 0.011532766376159364, 
              0.0025841499253242495, 0.00832255012728591, 0.008231082946554976]

    b2 = get_b2_term(au_polarizability_gradient)

    assert np.allclose(ref_b2, b2)


def test_get_a2_term():

    ref_a2 = [4.517730381024186e-09, 0.00752166488775672, 1.3735844316100002e-05, \
              2.785782425059312e-14, 0.0011768774195191735, 1.2617098748687706e-07]

    a2 = get_a2_term(au_polarizability_gradient)

    assert np.allclose(ref_a2, a2)


def test_requested_unit_incident_mode():

    specifications = ['Vib modes: 1/m']
    ref_incident_mode = 2194746.0394200613

    incident_mode = requested_unit_incident_mode(specifications, au_input_frequency)

    assert ref_incident_mode == incident_mode

    specifications = ['Vib modes: 1/cm']
    ref_incident_mode = 21947.460394200614

    incident_mode = requested_unit_incident_mode(specifications, au_input_frequency)

    assert ref_incident_mode == incident_mode

    specifications = ['Vib modes: 1/s']
    ref_incident_mode = 657968309843505.0

    incident_mode = requested_unit_incident_mode(specifications, au_input_frequency)

    specifications = ['Vib modes: Eh']

    incident_mode = requested_unit_incident_mode(specifications, au_input_frequency)

    assert au_input_frequency == incident_mode
