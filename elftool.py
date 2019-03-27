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

def readPhdr(filepath, bits, ehdr):
    phdrtable = []
    if bits != 32 and bits != 64:
        raise ELFToolError('readPhdr: Invalid parameter')
    with open(filepath, "rb") as f:
        f.seek(ehdr.e_phoff)
        for i in range(ehdr.e_shnum):
            if bits == 32:
                phdr = Elf32_Phdr()
            else:
                phdr = Elf64_Phdr()
            buffer = io.BytesIO(f.read(ehdr.e_shentsize))
            buffer.readinto(phdr)
            phdrtable.append(phdr)
            del phdr
    return phdrtable

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

def stripelf(filepath, ehdr, shdrtbl):
    with open(filepath, "rb") as f:
        # ELF Header
        buffer = f.read(ehdr.e_ehsize)
        with open(filepath + '_ehdr', "wb") as elfheader:
            elfheader.write(buffer)
        # Program Header Table
        buffer = f.read(ehdr.e_phentsize * ehdr.e_phnum)
        with open(filepath + '_phdrtbl', "wb") as phdrtbl:
            phdrtbl.write(buffer)
        # Sections
        for i in range(1, ehdr.e_shnum):
            buffer = f.read(shdrtbl[i].sh_size)
            with open(filepath + '_' + readstr(filepath, shdrtbl[ehdr.e_shstrndx].sh_offset, shdrtbl[i].sh_name).decode('utf-8'), "wb") as section:
                section.write(buffer)
        # Section Header Table
        buffer = f.read(ehdr.e_shentsize * ehdr.e_shnum)
        with open(filepath + '_shdrtbl', "wb") as shdrtbl:
            shdrtbl.write(buffer)    

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
    shdrtbl = readShdr(filepath, bits, ehdr)
    stripelf(filepath, ehdr, shdrtbl)
    