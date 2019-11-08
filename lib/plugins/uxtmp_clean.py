# coding:utf-8
import struct
import traceback
from lib.common.pub import *


class UXTMPClean:
    def __init__(self, ip_list=[]):
        self.ip_list = ip_list
        self.utmp_file = "/var/run/utmp"
        self.wtmp_file = "/var/log/wtmp"
        self.tmp_struct = "hi32s4s32s256shhiii4i20x"
        self.tmp_struct_obj = struct.Struct("hi32s4s32s256shhiii4i20x")
        self.tmp_struct_size = struct.calcsize(self.tmp_struct)

    def run_wtmp(self):
        InvLog.Info("开始清除wtmp登录日志")
        try:
            # 清除wtmp相关
            with open(self.wtmp_file, "rb") as wtmp_f_r:
                wtmp_new = bytes()
                while True:
                    wtmp_bytes = wtmp_f_r.read(self.tmp_struct_size)
                    if not wtmp_bytes:
                        break
                    data = struct.unpack(self.tmp_struct, wtmp_bytes)
                    record = [(lambda s: str(s).split("\0", 1)[0])(i) for i in data]
                    ip_flag = False
                    for ip in self.ip_list:
                        if ip in record[5]:
                            ip_flag = True
                            break
                    if not ip_flag:
                        wtmp_new += wtmp_bytes
                with open(self.wtmp_file, "w+b") as wtmp_f_w:
                    wtmp_f_w.write(wtmp_new)
                wtmp_f_w.close()
            wtmp_f_r.close()
            InvLog.Info("wtmp登录日志中相关ip: "+str(self.ip_list)+" 已清除完成")
        except Exception:
            InvLog.Error(traceback.format_exc())

    def run_utmp(self):
        InvLog.Info("开始清除utmp登录日志")
        try:
            # 清除utmp相关
            with open(self.utmp_file, "rb") as utmp_f_r:
                utmp_new = bytes()
                while True:
                    utmp_bytes = utmp_f_r.read(self.tmp_struct_size)
                    if not utmp_bytes:
                        break
                    data = struct.unpack(self.tmp_struct, utmp_bytes)
                    record = [(lambda s: str(s).split("\0", 1)[0])(i) for i in data]
                    ip_flag = False
                    for ip in self.ip_list:
                        if ip in record[5]:
                            ip_flag = True
                            break
                    if not ip_flag:
                        utmp_new += utmp_bytes
                with open(self.utmp_file, "w+b") as utmp_f_w:
                    utmp_f_w.write(utmp_new)
                utmp_f_w.close()
            utmp_f_r.close()
            InvLog.Info("utmp登录日志中相关ip: "+str(self.ip_list)+" 已清除完成")
        except Exception:
            InvLog.Error(traceback.format_exc())


if __name__ == "__main__":
    UXTMPClean(ip_list=["172.28.14.121"]).run()