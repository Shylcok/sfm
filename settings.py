#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: settings.py
@time: 16/10/12 下午2:16
"""
import os
from tornado.options import parse_command_line, options, define

ENV = os.getenv('SFM_ENV')
"""
设置用户级别的环境变量
vi ~/.bashrc
export SFM_ENV="DEV"
souce ~/.bashrc
"""

if ENV == "DEV":
    from settings_dev import *
elif ENV == "PROD":
    from setting_prod import *
else:
    from settings_dev import *

"""
如果一个与define语句中同名的设置在命令行中被给出，那么它将成为全局options的一个属性。
如果用户运行程序时使用了--help选项，程序将打印出所有你定义的选项以及你在define函数的help参数中指定的文本。
如果用户没有为这个选项指定值，则使用default的值进行代替。
Tornado使用type参数进行基本的参数类型验证，当不合适的类型被给出时抛出一个异常。
因此，我们允许一个整数的port参数作为options.port来访问程序。如果用户没有指定值，则默认为8089
"""
define('port', default=CONFIG['HTTP']['PORT'], help='http server port', type=int)
define('log_file_prefix', default=CONFIG['LOG_PATH'], help='log path', type=str)
parse_command_line()
CONFIG['HTTP']['PORT'] = options.port  # 最后会使用CONFIG中的参数
