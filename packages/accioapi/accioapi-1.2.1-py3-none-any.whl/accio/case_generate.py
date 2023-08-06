# -*- encoding: utf-8 -*-
"""
@File    : case_generate.py
@Time    : 2020/10/16 10:39
@Author  : liyinlong
@Software: PyCharm
"""

import time
import os
from urllib.parse import urlparse
from accio import parse_tools


class Generate(object):

    def __init__(self, data, case_name=None):
        self.data = data
        self.case_name = case_name
        self.root_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
        if not os.path.exists(self.root_path + '\\temp\\Testcase'):
            os.makedirs(self.root_path + '\\temp\\Testcase')

    '''
    依据har文件method信息生成对应case
    如果传入文件名以传入文件名+数据在entries中的位置命名
    不传入文件名默认以path路径命名，截取path后两段命名
    如果没有path路径，以域名命名
    '''

    def case(self):
        case_name_list = []
        for t, each in enumerate(self.data):
            request = each.get('request')
            method_list = ['get', 'post', 'put']
            method = request.get('method').lower()
            url = request.get('url')
            parse_url = urlparse(url)
            url_netloc = parse_url.netloc
            url_path = parse_url.path
            key_list = parse_tools.Parse.post_data_key(request, t)
            if self.case_name is None:

                if url_path == '' or url_path == '/':
                    case_name = 'root_uri'
                    # case_name = url_netloc.replace('.', '_').replace(':', '_')
                    if case_name in case_name_list:
                        case_name = case_name + str(t)

                    case_name_list.append(case_name)
                else:
                    case_name = url_path.replace('/', '_').replace('.', '_')[1:]
                    case_name = parse_tools.Parse.path(case_name)
                    if case_name in case_name_list:
                        case_name = case_name + str(t)
                    case_name_list.append(case_name)
                file_name = 'test_' + str(case_name) + '.py'
            else:
                case_name_list.append(self.case_name)
                file_name = 'test_' + str(self.case_name) + str(t) + '.py'

            if method in method_list:
                file = os.path.join(self.root_path, "TestCase", file_name)
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                if len(key_list) >0:
                    keys = str(', '.join(key_list))+','
                else:
                    keys = str(', '.join(key_list))

                key_dict = str(dict(zip(key_list, key_list))).replace(": '", ": ").replace("',", ",").replace("'}", "}").replace("'", '"')

                case_template = '''# -*- coding: utf-8 -*-

"""
@File    : %(file_name)s
@Time    : %(localtime)s
@Author  : Automatic generation
"""
#--别名占位

from Common import Http


class Signing:

    def __init__(self):

        self.request = Http.Request()

    def person_signing(self, host, %(keys)s headers):
        """
           用例描述：数据源文件中第 %(t)s 个request
        """
        params = %(key_dict)s
        response = self.request.%(method)s(host+"%(url_path)s", params, headers)
        return response


'''
                case = case_template % locals()

                with open(file, 'w', encoding="utf-8") as outfile:
                    outfile.write(case)
        case_name_list = []

#
# if __name__ == '__main__':
#     from Common import analysis_har
#     data = analysis_har.Har().source()
#     Parse = Generate(data)
#     Parse.case()

