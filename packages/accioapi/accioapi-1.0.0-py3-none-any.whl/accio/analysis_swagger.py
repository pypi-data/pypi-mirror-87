import requests
import json
from accio import  parse_tools

class swgg_analysiy(object):
    def __init__(self, url_json):
        self.url_json = url_json

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
        host = js["host"]
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
                if parameters:
                        parameters = parameters[0]
                        postData["postData"].update({"text": json.dumps(parameters)})
                        postData["postData"].update({"mimeType": ""})
                request_dict = {}
                request_dict["request"] = {}
                request_dict["request"].update(postData)
                request_dict["request"].update({"headers": []})
                request_dict["request"].update({"bodySize": ""})
                request_dict["request"].update({"url":"http://"+ basePath + url})
                request_dict["request"].update({"cookies": []})
                request_dict["request"].update({"method": method})
                request_dict["request"].update({"httpVersion": ""})
                request_dict["response"] = {}
                template_data.append(request_dict)
                # print(request_dict)
        # print(template_data)
        return template_data
if __name__ == '__main__':
    sw = swgg_analysiy(url_json='http://smstest.imepaas.enncloud.cn/message-api/v2/api-docs')
    result_json = sw.res()
    result=sw.swgg_result(result_json)
    parse_tools.Parse.tmp(result,'1')

