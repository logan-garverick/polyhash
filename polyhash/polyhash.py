"""
Description: This will be the main execution file to accept and parse command 
             line arguments and determine the file structure of a provided 
             binary.
"""

import argparse
from os.path import exists

from utils.bcolors import *
from utils.binaryfile import *
from constants import *
from iced_x86 import *


def configure_parser():
    """Configures the argparse parser object which will be used to interpret command line arguments"""

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
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        default=False,
        action="store_true",
        help="enable verbose mode (default: False)",
    )


def get_format_info() -> dict:
    """Check the provided binary file for common magic numbers to determine file format

    Returns:
        str: the file format of the provided binary
    """
    with open(args.binary, "rb") as binary:
        fileHeader = binary.read(32)
        for format in FILE_FORMAT_INFO:
            if fileHeader.startswith(format.get("sig")):
                return format
        return None


def get_BinaryFile() -> BinaryFileFactory:
    """Verifies the provided binary and generates a PH_Binary object for it

    Raises:
        FileNotFoundError: raised when the provided file does not exist

    Returns:
        BinaryFile: the BinaryFile object that is created
    """

    try:
        # Verify that the provided file exists
        if exists(args.binary):
            if args.verbose:
                print(f"\t{colors.OKGREEN}LOG{colors.ENDC}:{args.binary} was found.")

            # Attempt to determine the file format of the provided binary
            formatInfo = get_format_info()
            if formatInfo is not None:
                if args.verbose:
                    print(
                        '\t{}LOG{}:Determined {} format is: "{}" ({})'.format(
                            colors.OKGREEN,
                            colors.ENDC,
                            args.binary,
                            formatInfo["name"],
                            formatInfo["abbr"],
                        )
                    )
            else:
                print(
                    f"\t{colors.FAIL}ERROR{colors.ENDC}:Unable to determine binary format. Stopping analysis."
                )
                exit(0)

            # Attempt to create a BinaryFile object
            return formatInfo["factory"]
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print(f"\t{colors.FAIL}ERROR:{colors.ENDC}{args.binary} was not found.")
        exit(1)


def polyhash():

    fileContent = None

    # Retrieve BinaryFile instance of binary
    bfFactory = get_BinaryFile()
    bf = bfFactory.get_binaryfile(args.binary)

    if args.verbose:
        print(
            f"\t{colors.OKGREEN}LOG{colors.ENDC}: -----Generated BinaryFile Information----- "
        )
        bf.display_format_info()
        print(f"\t     ------------------------------------------ ")

    # Retrieve BinaryFile file info to start analysis
    binaryInfo = bf.get_format_info()

    # Read the content of the binary file to give to decompiler
    with open(binaryInfo["path"], "rb") as f:
        f.seek(binaryInfo["entrypoint"])
        fileContent = f.read(binaryInfo["textSegLen"])

    # Attempt to decompile instructions
    decoder = Decoder(binaryInfo["bitness"], fileContent, ip=binaryInfo["entrypoint"])

    # Debug Info here
    counter = 0

    formatter = Formatter(FormatterSyntax.NASM)
    formatter.digit_separator = "`"
    formatter.first_operand_char_index = 10
    print(
        f"\t{colors.HEADER}     ------- DEBUG: Decoded Instruction ------- {colors.ENDC}"
    )
    for instr in decoder:
        disasm = formatter.format(instr)
        # print(f"\t\t{disasm}")

        start_index = instr.ip - binaryInfo["entrypoint"]
        bytes_str = fileContent[start_index : start_index + instr.len].hex().upper()
        # Eg. "00007FFAC46ACDB2 488DAC2400FFFFFF     lea       rbp,[rsp-100h]"
        print(f"{instr.ip:016X} {bytes_str:20} {disasm}")

        counter += 1
        if counter > 1:
            break
    print(f"\n\t\tPolyHash decoded {colors.BOLD}{counter}{colors.ENDC} instructions")
    print(
        f"\t{colors.HEADER}     ------------------------------------------ {colors.ENDC}"
    )


if __name__ == "__main__":
    # Initialize parser object
    parser = argparse.ArgumentParser(
        description="Analyze a binary file and produce a list of possible polymorphic signatures."
    )
    configure_parser()
    args = parser.parse_args()
    # Begin analysis
    polyhash()
