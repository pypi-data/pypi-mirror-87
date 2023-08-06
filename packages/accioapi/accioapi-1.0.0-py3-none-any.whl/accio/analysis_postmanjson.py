# -*- encoding: utf-8 -*-
"""
@File    : postmanjson_analysis.py
@Time    : 2020/10/19 9:40
@Author  : Yu Tao
@Software: PyCharm
"""

import codecs
import sys
from accio import parse_tools


class PMJson(object):

    def __init__(self):
        self.path_list = parse_tools.Parse.find_file('temp', 'json')

    def source(self):
        """
        生成用例数据集合
        :return: 数据集合
        """
        data_list = []
        try:
            for path in self.path_list:
                postmanjson_file = codecs.open(path, mode='r', encoding='utf-8-sig')
                file_context = eval(postmanjson_file.read())
                data = self.format_data(file_context)
                # data_list = data_list + data
                filename = path.split("\\")[-1].split('.')[0]
                parse_tools.Parse.tmp(data, filename)
                postmanjson_file.close()
        except:
            print('获取json文件数据失败！')
            sys.exit()
        return

    def format_data(self, file_context):
        """
        格式化数据，使其满足“用例生成”的调用要求
        :param file_context: 读出的json文件数据
        :return:
        """
        template_data = []
        request_list = file_context.get("item")

        for request_data in request_list:
            request_dict = {}
            request_dict["request"] = {}
            if request_data.get("request").get("body"):
                pardict = eval(request_data["request"]["body"]["raw"])
                postData = {}
                params = []
                for akey in pardict:
                    # params.append({akey:pardict[akey]})
                    params.append({"name":akey})
                postData["params"] = params
            else:
                postData = {}
            request_dict["request"].update({"postData": postData})
            # 处理header
            header_list = []
            for header_data in request_data["request"]["header"]:
                header_dict = {}
                header_dict.update({"name": header_data.get("key")})
                header_dict.update({"value": header_data.get("value")})
                header_list.append(header_dict)
            request_dict["request"].update({"headers": header_list})
            request_dict["request"].update({"bodySize": ""})
            request_dict["request"].update({"url": request_data["request"]["url"]["raw"]})
            request_dict["request"].update({"cookies": []})
            request_dict["request"].update({"method": request_data["request"]["method"]})
            request_dict["request"].update({"httpVersion": ""})
            template_data.append(request_dict)
        # print("===111", template_data)

        return template_data


if __name__ == '__main__':
    Parse = PMJson()
    Parse.source()
    parse_tools.Parse.tmp_create_case()