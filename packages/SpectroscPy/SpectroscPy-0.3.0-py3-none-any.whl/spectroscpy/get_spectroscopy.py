# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

from .openrsp_tensor_reader import read_openrsp_tensor_file, rspProperty
from .vib_analysis import get_vib_harm_freqs_and_eigvecs, read_mol
from .transform_nc_to_nm import transform_cartesian_to_normal, list_product_int

from .ir import get_ir_intensities, qi_prefactor2, get_harmonic_transition_moment
from .raman import get_raman_headers, get_raman_intensities, requested_unit_incident_mode
from .SpectroscPy_tools import check_spectroscopy_types_input
from .hyperraman import get_hyperraman_intensities
from .anharmonic import anharm_corrected_vibrational_energies, transform_to_reduced_nm_prep, \
                        anharmonicProperty, get_anharm_corrected_transition_moment

from .parameters import*
from sys import exit
import numpy as np
from math import sqrt, pi, log
import copy

class vibrationalProperty:

    def __init__(self, frequencies, ir, input_raman_frequencies, raman, input_hyperraman_frequencies, \
                       hyper_raman_vv, hyper_raman_hv):

        self.frequencies = frequencies
        self.ir = ir
        self.input_raman_frequencies = input_raman_frequencies
        self.raman = raman
        self.input_hyperraman_frequencies = input_hyperraman_frequencies
        self.hyper_raman_vv = hyper_raman_vv
        self.hyper_raman_hv = hyper_raman_hv


def get_spectroscopy_sanity_checks(hess_index, cubic_index, quartic_index, dip_grad_index, \
                                   dip_hess_index, dip_cubic_index, polariz_grad_index, \
                                   polariz_hess_index, polariz_cubic_index, \
                                   hyper_polariz_grad_index, hyper_polariz_hess_index, \
                                   hyper_polariz_cubic_index, IR, Raman, \
                                   hyper_raman, anharmonic):
    if (hess_index == []):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You forgot to calculate the hessian in your OpenRSP calculation')
        exit()
    if (anharmonic and cubic_index == []):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for anharmonic corresctions, but forgot to calculate the cubic forcefield')
        print('in your OpenRSP calculation')
        exit()
    if (anharmonic and quartic_index == []):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for anharmonic corresctions, but forgot to calculate the quartic forcefield')
        print('in your OpenRSP calculation')
        exit()
    if ((IR == True) and (dip_grad_index == [])):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for IR, but the dipole gradient was not calcuated in your OpenRSP calculation')
        exit()
    if (anharmonic and (IR == True) and (dip_hess_index == [])):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for IR anharmonic corrections, but the dipole hessian was not calcuated in')
        print('your OpenRSP calculation')
        exit()
    if (anharmonic and (IR == True) and (dip_cubic_index == [])):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for IR anharmonic corrections, but the dipole cubic was not calcuated in')
        print('your OpenRSP calculation')
        exit()
    if ((Raman == True) and (polariz_grad_index == [])):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for Raman, but the polarizability gradient was not calcuated in your OpenRSP')
        print('calculation')
        exit()
    if (anharmonic and (Raman == True) and (polariz_hess_index == [])):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for Raman anharmonic corrections, but the polarizability hessian was not')
        print('calcuated in your OpenRSP calculation')
        exit()
    if (anharmonic and (Raman == True) and (polariz_cubic_index == [])):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for Raman anharmonic corrections, but the polarizability cubic was not')
        print('calcuated in your OpenRSP calculation')
        exit()
    if ((hyper_raman == True) and (hyper_polariz_grad_index == [])):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for Hyper-Raman, but the hyper polarizability gradient was not calcuated in')
        print('your OpenRSP calculation')
        exit()
    if (anharmonic and (hyper_raman == True) and (hyper_polariz_hess_index == [])):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for Hyper-Raman, but the hyper polarizability hessian was not calcuated in')
        print('your OpenRSP calculation')
        exit()
    if (anharmonic and (hyper_raman == True) and (hyper_polariz_cubic_index == [])):
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You asked for Hyper-Raman, but the hyper polarizability cubic was not calcuated in')
        print('your OpenRSP calculation')
        exit()


def which_spectroscopies_to_be_calculated(spectroscopy_types):

    IR = False
    Raman = False
    hyper_raman = False

    check_spectroscopy_types_input(spectroscopy_types)

    if ('IR' in spectroscopy_types):
        IR = True

    if ('Raman' in spectroscopy_types):
        Raman = True

    if ('Hyper-Raman' in spectroscopy_types):
        hyper_raman = True

    return IR, Raman, hyper_raman


