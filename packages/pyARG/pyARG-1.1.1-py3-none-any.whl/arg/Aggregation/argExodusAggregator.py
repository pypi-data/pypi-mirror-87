# HEADER
#                     arg/Aggregation/argExodusAggregator.py
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
import math
import vtk
import vtkmodules.vtkFiltersExtraction as vtkFiltersExtraction

from arg.Common import argMath
from arg.Common.argMultiFontStringHelper import argMultiFontStringHelper
from arg.DataInterface.argDataInterface import argDataInterface
from arg.Generation import argVTK, argPlot
from arg.Aggregation.argAggregatorBase import argAggregatorBase


def update_or_create_dict_in_dict(dict_of_dicts, key1, key2, value, update_fct):
    """Update or create dict entry in a dict with given primary and
       secondary keys, and value to be used by provided updating function
    """

    # Fetch possibly empty dict in dict of dicts
    sub_dict = dict_of_dicts.get(key1, {})

    # Invoke update function
    sub_dict[key2] = update_fct(sub_dict.get(key2), value)

    # Save current block quality stats
    return sub_dict


def map_composite_keys(in_dict, key1, separator):
    """Retrieve key1@...@keyN keys and corresponding values from input dict
       and build output dict with the form {key2:[key3, ..., keyN, value]}
       where @ denotes a 1-character separator
    """

    # Initialize top-level dict
    out_dict = {}

    # Iterate over input dict and filter by prefix with form key1@
    prefix = key1 + separator
    n = len(prefix)
    for key in [l for l in in_dict if l[:n] == prefix]:
        # Make sure that at least 2 keys were retrieved
        subkeys = key.split(separator)
        if len(subkeys) < 2:
            # Ignore non-composite keys
            continue

        # Use key2 as output dict key
        key2 = subkeys[1].strip().lower()
        out_dict[key2] = subkeys[2:] + [in_dict[key]]

    # Return result
    return out_dict


