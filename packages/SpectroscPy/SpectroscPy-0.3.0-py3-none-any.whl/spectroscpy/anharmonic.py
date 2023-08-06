# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

# Anharmonic module

import numpy as np
from sys import exit
from .parameters import sqrt2, plancs_constant, speed_of_light, hartree_to_joule, martin_threshold
from math import sqrt, pi
from .transform_nc_to_nm import list_product_int
from .resonance_checks import is_fermi_resonance, add_fermi_resonance, is_11_resonance

# Class to hold harmonic, anharmonic fundamental, overtones and combotones from wavenumbers or intensities
class anharmonicProperty:

    def __init__(self, harmonic, fundamental, overtones, combotones, conversion_factor=1.0):

        self.harmonic = harmonic
        self.fundamental = fundamental
        self.overtones = overtones
        self.combotones = combotones
        self.conversion_factor = 1.0

        if (isinstance(conversion_factor, np.ndarray) or conversion_factor != 1.0):
            if isinstance(conversion_factor, int):
                conversion_factor = float(conversion_factor)

            self.conversion_factor = conversion_factor
            self.unit_change()

    def unit_change(self):
        self.harmonic = np.multiply(self.harmonic, self.conversion_factor)
        self.fundamental = np.multiply(self.fundamental, self.conversion_factor)
        self.overtones = np.multiply(self.overtones, self.conversion_factor)
        self.combotones = np.multiply(self.combotones, self.conversion_factor)


def get_red_prefactor(wn):

    prefactor = np.divide(1, wn)
    prefactor = np.multiply(prefactor, (plancs_constant/(4*pi**2*speed_of_light)))
    prefactor = np.sqrt(prefactor)

    return prefactor


# Properties should be in SI units
def transform_to_reduced_nm(prefactor, rank_el, out_mat, input_mat, offset, wn_prefactor):

    dims = np.shape(input_mat)
    if (len(dims) - rank_el == 0):
        input_mat = np.reshape(input_mat, list_product_int(np.shape(input_mat)))
        out_mat[offset:offset + len(input_mat)] = np.multiply(input_mat, prefactor)
        offset = offset + list_product_int(np.shape(input_mat))
    else:
        for i in range(list(dims)[0]):
            new_prefactor = prefactor*wn_prefactor[i]
            offset = transform_to_reduced_nm(new_prefactor, rank_el, out_mat, input_mat[i], offset, \
                                             wn_prefactor)

    return offset


def transform_to_reduced_nm_prep(energy_derivative, wn, rank_el):

    wn_prefactor = get_red_prefactor(wn)

    out_mat = np.zeros(list_product_int(np.shape(energy_derivative)))

    offset = transform_to_reduced_nm(1, rank_el, out_mat, energy_derivative, 0, wn_prefactor)
    transformed = np.reshape(out_mat, np.shape(energy_derivative))

    return transformed