def get_spectroscopy_indices(redundant_properties, operator):

    spectroscopy_indices = []

    for i in range(len(redundant_properties)):

        if (redundant_properties[i].operator == operator):
            spectroscopy_indices.append(i)

    return spectroscopy_indices


def reduced_dims(mat_dims, num_coordinates, min_element, max_element, rank_el):

    end_dims = []
    remove_elms = num_coordinates - (max_element - min_element + 1)
    for i in range(len(mat_dims) - rank_el):
        end_dims.append(mat_dims[i] - remove_elms)

    for i in range(rank_el):
        end_dims.append(mat_dims[len(mat_dims) - rank_el + i])

    end_dims = tuple(end_dims)

    return end_dims


def getting_the_subblocks(larger_mat, num_coordinates, min_element, max_element, out_mat, offset, \
                          rank_el):

    dims = np.shape(larger_mat)
    if (len(dims) - rank_el == 1):
        smaller_mat = larger_mat[min_element:max_element + 1]
        smaller_mat = np.reshape(smaller_mat, list_product_int(np.shape(smaller_mat)))
        out_mat[offset:offset + len(smaller_mat)] = smaller_mat
        offset = offset + len(smaller_mat)

    else:
        for i in range(min_element, max_element + 1):
            offset = getting_the_subblocks(larger_mat[i], num_coordinates, min_element, \
                                           max_element, out_mat, offset, rank_el)

    return offset


def get_energy_derivatives(index, tensors, redundant_properties, rank_geo, rank_el, \
                           num_coordinates, min_element, max_element, transformation_matrix):

    energy_derivatives = []

    for i in range(len(index)):
        temp = transform_cartesian_to_normal(tensors[index[i]], \
                                             redundant_properties[index[i]].components, rank_geo, \
                                             num_coordinates, min_element, max_element, \
                                             transformation_matrix)

        end_dims = reduced_dims(np.shape(temp), num_coordinates, min_element, max_element, rank_el)
        if (np.shape(temp) != end_dims):

            offset = 0
            vib_temp = np.zeros(list_product_int(end_dims))

            getting_the_subblocks(temp, num_coordinates, min_element, max_element, vib_temp, \
                                  offset, rank_el)

            vib_temp = np.reshape(vib_temp, end_dims)
            energy_derivatives.append(vib_temp)

        else:
            energy_derivatives.append(temp)

    return energy_derivatives


