"""
Description: This file defines the PE class inheriting from the BinaryFile class.
"""

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

            # Read BaseOfCode from _IMAGE_OPTIONAL_HEADER
            if self.endianness == "LE":
                (base,) = struct.unpack(
                    PE_FORMAT["DWORD_STRUCT"], bin.read(PE_FORMAT["DWORD_SIZE"])
                )
            else:
                base = int(bin.read(PE_FORMAT["DWORD_SIZE"]), 16)

        return entrypoint

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
        with open(self.path, "rb") as bin:

            # Find e_lfanew pointer to _IMAGE_NT_HEADERS
            bin.seek(PE_FORMAT["e_lfanew"], 1)
            (e_lfanew_ptr,) = struct.unpack(
                PE_FORMAT["DWORD_STRUCT"], bin.read(PE_FORMAT["DWORD_SIZE"])
            )

            # Get SizeOfCode in _IMAGE_OPTIONAL_HEADER
            bin.seek(e_lfanew_ptr + PE_FORMAT["SizeOfCode"], 0)
            if self.endianness == "LE":
                (sizeOfCode,) = struct.unpack(
                    PE_FORMAT["DWORD_STRUCT"], bin.read(PE_FORMAT["DWORD_SIZE"])
                )
            else:
                sizeOfCode = int(bin.read(PE_FORMAT["DWORD_SIZE"]), 16)

            return sizeOfCode

    def get_entry_point(self) -> int:
        return self.entrypoint

    def get_format_info(self) -> dict:
        return {
            "path": self.path,
            "bitness": self.bitness,
            "endianness": self.endianness,
            "entrypoint": self.entrypoint,
            "textSegLen": self.textSegLen,
        }

    def display_format_info(self) -> None:
        print(
            f"\t\tPath:\t\t{self.path}\n"
            + f"\t\tFormat:\t\t{self.fileFormatInfo['NAME']}\n"
            + f"\t\tBitness:\t{self.bitness}\n"
            + f"\t\tEndianness:\t{self.endianness}\n"
            + f"\t\tEntry Point:\t{hex(self.entrypoint)}\n"
            + f"\t\tText Seg. Len.:\t{hex(self.textSegLen)}"
        )
