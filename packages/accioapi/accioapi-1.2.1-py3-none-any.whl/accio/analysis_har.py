# -*- encoding: utf-8 -*-
"""
@File    : analysis_har.py
@Time    : 2020/10/13 14:21
@Author  : liyinlong
@Software: PyCharm
"""
import codecs
import json
import sys


class Har(object):

    def __init__(self):
        self.path_list = parse_tools.Parse.find_file('temp', 'har')

    def source(self):
        # data_list = []
        try:
            for path in self.path_list:
                har = codecs.open(path, mode='r', encoding='utf-8-sig')
                data = json.load(har)['log']['entries']
                filename = path.split("\\")[-1].split('.')[0]
                parse_tools.Parse.tmp(data, filename)
                # data_list = data_list + data
                har.close()
        except:
            print('获取har文件数据失败！')
            sys.exit()


# if __name__ == '__main__':
#     from Common import parse_tools
#     Parse = Har()
#     Parse.source()
#     # tmp文件生成case
#     parse_tools.Parse.tmp_create_case()
#