def get_vibrational_frequencies_and_intensities(tensor_file, molecule_file, spectroscopy_types, \
                                                specifications, print_level, temperature, outproj, \
                                                anharmonic_type, harmonic_frequency_limits):

    # For IR and Raman we need GG, GF, GFF

    IR, Raman, hyper_raman = which_spectroscopies_to_be_calculated(spectroscopy_types)

    if (anharmonic_type == 'Anharmonic: VPT2' or anharmonic_type == 'Anharmonic: DVPT2' or \
        anharmonic_type == 'Anharmonic: Freq DVPT2, Int VPT2' or \
        anharmonic_type == 'Anharmonic: DVPT2, w/ 1-1 checks' or \
        anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2' or \
        anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks' or \
        anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks and forced removal'):
        anharmonic = True
    else:
        anharmonic = False

    redundant_properties, tensors = read_openrsp_tensor_file(tensor_file)
    hess_index = []
    cubic_index = []
    quartic_index = []
    dip_grad_index = []
    dip_hess_index = []
    dip_cubic_index = []
    polariz_grad_index = []
    polariz_hess_index = []
    polariz_cubic_index = []
    hyper_polariz_grad_index = []
    hyper_polariz_hess_index = []
    hyper_polariz_cubic_index = []

    ## Find the property GG.  This is your hessian, to be done vib analysis on
    hess_index = get_spectroscopy_indices(redundant_properties, hess_operator)
    if (anharmonic):
        cubic_index = get_spectroscopy_indices(redundant_properties, cubic_operator)
        quartic_index = get_spectroscopy_indices(redundant_properties, quartic_operator)

    # Find the properties you are looking for
    if (IR == True):
        dip_grad_index = get_spectroscopy_indices(redundant_properties, dip_grad_operator)

        if (anharmonic):
            dip_hess_index = get_spectroscopy_indices(redundant_properties, dip_hess_operator)
            dip_cubic_index = get_spectroscopy_indices(redundant_properties, dip_cubic_operator)

    if (Raman == True):
        polariz_grad_index = get_spectroscopy_indices(redundant_properties, polariz_grad_operator)

        if (anharmonic):
            polariz_hess_index = \
                get_spectroscopy_indices(redundant_properties, polariz_hess_operator)
            polariz_cubic_index = \
                get_spectroscopy_indices(redundant_properties, polariz_cubic_operator)

    if (hyper_raman == True):
        hyper_polariz_grad_index = get_spectroscopy_indices(redundant_properties, \
                                                            hyper_polariz_grad_operator)
        if (anharmonic):
            hyper_polariz_hess_index = get_spectroscopy_indices(redundant_properties, \
                                                                hyper_polariz_hess_operator)
            hyper_polariz_cubic_index = get_spectroscopy_indices(redundant_properties, \
                                                                 hyper_polariz_cubic_operator)

    get_spectroscopy_sanity_checks(hess_index, cubic_index, quartic_index, dip_grad_index, \
                                   dip_hess_index, dip_cubic_index, polariz_grad_index, \
                                   polariz_hess_index, polariz_cubic_index, \
                                   hyper_polariz_grad_index, hyper_polariz_hess_index, \
                                   hyper_polariz_cubic_index, IR, Raman, \
                                   hyper_raman, anharmonic)

    hess = tensors[hess_index[0]]

    # Transform harmonic_frequency_limits to a.u. units
    if (harmonic_frequency_limits != 'Keep all'):
        if ('Vib modes: 1/m' in specifications):
            au_harmonic_frequency_limits = \
                np.multiply(harmonic_frequency_limits, plancs_constant*speed_of_light/hartree_to_joule)
        elif ('Vib modes: 1/cm' in specifications):
            au_harmonic_frequency_limits = \
                np.multiply(harmonic_frequency_limits, plancs_constant*speed_of_light* \
                            100.0/hartree_to_joule)
        elif ('Vib modes: 1/s' in specifications):
            au_harmonic_frequency_limits = \
                np.multiply(harmonic_frequency_limits, plancs_constant/hartree_to_joule)
        elif ('Vib modes: ang. 1/s' in specifications):
            au_harmonic_frequency_limits = \
                np.multiply(harmonic_frequency_limits, plancs_constant/(2*pi*hartree_to_joule))
        elif ('Vib modes: Eh' in specifications):
            au_harmonic_frequency_limits = harmonic_frequency_limits
        else:
            print('\n')
            print('Error in get_vibrational_frequencies_and_intensities')
            print('You forgot to specify the units for vibrational modes in specifications')
            exit()
    else:
        au_harmonic_frequency_limits = harmonic_frequency_limits

    # Do the vibrational analysis
    coords, charges, masses = read_mol(molecule_file)
    # num_coordinates = 3N = total degrees of freedom
    au_harmonic_vibrational_energies, transformation_matrix, num_coordinates, min_element, \
    max_element = \
        get_vib_harm_freqs_and_eigvecs(coords, charges, masses, hess, outproj, print_level, \
                                       au_harmonic_frequency_limits)

    if (min_element != 0):
        print('WARNING')
        print('You have chosen to cut off high-frequency modes.  If you do this in combination with')
        print('anharmonic calculations, be aware that this might severely change your results.')

    num_modes = len(au_harmonic_vibrational_energies)


    if (print_level > 0):
        print('\n')
        print('The harmonic frequencies have been calcuated from the molecular hessian')

    if (anharmonic):
        cubic_forcefield = get_energy_derivatives(cubic_index, tensors, redundant_properties, 3, \
                                                  0, num_coordinates, min_element, max_element, \
                                                  transformation_matrix)

        quartic_forcefield = get_energy_derivatives(quartic_index, tensors, redundant_properties, \
                                                    4, 0, num_coordinates, min_element, \
                                                    max_element, transformation_matrix)

        # Update to include possible coriolis
        rotational_constant = 0
        coriolis_constant = 'No coriolis'

        # Transforming to reduced coordinates
        harmonic_recp_m_wn = au_harmonic_vibrational_energies*hartree_to_joule/ \
                             (plancs_constant*speed_of_light)
        SI_cubic_forcefield = np.multiply(cubic_forcefield[0], \
                                          hartree_to_joule/(bohr_to_meter**3*electron_mass**1.5))
        red_cubic_forcefield = \
            transform_to_reduced_nm_prep(SI_cubic_forcefield, harmonic_recp_m_wn, 0)

        SI_quartic_forcefield = np.multiply(quartic_forcefield[0], \
                                            hartree_to_joule/(bohr_to_meter**4*electron_mass**2))
        red_quartic_forcefield = transform_to_reduced_nm_prep(SI_quartic_forcefield, \
                                                              harmonic_recp_m_wn, 0)

        # Get the anharmonic frequencies
        SI_harmonic_vibrational_energies = \
            np.multiply(au_harmonic_vibrational_energies, hartree_to_joule)

        SI_anharmonic_energies = \
            anharm_corrected_vibrational_energies(SI_harmonic_vibrational_energies, \
                                                  red_cubic_forcefield, \
                                                  red_quartic_forcefield, \
                                                  rotational_constant, \
                                                  coriolis_constant, anharmonic_type)
    else:
        SI_harmonic_vibrational_energies = np.multiply(au_harmonic_vibrational_energies, \
                                                       hartree_to_joule)
        SI_anharmonic_energies = anharmonicProperty(SI_harmonic_vibrational_energies, \
                                                    np.zeros((num_modes)), \
                                                    np.zeros((num_modes)),\
                                                    np.zeros((num_modes, num_modes)))

    # Set up the different units from SI energies
    # a.u. energies
    au_vibrational_energies = anharmonicProperty(SI_harmonic_vibrational_energies, \
                                                 SI_anharmonic_energies.fundamental, \
                                                 SI_anharmonic_energies.overtones, \
                                                 SI_anharmonic_energies.combotones, \
                                                 conversion_factor=(1/hartree_to_joule))

    # 1/m
    recp_m_wavenumbers = anharmonicProperty(SI_harmonic_vibrational_energies, \
                                              SI_anharmonic_energies.fundamental, \
                                              SI_anharmonic_energies.overtones, \
                                              SI_anharmonic_energies.combotones, \
                                              conversion_factor=(1/(plancs_constant*speed_of_light)))

    # 1/cm
    recp_cm_wavenumbers = anharmonicProperty(SI_harmonic_vibrational_energies, \
                                               SI_anharmonic_energies.fundamental, \
                                               SI_anharmonic_energies.overtones, \
                                               SI_anharmonic_energies.combotones, \
                                               conversion_factor=(0.01/ \
                                                   (plancs_constant*speed_of_light)))

    # 1/s not Angular
    vibrational_frequencies = anharmonicProperty(SI_harmonic_vibrational_energies, \
                                                SI_anharmonic_energies.fundamental, \
                                                SI_anharmonic_energies.overtones, \
                                                SI_anharmonic_energies.combotones, \
                                                conversion_factor=(1/plancs_constant))

    # 1/s Angular
    angular_vibrational_frequencies = anharmonicProperty(SI_harmonic_vibrational_energies, \
                                                        SI_anharmonic_energies.fundamental, \
                                                        SI_anharmonic_energies.overtones, \
                                                        SI_anharmonic_energies.combotones, \
                                                        conversion_factor=(2*pi/plancs_constant))

    if ('Vib modes: 1/m' in specifications):
        vibrational_modes = recp_m_wavenumbers
    elif ('Vib modes: 1/cm' in specifications):
        vibrational_modes = recp_cm_wavenumbers
    elif ('Vib modes: 1/s' in specifications):
        vibrational_modes = vibrational_frequencies
    elif ('Vib modes: ang. 1/s' in specifications):
        vibrational_modes = angular_vibrational_frequencies
    elif ('Vib modes: Eh' in specifications):
        vibrational_modes = au_vibrational_energies
    else:
        print('\n')
        print('Error in get_vibrational_frequencies_and_intensities')
        print('You forgot to specify the units for vibrational modes in specifications')
        exit()

    if (print_level > 1):
        print('\n')
        print('Harmonic Vibrational modes')
        print('%4s %17s %20s %26s' %('Mode', 'Energies a.u.', 'Frequencies 1/s', \
                                     'Angular frequencies 1/s'))
        for i in range(len(SI_harmonic_vibrational_energies)):
            print('%2d %20.9E %20.9E %22.9E' %(i, au_vibrational_energies.harmonic[i], \
                                               vibrational_frequencies.harmonic[i], \
                                               angular_vibrational_frequencies.harmonic[i]))

        print('\n')
        print('%4s %18s %18s' %('Mode', 'Wavenumbers 1/m', 'Wavenumbers 1/cm'))
        for i in range(len(SI_harmonic_vibrational_energies)):
            print('%2d %19.6f %19.8f' %(i, recp_m_wavenumbers.harmonic[i], \
                                        recp_cm_wavenumbers.harmonic[i]))

        if (anharmonic):
            print('\n')
            print('Fundamental')
            print(('%4s' + '%18s' + '%18s') %('Mode', 'Harmonic 1/cm', 'Anharmonic 1/cm'))
            for i in range(len(recp_cm_wavenumbers.harmonic)):
                print(('%2d' + '%19.6f' + '%19.6f') %(i, recp_cm_wavenumbers.harmonic[i], \
                                                      recp_cm_wavenumbers.fundamental[i]))
            print('\n')

            print('Overtones')
            print(('%4s' + '%18s' + '%18s') %('Mode', 'Harmonic 1/cm', 'Anharmonic 1/cm'))
            for i in range(len(recp_cm_wavenumbers.harmonic)):
                print(('%2d' + '%19.6f' + '%19.6f') %(i, recp_cm_wavenumbers.harmonic[i]*2, \
                                                      recp_cm_wavenumbers.overtones[i]))
            print('\n')

            print('Combotones')
            print(('%5s' + '%18s' + '%18s') %('Modes', 'Harmonic 1/cm', 'Anharmonic 1/cm'))
            for i in range(len(recp_cm_wavenumbers.harmonic)):
                for j in range(i):
                    print(('%2d' + '%2d' + '%19.6f' + '%19.6f') %(i, j, \
                        recp_cm_wavenumbers.harmonic[i] + recp_cm_wavenumbers.harmonic[j], \
                        recp_cm_wavenumbers.combotones[i][j]))
            print('\n')

    qi2 = qi_prefactor2(recp_m_wavenumbers.harmonic)
    # Use the info from the vib analysis to transfor all tensors to normal coordinates
    if (IR == True):
        dipole_gradient = get_energy_derivatives(dip_grad_index, tensors, redundant_properties, \
                                                 1, 1, num_coordinates, min_element, max_element, \
                                                 transformation_matrix)

        if (len(dipole_gradient) > 1):
            print('\n')
            print('Error in get_vibrational_frequencies_and_intensities')
            print('It doesnt make sense to have more than one configuration for the dipole gradient')
            print('Something is strange with your OpenRSP tensor file')
            exit()

        if (print_level > 1):
            print('\n')
            print('Dipole gradient a.u.')
            for i in range(len(dipole_gradient[0])):
                print('%2d' %(i), '\t'.join(['%24.18f' % val for val in dipole_gradient[0][i]]))

        SI_dipole_gradient = np.multiply(dipole_gradient, hartree_to_coulomb/sqrt(electron_mass))

        # Harmonic transition moment
        harmonic_transition_dipole_moment = \
            get_harmonic_transition_moment(SI_dipole_gradient[0], qi2)
        if (anharmonic):

            red_dipole_gradient = transform_to_reduced_nm_prep(SI_dipole_gradient[0], \
                                                               recp_m_wavenumbers.harmonic, 1)

            dipole_hessian = get_energy_derivatives(dip_hess_index, tensors, redundant_properties, \
                                                    2, 1, num_coordinates, min_element, \
                                                    max_element, transformation_matrix)

            dipole_hessian = np.multiply(dipole_hessian[0], hartree_to_coulomb/ \
                                         (bohr_to_meter*electron_mass))
            red_dipole_hessian = transform_to_reduced_nm_prep(dipole_hessian, \
                                                              recp_m_wavenumbers.harmonic, 1)

            dipole_cubic = get_energy_derivatives(dip_cubic_index, tensors, redundant_properties, \
                                                  3, 1, num_coordinates, min_element, max_element, \
                                                  transformation_matrix)

            dipole_cubic = np.multiply(dipole_cubic, hartree_to_coulomb/ \
                                       (bohr_to_meter**2*electron_mass**1.5))
            red_dipole_cubic = transform_to_reduced_nm_prep(dipole_cubic[0], \
                                                            recp_m_wavenumbers.harmonic, 1)

            # Get transition dipole moment
            transition_dipole_moment = \
                get_anharm_corrected_transition_moment(red_dipole_gradient, red_dipole_hessian, \
                                                       red_dipole_cubic, red_cubic_forcefield, \
                                                       red_quartic_forcefield, \
                                                       harmonic_transition_dipole_moment, \
                                                       SI_anharmonic_energies.harmonic, \
                                                       'No coriolis', 0, anharmonic_type)

        else:
            fundamental_transition_dipole_moment = \
                np.zeros(np.shape(harmonic_transition_dipole_moment))
            overtone_transition_dipole_moment = np.zeros(np.shape(harmonic_transition_dipole_moment))
            combotone_transition_dipole_moment = \
                np.zeros(np.shape(harmonic_transition_dipole_moment))

            transition_dipole_moment = anharmonicProperty(harmonic_transition_dipole_moment, \
                                                          fundamental_transition_dipole_moment, \
                                                          overtone_transition_dipole_moment, \
                                                          combotone_transition_dipole_moment)

        # Calculate the IR intensities
        ir_intensities, current_unit, header_format_string, format_string = \
            get_ir_intensities(specifications, transition_dipole_moment, recp_m_wavenumbers, \
                               anharmonic, print_level)

        if (print_level > 0):
            print('\n')
            print('IR intensities in', current_unit)
            print(header_format_string %('Mode', 'Wavenumbers', 'Intensities'))
            for i in range(num_modes):
                print(format_string %(i, vibrational_modes.harmonic[i], ir_intensities.harmonic[i]))

            if (anharmonic):
                print('\n')
                print('Fundamental Intensities')
                print(('%4s' + '%18s' + '%18s') %('Mode', 'Harmonic', 'Anharmonic'))
                for i in range(num_modes):
                    print(('%2d' + '%19.6f' + '%19.6f') %(i, ir_intensities.harmonic[i], \
                                                          ir_intensities.fundamental[i]))
                print('\n')

                print('Overtone Intensities')
                print(('%4s' + '%18s' + '%18s') %('Mode', 'Harmonic', 'Anharmonic'))
                for i in range(num_modes):
                    print(('%2d' + '%19s' + '%19.6f') %(i, ' -   ', ir_intensities.overtones[i]))

                print('\n')

                print('Combotones')
                print(('%5s' + '%18s' + '%18s') %('Modes', 'Harmonic', 'Anharmonic'))
                for i in range(num_modes):
                    for j in range(i):
                        print(('%2d' + '%2d' + '%19s' + '%19.6f') %(i, j, ' -    ', \
                                                                    ir_intensities.combotones[i][j]))
                print('\n')

    else:
        ir_intensities = anharmonicProperty(['You did not ask for IR intensities'], \
                                            ['You did not ask for IR intensities'], \
                                            ['You did not ask for IR intensities'], \
                                            ['You did not ask for IR intensities'])

    if (Raman == True):

        au_polarizability_gradients = get_energy_derivatives(polariz_grad_index, tensors, \
                                                             redundant_properties, 1, 2, \
                                                             num_coordinates, min_element, \
                                                             max_element, transformation_matrix)

        SI_polarizability_gradients = np.multiply(au_polarizability_gradients, \
                                       (hartree_to_coulomb**2*bohr_to_meter)/ \
                                       (hartree_to_joule*electron_mass**0.5))

        if (anharmonic):
            polarizability_hessian = get_energy_derivatives(polariz_hess_index, tensors, \
                                                            redundant_properties, 2, 2, \
                                                            num_coordinates, min_element, \
                                                            max_element, transformation_matrix)

            polarizability_hessian = np.multiply(polarizability_hessian, hartree_to_coulomb**2/ \
                                                 (hartree_to_joule*electron_mass))

            polarizability_cubic = get_energy_derivatives(polariz_cubic_index, tensors, \
                                                          redundant_properties, 3, 2, \
                                                          num_coordinates, min_element, \
                                                          max_element, transformation_matrix)

            polarizability_cubic = np.multiply(polarizability_cubic, hartree_to_coulomb**2/ \
                                               (hartree_to_joule*bohr_to_meter*electron_mass**1.5))

        raman_intensities = anharmonicProperty([], [], [], [])
        input_raman_modes = []

        for i in range(len(polariz_grad_index)):

            au_incident_vibration_energy = \
                abs(redundant_properties[polariz_grad_index[i]].frequencies[2])

            if (print_level > 0):
                print('\n')
                print('Calculating new Raman configuration, input frequency (au): ', \
                      au_incident_vibration_energy)

            if ((i > 0) and (au_incident_vibration_energy == old_incident_energy)):
                if (print_level > 0):
                    print('This configuration has already been calcuated, skip to next')
            else:

                if (print_level > 1):
                    print('Polarizability gradient in atomic units')
                    print('%4s %12s %15s %22s' %('Mode', 'x', 'y', 'z'))
                    for j in range(len(au_polarizability_gradients[i])):
                        for k in range(len(au_polarizability_gradients[i][j])):
                            if (k == 0):
                                print('%2d %3s' %(j, 'x'), '\t'.join(['%16.10f' % val for val in \
                                      au_polarizability_gradients[i][j][k]]))
                            elif (k == 1):
                                print('%2s %3s' %(' ', 'y'), '\t'.join(['%16.10f' % val for val in \
                                      au_polarizability_gradients[i][j][k]]))
                            elif (k == 2):
                                print('%2s %3s' %(' ', 'z'), '\t'.join(['%16.10f' % val for val in \
                                      au_polarizability_gradients[i][j][k]]))

                incident = requested_unit_incident_mode(specifications, au_incident_vibration_energy)
                SI_incident_wavenumbers = au_incident_vibration_energy*hartree_to_joule/ \
                                          (plancs_constant*speed_of_light)

                harmonic_transition_polarizability_moment = \
                    get_harmonic_transition_moment(SI_polarizability_gradients[i], qi2)

                if (anharmonic):

                    red_polariz_gradient = \
                        transform_to_reduced_nm_prep(SI_polarizability_gradients[i], \
                                                     recp_m_wavenumbers.harmonic, 2)

                    red_polariz_hessian = \
                        transform_to_reduced_nm_prep(polarizability_hessian[i], \
                                                     recp_m_wavenumbers.harmonic, 2)

                    red_polariz_cubic = \
                        transform_to_reduced_nm_prep(polarizability_cubic[i], \
                                                     recp_m_wavenumbers.harmonic, 2)

                    transition_polarizability_moment = \
                        get_anharm_corrected_transition_moment(red_polariz_gradient, \
                                                               red_polariz_hessian, \
                                                               red_polariz_cubic, \
                                                               red_cubic_forcefield, \
                                                               red_quartic_forcefield, \
                                                        harmonic_transition_polarizability_moment, \
                                                               SI_anharmonic_energies.harmonic, \
                                                               'No coriolis', 0, anharmonic_type)

                else:
                    fundamental_transition_polarizability_moment = \
                        np.zeros(np.shape(harmonic_transition_polarizability_moment))
                    overtone_transition_polarizability_moment = \
                        np.zeros(np.shape(harmonic_transition_polarizability_moment))
                    combotone_transition_polarizability_moment = \
                        np.zeros((num_modes, num_modes, 3, 3))

                    transition_polarizability_moment = \
                        anharmonicProperty(harmonic_transition_polarizability_moment, \
                                            fundamental_transition_polarizability_moment, \
                                            overtone_transition_polarizability_moment, \
                                            combotone_transition_polarizability_moment)

                temp_raman_intensities = \
                    get_raman_intensities(specifications, SI_incident_wavenumbers, \
                                          transition_polarizability_moment, \
                                          recp_m_wavenumbers, \
                                          anharmonic, print_level, temperature)

                input_raman_modes.append(incident)
                raman_intensities.harmonic.append(temp_raman_intensities.harmonic)
                raman_intensities.fundamental.append(temp_raman_intensities.fundamental)
                raman_intensities.overtones.append(temp_raman_intensities.overtones)
                raman_intensities.combotones.append(temp_raman_intensities.combotones)

                old_incident_energy = copy.deepcopy(au_incident_vibration_energy)

        if (print_level > 0):
            intensities_caption, format_string = get_raman_headers(specifications)

            print('\n')
            print('Raman intensities in', intensities_caption)
            print('%4s %14s %35s' %('Mode', 'Wavenumbers', 'Intensities'))
            print('%20s' %(' '), '\t'.join(['%9s %6.5E' % ('Input waven: ', val) for val in \
                  input_raman_modes]))
            for i in range(len(recp_m_wavenumbers.harmonic)):
                print('%2d %16.6f' %(i, recp_m_wavenumbers.harmonic[i]), '\t'.join([format_string % \
                      raman_intensities.harmonic[j][i] for j in \
                          range(len(raman_intensities.harmonic))]))

    else:
        raman_intensities = anharmonicProperty(['You did not ask for Raman intensities'], \
                                               ['You did not ask for Raman intensities'], \
                                               ['You did not ask for Raman intensities'], \
                                               ['You did not ask for Raman intensities'])
        input_raman_modes = ['You did not ask for Raman intensities']

    if (hyper_raman == True):

        au_hyper_polarizability_gradients = \
            get_energy_derivatives(hyper_polariz_grad_index, tensors, redundant_properties, 1, \
                                   3, num_coordinates, min_element, max_element, \
                                   transformation_matrix)

        SI_hyper_polarizability_gradients = \
            np.multiply(au_hyper_polarizability_gradients, hartree_to_coulomb**3*bohr_to_meter**2/ \
                        (hartree_to_joule**2*electron_mass**0.5))

        if (anharmonic):
            beta_hessian = get_energy_derivatives(hyper_polariz_hess_index, tensors, \
                                                  redundant_properties, 2, 3, num_coordinates, \
                                                  min_element, max_element, transformation_matrix)

            beta_hessian = np.multiply(beta_hessian, hartree_to_coulomb**3*bohr_to_meter/ \
                                       (hartree_to_joule**2*electron_mass))

            beta_cubic = get_energy_derivatives(hyper_polariz_cubic_index, tensors, \
                                                redundant_properties, 3, 3, num_coordinates, \
                                                min_element, max_element, transformation_matrix)

            beta_cubic = np.multiply(beta_cubic, hartree_to_coulomb**3/ \
                                     (hartree_to_joule**2*electron_mass**1.5))

        harmonic_hyperraman_vv_intensities = []
        harmonic_hyperraman_hv_intensities = []
        input_hyperraman_modes = []
        old_incident_energy = []

        hyperraman_vv_intensities = anharmonicProperty([], [], [], [])
        hyperraman_hv_intensities = anharmonicProperty([], [], [], [])

        for i in range(len(hyper_polariz_grad_index)):
            # FIX: unit considerations
            au_incident_vibration_energy = \
                abs(redundant_properties[hyper_polariz_grad_index[i]].frequencies[2])

            if (print_level > 0):
                print('\n')
                print('Calculating new hyperraman configuration, input frequency (au): ', \
                      au_incident_vibration_energy)

            if ((i > 0) and (au_incident_vibration_energy in old_incident_energy)):
                if (print_level > 0):
                    print('This configuration has already been calcuated, skip to next')
            else:

                incident = requested_unit_incident_mode(specifications, au_incident_vibration_energy)
                SI_incident_wavenumbers = au_incident_vibration_energy*hartree_to_joule/ \
                                          (plancs_constant*speed_of_light)

                harmonic_beta_transition_moment = \
                    get_harmonic_transition_moment(SI_hyper_polarizability_gradients[i], qi2)

                if (anharmonic):
                    red_beta_gradient = \
                        transform_to_reduced_nm_prep(SI_hyper_polarizability_gradients[i], \
                                                     recp_m_wavenumbers.harmonic, 3)

                    red_beta_hessian = transform_to_reduced_nm_prep(beta_hessian[i], \
                                                                    recp_m_wavenumbers.harmonic, 3)

                    red_beta_cubic = transform_to_reduced_nm_prep(beta_cubic[i], \
                                                                  recp_m_wavenumbers.harmonic, 3)

                    beta_transition_moment = \
                        get_anharm_corrected_transition_moment(red_beta_gradient, red_beta_hessian, \
                                                               red_beta_cubic, \
                                                               red_cubic_forcefield, \
                                                               red_quartic_forcefield, \
                                                               harmonic_beta_transition_moment, \
                                                               SI_anharmonic_energies.harmonic, \
                                                               'No coriolis', 0, anharmonic_type)

                else:
                    fundamental_beta_transition_moment = np.zeros((num_modes, 3, 3, 3))
                    overtones_beta_transition_moment = np.zeros((num_modes, 3, 3, 3))
                    combotones_beta_transition_moment = np.zeros((num_modes, num_modes, 3, 3, 3))

                    beta_transition_moment = anharmonicProperty(harmonic_beta_transition_moment, \
                                                                fundamental_beta_transition_moment, \
                                                                overtones_beta_transition_moment, \
                                                                combotones_beta_transition_moment)

                hyperraman_scs_SI_vv, hyperraman_scs_SI_hv = \
                    get_hyperraman_intensities(specifications, SI_incident_wavenumbers, \
                                               recp_m_wavenumbers, beta_transition_moment, \
                                               temperature, anharmonic, print_level)

                input_hyperraman_modes.append(incident)

                hyperraman_vv_intensities.harmonic.append(hyperraman_scs_SI_vv.harmonic)
                hyperraman_hv_intensities.harmonic.append(hyperraman_scs_SI_hv.harmonic)

                hyperraman_vv_intensities.fundamental.append(hyperraman_scs_SI_vv.fundamental)
                hyperraman_hv_intensities.fundamental.append(hyperraman_scs_SI_hv.fundamental)
                hyperraman_vv_intensities.overtones.append(hyperraman_scs_SI_vv.overtones)
                hyperraman_hv_intensities.overtones.append(hyperraman_scs_SI_hv.overtones)
                hyperraman_vv_intensities.combotones.append(hyperraman_scs_SI_vv.combotones)
                hyperraman_hv_intensities.combotones.append(hyperraman_scs_SI_hv.combotones)

                old_incident_energy.append(au_incident_vibration_energy)


    else:
        hyperraman_vv_intensities = \
            anharmonicProperty(['You did not ask for Hyper-Raman intensities'], \
                               ['You did not ask for Hyper-Raman intensities'], \
                               ['You did not ask for Hyper-Raman intensities'], \
                               ['You did not ask for Hyper-Raman intensities'])

        hyperraman_hv_intensities = \
            anharmonicProperty(['You did not ask for Hyper-Raman intensities'], \
                               ['You did not ask for Hyper-Raman intensities'], \
                               ['You did not ask for Hyper-Raman intensities'], \
                               ['You did not ask for Hyper-Raman intensities'])
        input_hyperraman_modes = ['You did not ask for Hyper-Raman intensities']

    properties = vibrationalProperty(vibrational_modes, ir_intensities, input_raman_modes, \
                                     raman_intensities, input_hyperraman_modes, \
                                     hyperraman_vv_intensities, hyperraman_hv_intensities)

    return properties
