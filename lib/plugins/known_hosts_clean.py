# coding:utf-8
from lib.common.global_var import *
from lib.common.pub import *
import os
import traceback


class KnownHostsClean:
    def __init__(self, ip_list=[]):
        self.ip_list = ip_list
        self.ssh_dir_name = ".ssh"
        self.known_hosts = "known_hosts"

    def run(self):
        try:
            InvLog.Info("开始清除known_hosts相关记录")
            user_dir_list = get_value("user_dir")
            for user_dir in user_dir_list:
                if not os.path.exists(user_dir):
                    continue
                files = [os.path.join(user_dir, self.ssh_dir_name + "/" + self.known_hosts) for i in
                         os.listdir(user_dir) if i == ".ssh"]
                for known_hosts in files:
                    match_file_and_remove(known_hosts, self.ip_list)
            InvLog.Info("known_hosts记录中相关ip: " + str(self.ip_list) + " 已清除完成")
        except Exception:
            InvLog.Error(traceback.format_exc())


