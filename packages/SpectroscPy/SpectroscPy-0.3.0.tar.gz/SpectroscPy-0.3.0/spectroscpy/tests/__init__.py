# SpectroscPy 0.3.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

from .test_cauchy import test_get_simple_averages, test_get_interquartile_range, test_get_gamma, \
                         test_cauchy_lincomb, test_get_standard_deviation
from .test_get_spectroscopy import test_get_vibrational_frequencies_and_intensities, \
                                   test_which_spectroscopies_to_be_calculated, \
                                   test_get_spectroscopy_indices, test_get_energy_derivatives, \
                                   test_reduced_dims, test_getting_the_subblocks
from .test_openrsp_tensor_reader import test_rspProperty, test_get_redundant_indices, \
                                        test_remove_whitespaces, test_read_openrsp_tensor_file
from .test_plotting_module import test_get_zero_padded_intensities, test_get_x_fit, test_get_sorted
from .test_transform_nc_to_nm import test_list_product_int, \
                                     test_transform_cartesian_to_normal_one_rank, \
                                     test_transform_cartesian_to_normal
from .test_vib_analysis import test_mol_is_linear, test_read_mol, test_project_out_transl_and_rot, \
                               test_get_vib_harm_freqs_and_eigvecs, test_get_vibrational_w_and_T, \
                               test_cut_at_harmonic_frequency_limits
from .test_ir import test_square_then_sum, test_qi_prefactor2, test_get_ir_intensities, \
                     test_get_harmonic_transition_moment
from .test_raman import test_get_combined_polarizabilites, test_raman_scattering_cross_section, \
                        test_get_exp_denominator, test_get_b2_term, test_get_a2_term, \
                        test_requested_unit_incident_mode, test_get_rscattering_cross_section
from .test_hyperraman import test_get_average_beta_aaa2, test_get_average_beta_baa2, \
                             test_get_hyperraman_SI_scs, test_get_hyperraman_intensities
from .test_anharmonic import test_get_X, test_get_anharm_fundamental_transition_moment, \
                             test_anharm_corrected_vibrational_energies, test_get_red_prefactor, \
                             test_transform_to_reduced_nm, test_transform_to_reduced_nm_prep, \
                             test_get_overtone_transition_moment, \
                             test_get_anharm_corrected_transition_moment
from .test_resonance_checks import test_is_fermi_resonance, test_is_11_resonance, \
                                   test_add_fermi_resonance
