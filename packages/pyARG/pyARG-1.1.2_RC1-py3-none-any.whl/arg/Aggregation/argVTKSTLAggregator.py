# HEADER
#                     arg/Aggregation/argVTKSTLAggregator.py
#               Automatic Report Generator (ARG) v. 1.0
#
# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
# Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Questions? Visit gitlab.com/AutomaticReportGenerator/arg
#
# HEADER

import os
import re

from arg.Common.argMultiFontStringHelper import argMultiFontStringHelper
from arg.DataInterface.argDataInterface import argDataInterface
from arg.Aggregation.argAggregatorBase import argAggregatorBase


class argVTKSTLAggregator(argAggregatorBase):
    """A class to aggregate information in a Exodus-specific way
    """

    def __init__(self, backend):

        # Call superclass init
        super().__init__(backend)

    def show_CAD_metadata(self, request_params, metadata):
        """Aggregate and show CAD metadata information
        """

        # Instantiate interface to CAD properties data
        parameters_root = request_params.get("parameters_root")
        regexp = re.compile(r"(.*)_parameters\.txt")
        cad_metadata = argDataInterface.factory(
            "key-value",
            os.path.join(self.Backend.Parameters.DataDir, parameters_root),
            {"expression": regexp})

        # Initialize body_lists
        all_body_lists = {}

        # Iterate over metadata items
        for metadatum in metadata:
            # Get information for current metadatum and iterate over it
            prop_info = cad_metadata.get_property_information(metadatum)
            for info_key, info_value in prop_info.iterator():
                # Initialize default values
                value = info_value[0][0]
                color, style = None, "default"

                # Handle particular values
                if value in ('', '-'):
                    color, value = "orange", "UNDEFINED"
                elif not value:
                    color, value = "red", "NOT FOUND"
                else:
                    style = "typewriter"

                # Update body list for this parameter file and value
                row = [argMultiFontStringHelper(self.Backend),
                       argMultiFontStringHelper(self.Backend)]
                row[0].append(prop_info.get_names()[0], "typewriter")
                row[1].append("{}".format(value), style, color)
                all_body_lists.setdefault(info_key, []).append(row)

        # Create one table per file
        for file_name, body_list in all_body_lists.items():
            self.Backend.add_table(
                ["CAD parameter", "parameter value"],
                body_list,
                "CAD metadata for part {}. ".format(
                    file_name.replace("_parameters.txt", '')))


    def aggregate(self, request_params):
        """Decide which aggregation operation is to be performed
        """

        # Switch between different aggregation types
        request_name = request_params["name"]
        print("[argVTKSTLAggregator] Processing {} request".format(request_name))

        # Operation show_CAD_metadata: create one table per reported CAD metadata
        if request_name == "show_CAD_metadata":

            # Get handle on data and ensure it has the right type
            metadata = request_params.get("metadata")

            # Aggregate
            if metadata:
                self.show_CAD_metadata(request_params, metadata)

        # Operation show_mesh_surface: create one figure for the entire mesh
        elif request_name.startswith("show_mesh_surface"):
            # Decide whether mesh edges are to be shown or not
            request_params["edges"] = request_name.endswith("with_edges")

            # Add specific request parameters
            request_params.setdefault("view_direction", ())

            # Get handle on data
            file_name = request_params["model"]
            data = argDataInterface.factory(
                "vtkSTL",
                os.path.join(self.Backend.Parameters.DataDir, file_name),
                request_params.get("merge", "True"))

            # Aggregate
            if data:
                self.show_mesh_surface(
                    request_params, data, file_name)
