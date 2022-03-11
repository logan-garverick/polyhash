"""
Description: This file defines the PH_Binary class
"""

from abc import ABC, abstractmethod
from utils.fileFormatConstants import *
import struct


class BinaryFile:
    """This is the Factory pattern for format specific binary analysis"""

    def __init__(self):
        self.path = None
        self.endianness = None
        self.entrypoint = None
        self.bitness = None

    @abstractmethod
    def _find_entry_point(self) -> int:
        """This method will find the entry point in the binary file based on its format"""

    @abstractmethod
    def _find_bitness(self) -> str:
        """This method will find the machine addressing (32 or 64 bit) in the binary file based on its format"""

    @abstractmethod
    def _find_endianness(self) -> str:
        """This method will find the endianess in the binary file based on its format"""

    @abstractmethod
    def get_entry_point(self) -> int:
        """This method will returned the entry point of the binary"""

    @abstractmethod
    def get_format_info(self) -> dict:
        """This method will get the abbreviation of the detected file format"""

    @abstractmethod
    def display_format_info(self) -> None:
        """This method will display the BinaryFile information"""


class ELF(BinaryFile):
    """Executable and Linkable Format"""

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.endianness = self._find_endianness()
        self.bitness = self._find_bitness()
        self.entrypoint = self._find_entry_point()

    def _find_entry_point(self) -> int:
        with open(self.path, "rb") as bin:

            # Seek to e_entrypoint in Elf32_Ehdr
            bin.seek(ELF_FORMAT["e_entrypoint"], 1)

            if self.endianness == "LE":
                if self.bitness == 32:
                    (entrypoint,) = struct.unpack("<L", bin.read(4))
                else:
                    (entrypoint,) = struct.unpack("<Q", bin.read(8))
            else:
                if self.bitness == 32:
                    entrypoint = int(bin.read(4), 16)
                else:
                    entrypoint = int(bin.read(8), 16)
        return entrypoint

    def _find_bitness(self) -> int:
        with open(self.path, "rb") as bin:
            bin.seek(ELF_FORMAT["e_type"], 1)
            (typeFlag,) = struct.unpack("<B", bin.read(1))
            if typeFlag == 1:
                return 32
            else:
                return 64

    def _find_endianness(self) -> str:
        with open(self.path, "rb") as bin:
            bin.seek(ELF_FORMAT["e_machine"], 1)
            (endiannessFlag,) = struct.unpack("<B", bin.read(1))
            if endiannessFlag == 1:
                return "LE"
            else:
                return "BE"

    def get_entry_point(self) -> int:
        return self.entrypoint

    def get_format_info(self) -> dict:
        return {
            "path": self.path,
            "bitness": self.bitness,
            "endianness": self.endianness,
            "entrypoint": self.entrypoint,
        }

    def display_format_info(self) -> None:
        print(
            f"\t\tPath:\t\t{self.path}\n"
            + f"\t\tBitness:\t{self.bitness}\n"
            + f"\t\tEndianness:\t{self.endianness}\n"
            + f"\t\tEntry Point:\t{hex(self.entrypoint)}"
        )


class DOS(BinaryFile):
    """DOS MZ executable (NE/PE)"""

    def __init__(self, path) -> None:
        super().__init__()
        self.path = path
        self.endianness = self._find_endianness()
        self.bitness = self._find_bitness()
        self.entrypoint = self._find_entry_point()

    def _find_entry_point(self) -> int:
        # Open the file for reading
        with open(self.path, "rb") as bin:

            # Find e_lfanew pointer to _IMAGE_NT_HEADERS
            bin.seek(DOS_FORMAT["e_lfanew"], 1)
            (e_lfanew_ptr,) = struct.unpack("<L", bin.read(4))

            # Get AddressOfEntryPoint in _IMAGE_OPTIONAL_HEADER
            bin.seek(
                e_lfanew_ptr + DOS_FORMAT["AddressOfEntryPoint"],
                0,
            )

            if self.endianness == "LE":
                if self.bitness == 32:
                    (entrypoint,) = struct.unpack("<L", bin.read(4))
                else:
                    (entrypoint,) = struct.unpack("<Q", bin.read(8))
            else:
                if self.bitness == 32:
                    entrypoint = int(bin.read(4), 16)
                else:
                    entrypoint = int(bin.read(8), 16)

        return entrypoint

    def _find_bitness(self) -> str:
        # Open the file for reading
        with open(self.path, "rb") as bin:

            # Find e_lfanew pointer to _IMAGE_NT_HEADERS
            bin.seek(DOS_FORMAT["e_lfanew"], 1)
            (e_lfanew_ptr,) = struct.unpack("<L", bin.read(4))

            # Get Addressing (32 or 64 bit) in _IMAGE_FILE_HEADER
            bin.seek(e_lfanew_ptr + DOS_FORMAT["Machine"], 0)
            if self.endianness == "LE":
                (machine_flag,) = struct.unpack("<H", bin.read(2))
            else:
                machine_flag = int(bin.read(2), 16)

            # Find what the addressing format of the binary is
            MACHINE_FLAGS = DOS_FORMAT["Machine_Flags"]
            for addressing in MACHINE_FLAGS:
                if machine_flag == MACHINE_FLAGS.get(addressing):
                    return addressing

    def _find_endianness(self) -> str:
        return "LE"

    def get_entry_point(self) -> int:
        return self.entrypoint

    def get_format_info(self) -> dict:
        return {
            "path": self.path,
            "bitness": self.bitness,
            "endianness": self.endianness,
            "entrypoint": self.entrypoint,
        }

    def display_format_info(self) -> None:
        print(
            f"\t\tPath:\t\t{self.path}\n"
            + f"\t\tBitness:\t{self.bitness}\n"
            + f"\t\tEndianness:\t{self.endianness}\n"
            + f"\t\tEntry Point:\t{hex(self.entrypoint)}"
        )


class BinaryFileFactory(ABC):
    """Factory that generates an BinaryFile object based on the file format signature discovered"""

    @abstractmethod
    def get_binaryfile(self, path) -> BinaryFile:
        """Returns a new BinaryFile instance"""


class ELFFactory(BinaryFileFactory):
    """Factory to provide an ELF instance"""

    def get_binaryfile(self, path) -> BinaryFile:
        """Returns a new BinaryFile instance"""
        return ELF(path)


class DOSFactory(BinaryFileFactory):
    """Factory to provide an DOS instance"""

    def get_binaryfile(self, path) -> BinaryFile:
        """Returns a new BinaryFile instance"""
        return DOS(path)
