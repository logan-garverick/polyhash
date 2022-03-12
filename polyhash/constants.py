from utils.binaryfile import *

FILE_FORMAT_INFO = [
    {
        "abbr": "ELF",
        "name": "Executable and Linkable Format",
        "sig": bytes([0x7F, 0x45, 0x4C, 0x46]),
        "factory": ELFFactory(),
    },
    {
        "abbr": "PE",
        "name": "Portable Executable (PE32/PE32+)",
        "sig": bytes([0x4D, 0x5A]),
        "factory": PEFactory(),
    },
]
