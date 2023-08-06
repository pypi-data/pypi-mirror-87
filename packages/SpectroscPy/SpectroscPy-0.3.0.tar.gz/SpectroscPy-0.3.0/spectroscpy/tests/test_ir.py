# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

from spectroscpy import qi_prefactor2, square_then_sum, get_ir_intensities, anharmonicProperty, \
                        get_harmonic_transition_moment
import numpy as np

dipole_gradient = [[-3.55354963e-03, -2.04896147e-03,  4.65337189e-04], \
                   [-1.33397762e-03,  2.30954121e-03, -1.03887613e-06], \
                   [ 5.38119485e-04, -9.34229818e-04,  5.72704375e-07], \
                   [ 2.05564469e-04,  1.21485607e-04,  5.08962422e-03], \
                   [ 4.87101901e-05, -8.45631492e-05,  7.73625610e-08], \
                   [ 4.34177615e-03, -7.53776354e-03,  4.54332159e-06]]

au_input_frequency = 0.1

au_vibrational_energies = [0.018901854754709915, 0.018867982944327566, 0.008117022651510061, \
                           0.007240633346545635, 0.006775176360266165, 0.0008338070305617636]

temperature = 298

wavenumbers = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, 148697.90566093,  \
               18299.94565116]

def test_square_then_sum():

    ref_intensities = [1.7042496777884122e-05, 7.113477970612742e-06, 1.1623582609672795e-06, \
                       2.596129020443402e-05, 9.523614807165442e-09, 7.566891996343323e-05]

    intensities = square_then_sum(dipole_gradient)

    assert np.allclose(ref_intensities, intensities)


def test_get_harmonic_transition_moment():

    dipole_gradient = [[-3.55354963e-03, -2.04896147e-03,  4.65337189e-04], \
                   [-1.33397762e-03,  2.30954121e-03, -1.03887613e-06], \
                   [ 5.38119485e-04, -9.34229818e-04,  5.72704375e-07], \
                   [ 2.05564469e-04,  1.21485607e-04,  5.08962422e-03], \
                   [ 4.87101901e-05, -8.45631492e-05,  7.73625610e-08], \
                   [ 4.34177615e-03, -7.53776354e-03,  4.54332159e-06]]

    qi2 = [6.74771801518888e-50, 6.759831521216551e-50, 1.5713198216234565e-49, \
           1.761508693292537e-49, 1.882524956794339e-49, 1.5296631135732734e-48]
    ref_transition = [[-9.23083202e-28, -5.32245814e-28,  1.20877710e-28],
                      [-3.46829859e-28,  6.00473232e-28, -2.70104428e-31],
                      [ 2.13309900e-28, -3.70327548e-28,  2.27019308e-31],
                      [ 8.62760883e-29,  5.09879115e-29,  2.13613214e-27],
                      [ 2.11344133e-29, -3.66903217e-29,  3.35661251e-32],
                      [ 5.36988921e-27, -9.32267204e-27,  5.61915971e-30]]

    transition = get_harmonic_transition_moment(dipole_gradient, qi2)

    assert np.allclose(ref_transition, transition)


def test_qi_prefactor2():

    ref_qi2 = [6.74771801518888e-50, 6.759831521216551e-50, 1.5713198216234565e-49, \
               1.761508693292537e-49, 1.882524956794339e-49, 1.5296631135732734e-48]

    qi2 = qi_prefactor2(wavenumbers)

    assert np.allclose(ref_qi2, qi2)


