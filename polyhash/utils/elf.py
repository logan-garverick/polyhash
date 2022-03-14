"""
Description: This file defines the ELF class inheriting from the BinaryFile class.
"""

from utils.fileFormatConstants import *
from utils.binaryfile import BinaryFile
import struct


class ELF(BinaryFile):
    """Executable and Linkable Format"""

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.endianness = self._find_endianness()
        self.bitness = self._find_bitness()
        self.entrypoint = self._find_entry_point()
        self.textSegLen = self._find_text_seg_len()
        self.fileFormatInfo = FILE_FORMAT_INFO[0]

    def _find_entry_point(self) -> int:
        with open(self.path, "rb") as bin:

            # Retrieve bitness specific offsets
            if self.bitness == 32:
                bitnessValues = ELF_FORMAT[32]
            else:
                bitnessValues = ELF_FORMAT[64]

            # Seek to e_entrypoint in Elf32_Ehdr
            bin.seek(ELF_FORMAT["e_entrypoint"], 1)

            if self.endianness == "LE":
                (entrypoint,) = struct.unpack(
                    bitnessValues["Addr_STRUCT"], bin.read(bitnessValues["Addr_SIZE"])
                )
            else:
                entrypoint = int(bin.read(bitnessValues["Addr_SIZE"]), 16)

        return entrypoint

    def _find_bitness(self) -> int:
        with open(self.path, "rb") as bin:
            bin.seek(ELF_FORMAT["e_type"], 1)
            (typeFlag,) = struct.unpack("<b", bin.read(1))
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

    def _find_text_seg_len(self) -> int:

        # Open the file for reading
        with open(self.path, "rb") as bin:

            # Retrieve bitness specific offsets
            if self.bitness == 32:
                bitnessValues = ELF_FORMAT[32]
            else:
                bitnessValues = ELF_FORMAT[64]

            # Find Section header string table index (e_shstrndx) in Program header
            bin.seek(bitnessValues["e_shstrndx"])
            if self.endianness == "LE":
                (e_shstrndx,) = struct.unpack(
                    bitnessValues["Half_STRUCT"],
                    bin.read(bitnessValues["Half_SIZE"]),
                )
            else:
                e_shstrndx = int(bin.read(bitnessValues["Half_SIZE"]), 16)

            # Find the number of section header entries (e_shnum)
            bin.seek(bitnessValues["e_shnum"])
            if self.endianness == "LE":
                (e_shnum,) = struct.unpack(
                    bitnessValues["Half_STRUCT"],
                    bin.read(bitnessValues["Half_SIZE"]),
                )
            else:
                e_shnum = int(bin.read(bitnessValues["Half_SIZE"]), 16)

            # Find the size of section header entries (e_shentsize)
            bin.seek(bitnessValues["e_shentsize"])
            if self.endianness == "LE":
                (e_shentsize,) = struct.unpack(
                    bitnessValues["Half_STRUCT"],
                    bin.read(bitnessValues["Half_SIZE"]),
                )
            else:
                e_shentsize = int(bin.read(bitnessValues["Half_SIZE"]), 16)

            # Get Section header table offset (e_shoff)
            bin.seek(bitnessValues["e_shoff"])
            if self.endianness == "LE":
                (e_shoff,) = struct.unpack(
                    bitnessValues["Addr_STRUCT"],
                    bin.read(bitnessValues["Addr_SIZE"]),
                )
            else:
                e_shoff = int(bin.read(bitnessValues["Addr_SIZE"]), 16)

            # Search section headers for the Section Header String Table entry offset
            shstr_shaddr = self._get_section_header_offset_from_index(
                e_shoff, e_shnum, e_shentsize, e_shstrndx
            )

            # Read the "Section Header String Table" section header for address
            bin.seek((shstr_shaddr + bitnessValues["sh_offset_offset"]))
            if self.endianness == "LE":
                (shstrOffset,) = struct.unpack(
                    bitnessValues["Addr_STRUCT"],
                    bin.read(bitnessValues["Addr_SIZE"]),
                )
            else:
                shstrOffset = int(bin.read(bitnessValues["Addr_SIZE"]), 16)

            # Get the section header names and indexes
            sh_dict = self._read_sh_string_table(shstrOffset, e_shnum)

            # Find the index of ".text" in Section Header String Table
            textSectionInfo = sh_dict[".text"]
            text_shindx = textSectionInfo["index"]

            # Get the address of the .text section header
            text_shaddr = self._get_section_header_offset_from_index(
                e_shoff, e_shnum, e_shentsize, text_shindx
            )

            # Read the .text section header for the section size
            bin.seek(text_shaddr + bitnessValues["sh_size_offset"])
            if self.endianness == "LE":
                (text_shsize,) = struct.unpack(
                    bitnessValues["Xword_STRUCT"],
                    bin.read(bitnessValues["Xword_SIZE"]),
                )
            else:
                text_shsize = int(bin.read(bitnessValues["Xword_SIZE"]), 16)

            # Return the length of the text segment
            return text_shsize

    def _get_section_header_offset_from_index(
        self, shoff, shnum, shentsize, shstrndx
    ) -> int:
        """Function to get the offset of a specific section header (from the beginning
           of a file) based on it's section index

        Args:
            shoff (int): offset to the beginning of the section header table
            shnum (int): number of section headers
            shentsize (int): size of each section header entry
            shstrndx (int): index of desired section header

        Returns:
            int: offset to the requested section header from the beginning of the file
        """
        with open(self.path, "rb") as bin:
            bin.seek(shoff)
            for ndx in range(shnum):
                # Check if the section header is for the requested Section Header String Table index
                if ndx == shstrndx:
                    return bin.tell()
                # If section header name is not the requested index, move to the next section
                else:
                    bin.seek(shentsize, 1)

    def _read_sh_string_table(self, shstraddr, e_shnum) -> dict:
        """Function to iterate through section header string table

        Args:
            shstraddr (int): the address of the section header string table
            e_shnum (int): the number of sections in the binary

        Returns:
            dict: a dictionary containing all section header names and their corresponding index
        """
        with open(self.path, "rb") as f:
            sections = dict()

            # Jump to Section Header String Table
            f.seek(shstraddr + 1, 0)

            # Read section header names
            for ndx in range(-1, e_shnum):
                sectionName = "".join(iter(lambda: f.read(1).decode("ascii"), "\x00"))
                sections.update(
                    {
                        sectionName: {
                            "index": ndx,
                            "offset": (f.tell() - (shstraddr + 1) - (len(sectionName))),
                        },
                    }
                )

            return sections

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
