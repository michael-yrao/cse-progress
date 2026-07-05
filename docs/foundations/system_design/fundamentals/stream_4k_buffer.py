"""
### 2. Why 4096 Bytes? (The Low-Level Infrastructure Story)

The number `4096` bytes (exactly 4 Kilobytes) is not a random number pulled out of thin air.
It is one of the most foundational constants in hardware infrastructure and operating system design.

When your code calls `file.read()`, it interacts with three deep system layers that are hardwired to process data in blocks of 4096:

#### A. Hard Drives and SSDs (Sector Sizes)
Physical storage drives do not read or write data one single letter at a time. They divide their physical storage space into small blocks called **sectors**. Modern hard drives and Solid State Drives (SSDs) use a standard sector size of exactly **4096 bytes**. If your code requests 1 byte, the hardware still spins up and grabs a full 4096-byte chunk anyway.

#### B. The Operating System (Virtual Memory Paging)
Your computer's Operating System (Windows, macOS, or Linux) manages RAM using a mechanism called **Paging**. Memory is divided into small, fixed-size chunks called "pages," and the industry standard size for a single memory page is exactly **4096 bytes**.

#### C. System Call Efficiency
Every time a programming language reads data from a file, it must pause and make an expensive request to the operating system kernel (a "System Call").
* If you read a 20GB file **1 byte at a time**, your code must make ~20 billion system calls, causing your CPU to lock up from administrative overhead.
* By reading in **4096-byte chunks**, you match the exact size of the hard drive sectors and the OS memory pages perfectly. One read operation maps to one physical hardware block pull, making the system perform at maximum possible physical speed.

Read-mode guide:
* `file.read()`        — small files only; loads the whole thing into RAM (OOM risk on big files).
* `file.read(4096)`    — raw/unstructured streams (binary, images); flat memory footprint.
* `for line in file:`  — structured, line-delimited data (logs, CSV, JSON Lines).
"""

from typing import Dict, List, Set


def validate_massive_file(file_path: str) -> bool:
    """Stream a huge file in 4 KB chunks and check balanced brackets, without loading it into RAM.

    The stack persists across chunk boundaries, so brackets that span two reads are still matched.
    """
    open_to_close: Dict[str, str] = {"(": ")", "{": "}", "[": "]"}
    closing_set: Set[str] = set(open_to_close.values())  # O(1) membership
    stack: List[str] = []                                # unmatched opening brackets

    # Open as a stream instead of loading the whole file into memory.
    with open(file_path, "r", encoding="utf-8") as file:
        while True:
            chunk = file.read(4096)          # one memory-page-sized read
            if not chunk:
                break                        # reached end of file
            for char in chunk:
                if char in closing_set:
                    # Empty stack, or the most recent opener doesn't match this closer.
                    if not stack or open_to_close[stack[-1]] != char:
                        return False
                    stack.pop()
                elif char in open_to_close:
                    stack.append(char)

    # Balanced iff every opener was matched and popped.
    return not stack