def test_get_ir_intensities():

    specifications = ['IR: SSDG, a.u.']
    print_level = 0

    ref_harmonic_intensities = [1.70424968e-05, 7.11347797e-06, 1.16235826e-06, \
                                2.59612902e-05, 9.52361481e-09, 7.56689200e-05]
    ref_fundamental_intensities = np.zeros(len(ref_harmonic_intensities))
    ref_overtone_intensities = np.zeros(len(ref_harmonic_intensities))
    ref_combotone_intensities = np.zeros(len(ref_harmonic_intensities))

    harmonic_transition_moment = [[-1.54955410e-31, -8.93466247e-32,  2.02914051e-32], \
                         [-5.82213640e-32,  1.00799772e-31, -4.53416792e-35], \
                         [ 3.58077398e-32, -6.21658556e-32,  3.81090999e-35], \
                         [ 1.44829270e-32,  8.55919892e-33,  3.58586562e-31], \
                         [ 3.54777519e-33, -6.15910227e-33,  5.63465208e-36], \
                         [ 9.01428369e-31, -1.56497103e-30,  9.43272714e-34]]

    transition_moment = anharmonicProperty(harmonic_transition_moment, \
                                           np.zeros(np.shape(harmonic_transition_moment)), \
                                           np.zeros(np.shape(harmonic_transition_moment)), \
                                           np.zeros(np.shape(harmonic_transition_moment)))

    harmonic_wavenumbers = [414847.6830235662, 414104.2828525629, 178148.02217701354, 158913.5038025385, \
                       148697.90566093015, 18299.94565115991]

    wavenumbers = anharmonicProperty(harmonic_wavenumbers, [], [], [])
    
    
    qi2 = [6.74771801518888e-50, 6.759831521216551e-50, 1.5713198216234565e-49, \
           1.761508693292537e-49, 1.882524956794339e-49, 1.5296631135732734e-48]

    ir_intensities, current_unit, header_format_string, format_string = \
        get_ir_intensities(specifications, transition_moment, wavenumbers, False, \
                           print_level)

    assert np.allclose(ref_harmonic_intensities, ir_intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, ir_intensities.fundamental)
    assert np.allclose(ref_overtone_intensities, ir_intensities.overtones)
    assert np.allclose(ref_combotone_intensities, ir_intensities.combotones)
    assert 'SSDG, a.u.' == current_unit
    assert '%4s %15s %15s' == header_format_string
    assert '%2d %17.6f %22.17f' == format_string

    specifications = ['IR: SSDG, C**2/kg']

    ref_harmonic_intensities = [4.80247389e-13, 2.00453564e-13, 3.27545622e-14, \
                                7.31573666e-13, 2.68369782e-16, 2.13230501e-12]

    ir_intensities, current_unit, header_format_string, format_string = \
        get_ir_intensities(specifications, transition_moment, wavenumbers, False, \
                           print_level)

    assert np.allclose(ref_harmonic_intensities, ir_intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, ir_intensities.fundamental)
    assert np.allclose(ref_overtone_intensities, ir_intensities.overtones)
    assert np.allclose(ref_combotone_intensities, ir_intensities.combotones)
    assert 'SSDG, C**2/kg' == current_unit
    assert '%4s %15s %16s' == header_format_string
    assert '%2d %17.6f %25.20f' == format_string

    specifications = ['IR: SSDG, D2A2/amu']

    ref_harmonic_intensities = [7.16729878e-01, 2.99160520e-01, 4.88835002e-02, \
                                1.09181375e+00, 4.00519910e-04, 3.18229051e+00]


    ir_intensities, current_unit, header_format_string, format_string = \
        get_ir_intensities(specifications, transition_moment, wavenumbers, False, \
                           print_level)

    assert np.allclose(ref_harmonic_intensities, ir_intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, ir_intensities.fundamental)
    assert np.allclose(ref_overtone_intensities, ir_intensities.overtones)
    assert np.allclose(ref_combotone_intensities, ir_intensities.combotones)
    assert '(D/Å)**2/amu' == current_unit
    assert '%4s %15s %14s' == header_format_string
    assert '%2d %17.6f %15.10f' == format_string

    specifications = ['IR: MDAC, m**2/(s*mol)']

    ref_harmonic_intensities = [2.47758986e+13, 1.03413726e+13, 1.68980349e+12, \
                                3.77417877e+13, 1.38451612e+10, 1.10005331e+14]

    ir_intensities, current_unit, header_format_string, format_string = \
        get_ir_intensities(specifications, transition_moment, wavenumbers, False, \
                           print_level)

    assert np.allclose(ref_harmonic_intensities, ir_intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, ir_intensities.fundamental)
    assert np.allclose(ref_overtone_intensities, ir_intensities.overtones)
    assert np.allclose(ref_combotone_intensities, ir_intensities.combotones)
    assert 'MDAC, m**2/(s*mol)' == current_unit
    assert '%4s %15s %14s' == header_format_string
    assert '%2d %17.6f %20.1f' == format_string

    specifications = ['IR: MDAC, L/(cm*s*mol)']

    ref_harmonic_intensities = [2.47758986e+14, 1.03413726e+14, 1.68980349e+13, \
                                3.77417877e+14, 1.38451612e+11, 1.10005331e+15]

    ir_intensities, current_unit, header_format_string, format_string = \
        get_ir_intensities(specifications, transition_moment, wavenumbers, False, \
                           print_level)

    assert np.allclose(ref_harmonic_intensities, ir_intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, ir_intensities.fundamental)
    assert np.allclose(ref_overtone_intensities, ir_intensities.overtones)
    assert np.allclose(ref_combotone_intensities, ir_intensities.combotones)
    assert 'MDAC, L/(cm*s*mol)' == current_unit
    assert '%4s %15s %16s' == header_format_string
    assert '%2d %17.6f %20.1f' == format_string

    specifications = ['IR: NIMAC, m/mol']

    ref_harmonic_intensities = [3.02861824e+04, 1.26413456e+04, 2.06562423e+03, \
                                4.61357499e+04, 1.69243943e+01, 1.34471066e+05]

    ir_intensities, current_unit, header_format_string, format_string = \
        get_ir_intensities(specifications, transition_moment, wavenumbers, False, \
                           print_level)

    assert np.allclose(ref_harmonic_intensities, ir_intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, ir_intensities.fundamental)
    assert np.allclose(ref_overtone_intensities, ir_intensities.overtones)
    assert np.allclose(ref_combotone_intensities, ir_intensities.combotones)
    assert 'NIMAC, m/mol' == current_unit
    assert '%4s %15s %16s' == header_format_string
    assert '%2d %17.6f %17.8f' == format_string

    specifications = ['IR: NIMAC, km/mol']

    ref_harmonic_intensities = [3.02861824e+01, 1.26413456e+01, 2.06562423e+00, \
                                4.61357499e+01, 1.69243943e-02, 1.34471066e+02]

    ir_intensities, current_unit, header_format_string, format_string = \
        get_ir_intensities(specifications, transition_moment, wavenumbers, False, \
                           print_level)

    assert np.allclose(ref_harmonic_intensities, ir_intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, ir_intensities.fundamental)
    assert np.allclose(ref_overtone_intensities, ir_intensities.overtones)
    assert np.allclose(ref_combotone_intensities, ir_intensities.combotones)
    assert 'NIMAC, km/mol' == current_unit
    assert '%4s %15s %16s' == header_format_string
    assert '%2d %17.6f %17.10f' == format_string

    # Try an anharmonic for safety
    ref_fundamental_intensities = [ 2.89025391e+01,  4.24532440e+00,  1.05339708e+00, \
                                    5.31547861e+01, 2.62569111e-03, -2.96890570e+03]
    ref_overtone_intensities = [ 1.04930318e-01,  5.18135350e-02,  2.26045531e-01,  \
                                 2.50824983e-02, 2.08331792e-03, -1.48397129e+02]
    ref_combotone_intensities = [[ 2.85435997e-03,  1.87735589e+00,  4.10248449e-01  , \
                                   1.47112129e-02,  3.97494610e-01,  4.25470751e+01], \
                                 [ 1.87735589e+00,  9.25594968e-03,  4.38387667e-03  , \
                                   9.50776260e-01,  6.41299705e-03,  7.98226196e+00], \
                                 [ 4.10248449e-01,  4.38387667e-03,  3.04301666e-06  , \
                                   2.88915248e-01,  7.57227453e-03,  4.58072248e-01],  \
                                 [ 1.47112129e-02,  9.50776260e-01,  2.88915248e-01  , \
                                   2.55419861e-01,  4.37468835e-02,  1.04435729e+01], \
                                 [ 3.97494610e-01,  6.41299705e-03,  7.57227453e-03  , \
                                   4.37468835e-02,  2.49313855e-03,  3.40110436e-02], \
                                 [ 1.32344110e+00,  1.72556837e+01,  7.39284887e-01, \
                                   2.56877423e-01,  1.21650083e-02, -2.92574454e+01]]

    fundamental_transition_moment = [[-1.58248635e-31, -7.89632834e-32,  3.33860303e-32], \
                                     [-4.07030444e-32,  5.47511716e-32,  8.75375758e-34], \
                                     [ 2.55334272e-32, -4.43282917e-32,  3.08927359e-35], \
                                     [ 7.14901564e-33,  4.36237082e-33,  4.04138074e-31], \
                                     [ 1.40343162e-33, -2.43639198e-33,  4.43322384e-36], \
                                     [-3.75078465e-30,  6.51174287e-30, -3.92544663e-33]]
    
    overtone_transition_moment = [[-3.83684224e-33,  6.67476567e-33, -4.02619386e-35], \
                                  [-2.67594361e-33,  4.63197842e-33,  3.33986419e-35], \
                                  [-8.46622294e-33,  1.46975978e-32, -8.84977244e-36], \
                                  [-3.14670148e-33,  5.46284380e-33, -3.47923886e-36], \
                                  [ 8.85586169e-34, -1.53738785e-33,  1.04613873e-36], \
                                  [-4.39611811e-31,  7.63209403e-31, -4.59852000e-34]]

    combotone_transition_moment = [[[-6.44391918e-34,  1.09009267e-33, -4.90308479e-35], \
                                    [ 7.95983142e-33,  4.60680592e-33,  3.11589667e-32], \
                                    [-6.63248836e-34, -3.72943761e-34,  1.78367293e-32], \
                                    [ 1.72756273e-33, -3.00702088e-33, -1.92948673e-35], \
                                    [-1.98611771e-33, -1.15274897e-33, -1.78767959e-32], \
                                    [-1.41998853e-31,  1.78356620e-31,  2.06236671e-32]], \
                                   [[ 7.95983142e-33,  4.60680592e-33,  3.11589667e-32], \
                                    [ 1.13852711e-33, -1.94799768e-33,  4.95289137e-35], \
                                    [-9.13886539e-34,  1.58544217e-33,  1.29461419e-35], \
                                    [ 4.36267456e-33,  2.52625604e-33,  2.72154868e-32], \
                                    [ 1.13196448e-33, -1.96876927e-33, -1.25605110e-35], \
                                    [-4.82759371e-32,  8.26077856e-32,  3.11405740e-35]], \
                                   [[-6.63248836e-34, -3.72943761e-34,  1.78367293e-32], \
                                    [-9.13886539e-34,  1.58544217e-33,  1.29461419e-35], \
                                    [-3.08181904e-35,  5.36292228e-35, -1.64806366e-38], \
                                    [ 1.66236770e-32,  9.57809116e-33,  4.73402610e-33], \
                                    [ 1.60524224e-33, -2.78667459e-33,  1.69934422e-36], \
                                    [-1.70058141e-32,  2.95238724e-32, -1.75383350e-35]], \
                                   [[ 1.72756273e-33, -3.00702088e-33, -1.92948673e-35], \
                                    [ 4.36267456e-33,  2.52625604e-33,  2.72154868e-32], \
                                    [ 1.66236770e-32,  9.57809116e-33,  4.73402610e-33], \
                                    [ 9.96437480e-33, -1.72994541e-32,  1.02948532e-35], \
                                    [-3.72755175e-34, -2.09895312e-34,  8.14589290e-33], \
                                    [-1.05882170e-31,  1.84629737e-31,  3.36791074e-32]], \
                                   [[-1.98611771e-33, -1.15274897e-33, -1.78767959e-32], \
                                    [ 1.13196448e-33, -1.96876927e-33, -1.25605110e-35], \
                                    [ 1.60524224e-33, -2.78667459e-33,  1.69934422e-36], \
                                    [-3.72755175e-34, -2.09895312e-34,  8.14589290e-33], \
                                    [ 9.67869679e-34, -1.68029055e-33,  1.11893306e-36], \
                                    [ 5.47570469e-33, -9.50640945e-33,  6.00935286e-36]], \
                                   [[-3.00393945e-32, -1.71642448e-32,  2.08073555e-32], \
                                    [ 7.01920639e-32, -1.21914251e-31,  8.96674443e-35], \
                                    [-2.16040776e-32,  3.75070104e-32, -2.24294398e-35], \
                                    [ 3.40462398e-34,  2.16450680e-34,  3.37927062e-32], \
                                    [ 3.27478318e-33, -5.68543853e-33,  3.57389383e-36], \
                                    [ 2.21752746e-31, -3.84987642e-31,  2.32446226e-34]]]

    transition_moment = anharmonicProperty(harmonic_transition_moment, \
                                           fundamental_transition_moment, \
                                           overtone_transition_moment, \
                                           combotone_transition_moment)

    fundamental_wn = [396057.43586589, 404798.68025287, 178674.28173888, 144398.42376189, \
                    147425.41271963, -23336.48757966]
    overtones_wn = [785763.7904302,  803683.37589429, 348760.7362605,  280130.8044133, \
                     293772.40096096, -84912.43065987]
    combotones_wn = [[788939.33108099, 789532.03985542, 571337.7795644,  542945.85920111, \
                       543137.76510721, 360415.71484211], \
                      [789532.03985542, 806640.36820002, 581047.24654331, 550884.16599507, \
                       551929.17084098, 387036.60853707], \
                      [571337.7795644,  581047.24654331, 353054.64986912, 328411.46648376, \
                       324992.05211235, 175154.50294195], \
                      [542945.85920111, 550884.16599507, 328411.46648376, 284463.82596854, \
                       291836.56645761,  99835.30939149], \
                      [543137.76510721, 551929.17084098, 324992.05211235, 291836.56645761, \
                       294311.61320011, 125435.70604639], \
                      [360415.71484211, 387036.60853707, 175154.50294195,  99835.30939149, \
                       125435.70604639, -65792.70290959]]
    wavenumbers = anharmonicProperty(harmonic_wavenumbers, fundamental_wn, overtones_wn, combotones_wn)

    ir_intensities, current_unit, header_format_string, format_string = \
        get_ir_intensities(specifications, transition_moment, wavenumbers, True, \
                           print_level)

    assert np.allclose(ref_harmonic_intensities, ir_intensities.harmonic)
    assert np.allclose(ref_fundamental_intensities, ir_intensities.fundamental)
    assert np.allclose(ref_overtone_intensities, ir_intensities.overtones)
    assert np.allclose(ref_combotone_intensities, ir_intensities.combotones)
    assert 'NIMAC, km/mol' == current_unit
    assert '%4s %15s %16s' == header_format_string
    assert '%2d %17.6f %17.10f' == format_string
