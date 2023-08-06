# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

# This module contains only one function, SpectroscPy_run, which is the startpoint for all the calculations

from .get_spectroscopy import get_vibrational_frequencies_and_intensities, vibrationalProperty
from .plotting_module import visualize_spectrum, anharmonic_visualize_spectrum
from .SpectroscPy_tools import check_spectroscopy_specifications_input, \
                               check_spectroscopy_types_input, check_command_input, \
                               check_cauchy_type, check_run_specification, \
                               get_mode_captions, get_ir_captions, get_raman_captions, \
                               get_cauchy_prefactor, get_hR_captions
from .cauchy import get_simple_averages, average_over_snapshots, get_standard_deviation
from .anharmonic import anharmonicProperty
import numpy as np
from sys import exit

# File location MUST contain a backslash at the end
def SpectroscPy_run(run_specification, spectroscopy_types, spectroscopy_specifications, \
                    cauchy_type, names, harmonic_frequency_limits, spectral_boundaries, \
                    print_level, temperature, ticker_distance):

    # run_specification is set up as follow
    # A) Is it at single or multiple snapshots? => 'Single snapshot', 'Multiple snapshots'
    # B) Do you want something plotted?  Then specify it by any combination of 'Plot IR',
    #    'Plot Raman separately', 'Plot IR and all Raman together', 'Plot Raman together',
    #    'Plot IR and individual Raman together', 'Plot all Hyper-Raman separately',
    #    'Plot Hyper-Raman VV and HV separately' or 'Plot all Hyper-Raman together'.  Otherwise no 
    #    plots will be created
    # C) 'FraME' or 'No FraME'
    # D) 'Outproj' or 'No outproj'
    # E) 'Symbolic labels' or nothing
    # F) 'Harmonic' or 'Anharmonic'.  If nothing is specified, 'Harmonic' is chosen

    #run_specification = ['Single snapshot', ...]
    #run_specification = ['Multiple snapshots', ...]

    # spectroscopy_types specifies what spectroscopies we want, at least one of IR, Raman and 
    # Hyper-Raman
    # spectroscopy_types = ['IR', 'Raman', 'Hyper-Raman']

    # spectroscopy_specifications specifies the exant quantity we wish to calculuate and it's units.
    # Mandatory options vibrational frequencies: 'Vib modes: 1/m', 'Vib modes: 1/cm', 
    # 'Vib modes: 1/s' (this is a frequency, not an angular frequency), 
    # 'Vib modes: ang. 1/s' (angular), 'Vib modes: Eh'

    # Mandatory options IR: 'IR: SSDG, a.u.', 'IR: SSDG, C**2/kg', 'IR: SSDG, D2A2/amu', 
    # 'IR: MDAC, m**2/(s*mol)', 'IR: MDAC, L/(cm*s*mol)', 'IR: NIMAC, m/mol', 'IR: NIMAC, km/mol'
    #
    # Mandatory options Raman: 'Raman: CPG 45+4, a.u.', 'Raman: CPG 45+7, a.u.', 
    # 'Raman: PCPG 45+4, Å^4/amu', 'Raman: PCPG 45+7, Å^4/amu', 'Raman: SCS 45+4, SI units'
    # 'Raman: SCS 45+7, SI units'

    # Mandatory options for Hyper-Raman: 'Hyper-Raman: SI complete', 'Hyper-Raman: Relative'

    # cauchy_type specifies what type of Cauchy distribution you want, fixed gamma or width made 
    # from the distribution of the snapshots. For fixed gamma, insert 'GS' (this gives 
    # 0.001*max(wavenumber)) or the value that you wish.  For width determined gamma, insert 'WS'.  
    # If single snapshot, you do not need  to specify anything as fixed gamma is automatic, but you 
    # can specify a value if you wish.  Also, you can choose not have a lineshape at all, through 
    # the keyword 'Discrete'

    # names contains the names and locations etc for the files.  Two different setups, either for 
    # single or multiple snapshots
    # A) Single snapshot
    #    0) file location: folder where files are stored.  Must have backslash after
    #    1) rsp_tensor file
    #    2) mol file
    # B) Multiple snapshots
    #    0) file location: folder where files are stored
    #    1) start_snapshot: start number
    #    2) end_snapshot: end number
    #    3) dal name base
    #    4) mol name base
    #    5) json name base.  If FraME not used, write 'No FraME'
    #    6) list of any snapshots you wish to ship, f.eks [4, 48]

    # harmonic_frequency_limits specify cut-off of harmonic frequencies.  When running calculations 
    # with solvent, some lower-frequency modes might be seen as contaminated by translation and 
    # rotation.  These should therefore be removed so as not to confuse your results and to not 
    # enter into seemingly higher-frequency overtones and combination bands.  If you wish to keep 
    # all modes, choose 'Keep all', otherwise specify [min_x, max_x].  In the latter case, make sure 
    # that you choose a max_x value higher than you highest frequency when performing anharmonic 
    # calculations.  Otherwise you might up severely changing the anharmonic corrected results, also 
    # for modes that you have not chosen to remove.

    # spectral_boundaries specifies the boundary of the x-axis.  If you wish to plot the whole 
    # spectrum, choose 'Keep all', otherwise specify [min_freq, max_freq].  Note that the values
    # you put here are in your chosen frequency unit.

    # print_level is a number, where 0 is default.
    # A higher number indicates a higher degree of prints, a negative number means less

    # T is temperature

    print('\n', '********************************************************************** \n')
    print('SpectroscPy is a script package developed by and containing contributions from ')
    print('    Karen Oda Hjorth Minde Dundas')
    print('    Magnus Ringholm')
    print('    Yann Cornation')
    print('    Benedicte Ofstad')
    print('\n')
    print('The package is released under a LGPL licence')
    print('For questions, please contact on karen.o.dundas@uit.no')
    print('\n', '********************************************************************** \n')

    check_spectroscopy_types_input(spectroscopy_types)
    check_spectroscopy_specifications_input(spectroscopy_specifications)
    check_command_input(spectroscopy_types, run_specification)
    check_cauchy_type(cauchy_type, run_specification)
    check_run_specification(run_specification)

    print('Calculation')
    if ('Single snapshot' in run_specification):
        num_snapshots = 1
        range_snapshots = 1
        print('For a single snapshot')
    elif ('Multiple snapshots' in run_specification):
        num_snapshots = names[2] - names[1] - len(names[6]) + 1
        print('For multiple snapshots:', num_snapshots)
        range_snapshots = names[2] - names[1] + 1

    all_harmonic_wavenumbers = []
    all_frequencies = anharmonicProperty([], [], [], [])

    print('The following values will be determined')

    if ('Vib modes: 1/m' in spectroscopy_specifications):
        print('    Vibrational wavenumbers in 1/m')
    elif ('Vib modes: 1/cm' in spectroscopy_specifications):
        print('    Vibrational wavenumbers in 1/cm')
    elif ('Vib modes: 1/s' in spectroscopy_specifications):
        print('    Vibrational frequencies in 1/s')
    elif ('Vib modes: ang. 1/s' in spectroscopy_specifications):
        print('    Angular Vibrational frequencies in 1/s')
    elif ('Vib modes: Eh' in spectroscopy_specifications):
        print('    Vibrational energies in hartree')
    else:
        print('\n')
        print('Error in SpectroscPy_run')
        print('You forgot to specify the units for vibrational modes in spectroscopy_specifications')
        exit()

    if ('IR' in spectroscopy_types):
        if ('IR: SSDG, a.u.' in spectroscopy_specifications):
            print('    Infrared SSDG (summed and squared dipole gradients) in a.u')
        elif ('IR: SSDG, C**2/kg' in spectroscopy_specifications):
            print('    Infrared SSDG (summed and squared dipole gradients) in C²/kg')
        elif ('IR: SSDG, D2A2/amu' in spectroscopy_specifications):
            print('    Infrared SSDG (summed and squared dipole gradients) in \
                   (D/Å)²/amu')
        elif ('IR: MDAC, m**2/(s*mol)' in spectroscopy_specifications):
            print('    Infrared MDAC (Molar decadic attenuated coefficient) in m²/mol, or w/o lineshape in m²/(s*mol)')
        elif ('IR: MDAC, L/(cm*s*mol)' in spectroscopy_specifications):
            print('    Infrared MDAC (Molar decadic attenuated coefficient in L/(cm*mol), or w/o lineshape in L/(cm*s*mol)')
        elif ('IR: NIMAC, m/mol' in spectroscopy_specifications):
            print('    Infrared NIMAC (Naperian integrated molar absorption coefficient) in m/mol')
        elif ('IR: NIMAC, km/mol' in spectroscopy_specifications):
            print('    Infrared NIMAC (Naperian integrated molar absorption coefficient) in km/mol')
        else:
            print('\n')
            print('Error in SpectroscPy_run')
            print('You forgot to specify the IR spectroscopy_specifications')
            exit()

        # Contains IR intensity for each snapshot => 2D
        all_ir_intensities = anharmonicProperty([], [], [], [])

    if ('Raman' in spectroscopy_types):
        if ('Raman: CPG 45+4, a.u.' in spectroscopy_specifications):
            print('    Raman combined polarizability gradients, 45 + 4 combination rule, a.u')
        elif ('Raman: CPG 45+7, a.u.' in spectroscopy_specifications):
            print('    Raman combined polarizability gradients, 45 + 7 combination rule, a.u')
        elif ('Raman: PCPG 45+4, Å^4/amu' in spectroscopy_specifications):
            print('    Raman pseudo combined polarizability gradients, 45 + 4 combination rule, Å^4/amu')
        elif ('Raman: PCPG 45+7, Å^4/amu' in spectroscopy_specifications):
            print('    Raman pseudo combined polarizability gradients, 45 + 7 combination rule, Å^4/amu')
        elif ('Raman: SCS 45+4, SI units' in spectroscopy_specifications):
            print('    Absolute differential Raman scattering cross section, 45 + 4 combination rule, SI units')
        elif ('Raman: SCS 45+7, SI units' in spectroscopy_specifications):
            print('    Absolute differential Raman scattering cross section, 45 + 7 combination rule, SI units')
        else:
            print('\n')
            print('Error in SpectroscPy_run')
            print('You forgot to specify the Raman spectroscopy_specifications')
            exit()

        # Contains Raman intensities for each snapshot in each config => 3D
        all_raman_intensities = anharmonicProperty([], [], [], [])

    if ('Hyper-Raman' in spectroscopy_types):
        if ('Hyper-Raman: SI complete' in spectroscopy_specifications):
            print('    Hyper-Raman intensities, SI units')
        elif ('Hyper-Raman: Relative' in spectroscopy_specifications):
            print('    Relative Hyper-Raman intensities')
        else:
            print('\n')
            print('Error in SpectroscPy_run')
            print('You forgot to specify the Hyper-Raman spectroscopy_specifications')
            exit()

        all_hR_vv_intensities = anharmonicProperty([], [], [], [])
        all_hR_hv_intensities = anharmonicProperty([], [], [], [])

    if ('Outproj' in run_specification):
        outproj = True
    elif ('No outproj'):
        outproj = False

    if ('Harmonic' in run_specification):
        anharmonic = False
        anharmonic_type = False
    elif('Anharmonic: VPT2' in run_specification):
        anharmonic = True
        anharmonic_type = 'Anharmonic: VPT2'
        print('    Anharmonic VPT2 corrections to vibrational frequencies and intensities.')
        print('    All resonance checks are disabled.')
    elif('Anharmonic: DVPT2' in run_specification):
        anharmonic = True
        anharmonic_type = 'Anharmonic: DVPT2'
        print('    Anharmonic DVPT2 corrections to vibrational frequencies and intensities.')
        print('    Fermi resonance checks are performed while 1-1 resonance checks are disabled.')
    elif('Anharmonic: DVPT2, w/ 1-1 checks' in run_specification):
        anharmonic = True
        anharmonic_type = 'Anharmonic: DVPT2, w/ 1-1 checks'
        print('    Anharmonic DVPT2 corrections to vibrational frequencies and intensities.')
        print('    Fermi resonance checks and 1-1 resonance checks are performed.')
    elif('Anharmonic: Freq DVPT2, Int VPT2' in run_specification):
        anharmonic = True
        anharmonic_type = 'Anharmonic: Freq DVPT2, Int VPT2'
        print('    Anharmonic DVPT2 corrections to vibrational frequencies and VPT2 intensities')
        print('    Fermi resonance checks are performed for frequencies, but not intensities.')
        print('    1-1 resonance checks are disabled.')
    elif('Anharmonic: Freq GVPT2, Int DVPT2' in run_specification):
        anharmonic = True
        anharmonic_type = 'Anharmonic: Freq GVPT2, Int DVPT2'
        print('    Anharmonic GVPT2 corrections to vibrational frequencies and DVPT2 intensities')
        print('    Fermi resonance checks are performed while 1-1 resonance checks are disabled.')
        print('    Variational correction is done for frequencies, but not for intensities.')
    elif('Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks' in run_specification):
        anharmonic = True
        anharmonic_type = 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks'
        print('    Anharmonic GVPT2 corrections to vibrational frequencies and DVPT2 intensities')
        print('    Fermi resonance checks and 1-1 resonance checks are performed.')
        print('    Variational correction is done for frequencies, but not for intensities.')
    elif('Anharmonic' in run_specification):
        anharmonic = True
        anharmonic_type = 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks'
        print('    Anharmonic GVPT2 corrections to vibrational frequencies and DVPT2 intensities')
        print('    Fermi resonance checks and 1-1 resonance checks are performed.')
        print('    Variational correction is done for frequencies, but not for intensities.')
    elif ('Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks and forced removal' in run_specification):
        anharmonic = True
        anharmonic_type = 'Anharmonic: Freq GVPT2, Int DVPT2, w/ 1-1 checks and forced removal'
        print('    Anharmonic GVPT2 corrections to vibrational frequencies and DVPT2 intensities')
        print('    Fermi resonance checks and 1-1 resonance checks are performed.')
        print('    Upon discovering a 1-1 resonance for vi - vj, all such terms are removed.')
        print('    Variational correction is done for frequencies, but not for intensities.')
    else:
        anharmonic = False
        anharmonic_type = False

    dangerous_modes = []

    for i in range(range_snapshots):
        if (num_snapshots == 1):
            tensor_location = names[0] + names[1]
            mol_location = names[0] + names[2]
        else:

            snap = i + names[1]

            if (snap in names[6]):
                continue

            if (print_level > 0):
                print('\n')
                print('Snapshot nr', i)

            if ('No FraME' in run_specification):
                tensor_file = names[3] + '_' + names[4] + '_' + str(snap) + '.rsp_tensor'

            elif ('FraME' in run_specification):

                tensor_file = names[3] + '_' + names[4] + '_' + str(snap) + '_' + names[5] + '_' + \
                              str(snap) + '.rsp_tensor'

            molecule_file = names[4] + '_' + str(snap) + '.mol'

            tensor_location = names[0] + tensor_file
            mol_location = names[0] + molecule_file

        # Note that raman intensities here contains all configurations.  These are to be considered 
        # as if they were different properties, and therefore split up
        properties = get_vibrational_frequencies_and_intensities(tensor_location, mol_location, \
                                                                 spectroscopy_types, \
                                                                 spectroscopy_specifications, \
                                                                 print_level, temperature, \
                                                                 outproj, anharmonic_type, harmonic_frequency_limits)

        if (i == 0):
            num_modes = len(properties.frequencies.harmonic)
        else:
            if (len(properties.frequencies.harmonic) != num_modes):
                print('\n')
                print('Error in SpectroscPy_run')
                print('Not all the snapshots have the same amount of vibrational modes')
                print('Do all the rsp_tensor files belong to the same molecule?')
                exit()

        for j in range(num_modes):
            if ((properties.frequencies.harmonic[j] == 0.0 or properties.frequencies.harmonic[j].imag != 0.0) and not i in dangerous_modes):
                dangerous_modes.append(j)

        all_frequencies.harmonic.append(properties.frequencies.harmonic)
        if (anharmonic):
            all_frequencies.fundamental.append(properties.frequencies.fundamental)
            all_frequencies.overtones.append(properties.frequencies.overtones)
            all_frequencies.combotones.append(properties.frequencies.combotones)

        if ('IR' in spectroscopy_types):
            all_ir_intensities.harmonic.append(properties.ir.harmonic)
            if (anharmonic):
                all_ir_intensities.fundamental.append(properties.ir.fundamental)
                all_ir_intensities.overtones.append(properties.ir.overtones)
                all_ir_intensities.combotones.append(properties.ir.combotones)

        if ('Raman' in spectroscopy_types):
            if (i == 0):
                num_raman_configs = len(properties.raman.harmonic)
                for j in range(num_raman_configs):
                    all_raman_intensities.harmonic.append([])

                if (anharmonic):
                    for j in range(num_raman_configs):
                        all_raman_intensities.fundamental.append([])
                        all_raman_intensities.overtones.append([])
                        all_raman_intensities.combotones.append([])

            else:
                if (num_raman_configs != len(properties.raman.harmonic)):
                    print('NOT ALL rsp_tensors HAVE THE SAME AMOUNT OF GFF CONFIGS!! GO THROUGH')
                    print('YOUR .dal FILES AND CHECK THAT THEY ARE ALL IDENTICAL')

            # Reorganize to total array: num_raman_configs, num_snapshots, num_intensities
            for j in range(num_raman_configs):
                all_raman_intensities.harmonic[j].append(properties.raman.harmonic[j])

            if (anharmonic):
                for j in range(num_raman_configs):
                    all_raman_intensities.fundamental[j].append(properties.raman.fundamental[j])
                    all_raman_intensities.overtones[j].append(properties.raman.overtones[j])
                    all_raman_intensities.combotones[j].append(properties.raman.combotones[j])

        if ('Hyper-Raman' in spectroscopy_types):
            if (i == 0):
                num_hyperraman_configs = len(properties.input_hyperraman_frequencies)
                for j in range(num_hyperraman_configs):
                    all_hR_vv_intensities.harmonic.append([])
                    all_hR_hv_intensities.harmonic.append([])

                if (anharmonic):
                    for j in range(num_hyperraman_configs):
                        all_hR_vv_intensities.fundamental.append([])
                        all_hR_hv_intensities.fundamental.append([])
                        all_hR_vv_intensities.overtones.append([])
                        all_hR_hv_intensities.overtones.append([])
                        all_hR_vv_intensities.combotones.append([])
                        all_hR_hv_intensities.combotones.append([])

            else:
                if (num_hyperraman_configs != len(properties.hyper_raman_vv.harmonic)):
                    print('NOT ALL rsp_tensors HAVE THE SAME AMOUNT OF GFFF CONFIGS!! GO THROUGH')
                    print('YOUR .dal FILES AND CHECK THAT THEY ARE ALL IDENTICAL')

            # Reorganize to total array: num_hyperraman_configs, num_snapshots, num_intensities
            for j in range(num_hyperraman_configs):
                all_hR_vv_intensities.harmonic[j].append(properties.hyper_raman_vv.harmonic[j])
                all_hR_hv_intensities.harmonic[j].append(properties.hyper_raman_hv.harmonic[j])

            if (anharmonic):
                for j in range(num_hyperraman_configs):
                    all_hR_vv_intensities.fundamental[j].append(properties.hyper_raman_vv.fundamental[j])
                    all_hR_hv_intensities.fundamental[j].append(properties.hyper_raman_hv.fundamental[j])
                    all_hR_vv_intensities.overtones[j].append(properties.hyper_raman_vv.overtones[j])
                    all_hR_hv_intensities.overtones[j].append(properties.hyper_raman_hv.overtones[j])
                    all_hR_vv_intensities.combotones[j].append(properties.hyper_raman_vv.combotones[j])
                    all_hR_hv_intensities.combotones[j].append(properties.hyper_raman_hv.combotones[j])

    if (dangerous_modes != []):
        print('DANGEROUS MODES')
        print('The following modes have frequencies that are either zero or have nonzero imaginary')
        print('parts.  Use of any of these frequencies or intensities should be done with caution.')
        for i in range(len(dangerous_modes)):
            print(dangerous_modes[i])

    # AVERAGED VAULES PRINTING PART
    average_harmonic_frequencies = average_over_snapshots(all_frequencies.harmonic)
    if (anharmonic):
        average_fundamental = average_over_snapshots(all_frequencies.fundamental)
        average_overtones = average_over_snapshots(all_frequencies.overtones)
        average_combotones = average_over_snapshots(all_frequencies.combotones)
    else:
        average_fundamental = []
        average_overtones = []
        average_combotones = []

    average_frequencies = anharmonicProperty(average_harmonic_frequencies, \
                                             average_fundamental, \
                                             average_overtones, \
                                             average_combotones)
    if (num_snapshots > 1):
        std_harmonic_frequencies = \
            get_standard_deviation(average_frequencies.harmonic, all_frequencies.harmonic)

    if ('IR' in spectroscopy_types):
        average_harmonic_ir_intensities = average_over_snapshots(all_ir_intensities.harmonic)
        if (anharmonic):
            average_ir_fundamental = average_over_snapshots(all_ir_intensities.fundamental)
            average_ir_overtones = average_over_snapshots(all_ir_intensities.overtones)
            average_ir_combotones = average_over_snapshots(all_ir_intensities.combotones)
        else:
            average_ir_fundamental = []
            average_ir_overtones = []
            average_ir_combotones = []

        average_ir_intensities = anharmonicProperty(average_harmonic_ir_intensities, \
                                                    average_ir_fundamental, \
                                                    average_ir_overtones, \
                                                    average_ir_combotones)
        if (num_snapshots > 1):
            std_harmonic_ir = \
                get_standard_deviation(average_ir_intensities.harmonic, all_ir_intensities.harmonic)
    else:
        average_ir_intensities = anharmonicProperty([], [], [], [])

    if ('Raman' in spectroscopy_types):
        average_raman_harmonic = np.zeros((num_raman_configs, num_modes))

        for i in range(num_raman_configs):
            average_raman_harmonic[i] = average_over_snapshots(all_raman_intensities.harmonic[i])
        if (anharmonic):
            average_raman_fundamental = np.zeros((num_raman_configs, num_modes))
            average_raman_overtones = np.zeros((num_raman_configs, num_modes))
            average_raman_combotones = np.zeros((num_raman_configs, num_modes, num_modes))

            for i in range(num_raman_configs):
                average_raman_fundamental[i] = \
                    average_over_snapshots(all_raman_intensities.fundamental[i])
                average_raman_overtones[i] = \
                    average_over_snapshots(all_raman_intensities.overtones[i])
                average_raman_combotones[i] = \
                    average_over_snapshots(all_raman_intensities.combotones[i])
        else:
            average_raman_fundamental = []
            average_raman_overtones = []
            average_raman_combotones = []

        average_raman_intensities = anharmonicProperty(average_raman_harmonic, \
                                                       average_raman_fundamental, \
                                                       average_raman_overtones, \
                                                       average_raman_combotones)
        if (num_snapshots > 1):
            std_harmonic_raman = np.zeros((num_raman_configs, num_modes))
            for i in range(num_raman_configs):
                std_harmonic_raman[i] = \
                    get_standard_deviation(average_raman_intensities.harmonic[i], \
                                           all_raman_intensities.harmonic[i])
    else:
        average_raman_intensities = anharmonicProperty([], [], [], [])

    if ('Hyper-Raman' in spectroscopy_types):
        average_hR_vv_harmonic = np.zeros((num_hyperraman_configs, num_modes))
        average_hR_hv_harmonic = np.zeros((num_hyperraman_configs, num_modes))
        for i in range(num_hyperraman_configs):
            average_hR_vv_harmonic[i] = \
                average_over_snapshots(all_hR_vv_intensities.harmonic[i])
            average_hR_hv_harmonic[i] = \
                average_over_snapshots(all_hR_hv_intensities.harmonic[i])

        if (anharmonic):
            average_hR_vv_fundamental = np.zeros((num_hyperraman_configs, num_modes))
            average_hR_vv_overtones = np.zeros((num_hyperraman_configs, num_modes))
            average_hR_vv_combotones = np.zeros((num_hyperraman_configs, num_modes, num_modes))

            average_hR_hv_fundamental = np.zeros((num_hyperraman_configs, num_modes))
            average_hR_hv_overtones = np.zeros((num_hyperraman_configs, num_modes))
            average_hR_hv_combotones = np.zeros((num_hyperraman_configs, num_modes, num_modes))

            for i in range(num_hyperraman_configs):
                average_hR_vv_fundamental[i] = \
                    average_over_snapshots(all_hR_vv_intensities.fundamental[i])
                average_hR_vv_overtones[i] = \
                    average_over_snapshots(all_hR_vv_intensities.overtones[i])
                average_hR_vv_combotones[i] = \
                    average_over_snapshots(all_hR_vv_intensities.combotones[i])

                average_hR_hv_fundamental[i] = \
                    average_over_snapshots(all_hR_hv_intensities.fundamental[i])
                average_hR_hv_overtones[i] = \
                    average_over_snapshots(all_hR_hv_intensities.overtones[i])
                average_hR_hv_combotones[i] = \
                    average_over_snapshots(all_hR_hv_intensities.combotones[i])
        else:
            average_hR_vv_fundamental = []
            average_hR_vv_overtones = []
            average_hR_vv_combotones = []

            average_hR_hv_fundamental = []
            average_hR_hv_overtones = []
            average_hR_hv_combotones = []

        average_hR_vv_intensities = anharmonicProperty(average_hR_vv_harmonic, \
                                                       average_hR_vv_fundamental, \
                                                       average_hR_vv_overtones, \
                                                       average_hR_vv_combotones)
        average_hR_hv_intensities = anharmonicProperty(average_hR_hv_harmonic, \
                                                       average_hR_hv_fundamental, \
                                                       average_hR_hv_overtones, \
                                                       average_hR_hv_combotones)

    else:
        average_hR_vv_intensities = anharmonicProperty([], [], [], [])
        average_hR_hv_intensities = anharmonicProperty([], [], [], [])

    # Set captions for graphs and tables
    mode_caption, latex_mode_caption, mode_header_sting, mode_format_string, mode_std_format = \
        get_mode_captions(spectroscopy_specifications)

    if ('Symbolic labels' in run_specification):
        x_label = latex_mode_caption
    else:
        x_label = mode_caption

    if ('IR' in spectroscopy_types):
        IR_caption, IR_plot_caption, latex_ir_caption, header_format_string, format_string, ir_std_format = \
            get_ir_captions(spectroscopy_specifications)

        if ('Symbolic labels' in run_specification):
            ir_y_label = latex_ir_caption
        else:
            ir_y_label = IR_plot_caption

    if ('Raman' in spectroscopy_types):
        raman_caption, raman_plot_caption, latex_raman_caption = \
            get_raman_captions(spectroscopy_specifications)

        if ('Symbolic labels' in run_specification):
            raman_y_label = latex_raman_caption
        else:
            raman_y_label = raman_plot_caption

    if ('Hyper-Raman' in spectroscopy_types):
        vv_hR_caption, hv_hR_caption, vv_hR_plot_caption, hv_hR_plot_caption, vv_hR_latex, \
            hv_hR_latex, hR_caption, hR_plot_caption, hR_latex = \
                get_hR_captions(spectroscopy_specifications)

        if ('Symbolic labels' in run_specification):
            vv_hR_y_label = vv_hR_latex
            hv_hR_y_label = hv_hR_latex
            hR_y_label = hR_latex
        else:
            vv_hR_y_label = vv_hR_plot_caption
            hv_hR_y_label = hv_hR_plot_caption
            hR_y_label = hR_plot_caption

    print('\n')
    print('***************************************************************************************')
    print('AVERAGE SPECTROSCOPIC DATA')

    if (not ('IR' in spectroscopy_types) and not ('Raman' in spectroscopy_types) and \
        not ('Hyper-Raman' in spectroscopy_types)):

        if (anharmonic):
            print('Anharmonic corrected frequencies')
            print('\n')
            print('Fundamental')
            print(('%4s' + '%18s' + '%18s') %('Mode', 'Harmonic', 'Anharmonic'))
            for i in range(num_modes):
                print(('%2d' + '%19.6f' + '%19.6f') %(i, average_frequencies.harmonic[i], \
                                                      average_frequencies.fundamental[i]))
            print('\n')

            print('Overtones')
            print(('%4s' + '%18s' + '%18s') %('Mode', 'Harmonic', 'Anharmonic'))
            for i in range(num_modes):
                print(('%2d' + '%19.6f' + '%19.6f') %(i, average_frequencies.harmonic[i]*2, \
                                                      average_frequencies.overtones[i]))
            print('\n')

            print('Combotones')
            print(('%5s' + '%18s' + '%18s') %('Modes', 'Harmonic', 'Anharmonic'))
            for i in range(num_modes):
                for j in range(i):
                    print(('%2d' + '%2d' + '%19.6f' + '%19.6f') %(i, j, \
                        average_frequencies.harmonic[i] + average_frequencies.harmonic[j], \
                        average_frequencies.combotones[i][j]))
            print('\n')

        else:
            if (num_snapshots == 1):
                print(('%4s' + mode_header_sting) %('Mode', mode_caption))
                for i in range(num_modes):
                    print(('%2d' + mode_format_string) %(i, average_frequencies.harmonic[i]))
            else:
                print(('%4s' + mode_header_sting) %('Mode', mode_caption))
                for i in range(num_modes):
                    print(('%2d' + mode_format_string + '%1s' + mode_format_string + '%1s') \
                    %(i, average_frequencies.harmonic[i], '(', std_harmonic_frequencies[i], ')'))
            print('\n')

    if ('IR' in spectroscopy_types):
        if (anharmonic):

            print('\n')
            print('Frequencies: ', mode_caption)
            print('Intensities: ', IR_caption)
            print('Fundamental')
            print(('%4s' + '%18s' + '%18s' + '%17s' + '%17s') %('Mode', 'Harmonic freq.', \
                                                                'Anharmonic freq.', \
                                                                'Harmonic I', 'Anharmonic I'))
            for i in range(num_modes):
                print(('%2d' + mode_format_string + mode_format_string + format_string + \
                       format_string) \
                    %(i, average_frequencies.harmonic[i], average_frequencies.fundamental[i], \
                      average_ir_intensities.harmonic[i], average_ir_intensities.fundamental[i]))
            print('\n')

            print('Overtones')
            print(('%4s' + '%18s' + '%18s' + '%17s' + '%17s') %('Mode', 'Harmonic freq.', \
                                                                'Anharmonic freq.', \
                                                                'Harmonic I', 'Anharmonic I'))
            for i in range(num_modes):
                print(('%2d' + mode_format_string + mode_format_string + '%17s' + format_string) \
                    %(i, average_frequencies.harmonic[i]*2, average_frequencies.overtones[i], \
                      ' -     ', average_ir_intensities.overtones[i]))

            print('\n')

            print('Combotones')
            print(('%5s' + '%18s' + '%18s' + '%17s' + '%17s') %('Modes', 'Harmonic freq.', \
                                                                'Anharmonic freq.', \
                                                                'Harmonic I', 'Anharmonic I'))
            for i in range(num_modes):
                for j in range(i):
                    print(('%2d' + '%2d' + mode_format_string + mode_format_string + '%17s' + \
                          format_string) \
                         %(i, j, average_frequencies.harmonic[i] + \
                           average_frequencies.harmonic[j], \
                           average_frequencies.combotones[i][j],  ' -     ', \
                           average_ir_intensities.combotones[i][j]))
            print('\n')

        else:
            if (num_snapshots == 1):
                print(('%4s' + mode_header_sting + header_format_string) %('Mode', mode_caption, \
                       IR_caption))
                for i in range(num_modes):
                    print(('%2d' + mode_format_string + format_string) %(i, \
                           average_frequencies.harmonic[i], average_ir_intensities.harmonic[i]))
            else:
                print(('%4s %5s' + mode_header_sting + '%7s' + header_format_string) \
                    %('Mode', ' ', mode_caption, ' ', IR_caption))
                for i in range(num_modes):
                    print(('%2d' + mode_format_string + '%2s' + mode_std_format + '%1s' + \
                           format_string + '%2s' + ir_std_format + '%1s') %(i, \
                           average_frequencies.harmonic[i], '(', std_harmonic_frequencies[i], \
                           ')',   average_ir_intensities.harmonic[i], '(', std_harmonic_ir[i], ')'))
            print('\n')

    if ('Raman' in spectroscopy_types):

        if (anharmonic):

            for i in range(num_raman_configs):
                print('\n')
                print('Input frequency: ', properties.input_raman_frequencies[i])
                print('Frequencies: ', mode_caption)
                print('Intensities: ', raman_caption)
                print('Fundamental')
                print(('%4s' + '%18s' + '%19s' + '%17s' + '%19s') %('Mode', 'Harmonic freq.', \
                                                                    'Anharmonic freq.', \
                                                                    'Harmonic I', 'Anharmonic I'))
                for j in range(num_modes):
                    print(('%2d' + mode_format_string + mode_format_string + '%20.10E' + \
                          '%20.10E') \
                        %(j, average_frequencies.harmonic[j], average_frequencies.fundamental[j], \
                          average_raman_intensities.harmonic[i][j], \
                          average_raman_intensities.fundamental[i][j]))
                print('\n')

                print('Overtones')
                print(('%4s' + '%18s' + '%18s' + '%17s' + '%17s') %('Mode', 'Harmonic freq.', \
                                                                    'Anharmonic freq.', \
                                                                    'Harmonic I', 'Anharmonic I'))
                for j in range(num_modes):
                    print(('%2d' + mode_format_string + mode_format_string + '%17s' + '%20.10E') \
                           %(j, average_frequencies.harmonic[j]*2, \
                            average_frequencies.overtones[j], \
                             ' -     ', average_raman_intensities.overtones[i][j]))
                print('\n')

                print('Combotones')
                print(('%5s' + '%18s' + '%18s' + '%17s' + '%17s') %('Modes', 'Harmonic freq.', \
                                                                    'Anharmonic freq.', \
                                                                    'Harmonic I', 'Anharmonic I'))
                for j in range(num_modes):
                    for k in range(j):
                        print(('%2d' + '%2d' + mode_format_string + mode_format_string + '%17s' + \
                          '%20.10E') \
                         %(j, k, average_frequencies.harmonic[j] + \
                           average_frequencies.harmonic[k], \
                           average_frequencies.combotones[j][k],  ' -     ', \
                           average_raman_intensities.combotones[i][j][k]))
                print('\n')
        else:

            if (num_snapshots == 1):
                print(('%4s' + mode_header_sting + '%43s') %('Mode', mode_caption, raman_caption))
                print('%20s' %(' '), '\t'.join(['%9s %6.5E' % ('Input waven: ', val) for val in \
                                                properties.input_raman_frequencies ]))
                for i in range(num_modes):
                    print(('%2d' + mode_format_string) %(i, average_frequencies.harmonic[i]), \
                           '\t'.join(['%20.10E' % average_raman_intensities.harmonic[j][i] \
                                      for j in range(num_raman_configs)]))
            else:
                print(('%4s %5s' + mode_header_sting + '%43s') %('Mode', ' ', mode_caption, \
                       raman_caption))
                print('%30s' %(' '), '\t'.join(['%19s %6.5E' % ('Input waven: ', val) for val in \
                                                properties.input_raman_frequencies ]))
                for i in range(num_modes):
                    print(('%2d' + mode_format_string + '%2s' + mode_std_format + '%1s') \
                        %(i, average_frequencies.harmonic[i], '(', std_harmonic_frequencies[i], \
                           ')'), \
                           '\t'.join([('%20.10E' + '%2s' + '%6.3E' + '%1s') \
                            % (average_raman_intensities.harmonic[j][i], '(', \
                               std_harmonic_raman[j][i], ')')  \
                                      for j in range(num_raman_configs)]))
        print('\n')

    if ('Hyper-Raman' in spectroscopy_types):

        if (anharmonic):

            for i in range(num_hyperraman_configs):
                print('\n')
                print('Input frequency: ', properties.input_hyperraman_frequencies[i])
                print('Frequencies: ', mode_caption)
                print('Intensities: ', hR_caption)
                print('Fundamental')

                print(('%4s' + '%18s' + '%19s' + '%15s' + '%19s' + '%16s' + '%19s') %('Mode', \
                       'Harmonic freq.', 'Anharmonic freq.', 'VV Harmonic I', 'VV Anharmonic I', \
                       'HV Harmonic I', 'HV Anharmonic I'))
                for j in range(num_modes):
                    print(('%2d' + mode_format_string + mode_format_string + '%18.10E' + \
                           '%18.10E' + \
                           '%18.10E' + '%18.10E') \
                        %(j, average_frequencies.harmonic[j], average_frequencies.fundamental[j], \
                          average_hR_vv_intensities.harmonic[i][j], \
                          average_hR_vv_intensities.fundamental[i][j], \
                          average_hR_hv_intensities.harmonic[i][j], \
                          average_hR_hv_intensities.fundamental[i][j]))
                print('\n')

                print('Overtones')
                print(('%4s' + '%18s' + '%19s' + '%15s' + '%19s' + '%16s' + '%19s') %('Mode', \
                       'Harmonic freq.', 'Anharmonic freq.', 'VV Harmonic I', 'VV Anharmonic I', \
                       'HV Harmonic I', 'HV Anharmonic I'))
                for j in range(num_modes):
                    print(('%2d' + mode_format_string + mode_format_string + '%17s' + '%18.10E' + \
                           '%17s' + '%18.10E') \
                           %(j, average_frequencies.harmonic[j]*2, \
                             average_frequencies.overtones[j], \
                             ' -     ', average_hR_vv_intensities.overtones[i][j], ' -     ', \
                             average_hR_hv_intensities.overtones[i][j]))
                print('\n')

                print('Combotones')
                print(('%5s' + '%18s' + '%19s' + '%15s' + '%19s' + '%16s' + '%19s') %('Mode', \
                       'Harmonic freq.', 'Anharmonic freq.', 'VV Harmonic I', 'VV Anharmonic I', \
                       'HV Harmonic I', 'HV Anharmonic I'))
                for j in range(num_modes):
                    for k in range(j):
                        print(('%2d' + '%2d' + mode_format_string + mode_format_string + '%16s' + \
                               '%19.10E' + '%16s' + '%19.10E') \
                         %(j, k, average_frequencies.harmonic[j] + \
                           average_frequencies.harmonic[k], \
                           average_frequencies.combotones[j][k],  ' -     ', \
                           average_hR_hv_intensities.combotones[i][j][k], ' -     ', \
                           average_hR_vv_intensities.combotones[i][j][k]))
                print('\n')

        else:
            print(('%4s' + mode_header_sting + '%55s') %('Mode', mode_caption, vv_hR_caption))
            print('%20s' %(' '), '\t'.join(['%20s %3.2E' % ('Input waven: ', val) for val in \
                                        properties.input_hyperraman_frequencies]))
            for i in range(num_modes):
                print(('%2d' + mode_format_string) %(i, average_frequencies.harmonic[i]), \
                                                     '\t'.join(['%25.10E' % \
                                                     average_hR_vv_intensities.harmonic[j][i] \
                                                     for j in range(num_hyperraman_configs)]))

            print('\n')

            print(('%4s' + mode_header_sting + '%55s') %('Mode', mode_caption, hv_hR_caption))
            print('%20s' %(' '), '\t'.join(['%20s %3.2E' % ('Input waven: ', val) for val in \
                                        properties.input_hyperraman_frequencies]))
            for i in range(num_modes):
                print(('%2d' + mode_format_string) %(i, average_frequencies.harmonic[i]), \
                                                     '\t'.join(['%25.10E' % \
                                                     average_hR_hv_intensities.harmonic[j][i] \
                                                     for j in range(num_hyperraman_configs)]))
        print('\n')

    # PLOT
    plot_spectrum = False
    plot_commands = []
    for i in range(len(run_specification)):
        if ('Plot' in run_specification[i]):
            plot_spectrum = True
            plot_commands.append(run_specification[i])

    if (plot_spectrum):
        cauchy_prefactor = get_cauchy_prefactor(spectroscopy_specifications)

        if (cauchy_type == 'Discrete'):
            print('Only a stick spectrum of discrete peaks will be made')
            cauchy_type_or_value = cauchy_type
        elif (isinstance(cauchy_type, float) or isinstance(cauchy_type, int)):
            cauchy_type_or_value = float(cauchy_type)
            print('Fixed broadening factor, ', cauchy_type_or_value)
        elif (cauchy_type == 'WS'):
            cauchy_type_or_value = cauchy_type
            print('Width determined broadening factor')
        elif (cauchy_type == 'WA'):
            cauchy_type_or_value = cauchy_type
            print('Width determined broadening factor, but average values')
            print('\n')
            print('************************************************************')
            print('I do not know if this one works yet')
            print('************************************************************')
        else:
            cauchy_type_or_value = 0.001*max(all_frequencies.harmonic[0])
            print('Fixed broadening factor, ', cauchy_type_or_value)

    for i in range(len(plot_commands)):
        if (anharmonic):
            if ('Plot IR' == plot_commands[i] or \
                'Plot IR and all Raman together' == plot_commands[i] \
                or 'Plot IR and individual Raman together' == plot_commands[i]):

                spectrum_file = names[0] + 'anharmonic_ir.png'
                anharmonic_visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                                              all_frequencies, all_ir_intensities, x_label, \
                                              ir_y_label, spectrum_file, spectral_boundaries, ticker_distance)

            if ('Plot Raman separately' == plot_commands[i] or \
                'Plot Raman together' == plot_commands[i] \
                or 'Plot IR and all Raman together' == plot_commands[i] \
                or 'Plot IR and individual Raman together' == plot_commands[i]):

                for j in range(num_raman_configs):
                    spectrum_file = names[0] + 'anharmonic_raman_' + \
                                    str(('%4.1E' %properties.input_raman_frequencies[j])) + '.png'

                    curr_raman_intensities = \
                        anharmonicProperty(all_raman_intensities.harmonic[j], \
                                           all_raman_intensities.fundamental[j], \
                                           all_raman_intensities.overtones[j], \
                                           all_raman_intensities.combotones[j])
                    anharmonic_visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                                                  all_frequencies, curr_raman_intensities, \
                                                  x_label, raman_y_label, spectrum_file, \
                                                  spectral_boundaries, ticker_distance)

            if ('Plot all Hyper-Raman separately' == plot_commands[i] or \
                'Plot Hyper-Raman VV and HV separately' == plot_commands[i] or \
                'Plot all Hyper-Raman together' == plot_commands[i]):

                for j in range(num_hyperraman_configs):
                    # VV
                    spectrum_file = \
                        names[0] + 'anharmonic_hyperraman_vv_' + \
                        str(('%4.1E' %properties.input_hyperraman_frequencies[j])) + '.png'

                    curr_raman_intensities = \
                        anharmonicProperty(all_hR_vv_intensities.harmonic[j], \
                                           all_hR_vv_intensities.fundamental[j], \
                                           all_hR_vv_intensities.overtones[j], \
                                           all_hR_vv_intensities.combotones[j])
                    anharmonic_visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                                                  all_frequencies, curr_raman_intensities, \
                                                  x_label, vv_hR_caption, spectrum_file, \
                                                  spectral_boundaries, ticker_distance)
                    # HV
                    spectrum_file = \
                        names[0] + 'anharmonic_hyperraman_hv_' + \
                        str(('%4.1E' %properties.input_hyperraman_frequencies[j])) + '.png'

                    curr_raman_intensities = \
                        anharmonicProperty(all_hR_hv_intensities.harmonic[j], \
                                           all_hR_hv_intensities.fundamental[j], \
                                           all_hR_hv_intensities.overtones[j], \
                                           all_hR_hv_intensities.combotones[j])
                    anharmonic_visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                                                  all_frequencies, curr_raman_intensities, \
                                                  x_label, hv_hR_caption, spectrum_file, \
                                                  spectral_boundaries, ticker_distance)

        if (('Plot IR' == plot_commands[i]) or \
            ('Plot IR and all Raman together' == plot_commands[i]) or \
            ('Plot Raman together' == plot_commands[i])):

            if ('Plot IR' == plot_commands[i]):
                print('IR spectrum')
                spectrum_file = names[0] + 'ir_spectrum.png'

                all_intensities = np.copy([all_ir_intensities.harmonic])
                y_label = np.copy([ir_y_label])
                legends = 0
                plotting_info = []

            if (('Plot IR and all Raman together' == plot_commands[i]) or \
               ('Plot Raman together' == plot_commands[i])):

                legends = []

                if ('Plot IR and all Raman together' == plot_commands[i]):

                    print('IR and Raman spectrum')
                    print('Be aware that the graphs will be scaled')

                    plotting_info = []
                    if (num_raman_configs == 1):
                        # FIX this!! Should be the same as for IR and individual Raman together
                        y_label = []
                        y_label.append('IR')
                        y_label.append('Raman')
                    else:
                        y_label = []

                    all_intensities = []
                    max_ir = 0.0
                    for j in range(num_snapshots):
                        if (max(all_ir_intensities.harmonic[j]) > max_ir):
                            max_ir = max(all_ir_intensities.harmonic[j])

                    max_raman = 0.0
                    for j in range(num_raman_configs):
                        for k in range(num_snapshots):
                            if (max(all_raman_intensities.harmonic[j][k]) > max_raman):
                                max_raman = max(all_raman_intensities.harmonic[j][k])

                    all_intensities.append(np.multiply(all_ir_intensities.harmonic, 1/max_ir))
                    for j in range(num_raman_configs):
                        all_intensities.append(np.multiply(all_raman_intensities.harmonic[j], \
                                                           1/max_raman))

                    legends.append('IR')

                    spectrum_file = names[0] + 'ir_raman_all_inp_spectrum.png'

                for j in range(num_raman_configs):
                    tmp_caption = 'Raman freq: ' + \
                        str(('%4.1E' %properties.input_raman_frequencies[j]))
                    legends.append(tmp_caption)

                if ('Plot Raman together' == plot_commands[i]):
                    print('Raman spectrum')
                    print('Be aware that the graphs will be scaled')

                    spectrum_file = names[0] + 'raman_spectrum_all_inp.png'

                    all_intensities = np.copy(all_raman_intensities.harmonic)
                    plotting_info = ['all one type']
                    y_label = raman_y_label

            visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, all_frequencies.harmonic, \
                               all_intensities, x_label, y_label, legends, spectrum_file, \
                               spectral_boundaries, plotting_info, ticker_distance)


        if (('Plot IR and individual Raman together' == plot_commands[i]) or \
            ('Plot Raman separately' == plot_commands[i])):

            if ('Plot IR and individual Raman together' == plot_commands[i]):

                print('IR and individual Raman spectra')
                print('Be aware that the graphs will be scaled')

                name_base = names[0] + 'ir_raman_'

                max_ir = 0.0
                for j in range(num_snapshots):
                    if (max(all_ir_intensities.harmonic[j]) > max_ir):
                        max_ir = max(all_ir_intensities.harmonic[j])

            if ('Plot Raman separately' == plot_commands[i]):
                print('Individual Raman spectra')

                name_base = names[0] + 'raman_'

            for j in range(num_raman_configs):

                all_intensities = []
                y_label = []
                legends = []

                spectrum_file = name_base + \
                    str(('%4.1E' %properties.input_raman_frequencies[j])) + '_spectrum.png'

                if ('Plot IR and individual Raman together' == plot_commands[i]):
                    max_raman = 0.0
                    for k in range(num_snapshots):
                        if (max(all_raman_intensities.harmonic[j][k]) > max_raman):
                            max_raman = max(all_raman_intensities.harmonic[j][k])

                    all_intensities.append(all_ir_intensities.harmonic)
                    all_intensities.append(all_raman_intensities.harmonic[j])

                    y_label.append(ir_y_label)
                    y_label.append(raman_y_label)

                    legends.append('IR')
                    legends.append('Raman')

                if ('Plot Raman separately' == plot_commands[i]):
                    print('Input wavenumber: ', properties.input_raman_frequencies[j])

                    all_intensities.append(all_raman_intensities.harmonic[j])
                    y_label.append(raman_y_label)
                    legends = 0

                plotting_info = []
                visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                                   all_frequencies.harmonic, all_intensities, x_label,  y_label, \
                                   legends, spectrum_file, spectral_boundaries, plotting_info, ticker_distance)

        if ('Plot all Hyper-Raman separately' == plot_commands[i]):

            for j in range(num_hyperraman_configs):
                print('Input frequency: ', '%4.1E' %properties.input_hyperraman_frequencies[j])
                tmp_y_label = vv_hR_y_label
                tmp_name = 'hyperraman_vv_freq_' + \
                    str(('%4.1E' %properties.input_hyperraman_frequencies[j])) + '.svg'

                visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                                   all_frequencies.harmonic, [all_hR_vv_intensities.harmonic[j]], \
                                   x_label, [tmp_y_label], [], tmp_name, spectral_boundaries, [], ticker_distance)

                tmp_y_label = hv_hR_y_label
                tmp_name = 'hyperraman_hv_freq_' + \
                    str(('%4.1E' %properties.input_hyperraman_frequencies[j])) + '.svg'

                visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                                   all_frequencies.harmonic, [all_hR_hv_intensities.harmonic[j]], \
                                   x_label, [tmp_y_label], [], tmp_name, spectral_boundaries, [], ticker_distance)

        if ('Plot Hyper-Raman VV and HV separately' == plot_commands[i]):
            legends = []
            for j in range(num_hyperraman_configs):
                tmp_legend = 'Input freq: ' + \
                    str(('%4.1E' %properties.input_hyperraman_frequencies[j]))
                legends.append(tmp_legend)

            visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                               all_frequencies.harmonic, all_hR_vv_intensities.harmonic, \
                               x_label, [vv_hR_y_label, ''], legends, \
                               'vv_hyperraman.svg', spectral_boundaries, [], ticker_distance)

            visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                               all_frequencies.harmonic, all_hR_hv_intensities.harmonic, \
                               x_label, [hv_hR_y_label, ''], legends, \
                               'hv_hyperraman.svg', spectral_boundaries, [], ticker_distance)

        if ('Plot all Hyper-Raman together' == plot_commands[i]):
            legends = []
            all_hyperraman_intensities = []
            for j in range(num_hyperraman_configs):
                tmp_legend = 'VV Input freq: ' + \
                    str(('%4.1E' %properties.input_hyperraman_frequencies[j]))
                legends.append(tmp_legend)
                tmp_legend = 'HV Input freq: ' + \
                    str(('%4.1E' %properties.input_hyperraman_frequencies[j]))
                legends.append(tmp_legend)

                all_hyperraman_intensities.append(all_hR_vv_intensities.harmonic[j])
                all_hyperraman_intensities.append(all_hR_hv_intensities.harmonic[j])

            visualize_spectrum(cauchy_type_or_value, cauchy_prefactor, \
                               all_frequencies.harmonic, all_hyperraman_intensities, x_label, \
                               hR_y_label, legends, 'all_hyperraman.svg', spectral_boundaries, \
                               ['all one type'], ticker_distance)

    # Part for wrapping up and returning the average wavenumbers and intensities.  Intensities are
    # returned in order IR, Raman, Hyper-Raman VV, Hyper-Raman HV.
    average_properties = vibrationalProperty(average_frequencies, average_ir_intensities, \
                                             properties.input_raman_frequencies, \
                                             average_raman_intensities, \
                                             properties.input_hyperraman_frequencies, \
                                             average_hR_vv_intensities, \
                                             average_hR_hv_intensities)

    return average_properties
