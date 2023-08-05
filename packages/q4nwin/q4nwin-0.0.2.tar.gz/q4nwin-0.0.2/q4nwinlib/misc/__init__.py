from __future__ import absolute_import


from q4nwinlib.misc import log

__all__ = ['log']

# -*- coding=Latin1 -*-
# import os
import subprocess
import struct
import time
import sys
import os
import six

from q4nwinlib.context import context

def NOPIE(fpath=""):
    import pefile
    pe_fp=pefile.PE(fpath)
    pe_fp.OPTIONAL_HEADER.DllCharacteristics &= \
        ~pefile.DLL_CHARACTERISTICS["IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE"]
    pe_fp.OPTIONAL_HEADER.CheckSum = pe_fp.generate_checksum()
    pe_fp.write(fpath)
def PIE(fpath=""):
    import pefile
    pe_fp=pefile.PE(fpath)
    pe_fp.OPTIONAL_HEADER.DllCharacteristics |= \
        pefile.DLL_CHARACTERISTICS["IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE"]
    pe_fp.OPTIONAL_HEADER.CheckSum = pe_fp.generate_checksum()
    pe_fp.write(fpath)

def pause(string=None):
    print(color("\n[=]: pausing",'purple'))
    if string is not None:
        print(color(string,'purple'))
    sys.stdin.readline()
def sleep(n):
    time.sleep(n)

def p64(i):
    endian = None
    if context.endian == 'little':
        endian = '<'
    else:
        endian = '>'
    l=struct.pack(endian+'Q', i)
    if sys.version_info[0]==3:
        return Latin1_decode(l)
    return l
def u64(s):
    endian = None
    if context.endian == 'little':
        endian = '<'
    else:
        endian = '>'
    return struct.unpack(endian+'Q', Latin1_encode(s))[0]
def p32(i):
    endian = None
    if context.endian == 'little':
        endian = '<'
    else:
        endian = '>'
    l=struct.pack(endian+'I', i)
    if sys.version_info[0]==3:
        return Latin1_decode(l)
    return l
def u32(s):
    endian = None
    if context.endian == 'little':
        endian = '<'
    else:
        endian = '>'
    return struct.unpack(endian+'I', Latin1_encode(s))[0]
def p16(i):
    endian = None
    if context.endian == 'little':
        endian = '<'
    else:
        endian = '>'
    l=struct.pack(endian+'H', i)
    if sys.version_info[0]==3:
        return Latin1_decode(l)
    return l
def u16(s):
    endian = None
    if context.endian == 'little':
        endian = '<'
    else:
        endian = '>'
    return struct.unpack(endian+'H', Latin1_encode(s))[0]
def p8(i):
    endian = None
    if context.endian == 'little':
        endian = '<'
    else:
        endian = '>'
    l=struct.pack(endian+'B', i)
    if sys.version_info[0]==3:
        return Latin1_decode(l)
    return l
def u8(s):
    endian = None
    if context.endian == 'little':
        endian = '<'
    else:
        endian = '>'
    return struct.unpack(endian+'B', Latin1_encode(s))[0]

def Latin1_encode(string): # -> bytes
    if sys.version_info[0]==3:
        return bytes(string,"Latin1")
    return bytes(string)
def Latin1_decode(string): # -> str
    if sys.version_info[0]==3:
        return str(string,'Latin1')
    return string

def color(content,color='purple'):
    if context.nocolor:
        return content
    c = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "purple": 35,
        "cyan": 36,
        "white": 37,
    }
    return "\033[0;{}m{}\033[0m".format(c.get(color), content)

def hexdump(src,length=16,all=True):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in range(0, len(src), length):
        chars = src[c:c+length]
        hex=''
        printable=''
        for i in range(len(chars)):
            chex="%02x " % ord(chars[i])
            pchar=("%s" % ((ord(chars[i]) <= 127 and FILTER[ord(chars[i])]) or '.'))
            if (i%4)==0:
                chex=' '+chex
                pchar=color('|','red')+pchar
            hex+=chex
            printable+=pchar
        lines.append(color(
            "{:04x}".format(c)) +
            "  {}  {}\n".format(color(hex.ljust(52,' '),'yellow'),printable)
        )
    if not all:
        if len(lines)>=0x20:
            lines=lines[0:8]+['......\n']+lines[-8:]
    print(''.join(lines).strip())
def showbanner(markstr,colorstr='green',typestr='[+]',is_noout=None):
    if is_noout is None:
        is_noout=context.noout
    if not is_noout:
        print(color('\n'+typestr+': '+markstr,colorstr))
def showbuf(buf,is_noout=None):
    if is_noout is None:
        is_noout=context.noout
    if not is_noout:
        if context.log_level=='debug':
            hexdump(buf)
        if buf.endswith(context.newline):
            os.write(sys.stdout.fileno(), Latin1_encode(buf))
        else:
            os.write(sys.stdout.fileno(), Latin1_encode(buf+'\n'))

def packer(value): # -> str
    if context.arch == "amd64":
        return p64(value)
    elif context.arch == "x86":
        return p32(value)
    else:
        raise Exception(color("no such context.arch",'red'))

def _flat(arg): # -> bytes
    if isinstance(arg, (list, tuple)):
        val = b''
        for it in arg:
            val += _flat(it)
    elif isinstance(arg, bytes):
        val = arg
    elif isinstance(arg, six.text_type):
        val = arg.encode('utf8')
    elif isinstance(arg, six.integer_types):
        val = Latin1_encode(packer(arg))
    elif isinstance(arg, bytearray):
        val = bytes(arg)    
    else:
        raise Exception(color("flat/fit doesn't support such type: "+str(type(arg)),'red'))
    return val
def flat(*args): # -> bytes
    # Flat simplified version
    result = b''
    for item in args:
        result += _flat(item)
    return result

fit = flat
