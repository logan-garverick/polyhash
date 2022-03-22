"""
Description: This file defines the instructions that PolyHash should search for and possible 
             "hot-swappable" instructions to change hash of a file without altering execution.
"""

SWAPLIST_2_BYTES = [
    # 1 byte opcode swaps
    bytes([0x90, 0x90]),
    # 2 byte opcode swaps
    bytes([0x66, 0x90]),
]

SWAPLIST_3_BYTES = [
    # 1 byte opcode swaps
    bytes([0x90, 0x90, 0x90]),
    # 2+1 byte opcode swaps
    bytes([0x66, 0x90, 0x90]),
    bytes([0x90, 0x66, 0x90]),
    # 3 byte opcode swaps
    bytes([0x0F, 0x1F, 0x00]),
]

SWAPLIST_4_BYTES = [
    # 1 byte opcode swaps
    bytes([0x90, 0x90, 0x90, 0x90]),
    # 2+1 byte opcode swaps
    bytes([0x66, 0x90, 0x90, 0x90]),
    bytes([0x90, 0x66, 0x90, 0x90]),
    bytes([0x90, 0x90, 0x66, 0x90]),
    # 2 byte opcode swaps
    bytes([0x66, 0x90, 0x66, 0x90]),
    # 3+1 byte opcode swaps
    bytes([0x0F, 0x1F, 0x00, 0x90]),
    bytes([0x90, 0x0F, 0x1F, 0x00]),
    # 4 byte opcode swaps
    bytes([0x0F, 0x1F, 0x40, 0x00]),
]

SWAPLIST_5_BYTES = [
    # 1 byte opcode swaps
    bytes([0x90, 0x90, 0x90, 0x90, 0x90]),
    # 2+1 byte opcode swaps
    bytes([0x66, 0x90, 0x90, 0x90, 0x90]),
    bytes([0x90, 0x66, 0x90, 0x90, 0x90]),
    bytes([0x90, 0x90, 0x66, 0x90, 0x90]),
    bytes([0x90, 0x90, 0x90, 0x66, 0x90]),
    bytes([0x66, 0x90, 0x66, 0x90, 0x90]),
    bytes([0x90, 0x66, 0x90, 0x66, 0x90]),
    # 3+1 byte opcode swaps
    bytes([0x0F, 0x1F, 0x00, 0x90, 0x90]),
    bytes([0x90, 0x0F, 0x1F, 0x00, 0x90]),
    bytes([0x90, 0x90, 0x0F, 0x1F, 0x00]),
    # 3+2 byte opcode swaps
    bytes([0x0F, 0x1F, 0x00, 0x66, 0x90]),
    bytes([0x66, 0x90, 0x0F, 0x1F, 0x00]),
    # 4+1 byte opcode swaps
    bytes([0x0F, 0x1F, 0x40, 0x00, 0x90]),
    bytes([0x90, 0x0F, 0x1F, 0x40, 0x00]),
    # 5 byte
    bytes([0x0F, 0x1F, 0x40, 0x00, 0x00]),
]

INSTR_SET = [
    {
        # Multi-byte NOP (2 bytes)
        "ORIG_INSTR": bytes([0x66, 0x90]),
        "SWAPS": SWAPLIST_2_BYTES,
    },
    {
        # Multi-byte NOP (3 bytes)
        "ORIG_INSTR": bytes([0x0F, 0x1F, 0x00]),
        "SWAPS": SWAPLIST_3_BYTES,
    },
    {
        # Multi-byte NOP (4 bytes)
        "ORIG_INSTR": bytes([0x0F, 0x1F, 0x40, 0x00]),
        "SWAPS": SWAPLIST_4_BYTES,
    },
]