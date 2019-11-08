# coding:utf-8

import optparse
from lib.common.global_var import *
from lib.plugins.clean import *

if __name__ == "__main__":
    progam = u'''
 _____            _    _            _
|_   _|          | |  | |          | |
  | |  _ ____   _| |__| | __ _  ___| | __
  | | | '_ \ \ / /  __  |/ _` |/ __| |/ /
 _| |_| | | \ V /| |  | | (_| | (__|   <
|_____|_| |_|\_/ |_|  |_|\__,_|\___|_|\_\__
    '''
    print(progam)

    # 初始化选项
    parser = optparse.OptionParser()
    parser.add_option("--version", dest="version", default=False, action="store_true")

    mode = optparse.OptionGroup(parser, "Mode", "清除模式选项")
    mode.add_option("--force", dest="force", default=False, action="store_true", help=u"强力清除模式，该模式易被察觉")
    mode.add_option("--accurate", dest="accurate", default=False, action="store_true", help=u"精确清除模式，该模式可能存在遗漏")
    parser.add_option_group(mode)

    options, _ = parser.parse_args()

    # 初始化全局变量配置
    global_init()

    # 设置选项
    options.version = "1.0"
    if options.accurate:
        # input("是否为横向渗透[y/N]:")

        # 设置ip
        ip_list = input("请输入攻击IP(多个ip请用/分割):")
        ip_list = ip_list.split("/")
        set_value("ip", ip_list)

        # 设置登录用户名
        username_list = input("请输入ssh登录用户名(多个用户名请用/分割):")
        username_list = username_list.split("/")
        set_value("username", username_list)

        # 是否全局搜索日志文件
        global_search_suffix = input("是否全局搜索文件，如果是，请输入需要搜索文件的后缀[多个后缀用/分割]:")
        global_search_suffix_list = global_search_suffix.split("/")
        set_value("global_search_suffix", global_search_suffix_list)

        # history清除模式
        history_clean_mode = input("请选择history清除模式(1.根据关键字清除 2.逐条确认是否清除 3.全部清除)[1/2/3]:")
        set_value("history_clean_mode", history_clean_mode)
        if history_clean_mode == "1":
            history_clean_keyword = input("请输入history中需要清除的关键字(多个关键字请用/分割):")
            history_clean_keyword = history_clean_keyword.split("/")
            set_value("history_clean_keyword", history_clean_keyword)

        # 获取所有用户目录
        dir_list = get_user_dir()
        set_value("user_dir", dir_list)
        # 获取用户名为键，目录为值的字典
        dir_list_dict = get_user_dir_dict()
        set_value("user_dir_dict", dir_list_dict)

        # 开始清除
        Clean().run()
    elif options.force:
        pass
    else:
        print(u"必须选择清除模式，具体可使用python Inv.py --help参考")