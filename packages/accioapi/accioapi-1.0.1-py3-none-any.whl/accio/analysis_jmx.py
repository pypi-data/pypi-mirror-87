import xml.etree.ElementTree as ET
from accio import  parse_tools
class jmx_analysiy(object):
    # file = './message_api1jmx'
    def __init__(self,path):
         self.path=path

    def readXML(self,path):
        tree=self.path
        treeurl = ET.ElementTree(file=tree)
        template_data=[]
        count=-1
        basepath=""
        url=""
        method=""
        swich = 0
        params = []
        for elem in treeurl.iter(tag='stringProp'):
                if elem.attrib['name'] == 'HTTPSampler.domain' and elem.text is not None:
                    basepath= elem.text
                else:
                    if elem.attrib['name'] == 'HTTPSampler.path' and elem.text is not None:
                        url=elem.text
                        # print("=========")
                    if elem.attrib['name'] == 'HTTPSampler.method' and elem.text is not None:
                        method=elem.text
                        swich = 1
                if swich == 1:
                    return_result=self.getparams(tree)
                    request_dict = {}
                    count +=1
                    # print(count)
                    request_dict["request"] = {}
                    request_dict["request"].update({"postData": return_result[count]['postData']})
                    request_dict["request"].update({"headers": []})
                    request_dict["request"].update({"bodySize": ""})
                    request_dict["request"].update({"url": "http:/"+ url})
                    request_dict["request"].update({"cookies": []})
                    request_dict["request"].update({"method": method})
                    request_dict["request"].update({"httpVersion": ""})
                    request_dict["response"] = {}
                    template_data.append(request_dict)
                    # print(request_dict)
                swich = 0
        # print(template_data)
        return  template_data

    def getparams(self,root):
        tree = ET.parse(root)
        root = tree.getroot()
        count=[]
        for child in root:
            # 第二层节点的标签名称和属性
            # print(child.tag,":", child.attrib)
            # 遍历xml文档的第三层
            for children in child:
                # 第三层节点的标签名称和属性
                # print(children.tag, ":", children.attrib)
                for children4 in children:
                    for children5 in children4:
                        for country1 in children5.findall("stringProp"):
                            path = country1.get("name")
                            if path == 'HTTPSampler.path' and path is not None:
                                url = country1.get("name")
                        for country2 in children5.findall("elementProp"):
                            swich = 0
                            for country2 in country2.findall("collectionProp"):
                                params = []
                                for country4 in country2.findall("elementProp"):
                                    name = country4.get("name")
                                    params.append({"name": name})
                                    swich = 1
                                if swich == 1:
                                    postData_inner = {}
                                    postData_inner["postData"] = {}
                                    postData_inner["postData"].update({"params": params})
                                    postData_inner["postData"].update({"mimeType": "application/x-www-form-urlencoded"})
                                    # print(postData_inner)
                                    # print("+++++++++")
                                    count.append(postData_inner)
        # print(count)
        return count

if __name__ == '__main__':
    zhulei=jmx_analysiy(path="./message_api1.jmx")
    result=zhulei.readXML(path=zhulei.path)
    parse_tools.Parse.tmp(result, 'j')
    parse_tools.Parse.tmp_create_case()


