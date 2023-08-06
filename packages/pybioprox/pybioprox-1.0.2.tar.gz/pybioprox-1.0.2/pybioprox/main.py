"""main.py

Main entry module for pybioprox

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
import os
import csv
import dataclasses
import numpy as np
import tifffile
import matplotlib.pyplot as plt
import skimage.filters as skfilt
import scipy.ndimage as ndi
from pybioprox.distance_analysis import get_analyser
from pybioprox.utility import get_logger
plt.switch_backend('agg')

# ------------------------------
# Add in calibration of pixels in xy and z directions
# ------------------------------
__threshold_functions__ = {
    'li': skfilt.threshold_li,
    'otsu': skfilt.threshold_otsu,
}
logger = get_logger()  # pylint: disable=invalid-name


@dataclasses.dataclass(frozen=True)
class Config:  # pylint: disable=too-many-instance-attributes # (8/7)
    """
    Default configuration object.
    Once these have been set at input time, they cannot be changed
    """
    channel1_index: int = 0
    channel2_index: int = 1
    filter_method: str = 'none'
    threshold_method: str = 'none'
    distance_analyser: str = 'edge-to-edge'
    scales: tuple = (0.08, 0.75)
    units: tuple = ('um', 'um')
    max_num_objects = 10000

    def as_dict(self):
        """For simple conversion"""
        return dataclasses.asdict(self)


def get_files(folder):
    """
    find .tif files in input_folder_name, add to directory
    """
    listing = os.listdir(folder)
    filename_list = [
        os.path.join(folder, item)
        for item in listing if item.endswith(".tif")]
    return filename_list


def perform_filter_using_method(image, method):
    """
    Runs specified filter (or just returns the original image)
    """
    if (method is None) or method.lower() == 'none':
        return image
    method = method.lower()
    if method == "gaussian (sigma 3px)":
        return ndi.gaussian_filter(image, sigma=3.0)
    raise ValueError(f"Filter method [{method}] not supported")


def perform_thresholding(filtered1, filtered2, threshold_method):
    """
    Perform requested thresholding (or none) and return result
    """
    if threshold_method is not None:
        threshold_method = threshold_method.lower()
    if threshold_method not in (None, 'none'):
        threshold_function = __threshold_functions__[threshold_method]
        threshold_value1 = threshold_function(filtered1)
        threshold_value2 = threshold_function(filtered2)
        # apply threshold using comparison operator to generate binary stacks
        mask1 = filtered1 >= threshold_value1
        mask2 = filtered2 >= threshold_value2
    else:
        mask1 = filtered1
        mask2 = filtered2
    return mask1, mask2


def load_data(filepath, channel1_index, channel2_index):
    """
    Loads the data and performs necessary channel selection
    returns the selected channel images
    """
    # load the data using tifffile, unlike when
    # loading .czi files, no unnecessary
    # dimensions are added, meaning that we do not need to
    # use the .squeeze function.
    datain = tifffile.imread(filepath)

    # Move channel axis to front
    data = shuffle_smallest_dim_to_front(datain)

    if data.ndim > 4:
        raise ValueError(
            "Unhandled dimensionality of data"
            + f"\nData must be 3-4 dimensional, got {data.ndim}")
    if data.ndim < 3:
        raise ValueError(
            "Input image must contain 2 channels and therefore"
            " be at least 3d")

    # split channels
    channel1 = data[channel1_index]
    channel2 = data[channel2_index]

    if channel1.ndim == 3:
        channel1 = shuffle_smallest_dim_to_front(channel1)
        channel2 = shuffle_smallest_dim_to_front(channel2)

    logger.debug("Channel 1 data has shape: %s", channel1.shape)
    logger.debug("Channel 2 data has shape: %s", channel2.shape)
    return channel1, channel2


def detect_objects(channel1, channel2, config):
    """
    Only the detection part
    """
    logger.debug("Running detection with parameters:")
    logger.debug(config)
    mask1, mask2, *_ = detect_objects_with_filter_outputs(
        channel1,
        channel2,
        config)
    return mask1, mask2


def detect_objects_with_filter_outputs(channel1, channel2, config):
    """
    Only the detection part, including debugging output
    """
    # at this point extra filtering steps can be inserted; I
    # have pre-filtered tis data in image-j so no need for extra filtering
    filtered1 = perform_filter_using_method(channel1, config.filter_method)
    filtered2 = perform_filter_using_method(channel2, config.filter_method)
    # identify thresholding values using method selected
    mask1, mask2 = perform_thresholding(
        filtered1, filtered2, config.threshold_method)
    return mask1, mask2, filtered1, filtered2


def process_file(
        filepath,
        output_folder,
        **config):
    """
    Perform main processing on the file
    """
    config = Config(**config)
    channel1, channel2 = load_data(
        filepath, config.channel1_index, config.channel2_index)
    mask1, mask2 = detect_objects(channel1, channel2, config)
    distance_analyser = get_analyser(config.distance_analyser)
    # We now create overlay figures for channel 1 and 2
    # and save to the input folder to allow
    # the thresholding to be assessed
    # Create a new figure object, and set the window title

    plot_and_save_outlines(
        channel1, channel2, mask1, mask2, filepath)

    # So next, for each object in mask1, let's
    # See how far it's border pixels are from the
    # nearest object in mask2 (using distancemap2)...

    # First we create a "labelled" array, which
    # performs part of what happens with
    # "Analyze particles" in imagej; it identifies
    # connected clumps of pixels and gives them all a unique
    # label.
    distances_list, dist_stats_list = distance_analyser(
        mask1, mask2,
        scale={
            'xymicsperpix': config.scales[0],
            'zmicsperpix': config.scales[1]},
        max_num_objects=config.max_num_objects)

    if distances_list is not None:
        output_distances_and_stats(
            os.path.basename(filepath), output_folder,
            distances_list, dist_stats_list)


def output_distances_and_stats(name, folder, distances, dist_stats):
    """
    Outputs the distances and stats, for filename `name`
    into output folder `folder`
    """
    # Now that we have all the distances in a list, we could
    # perform statistical tests on them, or get their means,
    # maxima etc, but for now let's just write them to a
    # CSV (comma-seperated-values) file which can be loaded
    # into a variety of software (including Excel...) for
    # later inspection!

    if not os.path.isdir(folder):
        os.makedirs(folder)

    # To do this we're going to "open" a file (which returns
    # a "file-object" representing the open file
    # and then use the Python standard library's csv module
    # to send the data to the open file!
    file_out = open(os.path.join(folder, f"distance_table_{name}.csv"), "w")
    writer = csv.writer(file_out)
    writer.writerows(distances)
    file_out.close()

    file_out = open(os.path.join(folder, f"stats_table_{name}.csv"), "w")
    writer = csv.writer(file_out)
    writer.writerows(dist_stats)
    file_out.close()


def shuffle_smallest_dim_to_front(data):
    """
    Assumes smallest axis is channel axis and
    moves it to be the first dimension
    """
    channel_dim = np.argmin(data.shape)
    return np.moveaxis(data, channel_dim, 0)


def plot_and_save_outlines(channel1, channel2, mask1, mask2, filepath):
    """
    Creates and saves outline plots from the channel data and masks
    """
    figs, have_objects = plot_outlines(channel1, channel2, mask1, mask2)

    for num, (fig, has_objects) in enumerate(zip(figs, have_objects), start=1):
        if has_objects:
            savename = "{}_mask_{}.png".format(filepath, num)
        else:
            savename = "{}_mask_{}_NO_REGIONS.png".format(filepath, num)
        fig.savefig(savename)
        plt.close(fig)
    logger.info("Created overlay images")


def plot_outlines(channel1, channel2, mask1, mask2, axes=None):
    """
    Plot channel images with mask outlines
    """
    # channel1 overlay images:
    size = channel1.shape[-2:]
    slices = [slice(None) for dim in channel1.shape]
    for i in range(channel1.ndim-2):
        # Get middle slice of any remaining channels
        middle_index = channel1.shape[i]//2
        slices[i] = middle_index
    slices = tuple(slices)

    if axes is None:
        figs = (
            plt.figure(
                "Mask 1",
                figsize=(12, 12 * size[0] / size[1]),
                dpi=size[1] / 12,
            ),
            plt.figure(
                "Mask 2",
                figsize=(12, 12 * size[0] / size[1]),
                dpi=size[1] / 12,
            ))
        axes = tuple(fig.gca(position=[0, 0, 1, 1]) for fig in figs)
    else:
        figs = tuple(axis.get_figure() for axis in axes)

    for axis in axes:
        axis.clear()

    axes[0].imshow(channel1[slices], cmap="gray")
    mask1_has_objects = len(np.unique(mask1[slices])) > 1
    if mask1_has_objects:
        axes[0].contour(mask1[slices], levels=[0.5], colors=["r"])
        logger.debug("Values in mask1[slices]: %s", np.unique(mask1[slices]))

    # channel2 overlay images:
    axes[1].imshow(channel2[slices], cmap="gray")
    mask2_has_objects = len(np.unique(mask2[slices])) > 1
    if mask2_has_objects:
        axes[1].contour(mask2[slices], levels=[0.5], colors=["r"])
        logger.debug("Values in mask2[slices]: %s", np.unique(mask2[slices]))
    return figs, (mask1_has_objects, mask2_has_objects)


def batch(
        input_folder,
        output_folder=None,
        **config,
        ):
    """
    Batch process all the data files in a given folder,
    saving results to the nominated `output_folder`.
    """
    filename_list = get_files(input_folder)

    for index, filepath in enumerate(filename_list):
        filename = os.path.basename(filepath)
        logger.info(
            "processing file %s, this is file %d of %d",
            filename, index + 1, len(filename_list))
        process_file(
            filepath,
            output_folder=output_folder,
            **config
        )


def main(
        input_folder,
        output_folder=None,
        **config
        ):
    """
    Main entry point to run the pybioprox analysis pipeline
    """
    if output_folder is None:
        output_folder = os.path.join(input_folder, "tables")
    batch(
        input_folder=input_folder,
        output_folder=output_folder,
        **config
    )


def main_cli():
    """
    Main CLI interface
    """
    logger.debug("Running as script...")
    folder = input("Please enter an input folder")
    main(folder)


if __name__ == '__main__':
    main_cli()
