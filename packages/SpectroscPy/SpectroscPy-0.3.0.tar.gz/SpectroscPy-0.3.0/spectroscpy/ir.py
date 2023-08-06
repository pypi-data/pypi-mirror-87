# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

# For this routine, KD would like to thank John Kendrick for helpful discussions regardin IR

from .parameters import*
import numpy as np
from math import exp, pi, sqrt, log
from sys import exit
from .anharmonic import anharmonicProperty

def get_harmonic_transition_moment(property_gradient, qi2):

    qi = np.sqrt(qi2)
    transition = np.zeros(np.shape(property_gradient))

    for i in range(len(property_gradient)):
        transition[i] = np.multiply(property_gradient[i], qi[i])

    return transition


# Independent of units
def square_then_sum(dipole_gradient):

    red_dipole_strength = np.zeros((len(dipole_gradient)))

    square = np.multiply(dipole_gradient, dipole_gradient)

    for i in range(len(dipole_gradient)):
        for j in range(3):
            red_dipole_strength[i] = red_dipole_strength[i] + square[i][j]

    return red_dipole_strength


# SI units
def qi_prefactor2(wavenumbers):

    prefactor = plancs_constant/(8*pi**2*speed_of_light)

    qi2 = np.divide(prefactor, wavenumbers)

    return qi2


