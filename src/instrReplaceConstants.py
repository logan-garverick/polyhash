"""
Description: This file defines the instructions that PolyHash should search for and possible 
             "hot-swappable" instructions to change hash of a file without altering execution.
"""

# Multi-byte NOP Combos
XXXX = bytes([])
NOP1 = bytes([0x90])
NOP2 = bytes([0x66, 0x90])
NOP3 = bytes([0x0F, 0x1F, 0x00])
NOP4 = bytes([0x0F, 0x1F, 0x40, 0x00])
NOP5 = bytes([0x0F, 0x1F, 0x40, 0x00, 0x00])
NOP6 = bytes([0x66, 0x0F, 0x1F, 0x44, 0x00, 0x00])
NOP7 = bytes([0x0F, 0x1F, 0x80, 0x00, 0x00, 0x00, 0x00])
NOP8 = bytes([0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00])
NOP9 = bytes([0x66, 0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00])


SWAPLIST_1_BYTES = []

SWAPLIST_2_BYTES = [
    # 1 byte opcode swaps
    NOP1 + NOP1,
    # 2 byte opcode swaps
    NOP2 + XXXX,
]

SWAPLIST_3_BYTES = [
    # 1 byte opcode swaps
    NOP1 + NOP1 + NOP1,
    # 2+1 byte opcode swaps
    NOP2 + NOP1 + XXXX,
    NOP1 + NOP2 + XXXX,
    # 3 byte opcode swaps
    NOP3 + XXXX + XXXX,
]

SWAPLIST_4_BYTES = [
    # 1 byte opcode swaps
    NOP1 + NOP1 + NOP1 + NOP1,
    # 2+1 byte opcode swaps
    NOP2 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP2 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP2 + XXXX,
    # 2 byte opcode swaps
    NOP2 + NOP2 + XXXX + XXXX,
    # 3+1 byte opcode swaps
    NOP3 + NOP1 + XXXX + XXXX,
    NOP1 + NOP3 + XXXX + XXXX,
    # 4 byte opcode swaps
    NOP4 + XXXX + XXXX + XXXX,
]

SWAPLIST_5_BYTES = [
    # 1 byte opcode swaps
    NOP1 + NOP1 + NOP1 + NOP1 + NOP1,
    # 2+1 byte opcode swaps
    NOP2 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP2 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP2 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP2 + XXXX,
    NOP2 + NOP2 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP2 + XXXX + XXXX,
    NOP1 + NOP2 + NOP2 + XXXX + XXXX,
    # 3+1 byte opcode swaps
    NOP3 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP3 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP3 + XXXX + XXXX,
    # 3+2 byte opcode swaps
    NOP3 + NOP2 + XXXX + XXXX + XXXX,
    NOP2 + NOP3 + XXXX + XXXX + XXXX,
    # 4+1 byte opcode swaps
    NOP4 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP4 + XXXX + XXXX + XXXX,
    # 5 byte opcode swaps
    NOP5 + XXXX + XXXX + XXXX + XXXX,
]

SWAPLIST_6_BYTES = [
    # 1 byte opcode swaps
    NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1,
    # 2 byte opcode swaps
    NOP2 + NOP2 + NOP2 + XXXX + XXXX + XXXX,
    # 3 byte opcode swaps
    NOP3 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    # 6 byte opcode swaps
    NOP6 + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 2+1 byte opcode swaps
    NOP2 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP2 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP2 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP2 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP2 + XXXX,
    NOP2 + NOP2 + NOP1 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP2 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP2 + XXXX + XXXX,
    NOP1 + NOP2 + NOP2 + NOP1 + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP2 + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP2 + XXXX + XXXX,
    # 3+1 byte opcode swaps
    NOP3 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP3 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP3 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP3 + XXXX + XXXX,
    # 4+1 byte opcode swaps
    NOP4 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP4 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP4 + XXXX + XXXX + XXXX,
    # 5+1 byte opcode swaps
    NOP5 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP5 + XXXX + XXXX + XXXX + XXXX,
    # 4+2 byte opcode swaps
    NOP4 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP4 + XXXX + XXXX + XXXX + XXXX,
    # 3+2+1 byte opcode swaps
    NOP3 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP2 + XXXX + XXXX + XXXX,
    NOP2 + NOP3 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP3 + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP3 + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP2 + XXXX + XXXX + XXXX,
]

