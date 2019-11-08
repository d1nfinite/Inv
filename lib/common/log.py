# coding:utf-8


class Log:
    def __init__(self, mode=''):
        self.mode = mode

    def Info(self, info_str=''):
        print(u"[Info] " + info_str)

    def Debug(self, debug_str=''):
        if self.mode == "debug":
            print (u"[Debug] " + debug_str)

    def Error(self, error_str=''):
        print(u"[Error] " + error_str)


global InvLog
InvLog = Log(mode="debug")