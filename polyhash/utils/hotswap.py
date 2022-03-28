"""
Description: This will be the definitions of the instruction hot-swapping functionality.
"""
from utils.instrReplaceConstants import *
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


def gen_hash_list(binary, swaps, startaddr) -> list:
    # Init locals
    content = None
    hashlist = []

    # Open binary file and read until EOF
    with open(binary, "rb") as bin:
        content = bin.read()

    # Generate original hash
    hashlist.append(generate_MD5_hash(content))

    # Generate possible hashes
    hashlist += gen_swaps(content, swaps, startaddr)

    print(f"NUMBER OF HASHES GENERATED --> {len(hashlist)}")

    # Clear any duplicate hash values
    hashlist = list(set(hashlist))

    return hashlist


def gen_swaps(content, swaps, startaddr) -> list:
    # Init locals
    hashlist = []

    # Generate possible swap contents
    for swap in swaps:

        # Make a clean copy of the file contents
        tempContent = bytearray(content)

        for bytesToSwap in swap["swaplist"]:
            for idx in range(len(bytesToSwap)):
                tempContent[startaddr + idx] = bytesToSwap[idx]

            # Generate hash of swapped file contents
            swapHash = generate_MD5_hash(tempContent)

            # Append generated hash onto hashlist
            hashlist.append(swapHash)

            # Remove current swap from swaps list
            if len(swaps) > 1:
                tempSwaps = [] + swaps
                tempSwaps.remove(swap)

                # Recursive call to generate all possible swap combinations
                print(f"DEBUG: RECURSIVE CALL WITH --> {len(tempSwaps)} SWAPS")
                hashlist += gen_swaps(
                    bytes(tempContent),
                    tempSwaps,
                    startaddr,
                )

    return hashlist


def generate_MD5_hash(content):

    # Split content into byteBlocks
    BLOCKSIZE = 4096
    byteBlocks = [content[i : i + BLOCKSIZE] for i in range(0, len(content), BLOCKSIZE)]

    # Pack the file contents into hash generator
    swapHash = md5()
    for byteBlock in iter(byteBlocks):
        swapHash.update(byteBlock)

    # Generate hash and return
    return swapHash.digest().hex()
