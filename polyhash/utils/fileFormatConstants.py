DOS_FORMAT = {
    "e_lfanew": 60,
    "Machine": 4,
    "Machine_Flags": {
        "32-bit": 0x014C,
        "64-bit": 0x8664,
    },
    "AddressOfEntryPoint": 40,
}

ELF_FORMAT = {
    "e_type": 4,
    "e_machine": 5,
    "e_entrypoint": 24,
}
