#!/usr/bin/env python3
from ctypes import *
import io

# ======================================
# ELF Header struct
# ======================================
# 32bit
"""
/usr/include/linux/elf.h

typedef struct elf32_hdr{
  unsigned char	e_ident[EI_NIDENT];
  Elf32_Half	e_type;
  Elf32_Half	e_machine;
  Elf32_Word	e_version;
  Elf32_Addr	e_entry;  /* Entry point */
  Elf32_Off	e_phoff;
  Elf32_Off	e_shoff;
  Elf32_Word	e_flags;
  Elf32_Half	e_ehsize;
  Elf32_Half	e_phentsize;
  Elf32_Half	e_phnum;
  Elf32_Half	e_shentsize;
  Elf32_Half	e_shnum;
  Elf32_Half	e_shstrndx;
} Elf32_Ehdr;
"""
class Elf32_Ehdr(Structure):
  _fields_ = (
    ('e_ident', c_char * 16),
    ('e_type', c_uint16),
    ('e_machine', c_uint16),
    ('e_version', c_uint32),
    ('e_entry', c_uint32),
    ('e_phoff', c_uint32),
    ('e_shoff', c_uint32),
    ('e_flags', c_uint32),
    ('e_ehsize', c_uint16),
    ('e_phentsize', c_uint16),
    ('e_phnum', c_uint16),
    ('e_shentsize', c_uint16),
    ('e_shnum', c_uint16),
    ('e_shstrndx', c_uint16)
  )

# 64bit
"""
/usr/include/linux/elf.h

typedef struct elf64_hdr {
  unsigned char	e_ident[EI_NIDENT];	/* ELF "magic number" */
  Elf64_Half e_type;
  Elf64_Half e_machine;
  Elf64_Word e_version;
  Elf64_Addr e_entry;		/* Entry point virtual address */
  Elf64_Off e_phoff;		/* Program header table file offset */
  Elf64_Off e_shoff;		/* Section header table file offset */
  Elf64_Word e_flags;
  Elf64_Half e_ehsize;
  Elf64_Half e_phentsize;
  Elf64_Half e_phnum;
  Elf64_Half e_shentsize;
  Elf64_Half e_shnum;
  Elf64_Half e_shstrndx;
} Elf64_Ehdr;
"""
class Elf64_Ehdr(Structure):
  _fields_ = (
    ('e_ident', c_char * 16),
    ('e_type', c_uint16),
    ('e_machine', c_uint16),
    ('e_version', c_uint32),
    ('e_entry', c_uint64),
    ('e_phoff', c_uint64),
    ('e_shoff', c_uint64),
    ('e_flags', c_uint32),
    ('e_ehsize', c_uint16),
    ('e_phentsize', c_uint16),
    ('e_phnum', c_uint16),
    ('e_shentsize', c_uint16),
    ('e_shnum', c_uint16),
    ('e_shstrndx', c_uint16)
  )

# ======================================
# Program Header Struct
# ======================================
# 32bit
"""
typedef struct elf32_phdr{
  Elf32_Word	p_type;
  Elf32_Off	p_offset;
  Elf32_Addr	p_vaddr;
  Elf32_Addr	p_paddr;
  Elf32_Word	p_filesz;
  Elf32_Word	p_memsz;
  Elf32_Word	p_flags;
  Elf32_Word	p_align;
} Elf32_Phdr;
"""
class Elf32_Phdr(Structure):
  _fields_ = (
    ('p_type', c_uint32),
    ('p_offset', c_uint32),
    ('p_vaddr', c_uint32),
    ('p_paddr', c_uint32),
    ('p_filesz', c_uint32),
    ('p_memsz', c_uint32),
    ('p_flags', c_uint32),
    ('p_align', c_uint32)
  )

# 64bit
"""
typedef struct elf64_phdr {
  Elf64_Word p_type;
  Elf64_Word p_flags;
  Elf64_Off p_offset;		/* Segment file offset */
  Elf64_Addr p_vaddr;		/* Segment virtual address */
  Elf64_Addr p_paddr;		/* Segment physical address */
  Elf64_Xword p_filesz;		/* Segment size in file */
  Elf64_Xword p_memsz;		/* Segment size in memory */
  Elf64_Xword p_align;		/* Segment alignment, file & memory */
} Elf64_Phdr;
"""
class Elf64_Phdr(Structure):
  _fields_ = (
    ('p_type', c_uint32),
    ('p_flags', c_uint32),
    ('p_offset', c_uint64),
    ('p_vaddr', c_uint64),
    ('p_paddr', c_uint64),
    ('p_filesz', c_uint64),
    ('p_memsz', c_uint64),
    ('p_align', c_uint64)
  )

# ======================================
# Section Header Struct
# ======================================
# 32bit
"""
typedef struct elf32_shdr {
  Elf32_Word	sh_name;
  Elf32_Word	sh_type;
  Elf32_Word	sh_flags;
  Elf32_Addr	sh_addr;
  Elf32_Off	sh_offset;
  Elf32_Word	sh_size;
  Elf32_Word	sh_link;
  Elf32_Word	sh_info;
  Elf32_Word	sh_addralign;
  Elf32_Word	sh_entsize;
} Elf32_Shdr;
"""
class Elf32_Shdr(Structure):
  _fields_ = (
    ('sh_name', c_uint32),
    ('sh_type', c_uint32),
    ('sh_flags', c_uint32),
    ('sh_addr', c_uint32),
    ('sh_offset', c_uint32),
    ('sh_size', c_uint32),
    ('sh_link', c_uint32),
    ('sh_info', c_uint32),
    ('sh_addralign', c_uint32),
    ('sh_entsize', c_uint32)
  )

# 64bit
"""
typedef struct elf64_shdr {
  Elf64_Word sh_name;		/* Section name, index in string tbl */
  Elf64_Word sh_type;		/* Type of section */
  Elf64_Xword sh_flags;		/* Miscellaneous section attributes */
  Elf64_Addr sh_addr;		/* Section virtual addr at execution */
  Elf64_Off sh_offset;		/* Section file offset */
  Elf64_Xword sh_size;		/* Size of section in bytes */
  Elf64_Word sh_link;		/* Index of another section */
  Elf64_Word sh_info;		/* Additional section information */
  Elf64_Xword sh_addralign;	/* Section alignment */
  Elf64_Xword sh_entsize;	/* Entry size if section holds table */
} Elf64_Shdr;
"""
class Elf64_Shdr(Structure):
  _fields_ = (
    ('sh_name', c_uint32),
    ('sh_type', c_uint32),
    ('sh_flags', c_uint64),
    ('sh_addr', c_uint64),
    ('sh_offset', c_uint64),
    ('sh_size', c_uint64),
    ('sh_link', c_uint32),
    ('sh_info', c_uint32),
    ('sh_addralign', c_uint64),
    ('sh_entsize', c_uint64)
  )