"""
Description: This will be the main execution file to accept and parse command 
             line arguments and determine the file structure of a provided 
             binary.
"""

import argparse


def configure_parser():
    parser.add_argument(
        "binary",
        action="store",
        type=str,
        help="path to the binary to analyze",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        default="polyhash_table.txt",
        action="store",
        type=str,
        help="path where the produced hash table should be stored (default: polyhash_table.txt)",
    )


def polyhash(args):
    pass


if __name__ == "__main__":
    # Initialize parser object
    parser = argparse.ArgumentParser(
        description="Analyze a binary file and produce a list of possible polymorphic signatures."
    )
    configure_parser()
    args = parser.parse_args()
    print(args)
    # Begin analysis
    polyhash(args)
