#!/usr/bin/env python
#-*-coding:utf-8-*-
import urllib,base64
import time
import hashlib,json
import hmac
import requests
from StringIO import StringIO

oauth_token_secret = "xxxxxxxxxx&sssssssssssssss"

def oauth_signature(base_url,oauth_token_secret,param=None,files=None):
    http_method = 'GET' if not files else "POST"
    params = {
            'oauth_consumer_key': 'oauth_consumer_key',
            'oauth_signature_method': 'HMAC-SHA1', #签名方法，暂只支持HMAC-SHA1
            'oauth_timestamp': str(int(time.time())), #时间戳
            'oauth_nonce': hashlib.md5(str(time.time())).hexdigest(),
            'oauth_version': '1.0', #版本号，1.0
            }
    if param:
        # print param
        params = dict(param.items()+params.items())
    queryString=[urllib.quote(k,safe='')+"="+urllib.quote(v,safe='') for k,v in params.items()]
    queryString.sort()
    baseStr="%s&%s&%s" % (http_method,urllib.quote(base_url,safe=""),
                             urllib.quote("&".join(queryString),safe=""))

    myhmac=hmac.new(oauth_token_secret,digestmod=hashlib.sha1)
    myhmac.update(baseStr)
    signatureValue=urllib.quote(base64.encodestring(myhmac.digest()).strip(),
                                safe="")
    params["oauth_signature"]=signatureValue
    url =  "%s?%s" %(base_url,"&".join([k+"="+urllib.quote(v,safe=".-_~%") for k,v in params.items()]))
    # print url
    if files:
        r = requests.post(url,files=files)
        return r.text
    else:
        r = requests.get(url,stream=True)
        return r



def test_base_def(base_url,params=None,method=None):
    #-- 基本常用方法 --#
    param = {"oauth_token":"oauth_token"}
    if params:
        param = dict(param.items()+params.items())
    result = oauth_signature(base_url, oauth_token_secret,param,method)
    return result

def test_account_info():
    #-- 查看用户信息 --#
    print "#-- 查看用户信息 --#"
    base_url = "http://openapi.kuaipan.cn/1/account_info"
    result =  test_base_def(base_url)
    print result
    return result


def test_metadata():
    #-- 文件夹信息 --#
    print "#-- 文件夹信息 --#"
    base_url = "http://openapi.kuaipan.cn/1/metadata/app_folder/"
    r =  test_base_def(base_url)
    r =  r.json()
    result = json.dumps(r,ensure_ascii=False, sort_keys=True, indent=4)
    print result
    return r

def test_upload_locate():
    #-- 获取上传链接 --#
    print "#-- 获取上传链接 --#"
    base_url = "http://api-content.dfs.kuaipan.cn/1/fileops/upload_locate"
    result =  test_base_def(base_url)
    print result
    return result
def test_upload_file(url):
    #-- 上传文件 --#
    print "#-- 上传文件 --#"
    upload_url = url.rstrip('/')+'/1/fileops/upload_file'

    param = {'overwrite':"True",'root':"app_folder",'path':r"test.py"}
    files = {'file': ('test.py', open('test.py', 'rb'))}
    result =  test_base_def(upload_url.encode('utf8'),params=param,method=files)
    print result
    return result

def test_create_folder():
    #-- 创建文件夹 --#
    print "#-- 创建文件夹 --#"
    base_url = "http://openapi.kuaipan.cn/1/fileops/create_folder"
    param = {"root":"app_folder","path":"/test1"}
    r =  test_base_def(base_url,params=param)
    print r
    return r
def test_delete_folder():
    #-- 删除文件夹 --#
    print "#-- 删除文件夹 --#"
    base_url = "http://openapi.kuaipan.cn/1/fileops/delete"
    param = {"root":"app_folder","path":"/test"}
    result =  test_base_def(base_url,params=param)
    print result
    return result

def test_move_folder():
    #-- 移动文件夹 --#
    print "#-- 移动文件夹 --#"
    base_url = "http://openapi.kuaipan.cn/1/fileops/move"
    param = {"root":"app_folder","from_path":"/test1/test","to_path":"/test"}
    result =  test_base_def(base_url,params=param)
    print result
    return result

def test_thumbnail():
    #-- 获取缩略图 --#
    from PIL import Image
    print "#-- 获取缩略图 --#"
    base_url = "http://conv.kuaipan.cn/1/fileops/thumbnail"
    param = {"root":"app_folder","path":"/test/test.jpg","width":"100","height":"100"}
    result =  test_base_def(base_url,params=param)
    i = Image.open(StringIO(result.content))
    i.save("aaa.jpg")
    return 'ok'
def test_documentView():
    #-- 文档转换 --#
    print "#-- 文档转换 --#"
    base_url = "http://conv.kuaipan.cn/1/fileops/documentView"
    param = {"root":"app_folder","path":"/test/PLC.doc","type":"doc","view":"normal","zip":"1"}
    r =  test_base_def(base_url,params=param)

    f = open('new.zip','wb')
    f.write(r.content)
    f.close()
    return 'ok'

def test_download_file():
    #-- 下载文件 --#
    print "#-- 下载文件 --#"
    base_url = "http://api-content.dfs.kuaipan.cn/1/fileops/download_file"
    param = {"root":"app_folder","path":"/test/aaa.doc"}
    r =  test_base_def(base_url,params=param)
    f = open('new.doc','wb')
    f.write(r.content)
    f.close()

def test_shares():
    #-- 获取文件分享链接 --#
    print "#-- 获取文件分享链接 --#"
    base_url = "http://openapi.kuaipan.cn/1/shares/app_folder/test/aaa.doc"
    param = {"access_code":"189"}
    r = test_base_def(base_url,params=param)
    print r.json()

def test_history():
    #-- 文件的历史版本 --#
    print "#-- 文件的历史版本 --#"
    base_url = "http://openapi.kuaipan.cn/1/history/app_folder/test/aaa.doc"
    r = test_base_def(base_url)
    print r.text


if __name__ == '__main__':
    # test_account_info()                     #-- 查看用户信息 --#
    # test_metadata()                       #-- 文件夹信息 --#
    # test_create_folder()                  #-- 创建文件夹 --#
    # test_delete_folder()                  #-- 删除文件夹 --#
    # test_move_folder()                    #-- 移动文件夹 --#
    # url = test_upload_locate().json()['url']     #-- 获取上传链接 --#
    # test_upload_file(url)                 #-- 上传文件 --#
    # test_thumbnail()                        #-- 获取缩略图 --#
    #test_documentView()                        #-- 文档转换 --#
    # test_download_file()                    #-- 下载文件 --#
    #test_shares()
    test_history()
