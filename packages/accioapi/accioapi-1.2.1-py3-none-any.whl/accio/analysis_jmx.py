import xml.etree.ElementTree as ET
from accio import  parse_tools
from accio import case_generate
import platform
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目目录


def source(file):
    try:
        creat_file(file)
        result=readXML(file.name)
        parse_tools.Parse.tmp(result, 'j')
        parse_tools.Parse.tmp_create_case()
    except:
        print('获取jmx文件数据失败！')
        sys.exit()

def creat_file(file):
    pattern = '/' if platform.system() != 'Windows' else '\\'
    if not os.path.exists(BASE_DIR + pattern+'Params'):
        os.makedirs(BASE_DIR + pattern+'Params')
    file_name=os.path.join(BASE_DIR, "Params", file.name)
    # print("=======")
    # print(file_name)
    d = open(file_name, 'wb')
    for chunk in file.chunks():
        d.write(chunk)
    d.close()
    # return file_name

def readXML(path):
    pattern = '/' if platform.system() != 'Windows' else '\\'
    rootPath = BASE_DIR + pattern+'Params'+ pattern+path
    tree=rootPath
    treeurl = ET.ElementTree(file=tree)
    template_data=[]
    count=-1
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
                return_result=getparams(tree)
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

def getparams(root):
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

# if __name__ == '__main__':
#     zhulei=jmx_analysiy()
#     result=zhulei.readXML(path="..//Params//message_api1jmx")
#     temp_list = parse_tools.Parse.tmp(result, 'j')
#     parse_tools.Parse.tmp_create_case()



