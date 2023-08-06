# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

import numpy as np
from .parameters import*
from math import sqrt, pi
from .raman import get_exp_denominator
from .anharmonic import anharmonicProperty

# Independent of units
def get_average_beta_aaa2(beta_grad):

    beta_aaa2 = np.zeros((len(beta_grad)))

    for i in range(len(beta_grad)):
        tmp = 0
        for a in range(3):
            tmp = tmp + beta_grad[i][a][a][a]**2

        beta_aaa2[i] = beta_aaa2[i] + (1/7)*tmp

        tmp = 0
        for a in range(3):
            for b in range(3):
                if (b != a):
                    beta_aaa = beta_grad[i][a][a][a]
                    beta_aab = beta_grad[i][a][a][b]
                    beta_abb = beta_grad[i][a][b][b]
                    beta_baa = beta_grad[i][b][a][a]
                    beta_bba = beta_grad[i][b][b][a]

                    tmp = tmp + 4*beta_aab**2 + 2*beta_aaa*beta_abb + 4*beta_baa*beta_aab + \
                                4*beta_aaa*beta_bba + beta_baa**2

        beta_aaa2[i] = beta_aaa2[i] + (1/35)*tmp

        tmp = 0
        for a in range(3):
            for b in range(3):
                if (b != a):
                    for g in range(3):
                        if ((g != b) and (g != a)):
                            beta_aab = beta_grad[i][a][a][b]
                            beta_abb = beta_grad[i][a][b][b]
                            beta_abg = beta_grad[i][a][b][g]
                            beta_baa = beta_grad[i][b][a][a]
                            beta_bag = beta_grad[i][b][a][g]
                            beta_bgg = beta_grad[i][b][g][g]
                            beta_ggb = beta_grad[i][g][g][b]

                            tmp = tmp + 4*beta_aab*beta_bgg + beta_baa*beta_bgg + \
                                        4*beta_aab*beta_ggb + 2*beta_abg**2 + 4*beta_abg*beta_bag

        beta_aaa2[i] = beta_aaa2[i] + (1/105)*tmp

    return beta_aaa2


# Independent of units
def get_average_beta_baa2(beta_grad):

    beta_baa2 = np.zeros((len(beta_grad)))

    for i in range(len(beta_grad)):
        tmp = 0
        for a in range(3):
            tmp = tmp + beta_grad[i][a][a][a]**2

        beta_baa2[i] = beta_baa2[i] + (1/35)*tmp

        tmp = 0
        for a in range(3):
            for b in range(3):
                if (b != a):
                    beta_aaa = beta_grad[i][a][a][a]
                    beta_aab = beta_grad[i][a][a][b]
                    beta_abb = beta_grad[i][a][b][b]
                    beta_baa = beta_grad[i][b][a][a]
                    beta_bba = beta_grad[i][b][b][a]

                    tmp = tmp + 4*beta_aaa*beta_abb + 8*beta_aab**2 - 6*beta_aaa*beta_bba + \
                                9*beta_abb**2 - 6*beta_aab*beta_baa

        beta_baa2[i] = beta_baa2[i] + (1/105)*tmp

        tmp = 0
        for a in range(3):
            for b in range(3):
                if (b != a):
                    for g in range(3):
                        if ((g != b) and (g != a)):
                            beta_aab = beta_grad[i][a][a][b]
                            beta_aag = beta_grad[i][a][a][g]
                            beta_abb = beta_grad[i][a][b][b]
                            beta_abg = beta_grad[i][a][b][g]
                            beta_agg = beta_grad[i][a][g][g]
                            beta_bag = beta_grad[i][b][a][g]
                            beta_bbg = beta_grad[i][b][b][g]
                            beta_bgg = beta_grad[i][b][g][g]

                            tmp = tmp + 3*beta_abb*beta_agg - 2*beta_aag*beta_bbg - \
                                        2*beta_aab*beta_bgg + 6*beta_abg**2 - 2*beta_abg*beta_bag

        beta_baa2[i] = beta_baa2[i] + (1/105)*tmp

    return beta_baa2


# Scattering cross section.  SI I/O
def get_hyperraman_SI_scs(incident_wn, wavenumbers, beta2, T):

    num_modes = len(beta2)
    sigma = np.zeros(num_modes)

    exp_denom = get_exp_denominator(wavenumbers, T)

    for i in range(num_modes):
        if (wavenumbers[i] == 0.0 or wavenumbers[i].imag != 0):
            sigma[i] = 0.0
            exp_denom[i] = 1.0
        else:
            sigma[i] = (2*incident_wn - wavenumbers[i])**4*beta2[i]

    sigma = np.divide(sigma, exp_denom)
    sigma = np.multiply(sigma, 16*pi**4*speed_of_light**4)

    return sigma