class argExodusAggregator(argAggregatorBase):
    """A class to aggregate information in a Exodus-specific way
    """

    def __init__(self, backend):

        # Call superclass init
        super().__init__(backend)

    def show_all_blocks(self, fig_params, data, file_names, verbose):
        """Add surface rendering figures to the document for each mesh block
           for a specified point or cell data, scalar or vector variable
        """

        do_histograms = True
        # All histogram plots have identical sizes and aspects
        histo_plot_params = {"type": "histogram", "xyratio": 3.5}

        # Retrieve mandatory figure parameters
        try:
            model_data = data["model"]
            model_file = file_names["model"]
        except:
            print("*  WARNING: ignoring request: not enough parameters to show all blocks of input model")
            return

        # Get handle on input data in VTK form
        vtk_data = model_data.get_VTK_reader_output_data(0)
        if not vtk_data:
            print("*  WARNING: ignoring request: could not read VTK data from input model", model_file)
            return

        # Retrieve or create block names and IDs
        meta_data = model_data.get_meta_information()[0]
        block_names = meta_data.get("block names", [])
        block_IDs = meta_data.get("block IDs", [])

        # Retrieve comments if provided
        comments = map_composite_keys(
            fig_params, "string", self.Backend.Parameters.KeySeparator)

        # Get handle on material and model properties when available
        block_materials = {}
        deck_file = file_names.get("deck")
        if deck_file:
            # Get handle on input deck data
            deck_data = data["deck"]

            # Select and retrieve material
            block_materials = dict(
                deck_data.get_property_information("block"))

        # No deck file was specified
        else:
            print("*  WARNING: no deck file specified when showing all blocks of input model")

        # Generate block visualizations as needed
        variable = argVTK.argVTKAttribute(
            model_data, fig_params.get("time_step", -1))
        block_id_to_flat, block_images_and_captions = argVTK.all_blocks(
            self.Backend.Parameters,
            fig_params,
            model_data,
            variable,
            model_file)

        # Build reverse lookup from flat to block indices
        block_flat_to_id = dict(
            (v, k) for k, vals in block_id_to_flat.items() for v in vals)

        # Storage for topological counts and values
        n_verts, n_elems, t_elems, q_stats, q_histo = ({} for _ in range(5))

        # Iterate over non-empty blocks and extract those
        it = vtk_data.NewIterator()
        it.GoToFirstItem()
        while not it.IsDoneWithTraversal():
            # Retrieve flat index of current non-empty leaf
            idx = it.GetCurrentFlatIndex()

            # Skip ignored blocks
            if idx not in block_flat_to_id:
                pass
            else:
                # Retrieve corresponding block ID and image file name
                b_id = block_flat_to_id[idx]

                # Extract mesh block
                extract = vtkFiltersExtraction.vtkExtractBlock()
                extract.SetInputData(vtk_data)
                extract.AddIndex(idx)
                extract.Update()
                mesh_block = extract.GetOutput().GetBlock(0)

                # Retrieve mesh block information and append it to global meta
                n_verts[b_id] = n_verts.get(b_id, 0) + mesh_block.GetNumberOfPoints()
                n_e_cur = n_elems.get(b_id, 0)
                n_e_blk = mesh_block.GetNumberOfCells()
                n_elems[b_id] = n_e_cur + n_e_blk
                elem_type_str, elem_q_type = argVTK.get_element_types(mesh_block)
                if True or elem_type_str:
                    t_elems.setdefault(b_id, elem_type_str)

                # Append mesh block quality when relevant
                if elem_q_type:
                    # Compute all desired quality statistics
                    for q_name, q_vtk in argVTK.quality_functions.items():
                        # Compute current block quality statistics and histogram
                        q_s_blk, q_h_blk = argVTK.get_mesh_quality(
                            mesh_block, q_vtk, elem_q_type, do_histograms)

                        # Update or create quality statistics for current block
                        q_stats[b_id] = update_or_create_dict_in_dict(
                            q_stats, b_id, q_name, q_s_blk,
                            argMath.aggregate_descriptive_statistics)

                        if do_histograms:
                            # Update or create quality histogram for current block
                            q_histo[b_id] = update_or_create_dict_in_dict(
                                q_histo, b_id, q_name, q_h_blk,
                                argMath.aggregate_histograms)

                # Iterate to next non-empty leaf
                it.GoToNextItem()

        # Report about ignored blocks if any
        ignored_block_keys = fig_params.get("ignore_blocks")
        if ignored_block_keys:
            # Insert paragraph on ignored blocks
            ignored_string = argMultiFontStringHelper(self.Backend)
            ignored_string.append("N.B.: ", "bold")
            ignored_string.append("Blocks with ranks or names in ", "default")
            ignored_string.append("{}".format(", ".join(ignored_block_keys)), "typewriter")
            ignored_string.append(" are ignored in this section.", "default")
            self.Backend.add_paragraph({"string": ignored_string})

        # Create per-block pages
        for b_id, (base_name, caption) in sorted(block_images_and_captions.items()):
            # Retrieve block ID and name
            block_name = block_names[block_IDs.index(b_id)]

            # Start new block summary page
            self.Backend.add_page_break()
            block_string = argMultiFontStringHelper(self.Backend)
            block_string.append("Block ", "default")
            block_string.append("{}".format(b_id), "typewriter")
            block_string.append(" (", "default")
            block_string.append(block_name, "typewriter")
            block_string.append(") summary", "default")
            self.Backend.add_subtitle({"title": block_string})

            # Initialize storage for block properties table body
            body = [
                ["number of nodes", "{}".format(n_verts[b_id])],
                ["number of elements", "{}".format(n_elems[b_id])]]

            # Start with input deck data if available
            if deck_file:
                # Look for block key in materials map
                for b_key in (block_name,
                              block_name.lower(),
                              "{}".format(b_id),
                              "block_{}".format(b_id)):
                    m_b = block_materials.get(b_key)
                    if m_b:
                        # Block was found, append corresponding material info
                        if m_b[0]:
                            material_string = argMultiFontStringHelper(self.Backend)
                            material_string.append(m_b[0], "typewriter")
                            body.append([
                                "prescribed material name",
                                material_string])
                        if len(m_b) > 1 and m_b[1]:
                            model_string = argMultiFontStringHelper(self.Backend)
                            model_string.append(m_b[1], "typewriter")
                            body.append([
                                "prescribed material model",
                                model_string])

                        # Break out as soon as block was found
                        break
                else:
                    print("*  WARNING: no material properties {} found in {}".format(
                        block_name,
                        deck_file))

            # Add block images only when element type is known
            if b_id in t_elems:
                # Add block images and element type to table body
                type_string = argMultiFontStringHelper(self.Backend)
                type_string.append(t_elems.get(b_id), "typewriter")
                body.append([
                    "type of first element in block",
                    type_string])
                self.Backend.add_figure({
                    "figure_file": base_name + ".png",
                    "caption_string": caption,
                    "width": fig_params.get("width", "12cm")})
            else:
                # Block element type is unknown
                body.append(["type of first element in block", "unknown"])

            # Generate table of block properties
            caption_string = argMultiFontStringHelper(self.Backend)
            caption_string.append("Properties of block ", "default")
            caption_string.append(block_name, "typewriter")
            if verbose:
                caption_string.append(" defined in ", "default")
                caption_string.append(model_file, "typewriter")
                if deck_file:
                    caption_string.append(" and ", "default")
                    caption_string.append(deck_file, "typewriter")
            caption_string.append('.', "default")
            self.Backend.add_table(
                ["property", "value"],
                body,
                caption_string,
                False,  # Do not do verbatim
                "hb!")  # Put table at bottom of page

            # Append per-block mesh quality information when available
            eqs = q_stats.get(b_id)
            if not eqs:
                # Mesh element type not supported by Verdict VTK
                print("*  WARNING: element type of block {} not supported by Verdict mesh quality library".format(b_id))
            else:
                # Start new block quality statistics page
                self.Backend.add_page_break()
                quality_string = argMultiFontStringHelper(self.Backend)
                quality_string.append("Block ", "default")
                quality_string.append("{}".format(b_id), "typewriter")
                quality_string.append(" (", "default")
                quality_string.append(block_name, "typewriter")
                quality_string.append(") element quality", "default")
                self.Backend.add_subtitle({"title": quality_string})

                # Create mesh quality table body
                body = []
                for q_n, q_s in eqs.items():
                    # Bail out if no quality statistics were provided
                    if not q_s:
                        continue

                    # Show standard deviation instead of variance
                    stdev = math.sqrt(q_s[3]) if q_s[3] > 0. else 0.
                    q_s[3] = stdev

                    # Compute coefficient of variation
                    q_s[4] = stdev / q_s[1] if q_s[1] > 1e-8 else float("inf")

                    # Create new row for current quality name
                    body.append([q_n] + ["{:.4g}".format(q) for q in q_s])

                # Generate table of block properties
                head = [argMultiFontStringHelper(self.Backend) for _ in range(6)]
                head[0].append("Q", "calligraphic")
                head[1].append("min(", "default")
                head[1].append("Q", "calligraphic")
                head[1].append(')', "default")
                head[2].append("mu", "greek")
                head[2].append('(', "default")
                head[2].append("Q", "calligraphic")
                head[2].append(')', "default")
                head[3].append("max(", "default")
                head[3].append("Q", "calligraphic")
                head[3].append(')', "default")
                head[4].append("sigma", "greek")
                head[4].append('(', "default")
                head[4].append("Q", "calligraphic")
                head[4].append(')', "default")
                head[5].append("sigma", "greek")
                head[5].append('/', "default")
                head[5].append("mu", "greek")
                head[5].append('(', "default")
                head[5].append("Q", "calligraphic")
                head[5].append(')', "default")
                stat_string = argMultiFontStringHelper(self.Backend)
                stat_string.append("Element quality statistics of block ", "default")
                stat_string.append(block_name, "typewriter")
                stat_string.append('.', "default")
                self.Backend.add_table(
                    head,
                    body,
                    stat_string)

                # Create and add histogram plot when requested and appropriate
                if do_histograms:
                    histo_map = q_histo.get(b_id, {})
                    for q_n, q_h in histo_map.items():
                        # Bail out if no quality histogram was provided
                        if not q_h:
                            continue

                        # Decide whether to show histogram depending on CoV
                        cv = q_stats.get(b_id).get(q_n)[4]
                        if cv < 1e-3:
                            # Quality spread is too tight for histogram
                            print("*  WARNING: coefficient of variation of block {} {} too small ({}) for histogram".format(
                                b_id,
                                q_name, cv))
                        else:
                            # Generate and insert histogram plot
                            histo_name = argPlot.create_plot(
                                self.Backend.Parameters,
                                histo_plot_params,
                                histo_map,
                                "block {}".format(b_id),
                                q_n,
                                'element count',
                                'o')
                            if histo_name:
                                histo_string = argMultiFontStringHelper(self.Backend)
                                histo_string.append("Histogram of {} element quality in block ".format(
                                    q_n), "default")
                                histo_string.append(block_name, "typewriter")
                                histo_string.append('.', "default")
                                self.Backend.add_figure({
                                    "figure_file": "{}.png".format(histo_name[0]),
                                    "caption_string": histo_string,
                                    "width": fig_params.get("histogram_width", "12cm")})

            # Append comment when defined for current block
            if not self.Backend.add_comment(comments, block_name):
                self.Backend.add_comment(comments, b_id)

        # Clear page after last block
        self.Backend.add_page_break()


    def show_all_modes(self, fig_params, data, file_name):
        """Add surface rendering figures for all mode shapes
           for the Disp variable,
           with a normalized displacement with given factor,
           laid out in n_cols columns by n_rows rows
        """

        # Bail out early if no modes are present
        times = data.get_available_times()
        if not times:
            return

        # Get handle on input data in VTK form
        vtk_data = data.get_VTK_reader_output_data(0)
        if not vtk_data:
            print("*  WARNING: could not read VTK data from input model {}".format(
                file_name))
            return

        # Retrieve first sought mode
        times = data.get_available_times()

        # Determine extreme modes
        mode_min = fig_params.get("mode_min")
        if mode_min:
            mode_min = float(mode_min)
            for i_min, m in enumerate(times):
                if m > mode_min:
                    break
        else:
            i_min = 0
        mode_max = fig_params.get("mode_max")
        if mode_max:
            mode_max = float(mode_max)
            for i_max, m in enumerate(reversed(times)):
                if m < mode_max:
                    break
            i_max = len(times) - 1 - i_max
        else:
            i_max = len(times) - 1

        # Determine numbers of complete images and of remaining modes
        n_modes_per_image = fig_params.get("n_cols", 1) * fig_params.get("n_rows", 1)
        n_images = i_max - i_min + 1
        n_figs, n_rem = divmod(n_images, n_modes_per_image)

        # Generate images and captions for each for each block of modes
        all_base_names, all_captions = [], []
        variable = argVTK.argVTKAttribute(data, )
        mode_range = [i_min, i_min + n_modes_per_image - 1]

        # Start with all complete images
        for _ in range(n_figs):
            fig_params["range"] = mode_range
            base_name, caption = argVTK.many_modes(
                self.Backend.Parameters,
                fig_params,
                data,
                variable,
                file_name)
            all_base_names.append(base_name)
            all_captions.append(caption)
            mode_range[0] += n_modes_per_image
            mode_range[1] += n_modes_per_image

        # Create incomplete image if modes remain
        if n_rem:
            mode_range[1] = mode_range[0] + n_rem - 1
            fig_params["range"] = mode_range
            base_name, caption = argVTK.many_modes(
                self.Backend.Parameters,
                fig_params,
                data,
                variable,
                file_name)
            all_base_names.append(base_name)
            all_captions.append(caption)

        # Add corresponding modal frequencies table
        modes = []
        for i, m in enumerate(times):
            # Retain only those modes that are in range
            if i < i_min:
                continue
            if i > i_max:
                break

            # Append mode to table body list
            mode_string = argMultiFontStringHelper(self.Backend)
            mode_string.append("{:.1f}".format(m), "typewriter")
            modes.append(["{}".format(i), mode_string])

        # Assemble frequency string
        freq_string = argMultiFontStringHelper(self.Backend)
        freq_string.append("Modal frequencies", "default")
        if mode_min:
            freq_string.append(" greater than {:.1f}Hz".format(mode_min), "default")
        if mode_min and mode_max:
            freq_string.append(" and", "default")
        if mode_max:
            freq_string.append(" less than {:.1f}Hz".format(mode_max), "default")
        freq_string.append('.', "default")
        self.Backend.add_table(
            ["mode number", "frequency (Hz)"],
            modes,
            freq_string)

        # Create figures
        fig_width = fig_params.get("width")
        for base_name, caption_string in zip(all_base_names, all_captions):
            self.Backend.add_figure({
                "figure_file": base_name + ".png",
                "caption_string": caption_string,
                "width": fig_width})


    def show_enumerated_fields(self, fig_params, data, file_name):
        """Add surface rendering figures to the document for a
           specified set of point or cell data, scalar or vector variables
        """

        # Set default figure width
        fig_params.setdefault("width", "12cm")

        # Create per-field pages
        for d in data:
            # Generate page header
            var_desc = "element" if d.AttributeBinding == "cell" else "node"
            var_desc += "-based {}".format(d.AttributeType)

            # Iterate over all available time
            for i, t in enumerate(d.get_available_times()):
                # Start with a new page for each time-step
                self.Backend.add_page_break()

                # Create variable page title
                variable_string = argMultiFontStringHelper(self.Backend)
                variable_string.append("Variable ", "default")
                variable_string.append(d.AttributeName, "typewriter")
                variable_string.append(" (" + var_desc, "default")

                # Append time when more than one time-step is availanle
                if len(d.get_available_times()) > 1:
                    variable_string.append(" at time ", "default")
                    variable_string.append("{:.6g}".format(t), "typewriter")

                # Create un-numbered subsection
                variable_string.append(')', "default")
                self.Backend.add_subtitle({"title": variable_string})

                # Get handle on input data in VTK form
                vtk_data = d.get_VTK_reader_output_data(i)
                if not vtk_data:
                    print("* {} WARNING: could not read VTK data from input model".format(file_name))
                    return

                # Generate clipped mesh surface view
                fig_params["time_step"] = i
                self.show_mesh_surface(self.Backend, fig_params, d, file_name, True)

        # Clear page after last field
        self.Backend.add_page_break()


    def aggregate(self, request_params):
        """Decide which aggregation operation is to be performed
        """

        # Switch between different aggregation types
        request_name = request_params["name"]
        print("[argExodusAggregator] Processing {} request".format(request_name))

        # Operation show_all_blocks: one 4-view figure and one table per mesh block
        if request_name.startswith("show_all_blocks"):
            # Decide whether mesh edges are to be shown or not
            request_params["edges"] = request_name.endswith("with_edges")

            # Add specific request parameters
            request_params.setdefault("view_direction", ())

            # Retrieve model file
            model_file = request_params.get("model")
            file_names = {"model": model_file}

            # Try to retrieve model data
            if model_file:
                model_data = argDataInterface.factory(
                    "ExodusII",
                    os.path.join(self.Backend.Parameters.DataDir, model_file),
                    request_params.get("var_name", ''))
            else:
                model_data = None
            data = {"model": model_data}

            # Aggregate
            if model_data:
                self.show_all_blocks(
                    request_params, data, file_names,
                    (int(request_params.get("verbosity", 0)) > 0))

        # Operation show_enumerated_fields: one figure page per field
        elif request_name == "show_enumerated_fields":
            # Decide whether mesh edges are to be shown or not
            request_params["edges"] = request_name.endswith("with_edges")

            # Add specific request parameters
            request_params.setdefault("view_direction", ())
            var_names = request_params.get("var_names")
            if not var_names:
                print("*  WARNING: no variable names provided for {}".format(
                    request_name))
                return

            # Get handle on data
            file_name = request_params["model"]
            data = [argDataInterface.factory(
                "ExodusII",
                os.path.join(self.Backend.Parameters.DataDir, file_name), v, False)
                for v in var_names]

            # Aggregate
            if data:
                self.show_enumerated_fields(
                    request_params, data, file_name)

        # Operation show_all_modes: one figure every n_cols x n_rows modes
        elif request_name.startswith("show_all_modes"):
            # Decide whether mesh edges are to be shown or not
            request_params["edges"] = request_name.endswith("with_edges")

            # Add specific request parameters
            request_params.setdefault("view_direction", ())
            request_params.setdefault("displacement", 2.)
            request_params.setdefault("n_cols", 4)
            request_params.setdefault("n_rows", 4)

            # Get handle on data
            file_name = request_params["model"]
            data = argDataInterface.factory(
                "ExodusII",
                os.path.join(self.Backend.Parameters.DataDir, file_name),
                request_params.get("var_name", "Disp"),
                False)

            # Aggregate
            self.show_all_modes(
                request_params, data, file_name)

        # Operation show_mesh_surface: create one figure for the entire mesh
        elif request_name.startswith("show_mesh_surface"):
            # Decide whether mesh edges are to be shown or not
            request_params["edges"] = request_name.endswith("with_edges")

            # Add specific request parameters
            request_params.setdefault("view_direction", ())

            # Get handle on data
            file_name = request_params["model"]
            data = argDataInterface.factory(
                "ExodusII",
                os.path.join(self.Backend.Parameters.DataDir, file_name),
                request_params.get("var_name", ''))

            # Aggregate
            if data:
                self.show_mesh_surface(
                    request_params, data, file_name)
