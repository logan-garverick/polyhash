"""
Description: This file defines the PE class inheriting from the BinaryFile class.
"""

from tracemalloc import start
from utils.fileFormatConstants import *
from utils.binaryfile import BinaryFile
import struct


class PE(BinaryFile):
    """Portable Executable (PE32/PE32+)"""

    def __init__(self, path) -> None:
        super().__init__()
        self.path = path
        self.endianness = self._find_endianness()
        self.bitness = self._find_bitness()
        self.entrypoint = self._find_entry_point()
        self.start = self._find_start_point()
        self.virtStart = self._find_virt_start_point()
        self.textSegLen = self._find_text_seg_len()
        self.fileFormatInfo = FILE_FORMAT_INFO[1]

    def _find_entry_point(self) -> int:
        # Open the file for reading
        with open(self.path, "rb") as bin:

            # Find e_lfanew pointer to _IMAGE_NT_HEADERS
            bin.seek(PE_FORMAT["e_lfanew"], 1)
            (e_lfanew_ptr,) = struct.unpack(
                PE_FORMAT["ADDR_STRUCT"], bin.read(PE_FORMAT["ADDR_SIZE"])
            )

            # Get AddressOfEntryPoint in _IMAGE_OPTIONAL_HEADER
            bin.seek(
                e_lfanew_ptr + PE_FORMAT["AddressOfEntryPoint"],
                0,
            )

            if self.endianness == "LE":
                (entrypoint,) = struct.unpack(
                    PE_FORMAT["ADDR_STRUCT"], bin.read(PE_FORMAT["ADDR_SIZE"])
                )
            else:
                entrypoint = int(bin.read(PE_FORMAT["ADDR_SIZE"]), 16)

        return entrypoint

    def _find_start_point(self) -> int:
        startpoint = None

        # Open the file for reading
        with open(self.path, "rb") as bin:

            # Find e_lfanew pointer to _IMAGE_NT_HEADERS
            bin.seek(PE_FORMAT["e_lfanew"])
            (e_lfanew_ptr,) = struct.unpack(
                PE_FORMAT["ADDR_STRUCT"], bin.read(PE_FORMAT["ADDR_SIZE"])
            )

            # Read NumberOfSections from _IMAGE_FILE_HEADER
            bin.seek(
                e_lfanew_ptr + PE_FORMAT["NumberOfSections"],
                0,
            )

            if self.endianness == "LE":
                (numberOfSections,) = struct.unpack(
                    PE_FORMAT["WORD_STRUCT"], bin.read(PE_FORMAT["WORD_SIZE"])
                )
            else:
                numberOfSections = int(bin.read(PE_FORMAT["WORD_SIZE"]), 16)

            # Retrieve bitness specific section header offsets
            if self.bitness == 32:
                sh_offset_dict = PE_FORMAT[32]
                sh_offset = sh_offset_dict["SectionHeaders"]
            else:
                sh_offset_dict = PE_FORMAT[64]
                sh_offset = sh_offset_dict["SectionHeaders"]

            # Jump to the first section header
            bin.seek(
                e_lfanew_ptr + sh_offset,
                0,
            )

            # Iterate over the number of sections and search for .text section
            for i in range(numberOfSections):

                # Read the section title
                # sec_title = str(bin.read(8))
                sec_title = bin.read(8).decode("utf-8")

                if sec_title.startswith(".text"):

                    # Read PointerToRawData of section
                    bin.seek(PE_FORMAT["PointerToRawData"], 1)

                    if self.endianness == "LE":
                        (startpoint,) = struct.unpack(
                            PE_FORMAT["DWORD_STRUCT"], bin.read(PE_FORMAT["DWORD_SIZE"])
                        )
                    else:
                        startpoint = int(bin.read(PE_FORMAT["DWORD_SIZE"]), 16)

                    break

                else:
                    bin.seek(PE_FORMAT["NextSection"], 1)

        return startpoint

    def _find_virt_start_point(self) -> int:
        virtstartpoint = None

        # Open the file for reading
        with open(self.path, "rb") as bin:

            # Find e_lfanew pointer to _IMAGE_NT_HEADERS
            bin.seek(PE_FORMAT["e_lfanew"])
            (e_lfanew_ptr,) = struct.unpack(
                PE_FORMAT["ADDR_STRUCT"], bin.read(PE_FORMAT["ADDR_SIZE"])
            )

            # Read NumberOfSections from _IMAGE_FILE_HEADER
            bin.seek(
                e_lfanew_ptr + PE_FORMAT["NumberOfSections"],
                0,
            )

            if self.endianness == "LE":
                (numberOfSections,) = struct.unpack(
                    PE_FORMAT["WORD_STRUCT"], bin.read(PE_FORMAT["WORD_SIZE"])
                )
            else:
                numberOfSections = int(bin.read(PE_FORMAT["WORD_SIZE"]), 16)

            # Retrieve bitness specific section header offsets
            if self.bitness == 32:
                sh_offset_dict = PE_FORMAT[32]
                sh_offset = sh_offset_dict["SectionHeaders"]
            else:
                sh_offset_dict = PE_FORMAT[64]
                sh_offset = sh_offset_dict["SectionHeaders"]

            # Jump to the first section header
            bin.seek(
                e_lfanew_ptr + sh_offset,
                0,
            )

            # Iterate over the number of sections and search for .text section
            for i in range(numberOfSections):

                # Read the section title
                # sec_title = str(bin.read(8))
                sec_title = bin.read(8).decode("utf-8")

                if sec_title.startswith(".text"):

                    # Read VirtualAddress of section
                    bin.seek(PE_FORMAT["VirtualAddress"], 1)

                    if self.endianness == "LE":
                        (virtstartpoint,) = struct.unpack(
                            PE_FORMAT["DWORD_STRUCT"], bin.read(PE_FORMAT["DWORD_SIZE"])
                        )
                    else:
                        virtstartpoint = int(bin.read(PE_FORMAT["DWORD_SIZE"]), 16)

                    break

                else:
                    bin.seek(PE_FORMAT["NextSection"], 1)

        return virtstartpoint

    def _find_bitness(self) -> int:
        # Open the file for reading
        with open(self.path, "rb") as bin:

            # Find e_lfanew pointer to _IMAGE_NT_HEADERS
            bin.seek(PE_FORMAT["e_lfanew"], 1)
            (e_lfanew_ptr,) = struct.unpack(
                PE_FORMAT["DWORD_STRUCT"], bin.read(PE_FORMAT["DWORD_SIZE"])
            )

            # Get format magic numbers (PE32/PE32+) in _IMAGE_OPTIONAL_HEADER
            bin.seek(e_lfanew_ptr + PE_FORMAT["Magic"], 0)
            if self.endianness == "LE":
                (machine_flag,) = struct.unpack(
                    PE_FORMAT["WORD_STRUCT"], bin.read(PE_FORMAT["WORD_SIZE"])
                )
            else:
                machine_flag = int(bin.read(PE_FORMAT["WORD_SIZE"]), 16)

            # Find what the bitness of the binary is
            BITNESSFLAGS = PE_FORMAT["Format_Bitness"]
            for bitness in BITNESSFLAGS:
                if machine_flag == BITNESSFLAGS.get(bitness):
                    return bitness

    def _find_endianness(self) -> str:
        # All Windows platforms have a fixed endianness (little)
        return "LE"

    def _find_text_seg_len(self) -> int:
        sec_size = None

        with open(self.path, "rb") as bin:

            # Find e_lfanew pointer to _IMAGE_NT_HEADERS
            bin.seek(PE_FORMAT["e_lfanew"], 1)
            (e_lfanew_ptr,) = struct.unpack(
                PE_FORMAT["DWORD_STRUCT"], bin.read(PE_FORMAT["DWORD_SIZE"])
            )

            # Read NumberOfSections from _IMAGE_FILE_HEADER
            bin.seek(
                e_lfanew_ptr + PE_FORMAT["NumberOfSections"],
                0,
            )

            if self.endianness == "LE":
                (numberOfSections,) = struct.unpack(
                    PE_FORMAT["WORD_STRUCT"], bin.read(PE_FORMAT["WORD_SIZE"])
                )
            else:
                numberOfSections = int(bin.read(PE_FORMAT["WORD_SIZE"]), 16)

            # Retrieve bitness specific section header offsets
            if self.bitness == 32:
                sh_offset_dict = PE_FORMAT[32]
                sh_offset = sh_offset_dict["SectionHeaders"]
            else:
                sh_offset_dict = PE_FORMAT[64]
                sh_offset = sh_offset_dict["SectionHeaders"]

            # Jump to the first section header
            bin.seek(
                e_lfanew_ptr + sh_offset,
                0,
            )

            # Iterate over the number of sections and search for .text section
            for i in range(numberOfSections):

                # Read the section title
                # sec_title = str(bin.read(8))
                sec_title = bin.read(8).decode("utf-8")

                if sec_title.startswith(".text"):

                    # Read SizeOfRawData of section
                    bin.seek(PE_FORMAT["SizeOfRawData"], 1)

                    if self.endianness == "LE":
                        (sec_size,) = struct.unpack(
                            PE_FORMAT["DWORD_STRUCT"], bin.read(PE_FORMAT["DWORD_SIZE"])
                        )
                    else:
                        sec_size = int(bin.read(PE_FORMAT["DWORD_SIZE"]), 16)

                    break

                else:
                    bin.seek(PE_FORMAT["NextSection"], 1)

        return sec_size

    def get_entry_point(self) -> int:
        return self.entrypoint

    def get_format_info(self) -> dict:
        return {
            "path": self.path,
            "bitness": self.bitness,
            "endianness": self.endianness,
            "entrypoint": self.entrypoint,
            "start": self.start,
            "virtualstart": self.virtStart,
            "textSegLen": self.textSegLen,
        }

    def display_format_info(self) -> None:
        print(
            f"\t\tPath:\t\t\t{self.path}\n"
            + f"\t\tFormat:\t\t\t{self.fileFormatInfo['NAME']}\n"
            + f"\t\tBitness:\t\t{self.bitness}\n"
            + f"\t\tEndianness:\t\t{self.endianness}\n"
            + f"\t\tEntry Point:\t\t{hex(self.entrypoint)}\n"
            + f"\t\tText Seg. Start:\t{hex(self.virtStart)}\n"
            + f"\t\tText Seg. Len.:\t\t{hex(self.textSegLen)}"
        )
