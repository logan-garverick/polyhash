"""
Description: This will be the definitions of the instruction hot-swapping functionality.
"""
from instrReplaceConstants import *
from hashlib import md5
from iced_x86 import *


def find_swaps(decoder, entrypoint, fileContent):
    # Init locals
    swaps = []
    swapset = None
    instrCnt = 0

    for instr in decoder:
        # Get instruction bytes
        start_index = instr.ip - entrypoint
        bytes_str = fileContent[start_index : start_index + instr.len]

        # Determine if instruction is hot-swappable
        if bytes_str in TARGET_INSTR_LIST:
            # Find corresponding swap list entry
            for ent in INSTR_SWAP_SETS:
                if bytes_str == ent["ORIG_INSTR"]:
                    swapset = ent["SWAPS"]

            # Create entry in list of possible swaps
            swaps.append(
                {
                    "offset": start_index,
                    "swaplist": swapset,
                }
            )

        # Increment instruction count
        instrCnt += 1

    return instrCnt, swaps
