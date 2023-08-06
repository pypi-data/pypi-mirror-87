# coding: utf-8
##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the JSON dataset loader.
"""

# Third party import
import json

# Package import
from .loader_base import LoaderBase


class JSON(LoaderBase):
    """ Define the JSON loader.
    """
    allowed_extensions = [".json", ]

    def load(self, path):
        """ A method that load a JSON file.

        Parameters
        ----------
        path: str
            the path to the JOSN file.

        Returns
        -------
        data: object
            the loaded data.
        """
        with open(path, "rt") as open_file:
            data = json.load(open_file)
        return data

    def save(self, data, outpath):
        """ A method that save the data in a JSON file.

        Parameters
        ----------
        data: object
            the data to be saved.
        outpath: str
            the path where the the data will be saved.
        """
        with open(path, "wt") as open_file:
            json.dump(data, open_file, indent=4)
