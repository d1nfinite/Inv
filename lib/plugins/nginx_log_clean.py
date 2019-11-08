# coding:utf-8
from subprocess import Popen, PIPE
from lib.common.pub import *
import traceback
import re


class NginxLogClean:
    def __init__(self, ip_list=[]):
        self.log_dir_list = []
        self.re_obj = re.compile('([^\s]+\.log)')
        self.ip_list = ip_list

    def search_log_dir(self):
        try:
            p1 = Popen('''find /Users/chenjingyuan1/Downloads/ -name "nginx.conf" |xargs cat |grep "log"''',
                       stdout=PIPE, shell=True)
            log_res_lines = p1.stdout.read().splitlines()
            for log_res in log_res_lines:
                log_res = str(log_res, encoding="utf-8")
                match_obj = self.re_obj.match(log_res)
                if match_obj:
                    file = match_obj.group(0)
                    file = file.split("/")
                    file_dir = "".join(file[:-1])
                    if os.path.isdir(file_dir):
                        self.log_dir_list.append(file_dir)
        except Exception:
            InvLog.Error(traceback.format_exc())

    def run(self):
        InvLog.Info("开始清除nginx相关日志")
        self.search_log_dir()
        try:
            # 遍历日志文件夹下所有日志
            for log_dir in self.log_dir_list:
                log_files = [os.path.join(log_dir, i) for i in os.listdir(log_dir)
                             if (not os.path.isdir(i))]
                for file in log_files:
                    match_file_and_remove(file, self.ip_list)
        except Exception:
            InvLog.Error(traceback.format_exc())
        InvLog.Info("nginx访问日志中相关ip: " + str(self.ip_list) + " 已清除完成")


if __name__ == "__main__":
    NginxLogClean().run()