# SI I/O
def get_hyperraman_intensities(specifications, incident_wavenumber, wavenumbers, \
                               beta_transition_moment, T, anharmonic, print_level):

    num_modes = len(wavenumbers.harmonic)

    harmonic_beta_aaa2 = get_average_beta_aaa2(beta_transition_moment.harmonic)
    harmonic_beta_baa2 = get_average_beta_baa2(beta_transition_moment.harmonic)

    if (anharmonic):
        fundamental_beta_aaa2 = get_average_beta_aaa2(beta_transition_moment.fundamental)
        fundamental_beta_baa2 = get_average_beta_baa2(beta_transition_moment.fundamental)
        overtones_beta_aaa2 = get_average_beta_aaa2(beta_transition_moment.overtones)
        overtones_beta_baa2 = get_average_beta_baa2(beta_transition_moment.overtones)

        combotones_beta_aaa2 = np.zeros((num_modes, num_modes))
        combotones_beta_baa2 = np.zeros((num_modes, num_modes))

        for i in range(num_modes):
            combotones_beta_aaa2[i] = get_average_beta_aaa2(beta_transition_moment.combotones[i])
            combotones_beta_baa2[i] = get_average_beta_baa2(beta_transition_moment.combotones[i])

    harmonic_sigma_vv = get_hyperraman_SI_scs(incident_wavenumber, wavenumbers.harmonic, \
                                              harmonic_beta_aaa2, T)
    harmonic_sigma_hv = get_hyperraman_SI_scs(incident_wavenumber, wavenumbers.harmonic, \
                                              harmonic_beta_baa2, T)

    if (anharmonic):
        fundamental_sigma_vv = get_hyperraman_SI_scs(incident_wavenumber, wavenumbers.fundamental, \
                                                     fundamental_beta_aaa2, T)
        fundamental_sigma_hv = get_hyperraman_SI_scs(incident_wavenumber, wavenumbers.fundamental, \
                                                     fundamental_beta_baa2, T)
        overtones_sigma_vv = get_hyperraman_SI_scs(incident_wavenumber, wavenumbers.overtones, \
                                                   overtones_beta_aaa2, T)
        overtones_sigma_hv = get_hyperraman_SI_scs(incident_wavenumber, wavenumbers.overtones, \
                                                   overtones_beta_baa2, T)

        combotones_sigma_vv = np.zeros((num_modes, num_modes))
        combotones_sigma_hv = np.zeros((num_modes, num_modes))

        for i in range(num_modes):
            combotones_sigma_vv[i] = \
                get_hyperraman_SI_scs(incident_wavenumber, wavenumbers.combotones[i], \
                                      combotones_beta_aaa2[i], T)
            combotones_sigma_hv[i] = \
                get_hyperraman_SI_scs(incident_wavenumber, wavenumbers.combotones[i], \
                                      combotones_beta_baa2[i], T)

    else:
        fundamental_sigma_vv = np.zeros((num_modes))
        fundamental_sigma_hv = np.zeros((num_modes))
        overtones_sigma_vv = np.zeros((num_modes))
        overtones_sigma_hv = np.zeros((num_modes))
        combotones_sigma_vv = np.zeros((num_modes, num_modes))
        combotones_sigma_hv = np.zeros((num_modes, num_modes))

    sigma_vv = anharmonicProperty(harmonic_sigma_vv, fundamental_sigma_vv, \
                                  overtones_sigma_vv, combotones_sigma_vv)
    sigma_hv = anharmonicProperty(harmonic_sigma_hv, fundamental_sigma_hv, \
                                  overtones_sigma_hv, combotones_sigma_hv)

    harmonic_relative_vv = np.divide(sigma_vv.harmonic, sum(sigma_vv.harmonic))
    harmonic_relative_hv = np.divide(sigma_hv.harmonic, sum(sigma_hv.harmonic))

    if (anharmonic):
        fundamental_relative_vv = np.divide(sigma_vv.fundamental, sum(sigma_vv.fundamental))
        fundamental_relative_hv = np.divide(sigma_hv.fundamental, sum(sigma_hv.fundamental))
        overtones_relative_vv = np.divide(sigma_vv.overtones, sum(sigma_vv.overtones))
        overtones_relative_hv = np.divide(sigma_hv.overtones, sum(sigma_hv.overtones))

        # I am uncertain whether this scaling is too severe for the combotones.  Should it for instance 
        # only be per row?
        combotones_relative_vv = np.divide(sigma_vv.combotones, sum(sigma_vv.combotones))
        combotones_relative_hv = np.divide(sigma_hv.combotones, sum(sigma_hv.combotones))

    else:
        fundamental_relative_vv = np.zeros((num_modes))
        fundamental_relative_hv = np.zeros((num_modes))
        overtones_relative_vv = np.zeros((num_modes))
        overtones_relative_hv = np.zeros((num_modes))
        combotones_relative_vv = np.zeros((num_modes, num_modes))
        combotones_relative_hv = np.zeros((num_modes, num_modes))

    relative_vv = anharmonicProperty(harmonic_relative_vv, fundamental_relative_vv, \
                                     overtones_relative_vv, combotones_relative_vv)
    relative_hv = anharmonicProperty(harmonic_relative_hv, fundamental_relative_hv, \
                                     overtones_relative_hv, combotones_relative_hv)

    if (print_level > 2):
        print('\n')
        print('Hyper-Raman VV')
        print('%4s %14s %18s' %('Mode', 'SI complete', 'Relative'))
        for i in range(num_modes):
            print('%2d %20.10E %16.10f' %(i, sigma_vv.harmonic[i], relative_vv.harmonic[i]))

        print('\n')
        print('Hyper-Raman HV')
        print('%4s %14s %18s' %('Mode', 'SI complete', 'Relative'))
        for i in range(num_modes):
            print('%2d %20.10E %16.10f' %(i, sigma_hv.harmonic[i], relative_hv.harmonic[i]))

    if ('Hyper-Raman: SI complete' in specifications):
        sigma_vv = sigma_vv
        sigma_hv = sigma_hv
    elif ('Hyper-Raman: Relative' in specifications):
        sigma_vv = relative_vv
        sigma_hv = relative_hv
    else:
        print('\n')
        print('You forgot to specify the hyper-Raman units in specifications')
        exit()

    return sigma_vv, sigma_hv
