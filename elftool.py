#!/usr/bin/env python3
from elfstruct import *
import io

class ELFToolError(Exception):
    pass

def checkelf(filepath):
    with open(filepath, "rb") as f:
        # Check ELF Magic
        magic = f.read(5)
    if magic == b'\x7fELF\x01': # ELF32
        print("==== 32Bit ELF ====")
        return 32
    elif magic == b'\x7fELF\x02': # ELF64
        print("==== 64Bit ELF ====")
        return 64
    else:
        raise ELFToolError('checkelf: Unsupport File')

def readEhdr(filepath, bits):
    if bits == 32:
        ehdr = Elf32_Ehdr()
    elif bits == 64:
        ehdr = Elf64_Ehdr()
    else:
        raise ELFToolError('readEhdr: Invalid parameter')
    # load to buffer
    with open(filepath, "rb") as f:
        buffer = io.BytesIO(f.read())
    # make ehdr instance
    buffer.readinto(ehdr)
    return ehdr
        
def readShdr(filepath, bits, ehdr):
    shdrtable = []
    if bits != 32 and bits != 64:
        raise ELFToolError('readShdr: Invalid parameter')
    with open(filepath, "rb") as f:
        f.seek(ehdr.e_shoff)
        for i in range(ehdr.e_shnum):
            if bits == 32:
                shdr = Elf32_Shdr()
            else:
                shdr = Elf64_Shdr()
            buffer = io.BytesIO(f.read(ehdr.e_shentsize))
            buffer.readinto(shdr)
            shdrtable.append(shdr)
            del shdr
    return shdrtable

def readstr(filepath, offset, index):
    if index == 0:
        return b''
    with open(filepath, "rb") as f:
        f.seek(offset + index)
        string = b''
        while True:
            chr = f.read(1)
            if chr != b'\x00':
                string += chr
            else:
                break
    return string

#def stripelf(filepath, ehdr, shdr):
    

if __name__ == "__main__":
    print("path?")
    while True:
        filepath = input()
        try:
            bits = checkelf(filepath)
            break
        except FileNotFoundError:
            print("File not found. Try again.")
    ehdr = readEhdr(filepath, bits)
    print("Start of program headers: {} (bytes into file)".format(ehdr.e_phoff))
    print("Start of section headers: {} (bytes into file)".format(ehdr.e_shoff))
    shdrtable = readShdr(filepath, bits, ehdr)
    print("==== Section Header List ====")
    for i in range(ehdr.e_shnum):
        print("{}: {}".format(i, readstr(filepath, shdrtable[ehdr.e_shstrndx].sh_offset, shdrtable[i].sh_name).decode('utf-8')))
    