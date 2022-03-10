"""
Description: This file defines the PH_Binary class
"""

from abc import ABC, abstractmethod


class BinaryFile:
    """This is the Factory pattern for format specific binary analysis"""

    @abstractmethod
    def get_entry_point(self):
        """This method will retreive the entry point of a binary file based on its format"""

    @abstractmethod
    def set_path(self, path):
        """This method will set the path to the designated binary"""

    @abstractmethod
    def get_format_info(self) -> str:
        """This method will get the abbreviation of the detected file format"""


class ELF(BinaryFile):
    """Executable and Linkable Format"""

    def __init__(self, path) -> None:
        self.path = path
        self.formatAbbr = "ELF"
        self.entrypoint = None

    def get_entry_point(self):
        return self.entrypoint

    def get_format_info(self) -> str:
        return self.formatAbbr


class DOS(BinaryFile):
    """DOS MZ executable (NE/PE)"""

    def __init__(self, path) -> None:
        self.path = path
        self.formatAbbr = "DOS"
        self.entrypoint = None

    def get_entry_point(self):
        return self.entrypoint

    def get_format_info(self) -> str:
        return self.formatAbbr


class BinaryFileFactory(ABC):
    """Factory that generates an BinaryFile object based on the file format signature discovered"""

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
