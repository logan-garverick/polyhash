from utils.binaryfile import *
from utils.fileFormatConstants import *


class BinaryFileFactory(ABC):
    """Factory that generates an BinaryFile object based on the file format signature discovered"""

    def get_BinaryFile_instance(self, path) -> BinaryFile:
        # Read the magic character values from the file and determine file type (if supported)
        formatInfo = self._read_magic(path)

        # Verify that a file format was determined
        if formatInfo == None:
            return None
        # If format was found, return the corresponding BinaryFile instance
        else:
            if formatInfo["ABBR"] == "ELF":
                return ELF(path)
            elif formatInfo["ABBR"] == "PE":
                return PE(path)

    def _read_magic(self, path) -> dict:
        """Check the provided binary file for common magic characters to determine file format

        Returns:
            str: the file format of the provided binary
        """
        with open(path, "rb") as binary:
            fileHeader = binary.read(32)
            for format in FILE_FORMAT_INFO:
                if fileHeader.startswith(format.get("MAGIC")):
                    return format
            return None