# 99% certain that this one is correct.  Have gone through manually and tested.
def get_X(harmonic_energies, cubic_forcefield, quartic_forcefield, rotational_constant, \
          coriolis_constant, do_resonance_checks):

    fermi_resonance = []
    X = np.zeros((len(harmonic_energies), len(harmonic_energies)))

    for i in range(len(harmonic_energies)):
        vi = harmonic_energies[i]
        X[i][i] = quartic_forcefield[i][i][i][i]/16.0

        rhs = 0

        for k in range(len(harmonic_energies)):
            vk = harmonic_energies[k]
            kiik = cubic_forcefield[i][i][k]

            tmp1 = 4.0/vk
            tmp2 = 1/(2.0*vi + vk)
            if (not is_fermi_resonance(2*vi - vk, kiik, True) or not do_resonance_checks):
                tmp3 = 1/(2.0*vi - vk)
            else:
                fermi_resonance = add_fermi_resonance(fermi_resonance, [k, i, i, True])
                tmp3 = 0.0

            rhs = rhs + (kiik**2/32.0)*(tmp1 + tmp2 - tmp3)

        X[i][i] = X[i][i] - rhs

        for j in range(i):
            vj = harmonic_energies[j]
            X[i][j] = quartic_forcefield[i][i][j][j]/4.0

            A = 0
            for k in range(len(harmonic_energies)):
                A = A + cubic_forcefield[i][i][k]*cubic_forcefield[j][j][k]/(4.0*harmonic_energies[k])

            B = 0
            for k in range(len(harmonic_energies)):
                vk = harmonic_energies[k]
                kijk = cubic_forcefield[i][j][k]

                tmp1 = 1/(vi + vj + vk)
                if (not is_fermi_resonance(-vi + vj + vk, kijk, k == j) or not do_resonance_checks):
                    tmp2 = 1/(-vi + vj + vk)
                else:
                    fermi_resonance = add_fermi_resonance(fermi_resonance, [i, j, k, k == j])
                    tmp2 = 0.0

                if (not is_fermi_resonance(vi - vj + vk, kijk, k == i) or not do_resonance_checks):
                    tmp3 = 1/(vi -vj + vk)
                else:
                    fermi_resonance = add_fermi_resonance(fermi_resonance, [j, k, i, k == i])
                    tmp3 = 0.0

                if (not is_fermi_resonance(vi + vj - vk, kijk, False) or not do_resonance_checks):
                    tmp4 = 1/(vi + vj - vk)
                else:
                    fermi_resonance = add_fermi_resonance(fermi_resonance, [k, i, j, False])
                    tmp4 = 0.0

                B = B + kijk**2/8.0*(tmp1 + tmp2 + tmp3 - tmp4)

            C = 0
            if (not coriolis_constant == 'No coriolis'):
                print('This has not been impleneted')
                exit()
                for k in range(len(rotational_constant)):
                    C = C + rotational_constant[k]*coriolis_constant[k][i][j]**2*\
                        (harmonic_energies[i]/harmonic_energies[j] + \
                         harmonic_energies[j]/harmonic_energies[i])

            X[i][j] = X[i][j] - A - B + C

            X[j][i] = np.copy(X[i][j])

    fermi_resonance = sorted(fermi_resonance)

    return X, fermi_resonance


