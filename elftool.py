#!/usr/bin/env python3
from elfstruct import *
import io

#TODO WIP
def stripelf(filepath):
    with open(filepath, "rb") as f:
        # Check ELF Magic
        magic = f.read(5)
        if magic == b'\x7fELF\x01': # ELF32
            print("32Bit ELF")
            elfhdr = Elf32_Ehdr()
        elif magic == b'\x7fELF\x02': # ELF 64
            print("64Bit ELF")
            elfhdr = Elf64_Ehdr()
        else:
            print("Unsupport file")
            return

        # Read to Buffer
        f.seek(0)
        buffer = io.BytesIO(f.read())
        buffer.readinto(elfhdr)
        print("Start of program headers: {} (bytes into file)".format(elfhdr.e_phoff))
        print("Start of section headers: {} (bytes into file)".format(elfhdr.e_shoff))

if __name__ == "__main__":
    print("path?")
    try:
        stripelf(input())
    except FileNotFoundError:
        print("File not found. Try again.")