SWAPLIST_7_BYTES = [
    # 1 byte opcode swaps
    NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1,
    # 7 byte opcode swaps
    NOP7 + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 2+1 byte opcode swaps
    NOP2 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP2 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP2 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP2 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP2 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP2 + XXXX,
    NOP2 + NOP2 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP2 + NOP1 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP2 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP1 + NOP2 + XXXX + XXXX,
    NOP1 + NOP2 + NOP2 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP2 + NOP1 + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP1 + NOP2 + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP2 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP1 + NOP2 + XXXX + XXXX,
    NOP2 + NOP2 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP2 + NOP1 + NOP2 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP2 + NOP2 + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP2 + NOP2 + XXXX + XXXX + XXXX,
    # 3+1 byte opcode swaps
    NOP3 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP3 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP3 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP3 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP3 + XXXX + XXXX,
    NOP3 + NOP3 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    # 4+1 byte opcode swaps
    NOP4 + NOP1 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP4 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP4 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP4 + XXXX + XXXX + XXXX,
    # 5+1 byte opcode swaps
    NOP5 + NOP1 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP5 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP5 + XXXX + XXXX + XXXX + XXXX,
    # 6+1 byte opcode swaps
    NOP6 + NOP1 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP6 + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 3+2 byte opcode swaps
    NOP3 + NOP2 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP3 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP2 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    # 5+2 byte opcode swaps
    NOP5 + NOP2 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP5 + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 4+3 byte opcode swaps
    NOP4 + NOP3 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP4 + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 3+2+1 byte opcode swaps
    NOP3 + NOP2 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP1 + NOP2 + XXXX + XXXX + XXXX,
    NOP2 + NOP3 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP3 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP3 + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP3 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP3 + NOP2 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP3 + XXXX + XXXX + XXXX,
    # 4+2+1 byte opcode swaps
    NOP4 + NOP2 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP4 + NOP1 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP4 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP4 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP4 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP4 + NOP2 + XXXX + XXXX + XXXX + XXXX,
]

