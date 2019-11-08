# coding:utf-8
import os
import re
import traceback
from lib.common.pub import *


class SSHClean:
    def __init__(self, ip_list=[]):
        # 设置要清除的ip
        self.ip_list = ip_list

        # 设置要搜索的目录
        self.log_dir = "/var/log/"

        # 设置sshd的list
        self.sshd_list = []

        # 临时文件
        self.tmp_file = "tmp.log"
        self.tmp_file_f = ""
        self._create_file()

    def _create_file(self):
        if os.path.exists(self.tmp_file):
            try:
                self.tmp_file_f = open(self.tmp_file, "a")
            except Exception as e:
                InvLog.Error(e)
            return
        else:
            f = open(self.tmp_file, "w")
            f.close()
            try:
                self.tmp_file_f = open(self.tmp_file, "a")
            except Exception as e:
                InvLog.Error(e)

    def run(self):
        InvLog.Info("开始清除ssh登录日志")
        try:
            # 遍历/var/log目录下包含secure关键字的文件
            files = [os.path.join(self.log_dir, i) for i in os.listdir(self.log_dir)
                     if (not os.path.isdir(i) and ('secure' in i))]
            for log in files:
                with open(log, "r") as log_open:
                    # 保存文件时间
                    mtime, atime = get_file_time(log)
                    for log_line in log_open.readlines():
                        for ip in self.ip_list:
                            if ip in log_line:
                                sshd_obj = re.match("(sshd\[\d+\])", log_line)
                                if sshd_obj:
                                    self.sshd_list.append(sshd_obj.group(0))

                    # 重新打开文件
                    log_open = open(log, "r")
                    for log_line in log_open.readlines():
                        sshd_flag = False
                        for sshd in self.sshd_list:
                            if sshd in log_line:
                                sshd_flag = True
                        if not sshd_flag:
                            self.tmp_file_f.writelines(log_line)
                self.tmp_file_f.close()
                os.replace(self.tmp_file, log)
                # 还原文件修改时间
                set_file_time(log, mtime, atime)

                InvLog.Info("ssh登录日志中相关ip: "+str(self.ip_list)+" 已清除完成")
        except Exception:
            InvLog.Error(traceback.format_exc())


if __name__ == "__main__":
    SSHClean(ip_list=["127.0.0.1"]).run()