def get_ir_intensities(specifications, transition_dipole_moment, recp_m_wavenumbers, anharmonic, \
                       print_level):

    num_modes = len(recp_m_wavenumbers.harmonic)
    harmonic_qi2 = qi_prefactor2(recp_m_wavenumbers.harmonic)
    harmonic_gathered_transition = square_then_sum(transition_dipole_moment.harmonic)

    if (anharmonic):
        fundamental_qi2 = qi_prefactor2(recp_m_wavenumbers.fundamental)
        overtones_qi2 = qi_prefactor2(recp_m_wavenumbers.overtones)
        combotones_qi2 = np.zeros((num_modes, num_modes))
        for i in range(num_modes):
            combotones_qi2[i] = qi_prefactor2(recp_m_wavenumbers.combotones[i])

        fundamental_gathered_transition = square_then_sum(transition_dipole_moment.fundamental)
        overtone_gathered_transition = square_then_sum(transition_dipole_moment.overtones)
        combotones_gathered_transition = np.zeros((num_modes, num_modes))

        for i in range(num_modes):
            combotones_gathered_transition[i] = square_then_sum(transition_dipole_moment.combotones[i])
    else:
        fundamental_qi2 = 1.0
        overtones_qi2 = 1.0
        combotones_qi2 = 1.0

        fundamental_gathered_transition = np.zeros(num_modes)
        overtone_gathered_transition = np.zeros(num_modes)
        combotones_gathered_transition = np.zeros(num_modes)

    gathered_transition = anharmonicProperty(harmonic_gathered_transition, \
                                             fundamental_gathered_transition, \
                                             overtone_gathered_transition, \
                                             combotones_gathered_transition)

    # SSDG: summed and squared dipole au_polarizability_gradients
    # Units: a.u. or D^2 Å^-2 amu^-1
    # Reported as intensities many places, for instance in Dalton
    # I wonder if these should be all divided by harmonic_qi2
    au_gathered_transition = \
        anharmonicProperty(np.divide(gathered_transition.harmonic, harmonic_qi2), \
                           np.divide(gathered_transition.fundamental, fundamental_qi2), \
                           np.divide(gathered_transition.overtones, overtones_qi2), \
                           np.divide(gathered_transition.combotones, combotones_qi2), \
                           conversion_factor=(electron_mass/hartree_to_coulomb**2))

    ir_SI_ssdg = anharmonicProperty(au_gathered_transition.harmonic, \
                                    au_gathered_transition.fundamental, \
                                    au_gathered_transition.overtones, \
                                    au_gathered_transition.combotones, \
                                    conversion_factor=(hartree_to_coulomb**2/electron_mass))

    ir_DA_ssdg = anharmonicProperty(au_gathered_transition.harmonic, \
                                    au_gathered_transition.fundamental, \
                                    au_gathered_transition.overtones, \
                                    au_gathered_transition.combotones, \
                                    conversion_factor=((hartree_to_coulomb*angstrom_to_meter)**2* \
                                                        one_twelfth_carbon/ \
                                                       (electron_mass*debye_to_coulomb_meter**2)))

    if (print_level > 2):
        print('\n')
        print('SSDG: summed and squared dipole gradients')
        print('%4s %14s %28s %29s' %('Mode', 'a.u', 'C**2/kg', '(D/Å)**2/amu'))
        for i in range(num_modes):
            print('%2d %27.22f %27.22f %27.22f' %(i, au_gathered_transition.harmonic[i], \
                                                  ir_SI_ssdg.harmonic[i], ir_DA_ssdg.harmonic[i]))

    conversion = avogadros_constant/(3*vacuum_permittivity*speed_of_light)

    ir_temp = anharmonicProperty(np.divide(gathered_transition.harmonic, harmonic_qi2), \
                                 np.divide(gathered_transition.fundamental, fundamental_qi2), \
                                 np.divide(gathered_transition.overtones, overtones_qi2), \
                                 np.divide(gathered_transition.combotones, combotones_qi2), \
                                 conversion_factor=conversion)

    # MDAC: Molar decadic attenuated coefficient
    # Without lineshape, so the units that should be m^2/mol are actually m^2/s*mol
    ir_SI_mdac = anharmonicProperty(ir_temp.harmonic, \
                                    ir_temp.fundamental, \
                                    ir_temp.overtones, \
                                    ir_temp.combotones, \
                                    conversion_factor=(pi/(2*log(10))))

    ir_Lcm_mdac = anharmonicProperty(ir_SI_mdac.harmonic, \
                                     ir_SI_mdac.fundamental, \
                                     ir_SI_mdac.overtones, \
                                     ir_SI_mdac.combotones, \
                                     conversion_factor=10)

    if (print_level > 2):
        print('\n')
        print('MDAC: Molar decadic attenuated coefficient.  Without lineshape, so therefore the')
        print('extra s^-1 unit')
        print('%4s %16s %22s' %('Mode', 'm**2/(s*mol)', 'L/(cm*s*mol)'))
        for i in range(num_modes):
            print('%2d %22.4f %22.4f' %(i, ir_SI_mdac.harmonic[i], ir_Lcm_mdac.harmonic[i]))

    # NIMAC: Naperian integrated molar absorption coefficient
    ir_SI_nimac = anharmonicProperty(ir_temp.harmonic, \
                                     ir_temp.fundamental, \
                                     ir_temp.overtones, \
                                     ir_temp.combotones, \
                                     conversion_factor=(1/(4*speed_of_light)))

    ir_kmmol_nimac = anharmonicProperty(ir_SI_nimac.harmonic, \
                                        ir_SI_nimac.fundamental, \
                                        ir_SI_nimac.overtones, \
                                        ir_SI_nimac.combotones, \
                                        conversion_factor=0.001)

    if (print_level > 2):
        print('\n')
        print('NIMAC: Naperian integrated molar absorption coefficient')
        print('%4s %12s %22s' %('Mode', 'm/mol', 'km/mol'))
        for i in range(num_modes):
            print('%2d %24.13f %24.19f' %(i, ir_SI_nimac.harmonic[i], ir_kmmol_nimac.harmonic[i]))

    if ('IR: SSDG, a.u.' in specifications):
        ir_intensities = au_gathered_transition
        current_unit = 'SSDG, a.u.'
        header_format_string = '%4s %15s %15s'
        format_string = '%2d %17.6f %22.17f'
    elif ('IR: SSDG, C**2/kg' in specifications):
        ir_intensities = ir_SI_ssdg
        current_unit = 'SSDG, C**2/kg'
        header_format_string = '%4s %15s %16s'
        format_string = '%2d %17.6f %25.20f'
    elif ('IR: SSDG, D2A2/amu' in specifications):
        ir_intensities = ir_DA_ssdg
        current_unit = '(D/Å)**2/amu'
        header_format_string = '%4s %15s %14s'
        format_string = '%2d %17.6f %15.10f'
    elif ('IR: MDAC, m**2/(s*mol)' in specifications):
        ir_intensities = ir_SI_mdac
        current_unit = 'MDAC, m**2/(s*mol)'
        header_format_string = '%4s %15s %14s'
        format_string = '%2d %17.6f %20.1f'
    elif ('IR: MDAC, L/(cm*s*mol)' in specifications):
        ir_intensities = ir_Lcm_mdac
        current_unit = 'MDAC, L/(cm*s*mol)'
        header_format_string = '%4s %15s %16s'
        format_string = '%2d %17.6f %20.1f'
    elif ('IR: NIMAC, m/mol' in specifications):
        ir_intensities = ir_SI_nimac
        current_unit = 'NIMAC, m/mol'
        header_format_string = '%4s %15s %16s'
        format_string = '%2d %17.6f %17.8f'
    elif ('IR: NIMAC, km/mol' in specifications):
        ir_intensities = ir_kmmol_nimac
        current_unit = 'NIMAC, km/mol'
        header_format_string = '%4s %15s %16s'
        format_string = '%2d %17.6f %17.10f'
    else:
        print('\n')
        print('You forgot to specify the IR units in specifications')
        exit()

    return ir_intensities, current_unit, header_format_string, format_string
