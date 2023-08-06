# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

from .parameters import*
import numpy as np
from math import exp
from sys import exit
from .ir import qi_prefactor2, get_harmonic_transition_moment
from .anharmonic import anharmonicProperty

# SI units
def get_exp_denominator(wavenumbers, temperature):

    exp_denominator = np.zeros((len(wavenumbers)))

    if (temperature == 0):
        for i in range(len(exp_denominator)):
            exp_denominator[i] = 1
    else:
        factor = np.multiply(wavenumbers, (-plancs_constant*speed_of_light/ \
                                           (boltzmann_constant_SI*temperature)))

        for i in range(len(wavenumbers)):
            exp_denominator[i] = 1 - exp(factor[i])

    return exp_denominator


# Unit independent
def get_b2_term(polarizability_gradients):

    b2 = np.zeros((len(polarizability_gradients)))

    for i in range(len(polarizability_gradients)):
        for j in range(3):
            for k in range(3):
                if (k != j):
                    b2[i] = b2[i] + 0.5*(polarizability_gradients[i][j][j] - \
                                         polarizability_gradients[i][k][k])**2 \
                                  + 3.0*(polarizability_gradients[i][j][k])**2

    b2 = 0.5*b2

    return b2


# Unit independent
def get_a2_term(polarizability_gradients):

    a2 = np.zeros((len(polarizability_gradients)))

    for i in range(len(polarizability_gradients)):
        for j in range(3):
            a2[i] = a2[i] + polarizability_gradients[i][j][j]

    a2 = a2/3

    a2 = a2**2

    return a2


# Independent of units
def get_combined_polarizabilites(polarizability_gradients, combination_type):

    a2 = get_a2_term(polarizability_gradients)
    b2 = get_b2_term(polarizability_gradients)

    if ('45+7' in combination_type):
        a_factor = 45.0
        b_factor = 7.0
    elif ('45+4' in combination_type):
        a_factor = 45.0
        b_factor = 4.0
    else:
        print('\n')
        print('Error in get_combined_polarizabilites')
        print('No combination rule specified')
        exit()

    combo = np.zeros((len(polarizability_gradients)))
    for i in range(len(polarizability_gradients)):
        combo[i] = a_factor*a2[i] + b_factor*b2[i]

    return combo


def get_rscattering_cross_section(exp_denominator, incident_wavenumbers, wavenumbers, \
                                  combined_polarizabilities):

    num_modes = len(exp_denominator)
    intensities = np.zeros((num_modes))

    for i in range(num_modes):
        intensities[i] = (incident_wavenumbers - wavenumbers[i])**4*combined_polarizabilities[i]

    intensities = np.divide(intensities, exp_denominator)

    return intensities


