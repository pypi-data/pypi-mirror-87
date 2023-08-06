#!python
"""
Script to launch pybioprox and collect
any user input using GUI interfaces

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
import sys
from dataclasses import make_dataclass, asdict
from PyQt5 import QtWidgets  # type: ignore
from PyQt5.QtCore import pyqtSignal  # pylint: disable=no-name-in-module
import matplotlib.pyplot as plt
from pybioprox import main as pybioprox_main
plt.switch_backend('qt5agg')


class FolderSelectionWidget(QtWidgets.QWidget):
    """
    Label, Text Edit, and Selection button to select
    a folder
    """
    # pylint: disable=c-extension-no-member
    folder_selected = pyqtSignal(str)

    def __init__(
            self,
            *args,
            label_text="Folder",
            button_text="Select",
            dialog_caption="Select folder",
            sizes=(1, 4, 1),
            slot=None,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.sizes = sizes
        self.starts = [
            sum(self.sizes[:ind])
            for ind in range(len(sizes))]
        self.dialog_caption = dialog_caption
        self.label = QtWidgets.QLabel(label_text, self)
        self.button = QtWidgets.QPushButton(button_text, self)
        self.line_edit = QtWidgets.QLineEdit(self)
        self.line_edit.setReadOnly(True)
        self.folder = None
        self.button.clicked.connect(self.select_folder)
        if slot:
            self.folder_selected.connect(slot)
        self.apply_layout()

    def apply_layout(self):
        """
        Generate the layout of the child controls
        """
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.label, 0, self.starts[0], 1, self.sizes[0])
        layout.addWidget(self.line_edit, 0, self.starts[1], 1, self.sizes[1])
        layout.addWidget(self.button, 0, self.starts[2], 1, self.sizes[2])
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def select_folder(self):
        """
        Select a folder and set the folder attribute
        """
        self.folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption=self.dialog_caption,
        )
        self.line_edit.setText(self.folder)
        self.folder_selected.emit(self.folder)


class ScalesWidget(QtWidgets.QWidget):
    """
    Label, and QDoubleSpinBox to select each of the 3 dimension
    sizes and labels and line-edits to select units names
    """
    # pylint: disable=c-extension-no-member

    def __init__(
            self,
            *args,
            sizes=(1, 1, 1, 1),
            # dimensions=("x", "y", "z"),
            dimensions=("x-y", "z"),
            **kwargs):
        super().__init__(*args, **kwargs)
        self.sizes = sizes
        self.labels_scale = [
            QtWidgets.QLabel(f"Scale {dim}", self)
            for dim in dimensions]
        self.entry_scales = [
            QtWidgets.QDoubleSpinBox(self, value=1)
            for dim in dimensions]
        self.labels_unit_name = [
            QtWidgets.QLabel(f"Units {dim}", self)
            for dim in dimensions]
        self.entry_units = [
            QtWidgets.QLineEdit(self, text="pixels")
            for dim in dimensions]

        self.apply_layout()

    def __len__(self):
        """
        Get the length of the widget, by summing the individual
        element sizes (in grid coordinates)
        """
        return sum(self.sizes)

    def apply_layout(self):
        """
        Generate the layout of the child controls
        """
        starts = [
            sum(self.sizes[:ind])
            for ind in range(len(self.sizes))]
        layout = QtWidgets.QGridLayout()
        for start, size, label in zip(
                starts[::2], self.sizes[::2], self.labels_scale):
            layout.addWidget(label, 0, start, 1, size)
        for start, size, control in zip(
                starts[1::2], self.sizes[1::2], self.entry_scales):
            layout.addWidget(control, 0, start, 1, size)
        for start, size, label in zip(
                starts[::2], self.sizes[::2], self.labels_unit_name):
            layout.addWidget(label, 1, start, 1, size)
        for start, size, control in zip(
                starts[1::2], self.sizes[1::2], self.entry_units):
            layout.addWidget(control, 1, start, 1, size)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


class ChannelSelectionWidget(QtWidgets.QWidget):
    """
    Label, and combo boxes, to select channels
    """
    # pylint: disable=c-extension-no-member
    # channels_changed = pyqtSignal(list)

    def __init__(
            self,
            *args,
            sizes=(1, 1, 1, 1),
            label1="Measure from channel",
            label2="to channel",
            channel_1_options=("1", "2", "3"),
            channel_2_options=("1", "2", "3"),
            # slot=None,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.sizes = sizes
        self.label1 = QtWidgets.QLabel(label1, self)
        self.label2 = QtWidgets.QLabel(label2, self)
        self.select_channel_1 = QtWidgets.QComboBox(self)
        self.select_channel_1.addItems(channel_1_options)
        self.select_channel_2 = QtWidgets.QComboBox(self)
        self.select_channel_2.addItems(channel_2_options)
        self.select_channel_2.setCurrentIndex(1)
        self.channels = [0, 1]
        self.select_channel_1.currentIndexChanged.connect(
            self.change_channel_1)
        self.select_channel_2.currentIndexChanged.connect(
            self.change_channel_2)
        # if slot:
        #     self.folder_selected.connect(slot)
        self.apply_layout()

    def apply_layout(self):
        """
        Generate the layout of the child controls
        """
        starts = [
            sum(self.sizes[:ind])
            for ind in range(len(self.sizes))]
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.label1, 0, starts[0], 1, self.sizes[0])
        layout.addWidget(self.select_channel_1, 0, starts[1], 1, self.sizes[1])
        layout.addWidget(self.label2, 0, starts[2], 1, self.sizes[2])
        layout.addWidget(self.select_channel_2, 0, starts[3], 1, self.sizes[3])
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def change_channel_1(self, value):
        """
        Slot to handle channel 1 selection
        """
        self.channels[0] = value

    def change_channel_2(self, value):
        """
        Slot to handle channel 2 selection
        """
        self.channels[1] = value


class FilterThresholdSelectionWidget(QtWidgets.QWidget):
    """
    Label, and combo boxes, to select filtering
    and thresholding settings
    """
    # pylint: disable=c-extension-no-member
    # channels_changed = pyqtSignal(list)

    def __init__(
            self,
            *args,
            sizes=(1, 1, 1, 1),
            label_filtering="Filtering",
            label_thresholding="Thresholding",
            threshold_options=("None", "Otsu", "Li"),
            filter_options=("None", "Gaussian (sigma 3px)"),
            # slot=None,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.sizes = sizes
        self.label_filtering = QtWidgets.QLabel(label_filtering, self)
        self.label_thresholding = QtWidgets.QLabel(label_thresholding, self)
        self.select_filter = QtWidgets.QComboBox(self)
        self.select_filter.addItems(filter_options)
        self.select_threshold = QtWidgets.QComboBox(self)
        self.select_threshold.addItems(threshold_options)
        self.filter = None
        self.threshold = None
        self.select_filter.currentTextChanged.connect(
            self.change_filter)
        self.select_threshold.currentTextChanged.connect(
            self.change_threshold)
        # if slot:
        #     self.folder_selected.connect(slot)
        self.apply_layout()

    def apply_layout(self):
        """
        Generate the layout of the child controls
        """
        layout = QtWidgets.QGridLayout()
        starts = [
            sum(self.sizes[:ind])
            for ind in range(len(self.sizes))]
        layout.addWidget(
            self.label_filtering, 0, starts[0], 1, self.sizes[0])
        layout.addWidget(
            self.select_filter, 0, starts[1], 1, self.sizes[1])
        layout.addWidget(
            self.label_thresholding, 0, starts[2], 1, self.sizes[2])
        layout.addWidget(
            self.select_threshold, 0, starts[3], 1, self.sizes[3])
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def change_filter(self, value):
        """
        Slot to handle filter selection
        """
        self.filter = value

    def change_threshold(self, value):
        """
        Slot to handle threshold selection
        """
        self.threshold = value


class PyBioProxSettingsWidget(QtWidgets.QWidget):
    """
    Class representing a dialog for inputting more advanced settings than just
    requesting the input folder name
    """
    # pylint: disable=c-extension-no-member
    # PyQt is full of these, so disabling globally for the class makes sense
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.resize(600, 480)
        self.select_input_widget = None
        self.select_output_widget = None
        self.select_channels_widget = None
        self.select_filter_threshold_widget = None
        self.select_scale_widget = None
        self.run_button = None
        self.generate_controls()
        self.generate_layout()
        self.setWindowTitle("PyBioProx Settings")
        self.show()

    def generate_controls(self):
        """
        Adds controls
        """
        self.select_input_widget = FolderSelectionWidget(
            self,
            label_text="Input folder",
            dialog_caption="Select input folder",
            slot=self.input_folder_changed)
        self.select_output_widget = FolderSelectionWidget(
            self,
            label_text="Output folder",
            dialog_caption="Select output folder",
            slot=self.output_folder_changed)
        self.select_channels_widget = ChannelSelectionWidget(self)
        self.select_filter_threshold_widget = FilterThresholdSelectionWidget(
            self)
        self.select_scale_widget = ScalesWidget(self)
        self.preview_button = QtWidgets.QPushButton("Preview", self)
        self.preview_button.setEnabled(False)
        self.preview_button.clicked.connect(self.run_preview)
        self.run_button = QtWidgets.QPushButton("Run", self)
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.do_run)

    def generate_layout(self):
        """
        Generates the layout
        """

        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(
            lambda: QtWidgets.QApplication.instance().exit(-1))

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.select_input_widget, 0, 0, 1, 6)
        layout.addWidget(self.select_output_widget, 1, 0, 1, 6)
        layout.addWidget(self.select_channels_widget, 2, 0, 1, 6)
        layout.addWidget(self.select_filter_threshold_widget, 3, 0, 1, 6)
        len_scale_widget = len(self.select_scale_widget)
        layout.addWidget(
            self.select_scale_widget,
            4, 6-len_scale_widget, 1, len_scale_widget)

        layout.addWidget(cancel_button, 5, 3)
        layout.addWidget(self.preview_button, 5, 4)
        layout.addWidget(self.run_button, 5, 5)
        self.setLayout(layout)

    def input_folder_changed(self, input_folder):
        """
        Select the input folder using a standard Qt Dialog.
        Also then conditionally sets the run button as enabled
        """
        output_folder = self.select_output_widget.folder
        can_run = bool(input_folder and output_folder)
        self.run_button.setEnabled(can_run)
        self.preview_button.setEnabled(bool(input_folder))

    def output_folder_changed(self, output_folder):
        """
        Select the output folder using a standard Qt Dialog.
        Also then conditionally sets the run button as enabled
        """
        input_folder = self.select_input_widget.folder
        can_run = bool(input_folder and output_folder)
        self.run_button.setEnabled(can_run)

    def get_settings(self):
        """
        Return the settings as a dictionary
        """
        settings = {
            "input_folder": self.select_input_widget.folder,
            "output_folder": self.select_output_widget.folder,
            "channel1_index": self.select_channels_widget.channels[0],
            "channel2_index": self.select_channels_widget.channels[1],
            "filter_method": self.select_filter_threshold_widget.filter,
            "threshold_method": self.select_filter_threshold_widget.threshold,
            "scales": [control.value()
                       for control in self.select_scale_widget.entry_scales],
            "units": [control.text()
                      for control in self.select_scale_widget.entry_units],
        }
        return make_dataclass(
            "Settings", settings.keys(), frozen=True)(**settings)

    def do_run(self):
        """
        Perform validation - if all good, quit the application with
        the correct code for continuing with running
        """
        problem = self.is_problem_with_options()
        if problem:
            self.show_problem(*problem)
        else:
            QtWidgets.QApplication.instance().quit()

    def show_problem(self, problem_title, problem):
        """
        Shows a simple message box with a warning symbol
        """
        message = QtWidgets.QMessageBox(self)
        message.setIcon(QtWidgets.QMessageBox.Warning)
        message.setText(problem_title)
        message.setInformativeText(problem)
        message.exec_()

    def is_problem_with_options(self):
        """
        Return message explaining problem with options if there is one
        or False if not
        """
        settings = self.get_settings()
        if not os.path.isdir(settings.input_folder):
            return (
                "Input folder problem",
                f"Input folder [{settings.input_folder}]"
                " must be an existing folder")
        if not os.path.isdir(settings.output_folder):
            return (
                "Output folder problem",
                f"Output folder [{settings.output_folder}]"
                " must be an existing folder")
        if settings.channel1_index == settings.channel2_index:
            return (
                "Channel selection problem",
                f"channel 1 [{settings.channel_1}]"
                f" must be diffent from channel 2 [{settings.channel_2}]")
        return False

    def run_preview(self):
        """Creates a preview of the current settings on the first file"""
        settings = asdict(self.get_settings())

        input_folder = settings.pop('input_folder')
        settings.pop('output_folder')
        config = pybioprox_main.Config(**settings)
        filename_list = pybioprox_main.get_files(input_folder)

        filepath = filename_list[0]

        channel1, channel2 = pybioprox_main.load_data(
            filepath, config.channel1_index, config.channel2_index)
        try:
            mask1, mask2 = pybioprox_main.detect_objects(
                channel1, channel2, config)

            pybioprox_main.plot_outlines(
                channel1, channel2, mask1, mask2)
            plt.show(block=False)
        except Exception as err:  # pylint: disable=broad-except
            self.show_problem(
                "An error occurred while previewing",
                str(err))


def get_settings():
    """
    Create and run the Settings dialog, returning the
    settings entered by the user
    """
    # pylint: disable=c-extension-no-member
    app = QtWidgets.QApplication([])
    window = PyBioProxSettingsWidget()
    return_code = app.exec_()
    if return_code != 0:
        print("Run cancelled, quitting")
        sys.exit()
    settings = window.get_settings()
    return settings


def main():
    """
    Main entry point function
    """
    settings = get_settings()
    print("Settings:", settings)
    pybioprox_main.main(**asdict(settings))


if __name__ == '__main__':
    main()
