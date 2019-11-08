# coding:utf-8
import traceback
from lib.common.global_var import *
from lib.common.log import *
from lib.common.pub import *
import os

"""
清除模式
1.根据关键字
2.逐条确认
3.全部清除
"""


class HistoryClean:
    def __init__(self):
        self.user_dir_dict = {}
        self.username_list = get_value("username")
        self.user_dir_dict = get_value("user_dir_dict")
        self.history_file_list = [".bash_history", ".zsh_history", ".csh_history", ".ksh_history"]
        self.mode = get_value("history_clean_mode")
        self.keyword = get_value("history_clean_keyword")

    def run(self):
        InvLog.Info("开始清除history相关记录")
        try:
            for username in self.username_list:
                if username not in self.user_dir_dict:
                    return
                user_dir = self.user_dir_dict[username]
                for history_file in self.history_file_list:
                    if os.path.isfile(os.path.join(user_dir, history_file)):
                        file_path = os.path.join(user_dir, history_file)
                        if self.mode == "1":
                            match_file_and_remove(file_path, self.keyword)
                        elif self.mode == "2":
                            match_file_and_remove_point(file_path)
                        elif self.mode == "3":
                            remove_file(file_path)
                            create_file(file_path)
                        else:
                            match_file_and_remove_point(file_path)
            InvLog.Info("history记录已清除完成")
        except Exception:
            InvLog.Error(traceback.format_exc())