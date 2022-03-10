from utils.executable import *

FILE_FORMAT_INFO = [
    {
        "abbr": "ELF",
        "name": "Executable and Linkable Format",
        "sig": bytes([0x7F, 0x45, 0x4C, 0x46]),
        "factory": ELFFactory(),
    },
    {
        "abbr": "DOS",
        "name": "DOS MZ executable (NE/PE)",
        "sig": bytes([0x4D, 0x5A]),
        "factory": DOSFactory(),
    },
]