# SI I/O
def raman_scattering_cross_section(polarizability_transition_moment, incident_wavenumbers, \
                                   wavenumbers, combination_type, print_level, \
                                   temperature):

    num_modes = len(wavenumbers.harmonic)

    harmonic_qi2 = qi_prefactor2(wavenumbers.harmonic)
    harmonic_a2 = get_a2_term(polarizability_transition_moment.harmonic)
    harmonic_b2 = get_b2_term(polarizability_transition_moment.harmonic)

    fundamental_qi2 = qi_prefactor2(wavenumbers.fundamental)
    fundamental_a2 = get_a2_term(polarizability_transition_moment.fundamental)
    fundamental_b2 = get_b2_term(polarizability_transition_moment.fundamental)

    overtones_qi2 = get_a2_term(polarizability_transition_moment.overtones)
    overtones_a2 = get_a2_term(polarizability_transition_moment.overtones)
    overtones_b2 = get_b2_term(polarizability_transition_moment.overtones)

    combotones_qi2 = np.zeros((num_modes, num_modes))
    combotones_a2 = np.zeros((num_modes, num_modes))
    combotones_b2 = np.zeros((num_modes, num_modes))

    for i in range(num_modes):
        combotones_qi2[i] = qi_prefactor2(wavenumbers.combotones[i])
        combotones_a2[i] = get_a2_term(polarizability_transition_moment.combotones[i])
        combotones_b2[i] = get_b2_term(polarizability_transition_moment.combotones[i])

    qi2 = anharmonicProperty(harmonic_qi2, fundamental_qi2, overtones_qi2, combotones_qi2)
    a2 = anharmonicProperty(harmonic_a2, fundamental_a2, overtones_a2, combotones_a2)
    b2 = anharmonicProperty(harmonic_b2, fundamental_b2, overtones_b2, combotones_b2)

    if ('45+7' in combination_type):
        intensities_caption = 'Intensities 45 + 7'
    elif ('45+4' in combination_type):
        intensities_caption = 'Intensities 45 + 4'
    else:
        print('\n')
        print('Error in raman_scattering_cross_section')
        print('No combination rule specified')
        exit()

    harmonic_combined_polarizabilities = \
        get_combined_polarizabilites(polarizability_transition_moment.harmonic, combination_type)
    fundamental_combined_polarizabilities = \
        get_combined_polarizabilites(polarizability_transition_moment.fundamental, combination_type)
    overtones_combined_polarizabilities = \
        get_combined_polarizabilites(polarizability_transition_moment.overtones, combination_type)

    combotones_combined_polarizabilities = np.zeros((num_modes, num_modes))
    for i in range(num_modes):
        combotones_combined_polarizabilities[i] = \
            get_combined_polarizabilites(polarizability_transition_moment.combotones[i], \
                                         combination_type)

    combined_polarizabilities = anharmonicProperty(harmonic_combined_polarizabilities, \
                                                   fundamental_combined_polarizabilities, \
                                                   overtones_combined_polarizabilities, \
                                                   combotones_combined_polarizabilities)

    harmonic_exp_denominator = get_exp_denominator(wavenumbers.harmonic, temperature)
    fundamental_exp_denominator = get_exp_denominator(wavenumbers.fundamental, temperature)
    overtones_exp_denominator = get_exp_denominator(wavenumbers.overtones, temperature)

    combotones_exp_denominator = np.zeros((num_modes, num_modes))
    for i in range(num_modes):
        combotones_exp_denominator[i] = get_exp_denominator(wavenumbers.combotones[i], temperature)

    exp_denominator = anharmonicProperty(harmonic_exp_denominator, fundamental_exp_denominator, \
                                         overtones_exp_denominator, combotones_exp_denominator)

    intensities = anharmonicProperty(np.zeros((num_modes)), np.zeros((num_modes)), \
                                     np.zeros((num_modes)), np.zeros((num_modes, num_modes)))

    intensities.harmonic = \
        get_rscattering_cross_section(exp_denominator.harmonic, incident_wavenumbers, \
                                      wavenumbers.harmonic, combined_polarizabilities.harmonic)
    intensities.fundamental = \
        get_rscattering_cross_section(exp_denominator.fundamental, incident_wavenumbers, \
                                      wavenumbers.fundamental, combined_polarizabilities.fundamental)
    intensities.overtones = \
        get_rscattering_cross_section(exp_denominator.overtones, incident_wavenumbers, \
                                      wavenumbers.overtones, combined_polarizabilities.overtones)
    for i in range(num_modes):
        intensities.combotones[i] = \
            get_rscattering_cross_section(exp_denominator.combotones[i], incident_wavenumbers, \
                                          wavenumbers.combotones[i], \
                                          combined_polarizabilities.combotones[i])

    # This is only done for practical reasons.
    for i in range(num_modes):
        intensities.combotones[i][i] = 0.0

    if (print_level > 3):
        print('\n')
        print('Raman SI values for input wavenumer ', incident_wavenumbers)
        print('%4s %18s %13s %20s %20s' %('Mode', 'Wavenumbers', 'a**2', 'b**2 ', 'qi**2'))
        for i in range(num_modes):
            print('%2d %20.6f %20.10E %20.10E %20.10E' %(i, wavenumbers.harmonic[i], a2.harmonic[i], \
                                                         b2.harmonic[i], qi2.harmonic[i]))
        print('\n')
        print('%4s %15s %25s' %('Mode', 'Boltzfac', intensities_caption))
        for i in range(num_modes):
            print('%2d %20.10E %20.10E' %(i, exp_denominator.harmonic[i], intensities.harmonic[i]))
        print('\n')

    return intensities


def get_raman_headers(specifications):

    if ('Raman: CPG 45+4, a.u.' in specifications):
        intensities_caption = 'CPG 45+4 a.u.'
        format_string = '%20.11f'
    elif ('Raman: CPG 45+7, a.u.' in specifications):
        intensities_caption = 'CPG 45+7 a.u.'
        format_string = '%20.11f'
    # Default in Dalton
    elif ('Raman: PCPG 45+4, Å^4/amu' in specifications):
        intensities_caption = 'PCPG 45+4 Å^4/amu'
        format_string = '%20.11f'
    elif ('Raman: PCPG 45+7, Å^4/amu' in specifications):
        intensities_caption = 'PCPG 45+7 Å^4/amu'
        format_string = '%20.11f'
    elif ('Raman: SCS 45+4, SI units' in specifications):
        intensities_caption = 'SCS 45+4 SI units'
        format_string = '%20.10E'
    elif ('Raman: SCS 45+7, SI units' in specifications):
        intensities_caption = 'SCS 45+7 SI units'
        format_string = '%20.10E'
    else:
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities ')
        print('You forgot to specify the Raman specifications')
        exit()

    return intensities_caption, format_string


