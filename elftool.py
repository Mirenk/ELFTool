#!/usr/bin/env python3
from elfstruct import *
import io

class ELFToolError(Exception):
    pass

def checkELF(filepath):
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
        
# For Section Header Table and Program Header Table
def readHdrTable(filepath, bits, type, offset, size):
    table = []
    if bits != 32 and bits != 64 and type != 'Shdr' and type != 'Phdr':
        raise ELFToolError('readShdr: Invalid parameter')
    with open(filepath, "rb") as f:
        f.seek(offset)
        for i in range(ehdr.e_shnum):
            if bits == 32:
                if type == 'Shdr':
                    hdr = Elf32_Shdr()
                elif type == 'Phdr':
                    hdr = Elf32_Phdr()
            elif bits == 64:
                if type == 'Shdr':
                    hdr = Elf64_Shdr()
                elif type == 'Phdr':
                    hdr = Elf64_Phdr()
            buffer = io.BytesIO(f.read(size))
            buffer.readinto(hdr)
            table.append(hdr)
            del hdr
    return table

# For string table(e.g. .dynstr, .shstrtab)
def readStr(filepath, offset, index):
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

def stripELF(filepath, ehdr, shtab):
    with open(filepath, "rb") as f:
        # ELF Header
        buffer = f.read(ehdr.e_ehsize)
        with open(filepath + '_ehdr', "wb") as elfheader:
            elfheader.write(buffer)
        # Program Header Table
        buffer = f.read(ehdr.e_phentsize * ehdr.e_phnum)
        with open(filepath + '_phtab', "wb") as phtab:
            phtab.write(buffer)
        # Sections
        for i in range(1, ehdr.e_shnum):
            buffer = f.read(shtab[i].sh_size)
            with open(filepath + '_' + readStr(filepath, shtab[ehdr.e_shstrndx].sh_offset, shtab[i].sh_name).decode('utf-8'), "wb") as section:
                section.write(buffer)
        # Section Header Table
        buffer = f.read(ehdr.e_shentsize * ehdr.e_shnum)
        with open(filepath + '_shtab', "wb") as shtab:
            shtab.write(buffer)    

if __name__ == "__main__":
    print("path?")
    while True:
        filepath = input()
        try:
            bits = checkELF(filepath)
            break
        except FileNotFoundError:
            print("File not found. Try again.")
    ehdr = readEhdr(filepath, bits)
    shtab = readHdrTable(filepath, bits, 'Shdr', ehdr.e_shoff, ehdr.e_shentsize)
    stripELF(filepath, ehdr, shtab)
    