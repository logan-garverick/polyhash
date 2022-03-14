"""
Description: This file defines the BinaryFile class and its abstract methods
"""

from abc import abstractmethod


class BinaryFile:
    """This is the class pattern for format specific BinaryFile instances"""

    def __init__(self):
        self.path = None
        self.endianness = None
        self.entrypoint = None
        self.textSegLen = 0
        self.bitness = None

    @abstractmethod
    def _find_entry_point(self) -> int:
        """This method will find the entry point in the binary file based on its format"""

    @abstractmethod
    def _find_bitness(self) -> int:
        """This method will find the machine addressing (32 or 64 bit) in the binary file based on its format"""

    @abstractmethod
    def _find_endianness(self) -> str:
        """This method will find the endianess in the binary file based on its format"""

    @abstractmethod
    def _find_text_seg_len(self) -> int:
        """This method will find the length of the text segment in the binary file based on its format"""

    @abstractmethod
    def get_entry_point(self) -> int:
        """This method will returned the entry point of the binary"""

    @abstractmethod
    def get_format_info(self) -> dict:
        """This method will get the abbreviation of the detected file format"""

    @abstractmethod
    def display_format_info(self) -> None:
        """This method will display the BinaryFile information"""
