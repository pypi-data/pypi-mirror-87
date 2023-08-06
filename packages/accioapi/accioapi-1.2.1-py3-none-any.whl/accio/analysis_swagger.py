import requests
import json
from accio import  parse_tools
import sys
class swgg_analysiy(object):
    def __init__(self, url_json):
        self.url_json = url_json

    def source(self,instance):
        try:
            result_json = instance.res()
            # print(result_json)

            result = instance.swgg_result(result_json)
            print(result)
            parse_tools.Parse.tmp(result, 'a')
            parse_tools.Parse.tmp_create_case()
        except:
            print('获取swagger文件数据失败！')
            sys.exit()

    def source_xiangmu(self,instance):
        try:
            result= instance.res()
            # print(result_json)
            result_json = json.loads(result["result"]["apiDoc"])
            result = instance.swgg_result(result_json)
            # print(result)
            parse_tools.Parse.tmp(result, 'a')
            parse_tools.Parse.tmp_create_case()
        except:
            print('获取swagger文件数据失败！')
            sys.exit()

    def res(self):
        res = requests.get(url=self.url_json)
        js = res.json()
        # print(js)
        return js

    # print(type(js["paths"]))
    def swgg_result(self, js):
        """

        :param js:
        :return:
        """
        self.js = js
        # host = js["host"]
        basePath = js["basePath"]
        template_data = []
        request_list =self.js["paths"].items()
        for key, vale in request_list:
            url = key
            postData = {}
            postData["postData"] = {}

            for k, v in vale.items():
                method = k
                parameters = v.get("parameters", {})
                # print(parameters)
                # print("===========")
                parameter = []
                if parameters:
                    parameter_temp = {}
                    for i,v in enumerate(parameters):

                        # if v.get("required") is True:
                        name=v.get("name")
                        parameter_temp[name]=name
                        parameter.append(parameter_temp)
                    # print(parameter_temp)
                            # print("=======")
                    #
                    # parameters = parameters[0]
                    # print("****")
                    postData["postData"].update({"text": str(parameter_temp)})
                    postData["postData"].update({"mimeType": ""})
                request_dict = {}
                request_dict["request"] = {}
                request_dict["request"].update(postData)
                request_dict["request"].update({"headers": []})
                request_dict["request"].update({"bodySize": ""})
                request_dict["request"].update({"url":"http:/"+ basePath + url})
                request_dict["request"].update({"cookies": []})
                request_dict["request"].update({"method": method})
                request_dict["request"].update({"httpVersion": ""})
                request_dict["response"] = {}
                template_data.append(request_dict)
                # print(request_dict)
        # print(template_data)
        return template_data
# if __name__ == '__main__':
#     # sw = swgg_analysiy(url_json='http://smstest.imepaas.enncloud.cn/message-api/v2/api-docs')
#     # sw.source(sw)
#     sw = swgg_analysiy(url_json='http://10.39.27.21:9529/api/apidoc/getdoc/27')
#     sw.source_xiangmu(sw)
#     # a = requests.get(url)
#     # a1 = json.loads(a.text)
#     # json_result=a1["result"]["apiDoc"]
#     # sw = swgg_analysiy(url_json=json_result)
#     # result=sw.swgg_result(json_result)
#     # print(result)
#     # parse_tools.Parse.tmp(result, 'a')
#     # parse_tools.Parse.tmp_create_case()
#
#
#     # result_json = sw.res()
#     # result=sw.swgg_result(result_json)
#     # parse_tools.Parse.tmp(result,'1')
#     # parse_tools.Parse.tmp_create_case()
#
