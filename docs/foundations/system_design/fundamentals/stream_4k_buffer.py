"""
### 2. Why 4096 Bytes? (The Low-Level Infrastructure Story)

The number `4096` bytes (exactly 4 Kilobytes) is not a random number pulled out of thin air. 
It is one of the most foundational constants in hardware infrastructure and operating system design. 

When your code calls `file.read()`, it interacts with three deep system layers that are hardwired to process data in blocks of 4096:

#### A. Hard Drives and SSDs (Sector Sizes)
Physical storage drives do not read or write data one single letter at a time. They divide their physical storage space into small blocks called **sectors**. Modern hard drives and Solid State Drives (SSDs) use a standard standard sector size of exactly **4096 bytes** [1]. If your code requests 1 byte, the hardware still spins up and grabs a full 4096-byte chunk anyway [1]. 

#### B. The Operating System (Virtual Memory Paging)
Your computer's Operating System (Windows, macOS, or Linux) manages RAM using a mechanism called **Paging**. Memory is divided into small, fixed-size chunks called "pages," and the industry standard size for a single memory page is exactly **4096 bytes**. 

#### C. System Call Efficiency
Every time a programming language reads data from a file, it must pause and make an expensive request to the operating system kernel (a "System Call"). 
* If you read a 20GB file **1 byte at a time**, your code must make **20 billion** system calls, causing your CPU to lock up from administrative overhead.
* By reading in **4096-byte chunks**, you match the exact size of the hard drive sectors and the OS memory pages perfectly [1]. This ensures that one single read operation maps to exactly one physical hardware block pull, making your system perform at maximum possible physical speed [1].
"""

class ValidParentheses:
    def validate_massive_file(file_path):
        openToCloseMap = {'(': ')', '{': '}', '[': ']'}
        closing_set = set(openToCloseMap.values()) # Pure O(1) lookups
        
        stack = [] # stack only holds unmatched opening brackets
        
        # Open the file as a stream instead of loading it into RAM
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                # Read exactly 4KB of text at a time into memory
                # 4KB is one memory page size
                # This is for data that is not separated line by line
                # line by line is doing page/multiple pages
                # use file.read() if file is small
                # use file.read(4096) for unstructured raw file/image/unstructured text
                # use for line in file for structured files like logs, csv and json
                chunk = file.read(4096) 
                if not chunk:
                    break # Reached the absolute end of the 20GB file
                    
                # processes the 4KB chunk character by character
                for char in chunk:
                    if char in closing_set:
                        # If stack is empty or top open bracket doesn't match this close bracket
                        if not stack or openToCloseMap[stack[-1]] != char:
                            return False
                        stack.pop()
                    elif char in openToCloseMap:
                        stack.append(char)
                        
        # If the stack is empty after processing all chunks, the file is valid
        return not stack