SWAPLIST_8_BYTES = [
    # 1 byte opcode swaps
    NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1,
    # 2 byte opcode swaps
    NOP2 + NOP2 + NOP2 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    # 4 byte opcode swaps
    NOP4 + NOP4 + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 8 byte opcode swaps
    NOP8 + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 2+1 byte opcode swaps
    NOP2 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP2 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP2 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP2 + NOP1 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP2 + NOP1 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP2 + NOP1 + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP2 + XXXX,
    NOP2 + NOP2 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP2 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP2 + NOP1 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP1 + NOP2 + NOP1 + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP1 + NOP1 + NOP2 + XXXX + XXXX,
    NOP1 + NOP2 + NOP2 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP2 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP1 + NOP2 + NOP1 + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP1 + NOP1 + NOP2 + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP2 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP1 + NOP2 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP1 + NOP1 + NOP2 + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP2 + NOP2 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP2 + NOP1 + NOP2 + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP2 + NOP2 + XXXX + XXXX,
    NOP2 + NOP2 + NOP2 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP2 + NOP1 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP2 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP2 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP2 + NOP1 + NOP1 + NOP2 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP2 + NOP1 + NOP2 + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP2 + NOP1 + NOP2 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP2 + NOP2 + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP2 + NOP2 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP2 + NOP2 + XXXX + XXXX + XXXX,
    # 3+1 byte opcode swaps
    NOP3 + NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP3 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP3 + NOP1 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP3 + NOP1 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP3 + NOP1 + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP1 + NOP3 + XXXX + XXXX,
    NOP3 + NOP3 + NOP1 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP3 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP1 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP3 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP1 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP3 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    # 4+1 byte opcode swaps
    NOP4 + NOP1 + NOP1 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP4 + NOP1 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP4 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP4 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP1 + NOP4 + XXXX + XXXX + XXXX,
    # 5+1 byte opcode swaps
    NOP5 + NOP1 + NOP1 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP5 + NOP1 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP5 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP5 + XXXX + XXXX + XXXX + XXXX,
    # 6+1 byte opcode swaps
    NOP6 + NOP1 + NOP1 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP6 + NOP1 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP6 + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 7+1 byte opcode swaps
    NOP7 + NOP1 + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP7 + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 3+2 byte opcode swaps
    NOP3 + NOP3 + NOP2 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP2 + NOP3 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP3 + NOP3 + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 4+2 byte opcode swaps
    NOP4 + NOP2 + NOP2 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP4 + NOP2 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP2 + NOP4 + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 6+2 byte opcode swaps
    NOP6 + NOP2 + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP6 + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 5+3 byte opcode swaps
    NOP5 + NOP3 + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP5 + XXXX + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 3+2+1 byte opcode swaps
    NOP3 + NOP2 + NOP1 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP2 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP1 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP1 + NOP1 + NOP2 + XXXX + XXXX + XXXX,
    NOP2 + NOP3 + NOP1 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP3 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP3 + NOP1 + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP1 + NOP3 + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP2 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP1 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP1 + NOP1 + NOP2 + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP3 + NOP1 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP3 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP1 + NOP3 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP3 + NOP2 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP3 + NOP1 + NOP2 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP3 + NOP1 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP1 + NOP3 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP3 + NOP2 + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP1 + NOP2 + NOP3 + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP2 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP3 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP2 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP3 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP3 + NOP2 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP2 + NOP3 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP2 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP2 + NOP1 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP2 + NOP1 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP3 + NOP1 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP2 + NOP2 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP2 + NOP3 + XXXX + XXXX + XXXX + XXXX,
    # 4+2+1 byte opcode swaps
    NOP4 + NOP1 + NOP2 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP2 + NOP4 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP4 + NOP1 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP4 + NOP1 + NOP1 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP4 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP4 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP1 + NOP4 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP1 + NOP4 + NOP2 + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP4 + NOP2 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP4 + NOP2 + NOP1 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP1 + NOP4 + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP4 + NOP1 + NOP1 + XXXX + XXXX + XXXX + XXXX,
    # 5+2+1 byte opcode swaps
    NOP5 + NOP2 + NOP1 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP5 + NOP1 + NOP2 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP5 + NOP1 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP2 + NOP5 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP2 + NOP1 + NOP5 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP5 + NOP2 + XXXX + XXXX + XXXX + XXXX + XXXX,
    # 4+3+1 byte opcode swaps
    NOP4 + NOP3 + NOP1 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP1 + NOP4 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP3 + NOP4 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP1 + NOP4 + NOP3 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP3 + NOP4 + NOP1 + XXXX + XXXX + XXXX + XXXX + XXXX,
    NOP4 + NOP1 + NOP3 + XXXX + XXXX + XXXX + XXXX + XXXX,
]

TARGET_INSTR_LIST = [
    NOP2,
    NOP3,
    NOP4,
    NOP5,
    NOP6,
    NOP7,
    NOP8,
]

INSTR_SWAP_SETS = [
    {
        # Multi-byte NOP (2 bytes)
        "ORIG_INSTR": NOP2,
        # "SWAPS": SWAPLIST_2_BYTES.remove(NOP2),
        "SWAPS": [x for x in SWAPLIST_2_BYTES if x != NOP2],
    },
    {
        # Multi-byte NOP (3 bytes)
        "ORIG_INSTR": NOP3,
        "SWAPS": [x for x in SWAPLIST_3_BYTES if x != NOP3],
    },
    {
        # Multi-byte NOP (4 bytes)
        "ORIG_INSTR": NOP4,
        "SWAPS": [x for x in SWAPLIST_4_BYTES if x != NOP4],
    },
    {
        # Multi-byte NOP (5 bytes)
        "ORIG_INSTR": NOP5,
        "SWAPS": [x for x in SWAPLIST_5_BYTES if x != NOP5],
    },
    {
        # Multi-byte NOP (6 bytes)
        "ORIG_INSTR": NOP6,
        "SWAPS": [x for x in SWAPLIST_6_BYTES if x != NOP6],
    },
    {
        # Multi-byte NOP (7 bytes)
        "ORIG_INSTR": NOP7,
        "SWAPS": [x for x in SWAPLIST_7_BYTES if x != NOP7],
    },
    {
        # Multi-byte NOP (8 bytes)
        "ORIG_INSTR": NOP8,
        "SWAPS": [x for x in SWAPLIST_8_BYTES if x != NOP8],
    },
]
