from utils.binaryfile import *

FILE_FORMAT_INFO = [
    {
        "ABBR": "ELF",
        "NAME": "Executable and Linkable Format",
        "MAGIC": bytes([0x7F, 0x45, 0x4C, 0x46]),
    },
    {
        "ABBR": "PE",
        "NAME": "Portable Executable (PE32/PE32+)",
        "MAGIC": bytes([0x4D, 0x5A]),
    },
]


PE_FORMAT = {
    "Machine": 4,
    "Format_Bitness": {
        32: 0x010B,
        64: 0x020B,
    },
    "e_lfanew": 60,
    "Magic": 24,
    "NumberOfSections": 6,
    "SizeOfCode": 28,
    "AddressOfEntryPoint": 40,
    32: {
        "SectionHeaders": 248,
    },
    64: {
        "SectionHeaders": 264,
    },
    "VirtualAddress": 4,
    "SizeOfRawData": 8,
    "PointerToRawData": 12,
    "NextSection": 32,
    "WORD_STRUCT": "<H",
    "WORD_SIZE": 2,
    "DWORD_STRUCT": "<L",
    "DWORD_SIZE": 4,
    "ADDR_STRUCT": "<L",
    "ADDR_SIZE": 4,
}

ELF_FORMAT = {
    "e_type": 4,
    "e_machine": 5,
    "e_entrypoint": 24,
    32: {
        "Word_STRUCT": "<l",
        "Word_SIZE": 4,
        "Half_STRUCT": "<h",
        "Half_SIZE": 2,
        "Addr_STRUCT": "<L",
        "Addr_SIZE": 4,
        "Xword_STRUCT": "<l",
        "Xword_SIZE": 4,
        "e_shoff": 32,
        "e_shentsize": 46,
        "e_shnum": 48,
        "e_shstrndx": 50,
        "sh_offset_offset": 16,
        "sh_size_offset": 20,
    },
    64: {
        "Word_STRUCT": "<l",
        "Word_SIZE": 4,
        "Half_STRUCT": "<h",
        "Half_SIZE": 2,
        "Addr_STRUCT": "<Q",
        "Addr_SIZE": 8,
        "Xword_STRUCT": "<q",
        "Xword_SIZE": 8,
        "e_shoff": 40,
        "e_shentsize": 58,
        "e_shnum": 60,
        "e_shstrndx": 62,
        "sh_offset_offset": 24,
        "sh_size_offset": 32,
    },
}
