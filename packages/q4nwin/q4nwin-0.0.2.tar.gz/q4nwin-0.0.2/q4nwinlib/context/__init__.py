# -*- coding=Latin1 -*-
class context():
    # basic
    arch='amd64' # x86
    endian='little' # big
    log_level=""
    timeout=512
    tick=0.0625
    newline='\r\n'
    pie=None

    # input output
    noout=None
    nocolor=None

    # debug
    dbginit="" # debugger init command
    windbg_path=None # set windbg.exe path 
