# -*- coding=Latin1 -*-
import tempfile
import os
import sys
import subprocess

from q4nwinlib.context import context
from q4nwinlib.misc import showbanner,Latin1_encode,sleep,pause,color

class windbg():
    @classmethod
    def attach(clx,target,script="",sysroot=None):
        
        showbanner('attaching','purple','[=]')
        if context.windbg_path is None:
            raise Exception(color("can't find windbg.exe, plz set context.windbg_path",'red'))
        else:
            windbgPath=context.windbg
        load_windbg=[windbgPath,'-p']
        if isinstance(target,int):
            load_windbg.append(str(target))
        else:
            load_windbg.append(str(target.pid))

        script=context.dbginit+'\n'+script+'\n'
        tmp=tempfile.NamedTemporaryFile(prefix = 'winpwn_', suffix = '.dbg',delete=False)
        tmp.write(Latin1_encode(script))
        tmp.flush()
        tmp.close()
        load_windbg += ['-c']             # exec command
        load_windbg+=['$$><{}'.format(tmp.name)+';.shell -x del {}'.format(tmp.name)]
        # print('script:',script)
        # print('load:',load_windbg)
        ter=subprocess.Popen(load_windbg)
        while(os.path.exists(tmp.name)):    # wait_for_debugger
            pass
        target.debugger=ter
        return ter.pid

class windbgx():
    @classmethod
    def attach(clx,target,script="",sysroot=None):
        showbanner('attaching','purple','[=]')
        windbgxPath='windbgx'
        load_windbg=[windbgxPath,'-p']

        if isinstance(target,int):
            load_windbg.append(str(target)) # target is pid
        else:
            load_windbg.append(str(target.pid))
        script=context.dbginit+'\n'+script+'\n'

        tmp=tempfile.NamedTemporaryFile(prefix = 'winpwn_', suffix = '.dbg',delete=False)
        tmp.write(Latin1_encode(script))
        tmp.flush()
        tmp.close()
        load_windbg += ['-c']             # exec command
        load_windbg+=['"$$><{}'.format(tmp.name)+';.shell -x del {}"'.format(tmp.name)]
        # print('script:',script)
        # print('load:',load_windbg)
        ter=subprocess.Popen(' '.join(load_windbg))
        while(os.path.exists(tmp.name)):    # wait_for_debugger
            pass
        target.debugger=ter
        # mark('attached')
        return ter.pid

