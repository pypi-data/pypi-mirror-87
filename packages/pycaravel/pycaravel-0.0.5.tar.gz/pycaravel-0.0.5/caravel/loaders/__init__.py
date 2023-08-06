# coding: utf-8
##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines common loaders for imaging-genetic datasets.
"""

from ._nifti import NIFTI
from ._tsv import TSV
from ._json import JSON
from ._dwi import DWI
from ._targz import TARGZ
from ._png import PNG
