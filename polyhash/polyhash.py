"""
Description: This will be the main execution file to accept and parse command 
             line arguments and determine the file structure of a provided 
             binary.
"""

import argparse
from os.path import exists
from utils.binaryfilefactory import *
from utils.bcolors import *
from utils.binaryfile import *
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


def get_BinaryFile() -> BinaryFile:
    """Verifies the provided binary and employs the BinaryFileFactory class to generate a BinaryFile instance

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

            # Attempt to create a BinaryFile object
            fac = BinaryFileFactory()
            bf = fac.get_BinaryFile_instance(args.binary)
            if bf is not None:
                if args.verbose:
                    print(
                        f"\t{colors.OKGREEN}LOG{colors.ENDC}: -----Generated BinaryFile Information----- "
                    )
                    bf.display_format_info()
                    print(f"\t     ------------------------------------------ ")
            else:
                print(
                    f"\t{colors.FAIL}ERROR{colors.ENDC}:Unable to determine binary format. Stopping analysis."
                )
                exit(0)

            return bf
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print(f"\t{colors.FAIL}ERROR:{colors.ENDC}{args.binary} was not found.")
        exit(1)


def polyhash():

    # Retrieve BinaryFile instance of binary
    bf = get_BinaryFile()

    # Retrieve BinaryFile file info to start analysis
    binaryInfo = bf.get_format_info()

    # Read the content of the binary file to give to decompiler
    fileContent = None
    with open(binaryInfo["path"], "rb") as f:
        f.seek(binaryInfo["entrypoint"])
        fileContent = f.read(binaryInfo["textSegLen"])

    # Attempt to decompile instructions
    decoder = Decoder(binaryInfo["bitness"], fileContent, ip=binaryInfo["entrypoint"])

    # ****************************** DEBUG INFO HERE ******************************
    counter = 0

    formatter = Formatter(FormatterSyntax.NASM)
    formatter.digit_separator = "`"
    formatter.first_operand_char_index = 10
    print(
        f"\t{colors.HEADER}     --------------------- DEBUG: Decoded Instruction --------------------- {colors.ENDC}"
    )
    print(
        f"\t{colors.HEADER}       |--Byte Address--|----Instr. Bytes----|Mnemonic|----Operands----|{colors.ENDC}"
    )
    for instr in decoder:
        disasm = formatter.format(instr)
        # print(f"\t\t{disasm}")

        start_index = instr.ip - binaryInfo["entrypoint"]
        bytes_str = fileContent[start_index : start_index + instr.len].hex()
        # Eg. "00007FFAC46ACDB2 488DAC2400FFFFFF     lea       rbp,[rsp-100h]"
        print(f"\t\t{instr.ip:016X} {bytes_str:20} {disasm}")

        counter += 1
        if counter == 10:
            break
    print(f"\n\t\tPolyHash decoded {colors.BOLD}{counter}{colors.ENDC} instructions")
    print(
        f"\t{colors.HEADER}     ---------------------------------------------------------------------- {colors.ENDC}"
    )
    # ****************************** DEBUG INFO HERE ******************************


if __name__ == "__main__":
    # Initialize parser object
    parser = argparse.ArgumentParser(
        description="Analyze a binary file and produce a list of possible polymorphic signatures."
    )
    configure_parser()
    args = parser.parse_args()
    # Begin analysis
    polyhash()
