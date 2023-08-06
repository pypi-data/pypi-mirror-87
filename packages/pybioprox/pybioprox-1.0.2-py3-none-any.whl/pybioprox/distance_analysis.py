"""distance_analysis.py

Distance analysis functions

Copyright (C) 2020  Jeremy Metz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from dataclasses import dataclass
import numpy as np
import scipy.ndimage as ndi
from pybioprox.utility import get_logger

logger = get_logger()  # pylint: disable=invalid-name


@dataclass(frozen=True)
class Scale:
    """
    Simple calibration scale dataclass
    """
    xymicsperpix: float
    zmicsperpix: float


def get_analyser(name):
    """
    Access a function in the current module by name
    Return a list of analysis functions in the current
    submodule
    """
    # Handle case we already have a function
    if callable(name):
        return name
    # Can't use hyphens or spaces
    name_sanitized = name.replace('-', '_').replace(' ', '_')
    candidates = {
        key: value
        for key, value in globals().items()
        if callable(value)}
    if name_sanitized not in candidates:
        raise ValueError(f'{name} is not a valid distance analysis function')
    return candidates[name_sanitized]


def edge_to_edge(mask1, mask2, scale=None, max_num_objects=None):
    """
    Analyses edge-to-edge distances TODO: COMPLETE ME
    """
    if max_num_objects is None:
        max_num_objects = np.inf
    scale = Scale(**dict({'xymicsperpix': 1, 'zmicsperpix': 1}, **scale or {}))
    # Generate distance map of mask2 - Note: because the distance
    # map here measures how far to the nearest OFF pixel (0), we need to
    # invert the mask while performing this function
    # Aside: the edt part of the function just stands for
    # Exact euclidean distance transform, as the module
    # also has other ways of calculating different
    # distance transforms!
    # NOTE: Includes pixel sampling factors;
    # so distances will be in microns
    sampling = [scale.xymicsperpix for shape in mask1.shape]
    if len(sampling) == 3:
        sampling[0] = scale.zmicsperpix
    distancemap2 = ndi.distance_transform_edt(~mask2, sampling=sampling)

    labels1, num_objects1 = ndi.label(mask1)

    if num_objects1 > max_num_objects:
        logger.critical("Too many objects found (%s), skipping", num_objects1)
        return None, None
    # NB: As this function is in scipy.ndimage - it happily handles
    # N-d data for us!
    # It also outputs the number of objects found, so we can show that
    # in the terminal...

    logger.info("Number of objects in mask1: %s", num_objects1)

    distances_list, dist_stats_list = edge_to_edge_process_individual_objects(
        labels1, num_objects1, distancemap2)
    return distances_list, dist_stats_list


def edge_to_edge_process_individual_objects(
        labels1, num_objects1, distancemap2):
    """
    We want to process each labelled region (~object)
    individually, so we will use a for-loop
    We know how many objects there are from num_objects1
    """

    # NOTE: The Python range function, when called with two inputs
    # generates the numbers input1, input1+1, input1+2, ... , input2-1
    # I.e. it does not generate input2, so if we want to have a
    # range of numbers go to X, then we have to use X+1 as the second input!

    # We're also going to create a list of distances - one
    # entry per object, but each entry itself is going to
    # be a list of distances!

    # First, let's create an empty list using []
    distances_list = []
    dist_stats_list = [
        [
            "PDmin",
            "Hausdorff Distance",
            "PDmean",
            # "median distance",
            # "sum distance",
            "Number of Perimeter Pixels",
        ]
    ]

    for label in range(1, num_objects1 + 1):

        # Now we generate a mask of just this object
        # which is kind of like an ROI object in imagej
        # We can do this by using the comparison operator ==
        # which evaluates to true where values in labels1 are equal
        # to label
        mask_obj = labels1 == label

        # Now we can generate an outline of this region by performing
        # binary erosion of this region and getting the pixels where
        # mask_obj is True, but the eroded version is False!
        # eroded = ndi.binary_erosion(mask_obj)
        outline = mask_obj & np.logical_not(ndi.binary_erosion(mask_obj))

        # Now we can get all the distances of the outline pixels
        # to the nearest object in mask2!
        distances = distancemap2[outline]
        dist_arr = np.array(distances)
        dist_stats = [
            np.min(dist_arr),
            np.max(dist_arr),
            np.mean(dist_arr),
            # np.median(dist_arr),
            # np.sum(dist_arr),
            np.shape(dist_arr)[0],
        ]
        # This uses "logical indexing", i.e. we can pass in a mask array
        # to extract only pixels in distancemap2 where the mask array
        # (in this case outline) is True.

        # Lastly we just need to decide what to do with the distances...
        # For now, let's create a table, so we're going to append the
        # current distances to the end of the list
        distances_list.append(distances)
        dist_stats_list.append(dist_stats)
    return distances_list, dist_stats_list