# Assumes reduced normal coordinates.  In other words, energy derivatives have units of energy, in J
# All frequencies and so in are also in J
def anharm_corrected_vibrational_energies(harmonic_energies, cubic_forcefield, quartic_forcefield, \
                                          rotational_constant, coriolis_constant, anharmonic_type):

    if(anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2'):
        do_variational_correction = True
        do_resonance_checks = True
    elif (anharmonic_type == 'Anharmonic: VPT2'):
        do_resonance_checks = False
        do_variational_correction = False
    elif (anharmonic_type == 'Anharmonic: DVPT2'):
        do_resonance_checks = True
        do_variational_correction = False
    elif (anharmonic_type == 'Anharmonic: Freq DVPT2, Int VPT2'):
        do_resonance_checks = True
        do_variational_correction = False
    elif (anharmonic_type == 'Anharmonic: DVPT2, w/ 1-1 checks'):
        do_resonance_checks = True
        do_variational_correction = False
    elif (anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks'):
        do_resonance_checks = True
        do_variational_correction = True
    elif (anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks and forced removal'):
        do_resonance_checks = True
        do_variational_correction = True
    else:
        print('\n')
        print('Something strange has happened in anharm_corrected_vibrational_energies')
        print('Anharmonic is called, but which type isn/t specified')
        exit()

    fundamental = np.zeros((len(harmonic_energies)))
    overtones = np.zeros((len(harmonic_energies)))
    combotones = np.zeros((len(harmonic_energies), len(harmonic_energies)))

    X, fermi_resonance = get_X(harmonic_energies, cubic_forcefield, quartic_forcefield, \
                               rotational_constant, coriolis_constant, do_resonance_checks)

    if (fermi_resonance != []):

        print('Fermi resonances')
        for a in range(len(fermi_resonance)):
            i = fermi_resonance[a][0]
            j = fermi_resonance[a][1]
            k = fermi_resonance[a][2]

            print(i, j, k, harmonic_energies[i], harmonic_energies[j], harmonic_energies[k], \
                  'type: ', fermi_resonance[a][3], \
                  np.multiply(cubic_forcefield[i][j][k], 0.01/(plancs_constant*speed_of_light)))

    for i in range(len(harmonic_energies)):
        fundamental[i] = fundamental[i] + harmonic_energies[i] + 2*X[i][i]

        fscr = 0
        for j in range(len(harmonic_energies)):
            if (j != i):
                fscr = fscr + 0.5*X[i][j]

        fundamental[i] = fundamental[i] + fscr

    for i in range(len(harmonic_energies)):
        overtones[i] = overtones[i] + 2*fundamental[i] + 2*X[i][i]

        for j in range(len(harmonic_energies)):
            if (i == j):
                continue
            combotones[i][j] = combotones[i][j] + fundamental[i] + fundamental[j] + X[i][j]

    if (do_variational_correction):
        adjusted_fundamental, adjusted_overtones, adjusted_combotones = \
            adjust_for_fermi_resonance(fundamental, overtones, combotones, cubic_forcefield, \
                                       fermi_resonance)
        anharmonic_energies = anharmonicProperty(harmonic_energies, adjusted_fundamental, \
                                                 adjusted_overtones, adjusted_combotones)
    else:
        anharmonic_energies = anharmonicProperty(harmonic_energies, fundamental, overtones, combotones)

    return anharmonic_energies



def x_matrix_position(a, b, n):
    pos = a
    for i in range(b):
        pos += i

    return pos + 2*n


def adjust_for_fermi_resonance(fundamental, overtones, combotones, cubic_forcefield, fermi_resonance):

    num_modes = len(fundamental)
    red_num_combotones = (num_modes**2 - num_modes)//2

    num_frequencies = num_modes*2 + red_num_combotones

    adjusted_frequencies = np.zeros((num_frequencies))
    V = np.zeros((num_frequencies, num_frequencies))

    k = 2*num_modes
    for i in range(num_modes):

        V[i][i] = fundamental[i]
        V[i + num_modes][i + num_modes] = overtones[i]

        for j in range(i):
            V[k][k] = combotones[i][j]

            k = k + 1

    for a in range(len(fermi_resonance)):
        i = fermi_resonance[a][0]
        j = fermi_resonance[a][1]
        k = fermi_resonance[a][2]
        fermi_type = fermi_resonance[a][3]

        if fermi_type:
            V[i][num_modes + j] = cubic_forcefield[j][k][i]/4.0
            V[num_modes + j][i] = V[i][num_modes + j]
        else:
            V[i][x_matrix_position(j, k, num_modes)] = cubic_forcefield[j][k][i]/sqrt(8.0)
            V[x_matrix_position(j, k, num_modes)][i] = V[i][x_matrix_position(j, k, num_modes)]

    eigenvalue, eigenvector = np.linalg.eig(V)

    k = 0
    for i in range(num_frequencies):
        orig_character = 0.0

        for j in range(num_frequencies):
            if (abs(eigenvector[i][j]) > orig_character):
                orig_character = abs(eigenvector[i][j])
                adjusted_frequencies[k] = eigenvalue[j]

                i_index = i
                j_index = j

        # A little uncertain of this one..
        for j in range(num_frequencies):
            eigenvector[j][j_index] = 0.0

        k = k + 1

    adjusted_fundamental = np.zeros((num_modes))
    adjusted_overtones = np.zeros((num_modes))
    adjusted_combotones = np.zeros((num_modes, num_modes))

    k = 2*num_modes
    for i in range(num_modes):
        adjusted_fundamental[i] = adjusted_frequencies[i]
        adjusted_overtones[i] = adjusted_frequencies[i + num_modes]

        for j in range(i):
            adjusted_combotones[i][j] = adjusted_frequencies[k]
            adjusted_combotones[j][i] = adjusted_combotones[i][j]

            k = k + 1

    return adjusted_fundamental, adjusted_overtones, adjusted_combotones


def get_anharm_corrected_transition_moment(property_gradient, property_hessian, property_cubic, \
                                           cubic_ff, quartic_ff, harmonic_transition_moment, \
                                           harmonic_energies, coriolis_constant, rotational_constant, \
                                           anharmonic_type):

    fundamental = get_anharm_fundamental_transition_moment(property_gradient, property_hessian, \
                                                           property_cubic, cubic_ff, quartic_ff, \
                                                           harmonic_energies, coriolis_constant, \
                                                           rotational_constant, anharmonic_type)

    overtones, combotones = get_overtone_transition_moment(property_gradient, property_hessian, \
                                                           cubic_ff, harmonic_energies, anharmonic_type)

    transition_moments = anharmonicProperty(harmonic_transition_moment, fundamental, overtones, \
                                            combotones)

    return transition_moments


# This routine is only for polarizability type properties, but with a fiew tweaks can easily be
# expanded to work also for magnetic
# Make sure to send in property_gradient[0] etc
# This routine is best tested through test_get_spectroscopy
def get_anharm_fundamental_transition_moment(property_gradient, property_hessian, property_cubic, \
                                             cubic_ff, quartic_ff, harmonic_energies, \
                                             coriolis_constant, rotational_constant, anharmonic_type):

    if (anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2'):
        do_variational_correction = False
        do_fermi_check = True
        do_DD_check = False
        do_forced_DD_removal = False
    elif (anharmonic_type == 'Anharmonic: VPT2'):
        do_variational_correction = False
        do_fermi_check = False
        do_DD_check = False
        do_forced_DD_removal = False
    elif (anharmonic_type == 'Anharmonic: DVPT2'):
        do_variational_correction = False
        do_fermi_check = True
        do_DD_check = False
        do_forced_DD_removal = False
    elif (anharmonic_type == 'Anharmonic: Freq DVPT2, Int VPT2'):
        do_variational_correction = False
        do_fermi_check = False
        do_DD_check = False
        do_forced_DD_removal = False
    elif (anharmonic_type == 'Anharmonic: DVPT2, w/ 1-1 checks'):
        do_variational_correction = False
        do_fermi_check = True
        do_DD_check = True
        do_forced_DD_removal = False
    elif (anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks'):
        do_variational_correction = False
        do_fermi_check = True
        do_DD_check = True
        do_forced_DD_removal = False
    elif (anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks and forced removal'):
        do_variational_correction = False
        do_fermi_check = True
        do_DD_check = True
        do_forced_DD_removal = True
    else:
        print('\n')
        print('Something strange has happened in get_anharm_fundamental_transition_moment')
        print('Anharmonic is called, but which type isn/t specified')
        exit()

    modes = len(property_gradient)
    prop_size = np.size(property_gradient[0])

    original_shape = np.shape(property_gradient)
    inner_original_shape = np.shape(property_gradient[0])

    temp_prop_grad = np.zeros((modes, prop_size))
    temp_prop_hess = np.zeros((modes, modes, prop_size))
    temp_prop_cubic = np.zeros((modes, modes, modes, prop_size))

    for i in range(modes):
        temp_prop_grad[i] = np.copy(np.reshape(property_gradient[i], prop_size))

        for j in range(modes):
            temp_prop_hess[i][j] = np.copy(np.reshape(property_hessian[i][j], prop_size))

            for k in range(modes):
                temp_prop_cubic[i][j][k] = np.copy(np.reshape(property_cubic[i][j][k], prop_size))

    transition_moment = np.zeros((modes, prop_size))

    if (len(harmonic_energies) != len(property_gradient)):
        print('\n')
        print('Error in get_anharm_fundamental_transition_moment.  Dimensions are off')
        print('len(harmonic_energies)', len(harmonic_energies))
        print('len(property_gradient)', len(property_gradient))
        exit()

    DD_resonances = []
    if (do_DD_check):
        for i in range(modes):
            vi = harmonic_energies[i]
            for j in range(i):
                vj = harmonic_energies[j]

                kijkk = 0.0
                prod1 = 0.0
                prod2 = 0.0
                for k in range(modes):
                    for l in range(modes):
                        if (abs(quartic_ff[i][j][k][k]) > kijkk):
                            kijkk = quartic_ff[i][j][k][k]
                        if (abs(cubic_ff[i][k][l]*cubic_ff[j][k][l]) > prod1):
                            prod1 = abs(cubic_ff[i][k][l]*cubic_ff[j][k][l])
                        if (abs(cubic_ff[i][j][k]*cubic_ff[l][l][k]) > prod2):
                            prod2 = abs(cubic_ff[i][j][k]*cubic_ff[l][l][k])

                if is_11_resonance(vi - vj, kijkk):
                    print('1-1 resonance: ', i, j)
                    DD_resonances.append(sorted([i, j]))
                else:
                    if is_11_resonance(vi - vj, prod1):
                        print('1-1 resonance: ', i, j)
                        DD_resonances.append(sorted([i, j]))
                    else:
                        if is_11_resonance(vi - vj, prod2):
                            print('1-1 resonance: ', i, j)
                            DD_resonances.append(sorted([i, j]))

    for i in range(modes):
        vi = harmonic_energies[i]
        for a in range(prop_size):
            Pia = temp_prop_grad[i][a]

            transition_moment[i][a] = transition_moment[i][a] + (1/sqrt2)*Pia

            for j in range(modes):
                vj = harmonic_energies[j]
                Pja = temp_prop_grad[j][a]
                Pija = temp_prop_hess[i][j][a]
                Pijja = temp_prop_cubic[i][j][j][a]

                transition_moment[i][a] = transition_moment[i][a] + (1/(4*sqrt2))*Pijja

                for k in range(modes):
                    vk = harmonic_energies[k]
                    Pjka = temp_prop_hess[j][k][a]
                    kijk = cubic_ff[i][j][k]
                    kjkk = cubic_ff[j][k][k]
                    kijkk = quartic_ff[i][j][k][k]

                    tmp1 = 1/(vi + vj)

                    if (i != j):
                        # 1-1 resonance
                        if (not is_11_resonance(vi - vj, kijkk) or not do_DD_check):
                            if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                tmp1 = tmp1 - 1/(vi - vj)

                    transition_moment[i][a] = transition_moment[i][a] - (1/(8*sqrt2))*kijkk*Pja*tmp1

                    # Fermi resonance
                    tmp1 = 1/(vi + vj + vk)
                    if (not is_fermi_resonance(vj + vk - vi, cubic_ff[j][k][i], j == k) or \
                        not do_fermi_check):
                        tmp1 = tmp1 - 1/(vi - vj - vk)

                    transition_moment[i][a] = transition_moment[i][a] - (1/(8*sqrt2))*kijk*Pjka*tmp1

                    transition_moment[i][a] = transition_moment[i][a] - (1/(4*sqrt2))*kjkk*Pija/vj

                    # Coriolis insert here

                    for l in range(modes):
                        vl = harmonic_energies[l]
                        kikl = cubic_ff[i][k][l]
                        kjkl = cubic_ff[j][k][l]
                        kllk = cubic_ff[l][l][k]

                        if ((j != i) and (k != i) and (l != i)):

                            # Fermi resonance
                            # 1-1 resonance
                            tmp1 = 1/((vi + vj)*(vj + vk + vl))
                            tmp1 = tmp1 + 1/((vi + vk + vl)*(vj + vk + vl))
                            tmp1 = tmp1 + 1/((vi + vj)*(vi + vk + vl))

                            if (not is_11_resonance(vi - vj, kikl*kjkl) or not do_DD_check):
                                if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                    tmp1 = tmp1 - 1/((vi - vj)*(vj + vk + vl))

                            if (not is_fermi_resonance(vk + vl - vi, cubic_ff[i][k][l], l == k) or \
                                not do_fermi_check):
                                tmp1 = tmp1 - 1/((vi - vk - vl)*(vj + vk + vl))

                                if (not is_11_resonance(vi - vj, kikl*kjkl) or \
                                    not do_DD_check):
                                    if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                        tmp1 = tmp1 + 1/((vi - vj)*(vi - vk - vl))

                            transition_moment[i][a] = transition_moment[i][a] + \
                                                      (1/(16*sqrt2))*kikl*kjkl*Pja*tmp1

                        if ((j == i) and (l != i)):
                            if (k == i):
                                prefactor = 2.0
                            else:
                                prefactor = 1.0

                            # Fermi resonance
                            tmp1 = 1/(2*vi*(vi + vk + vl))

                            if (not is_fermi_resonance(vk + vl - vi, cubic_ff[i][k][l], l == k) or \
                                not do_fermi_check):
                                tmp1 = tmp1 - 1/(2*vi*(vi - vk - vl))
                                tmp1 = tmp1 - 1/(2*(vi - vk - vl)**2)

                            tmp1 = tmp1 + 1/(2*(vi + vk + vl)**2)

                            transition_moment[i][a] = transition_moment[i][a] + \
                                (1/(16*sqrt2))*prefactor*kikl*kjkl*Pja*tmp1

                        if ((j != i) and (k != i) and (l == i)):

                            # Fermi resonance
                            # 1-1 resonance
                            tmp1 = 1/(vk*(vi + vj))
                            tmp1 = tmp1 + 2/((2*vi + vk)*(vi + vj))
                            tmp1 = tmp1 + 3/((vi + vj)*(vi + vj + vk))

                            if (not is_fermi_resonance(vj + vk - vi, cubic_ff[i][j][k], k == j) or \
                                not do_fermi_check):
                                tmp1 = tmp1 - 1/(vk*(vi - vj - vk))
                                if (not is_11_resonance(vi - vj, kikl*kjkl) or not do_DD_check):
                                    if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                        tmp1 = tmp1 + 1/((vi - vj)*(vi - vj - vk))

                            if (not is_11_resonance(vi - vj, kikl*kjkl) or not do_DD_check):
                                if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                    tmp1 = tmp1 - 2/((vi - vj)*(vi + vj + vk))
                                    tmp1 = tmp1 - 3/(vk*(vi - vj))

                            tmp1 = tmp1 + 2/((2*vi + vk)*(vi + vj + vk))
                            tmp1 = tmp1 + 3/(vk*(vi + vj + vk))

                            transition_moment[i][a] = transition_moment[i][a] + \
                                (1/(16*sqrt2))*kikl*kjkl*Pja*tmp1

                        if (j == i):
                            if ((k == i) and (l == i)):
                                prefactor = 1.0 + 2.0/9.0
                            else:
                                prefactor = 1.0

                            transition_moment[i][a] = transition_moment[i][a] + \
                                (1/(16*sqrt2))*prefactor*kijk*kllk*Pja/(vi*vk)

                        if ((j != i) and (k != i) and (l != i)):

                            # Fermi resonance
                            # 1-1 resonance
                            tmp1 = 1/((vi + vj)*(vi + vj + vk))
                            tmp1 = tmp1 + 1/(vk*(vi + vj))
                            tmp1 = tmp1 + 1/(vk*(vi + vj + vk))

                            if (not is_11_resonance(vi - vj, kijk*kllk) or not do_DD_check):
                                if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                    tmp1 = tmp1 - 1/(vk*(vi - vj))

                            if (not is_fermi_resonance(vj + vk - vi, cubic_ff[i][j][k], k == j) or \
                                not do_fermi_check):
                                tmp1 = tmp1 - 1/(vk*(vi - vj - vk))
                                if (not is_11_resonance(vi - vj, kijk*kllk) or not do_DD_check):
                                    if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                        tmp1 = tmp1 + 1/((vi - vj)*(vi - vj - vk))

                            transition_moment[i][a] = transition_moment[i][a] + \
                                (1/(16*sqrt2))*kijk*kllk*Pja*tmp1

                        if ((j != i) and (k == i)):

                            if (l == i):
                                prefactor = 2.0
                            else:
                                prefactor = 1.0

                            # 1-1 resonance
                            tmp1 = 1/((2*vi + vj)*(vi + vj))
                            tmp1 = tmp1 + 1/(vi*(2*vi + vj))
                            if (not is_11_resonance(vi - vj, kijk*kllk) or not do_DD_check):
                                if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                    tmp1 = tmp1 - 1/(vi*(vi - vj))

                            tmp1 = tmp1*prefactor

                            if (l == i):
                                tmp1 = tmp1 + 1/(3*vi*(vi + vj))
                                tmp1 = tmp1 + 1/(3*vi*(2*vi + vj))

                                if (not is_11_resonance(vi - vj, kijk*kllk) or not do_DD_check):
                                    if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                        tmp1 = tmp1 - 1/((vi - vj)*(2*vi + vj))

                            tmp1 = tmp1 + 1/(vi*(vi + vj))
                            tmp1 = tmp1 + 1/(vi*vj)

                            if (not is_11_resonance(vi - vj, kijk*kllk) or not do_DD_check):
                                if not (do_forced_DD_removal and (sorted([i, j]) in DD_resonances)):
                                    tmp1 = tmp1 - 1/(vj*(vi - vj))

                            transition_moment[i][a] = transition_moment[i][a] + \
                                (1/(16*sqrt2))*kijk*kllk*Pja*tmp1

    out_transition_moment = np.zeros((original_shape))

    for i in range(modes):
        out_transition_moment[i] = np.copy(np.reshape(transition_moment[i], inner_original_shape))

    return out_transition_moment


def get_overtone_transition_moment(property_gradient, property_hessian, cubic_ff, harmonic_energies, \
                                   anharmonic_type):

    if(anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2'):
        do_variational_correction = False
        do_resonance_checks = True
    elif (anharmonic_type == 'Anharmonic: VPT2'):
        do_resonance_checks = False
        do_variational_correction = False
    elif (anharmonic_type == 'Anharmonic: DVPT2'):
        do_resonance_checks = True
        do_variational_correction = False
    elif (anharmonic_type == 'Anharmonic: Freq DVPT2, Int VPT2'):
        do_resonance_checks = False
        do_variational_correction = False
    elif (anharmonic_type == 'Anharmonic: DVPT2, w/ 1-1 checks'):
        do_resonance_checks = True
        do_variational_correction = False
    elif (anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks'):
        do_resonance_checks = True
        do_variational_correction = False
    elif (anharmonic_type == 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks and forced removal'):
        do_resonance_checks = True
        do_variational_correction = False
    else:
        print('\n')
        print('Something strange has happened in get_overtone_transition_moment')
        print('Anharmonic is called, but which type isn/t specified')
        exit()

    modes = len(property_gradient)
    prop_size = np.size(property_gradient[0])

    original_shape = np.shape(property_gradient)
    inner_original_shape = np.shape(property_gradient[0])

    temp_prop_grad = np.zeros((modes, prop_size))
    temp_prop_hess = np.zeros((modes, modes, prop_size))

    for i in range(modes):
        temp_prop_grad[i] = np.copy(np.reshape(property_gradient[i], prop_size))

        for j in range(modes):
            temp_prop_hess[i][j] = np.copy(np.reshape(property_hessian[i][j], prop_size))

    overtones = np.zeros((modes, prop_size))
    combotones = np.zeros((modes, modes, prop_size))

    for i in range(modes):
        vi = harmonic_energies[i]

        for a in range(prop_size):
            Piia = temp_prop_hess[i][i][a]
            overtones[i][a] = overtones[i][a] + 1/(2*sqrt2)*Piia

            for j in range(modes):
                vj = harmonic_energies[j]
                if (j != i):
                    Pija = temp_prop_hess[i][j][a]
                    combotones[i][j][a] = combotones[i][j][a] + 0.5*Pija

                B = 0
                for k in range(modes):
                    vk = harmonic_energies[k]
                    Pka = temp_prop_grad[k][a]
                    kijk = cubic_ff[i][j][k]

                    tmp1 = -1/(vi + vj + vk)
                    if (not is_fermi_resonance(vi + vj - vk, kijk, j == i) or not do_resonance_checks):
                        tmp1 = tmp1 + 1/(vi + vj - vk)

                    if (j == i):
                        overtones[i][a] = overtones[i][a] + 1/(4*sqrt2)*kijk*Pka*tmp1
                    else:
                        combotones[i][j][a] = combotones[i][j][a] + 0.25*kijk*Pka*tmp1

    out_overtones = np.zeros((original_shape))
    combotone_shape = [modes, modes]
    for i in range(len(inner_original_shape)):
        combotone_shape.append(inner_original_shape[i])

    out_combotones = np.zeros((tuple(combotone_shape)))

    for i in range(modes):
        out_overtones[i] = np.copy(np.reshape(overtones[i], inner_original_shape))

        for j in range(modes):
            out_combotones[i][j] = np.copy(np.reshape(combotones[i][j], inner_original_shape))

    return out_overtones, out_combotones
