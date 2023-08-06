"""cli.py

Command Line Interface for pybioprox

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

import argparse
import pybioprox.main as main


def create_parser():
    """
    Create the parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Folder to process")
    parser.add_argument("--output-folder", help="Output folder")
    # parser.add_argument(
    #    "-v", "--verbose", help="Increase output verbosity",
    #    action="store_true")
    # parser.add_argument("-d", type=int, choices=[0, 1, 2],
    #                    help="Choices...")
    return parser


def run():
    """
    Main CLI run function

    Creates an appropriate ArgumentParser and parses the command
    line arguments, passing parameters through to pybioprox.main.main
    """
    parser = create_parser()
    args = parser.parse_args()

    main.main(args.folder, output_folder=args.output_folder)
