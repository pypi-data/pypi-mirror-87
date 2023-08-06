SpectroscPy is a script package developed by and containing contributions from

    Karen Oda Hjorth Minde Dundas
    Magnus Ringholm
    Yann Cornation
    Benedicte Ofstad

The package is released under a LGPL licence.

Copyright (C) 2019 Karen Oda Hjorth Minde Dundas, Magnus Ringholm, Yann Cornaton, and Benedicte Ofstad.

SpectroscPy is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SpectroscPy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SpectroscPy.  If not, see https://www.gnu.org/licenses/.

For questions, please contact on karen.o.dundas@uit.no

This package is created to postprocess the tensors resulting from an OpenRSP properties calculation.
It is especially aimed at vibrational properties, such as IR and Raman.
It will do

    1) Read the tensors and unpack them into (non-non)redundant (many-dimensional)matrices
    2) Hessian eigen-analysis to find normal modes and frequencies
    3) Transform all other property-matrices to normal coordinates
    4) Calculate intensities
    5) Plot spectra

For more info, check out the documentation folder.

*****************************************************************************************************
Dalton legacy:
The functionality in transform_nc_to_nm.py and vib_analysis.py to various extents replicates or was written on the basis of (or inspired by) corresponding functionality in the Dalton quantum chemistry program (Copyright (C) 2018 by the authors of Dalton) and unreleased code associated with Dalton/OpenRSP. In the released Dalton program, the source code files containing this functionality are DALTON/abacus/abavib.F and DALTON/abacus/hergp.F. An overview of the routines in these two scripts for which this applies and the routines in Dalton from which the functionality was replicated, based upon or inspired by, can be found in our source codes transform_nc_to_nm.py and vib_analysis.py.

Dalton is released under a GNU Lesser General Public License v2.1, which can be found at
https://gitlab.com/dalton/dalton/blob/master/LICENSE

The full sourcecode of Dalton can be found at https://gitlab.com/dalton/dalton
