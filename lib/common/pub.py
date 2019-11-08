# coding:utf-8
from subprocess import Popen, PIPE
from lib.common.log import *
from lib.common.global_var import *
import os
import time
import traceback
import random
import string


def get_file_time(filename=''):
    try:
        stat = os.stat(filename)
        return stat.st_mtime, stat.st_atime
    except Exception:
        InvLog.Error(traceback.format_exc())


def set_file_time(filename='', st_mtime=0, st_atime=0):
    try:
        # 转换时间格式
        atime_local = time.localtime(st_atime)
        atime_dt = time.strftime("%Y%m%d%H%M", atime_local)
        mtime_local = time.localtime(st_mtime)
        mtime_dt = time.strftime("%Y%m%d%H%M", mtime_local)

        p1 = Popen("touch -at "+atime_dt+" "+filename, stdout=PIPE, shell=True)
        p1_res = p1.stdout.read().splitlines()
        if p1_res:
            InvLog.Error("修改文件 "+filename+" 时间失败， 失败原因: " + p1_res)
        p2 = Popen("touch -mt "+mtime_dt+" "+filename, stdout=PIPE, shell=True)
        p2_res = p2.stdout.read().splitlines()
        if p2_res:
            InvLog.Error("修改文件 "+filename+" 时间失败， 失败原因: " + p2_res)
    except Exception as e:
        InvLog.Error(traceback.format_exc())


def get_user_dir():
    try:
        dir_dict = {}
        dir_list = []
        user_dir_file = "/etc/passwd"
        with open(user_dir_file, "r") as user_dir_file_f:
            for line in user_dir_file_f.readlines():
                line = line.replace("\n", "")
                line_split = line.split(":")
                if len(line_split) != 7:
                    continue
                if line_split[6] != "/sbin/nologin" and "false" not in line_split[6] and not line_split[5] in dir_dict:
                    dir_list.append(line_split[5])
                    dir_dict[line_split[5]] = 1
        return dir_list
    except Exception:
        InvLog.Error(traceback.format_exc())


def get_user_dir_dict():
    try:
        dir_dict = {}
        dir_dict_res = {}
        user_dir_file = "/etc/passwd"
        with open(user_dir_file, "r") as user_dir_file_f:
            for line in user_dir_file_f.readlines():
                line = line.replace("\n", "")
                line_split = line.split(":")
                if len(line_split) != 7:
                    continue
                if line_split[6] != "/sbin/nologin" and "false" not in line_split[6] and not line_split[5] in dir_dict:
                    dir_dict_res[line_split[0]] = line_split[5]
                    dir_dict[line_split[5]] = 1
        return dir_dict_res
    except Exception:
        InvLog.Error(traceback.format_exc())


def convert_list_to_dict(lst):
    dct = {lst[i]: 1 for i in lst}
    return dct


def create_file(filename):
    if os.path.exists(filename):
        return
    else:
        f = open(filename, "w")
        f.close()


def remove_file(filename):
    try:
        os.remove(filename)
    except Exception:
        InvLog.Error(traceback.format_exc())


def create_random_str():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return salt


def match_file_and_remove(filename, keyword_list=[]):
    tmp_file = create_random_str()
    create_file(tmp_file)
    tmp_file_f = open(tmp_file, "w")
    with open(filename, "r") as filename_open:
        # 保存文件时间
        mtime, atime = get_file_time(filename)

        filename_open = open(filename, "r")
        for log_line in filename_open.readlines():
            keyword_flag = False
            for sshd in keyword_list:
                if sshd in log_line:
                    keyword_flag = True
            if not keyword_flag:
                tmp_file_f.writelines(log_line)
    tmp_file_f.close()
    os.replace(tmp_file, filename)
    # 还原文件修改时间
    set_file_time(filename, mtime, atime)


def match_file_and_remove_point(filename):
    tmp_file = create_random_str()
    create_file(tmp_file)
    tmp_file_f = open(tmp_file, "w")
    with open(filename, "r") as filename_open:
        # 保存文件时间
        mtime, atime = get_file_time(filename)

        filename_open = open(filename, "r")
        # 判断是否每条询问
        c_flag = False
        for log_line in filename_open.readlines():
            answer = input("请确认命令记录: " + log_line.replace("\n", "") + " 是否要删除(输入c默认不再删除)[y/N/c]:")
            if answer == "c":
                c_flag = True
            if answer != "y" or c_flag:
                tmp_file_f.writelines(log_line)
    tmp_file_f.close()
    os.replace(tmp_file, filename)
    # 还原文件修改时间
    set_file_time(filename, mtime, atime)


if __name__ == "__main__":
    # a, m = get_file_time("log.pyc")
    # set_file_time("log.pyc", m, a)
    # get_user_dir()
    match_file_and_remove("a", "222")