def requested_unit_incident_mode(specifications, au_incident_vibration_energy):

    incident_frequencies = au_incident_vibration_energy*hartree_to_joule/plancs_constant
    incident_recp_m_wn = au_incident_vibration_energy*hartree_to_joule/(plancs_constant*speed_of_light)
    incident_recp_cm_wn = incident_recp_m_wn*1.0e-2

    if ('Vib modes: 1/m' in specifications):
        incident_mode = incident_recp_m_wn
    elif ('Vib modes: 1/cm' in specifications):
        incident_mode = incident_recp_cm_wn
    elif ('Vib modes: 1/s' in specifications):
        incident_mode = incident_frequencies
    elif ('Vib modes: Eh' in specifications):
        incident_mode = au_incident_vibration_energy

    return incident_mode


def get_raman_intensities(specifications, incident_wavenumbers, polarizability_transition_moment, \
                          wavenumbers, anharmonic, print_level, temperature):

    num_modes = len(wavenumbers.harmonic)
    au_incident_vibration_energy = incident_wavenumbers*plancs_constant*speed_of_light/hartree_to_joule
    harmonic_qi2 = qi_prefactor2(wavenumbers.harmonic)
    harmonic_polarizability_gradient = \
        get_harmonic_transition_moment(polarizability_transition_moment.harmonic, \
                                       np.divide(1.0, harmonic_qi2))

    if (anharmonic):
        fundamental_qi2 = qi_prefactor2(wavenumbers.fundamental)
        overtones_qi2 = qi_prefactor2(wavenumbers.overtones)
        combotones_qi2 = np.zeros((num_modes, num_modes))
        for i in range(num_modes):
             combotones_qi2[i] = qi_prefactor2(wavenumbers.combotones[i])

        fundamental_polarizability_gradient = \
            get_harmonic_transition_moment(polarizability_transition_moment.fundamental, \
                                           np.divide(1.0, fundamental_qi2))
        overtones_polarizability_gradient = \
            get_harmonic_transition_moment(polarizability_transition_moment.overtones, \
                                           np.divide(1.0, overtones_qi2))
        combotones_polarizability_gradient = \
            np.zeros(np.shape(polarizability_transition_moment.combotones))

        for i in range(num_modes):
            combotones_polarizability_gradient[i] = \
                get_harmonic_transition_moment(polarizability_transition_moment.combotones[i], \
                                               np.divide(1.0, combotones_qi2[i]))

    else:
        fundamental_qi2 = 1.0
        overtones_qi2 = 1.0
        combotones_qi2 = 1.0

        fundamental_polarizability_gradient = np.zeros((num_modes, 3, 3))
        overtones_polarizability_gradient = np.zeros((num_modes, 3, 3))
        combotones_polarizability_gradient = np.zeros((num_modes, num_modes, 3, 3))

    polarizability_gradient = anharmonicProperty(harmonic_polarizability_gradient, \
                                                 fundamental_polarizability_gradient, \
                                                 overtones_polarizability_gradient, \
                                                 combotones_polarizability_gradient)

    harmonic_combined_polarizabilities_45_4 = \
        get_combined_polarizabilites(polarizability_gradient.harmonic, '45+4')
    fundamental_combined_polarizabilities_45_4 = \
        get_combined_polarizabilites(polarizability_gradient.fundamental, '45+4')
    overtones_combined_polarizabilities_45_4 = \
        get_combined_polarizabilites(polarizability_gradient.overtones, '45+4')

    combotones_combined_polarizabilities_45_4 = np.zeros((num_modes, num_modes))
    for i in range(num_modes):
        combotones_combined_polarizabilities_45_4[i] = \
            get_combined_polarizabilites(polarizability_gradient.combotones[i], '45+4')

    harmonic_combined_polarizabilities_45_7 = \
        get_combined_polarizabilites(polarizability_gradient.harmonic, '45+7')
    fundamental_combined_polarizabilities_45_7 = \
        get_combined_polarizabilites(polarizability_gradient.fundamental, '45+7')
    overtones_combined_polarizabilities_45_7 = \
        get_combined_polarizabilites(polarizability_gradient.overtones, '45+7')

    combotones_combined_polarizabilities_45_7 = np.zeros((num_modes, num_modes))
    for i in range(num_modes):
        combotones_combined_polarizabilities_45_7[i] = \
            get_combined_polarizabilites(polarizability_gradient.combotones[i], '45+7')

    raman_au_cpg_45_4 = \
        anharmonicProperty(harmonic_combined_polarizabilities_45_4, \
                           fundamental_combined_polarizabilities_45_4, \
                           overtones_combined_polarizabilities_45_4, \
                           combotones_combined_polarizabilities_45_4, \
                           conversion_factor=(hartree_to_joule**2*electron_mass/ \
                                              (hartree_to_coulomb**4*bohr_to_meter**2)))

    raman_au_cpg_45_7 = \
        anharmonicProperty(harmonic_combined_polarizabilities_45_7, \
                           fundamental_combined_polarizabilities_45_7, \
                           overtones_combined_polarizabilities_45_7, \
                           combotones_combined_polarizabilities_45_7, \
                           conversion_factor=(hartree_to_joule**2*electron_mass/ \
                                              (hartree_to_coulomb**4*bohr_to_meter**2)))

    if (print_level > 2):
        print('\n')
        print('CPG: Combined polarizability gradients a.u., input energy. ', \
              au_incident_vibration_energy)
        print('%4s %14s %28s' %('Mode', '45+4', '45+7'))
        for j in range(num_modes):
            print('%2d %27.22f %27.22f' %(j, raman_au_cpg_45_4.harmonic[j], \
                                          raman_au_cpg_45_7.harmonic[j]))

    # PCPG: Pseudo combined polarizability gradients
    # Units: Å**4/amu
    raman_A4amu_pcpg_45_4 = \
        anharmonicProperty(raman_au_cpg_45_4.harmonic, \
                           raman_au_cpg_45_4.fundamental, \
                           raman_au_cpg_45_4.overtones, \
                           raman_au_cpg_45_4.combotones, \
                           conversion_factor=((bohr_to_meter*10**(10))**4* \
                                              one_twelfth_carbon/electron_mass))

    raman_A4amu_pcpg_45_7 = \
        anharmonicProperty(raman_au_cpg_45_7.harmonic, \
                           raman_au_cpg_45_7.fundamental, \
                           raman_au_cpg_45_7.overtones, \
                           raman_au_cpg_45_7.combotones, \
                           conversion_factor=((bohr_to_meter*10**(10))**4* \
                                               one_twelfth_carbon/electron_mass))

    if (print_level > 2):
        print('\n')
        print('Dalton-units.  They do not quite make sense, so use only for comparison.')
        print('PCPG: Pseudo combined polarizability gradients Å^4/amu, input energy. ', \
                au_incident_vibration_energy)
        print('%4s %14s %28s' %('Mode', '45+4', '45+7'))
        for j in range(num_modes):
            print('%2d %27.22f %27.22f' %(j, raman_A4amu_pcpg_45_4.harmonic[j], \
                                          raman_A4amu_pcpg_45_7.harmonic[j]))

    # SCS: Absolute differential scattering cross section
    raman_SI_scs_45_4 = raman_scattering_cross_section(polarizability_transition_moment, \
                                                       incident_wavenumbers, \
                                                       wavenumbers, '45+4', \
                                                       print_level,  temperature)

    raman_SI_scs_45_7 = raman_scattering_cross_section(polarizability_transition_moment, \
                                                       incident_wavenumbers, \
                                                       wavenumbers, '45+7', \
                                                       print_level, temperature)

    if (print_level > 2):
        print('\n')
        print('SCS: Absolute differential scattering cross section SI units, input energy. ', \
                au_incident_vibration_energy)
        print('%4s %14s %28s' %('Mode', '45+4', '45+7'))
        for j in range(num_modes):
            print('%2d %27.18E %27.18E' %(j, raman_SI_scs_45_4.harmonic[j], \
                                          raman_SI_scs_45_7.harmonic[j]))

    if ('Raman: CPG 45+4, a.u.' in specifications):
        raman_intensities = raman_au_cpg_45_4
    elif ('Raman: CPG 45+7, a.u.' in specifications):
        raman_intensities = raman_au_cpg_45_7
    # Default in Dalton
    elif ('Raman: PCPG 45+4, Å^4/amu' in specifications):
        raman_intensities = raman_A4amu_pcpg_45_4
    elif ('Raman: PCPG 45+7, Å^4/amu' in specifications):
        raman_intensities = raman_A4amu_pcpg_45_7
    elif ('Raman: SCS 45+4, SI units' in specifications):
        raman_intensities = raman_SI_scs_45_4
    elif ('Raman: SCS 45+7, SI units' in specifications):
        raman_intensities = raman_SI_scs_45_7
    else:
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities ')
        print('You forgot to specify the Raman specifications')
        exit()

    return raman_intensities
