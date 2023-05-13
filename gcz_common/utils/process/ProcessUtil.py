import ctypes
from multiprocessing import Process
import os
import signal

class ProcessUtil():
    def __init__(self, statement=True):
        self.process = ''
        if statement: self.statement()

    def startProcess(self, function, args=(), kwargs={}):
        """
        启动进程
        @param function: 函数
        @return: 该进程类
        """
        self.process = Process(target=function, args=args, kwargs=kwargs)
        self.process.start()
        return self.process

    def stopProcess(self, tid=0):
        """
        结束进程
        @param tid: 进程id
        @return:
        """
        if tid == 0:
            process = self.process
            tid = ctypes.c_long(process.ident).value
        if (type(tid) == Process):
            tid = ctypes.c_long(tid.ident).value
        try:
            os.kill(tid, signal.SIGILL)
        except Exception as e:
            print("结束进程失败！")

    def statement(self):
        statement = f'{self.__class__.__name__}\n' \
                    '作者: 梦辰雪（Cui Mengchao）\n' \
                    '版本号: v1.0.0\n' \
                    '更新时间: 2023-05-13\n' \
                    'gitee: https://gitee.com/mcxgitee\n'
        print(f'\033[1;33m{statement}\033[0m\n')

# region 单例
instance = None

def initInstance(statement=True):
    global instance
    if not instance:
        instance = ProcessUtil(statement=statement)
    return instance
# endregion