# coding:utf-8
from lib.plugins.ssh_clean import *
from lib.plugins.uxtmp_clean import *
from lib.common.global_var import *
from lib.plugins.known_hosts_clean import *
from lib.plugins.history_clean import *
from lib.plugins.nginx_log_clean import *


class Clean:
    def __init__(self):
        self.ip_list = get_value("ip")
        self.username_list = get_value("username")

    def run(self):
        SSHClean(ip_list=self.ip_list).run()
        UXTMPClean(ip_list=self.ip_list).run_utmp()
        UXTMPClean(ip_list=self.ip_list).run_wtmp()
        KnownHostsClean(ip_list=self.ip_list).run()
        HistoryClean().run()
        NginxLogClean(ip_list=self.ip_list).run()