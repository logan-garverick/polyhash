DOS_FORMAT = {
    "e_lfanew": 60,
    "Machine": 4,
    "Machine_Flags": {
        32: 0x014C,
        64: 0x8664,
    },
    "AddressOfEntryPoint": 40,
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
