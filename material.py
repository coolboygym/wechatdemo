# -*- coding: utf-8 -*-
# filename: material.py
import urllib2
import json
import poster.encode
from poster.streaminghttp import register_openers
from basic import Basic


class Material(object):

    def __init__(self):
        register_openers()

    #上传图文
    def add_news(self, accessToken, news):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=%s" % accessToken
        urlResp = urllib2.urlopen(postUrl, news)
        print urlResp.read()

    # 上传
    def uplaod(self, accessToken, filePath, mediaType):
        openFile = open(filePath, "rb")
        fileName = "hello"
        param = {'media': openFile, 'filename': fileName}
        # param = {'media': openFile}
        postData, postHeaders = poster.encode.multipart_encode(param)

        postUrl = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" % (
        accessToken, mediaType)
        request = urllib2.Request(postUrl, postData, postHeaders)
        urlResp = urllib2.urlopen(request)
        print urlResp.read()

    # 下载
    def get(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib2.urlopen(postUrl, postData)
        headers = urlResp.info().__dict__['headers']
        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            jsonDict = json.loads(urlResp.read())
            print jsonDict
        else:
            buffer = urlResp.read()  # 素材的二进制
            mediaFile = file("test_media.jpg", "wb")
            mediaFile.write(buffer)
            print "get successful"

    # 删除
    def delete(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/del_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib2.urlopen(postUrl, postData)
        print urlResp.read()

    # 获取素材列表
    def batch_get(self, accessToken, mediaType, offset=0, count=20):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/material"
                   "/batchget_material?access_token=%s" % accessToken)
        postData = ("{ \"type\": \"%s\", \"offset\": %d, \"count\": %d }"
                    % (mediaType, offset, count))
        urlResp = urllib2.urlopen(postUrl, postData)
        print urlResp.read()


if __name__ == '__main__':
    myMaterial = Material()
    accessToken = Basic().get_access_token()
    news = (
    {
        "articles":
        [
            {
            "title": "test",
            "thumb_media_id": "X2UMe5WdDJSS2AS6BQkhTw9raS0pBdpv8wMZ9NnEzns",
            "author": "vickey",
            "digest": "",
            "show_cover_pic": 1,
            "content": "<p><img data-s=\"300,640\" data-type=\"jpeg\" data-src=\"http://mmbiz.qpic.cn/mmbiz/iaK7BytM0QFPLhxfSMhOHlZd2Q5cw3YibKVf4dgNpLHXdUkvl65NBSMU71rFfOEKF3ucmXuwAQbNdiaaS3441d5rg/0?wx_fmt=jpeg\" data-ratio=\"0.748653500897666\" data-w=\"\"  /><br  /><img data-s=\"300,640\" data-type=\"jpeg\" data-src=\"http://mmbiz.qpic.cn/mmbiz/iaK7BytM0QFPLhxfSMhOHlZd2Q5cw3YibKiaibdNgh0ibgOXAuz9phrGjYFBUKlyTBcrv5WE5zic08FUcz5ODXCHEykQ/0?wx_fmt=jpeg\" data-ratio=\"0.748653500897666\" data-w=\"\"  /><br  /></p>",
            "content_source_url": "",
            }
        ]
    })

    #news 是个dict类型，可通过下面方式修改内容
    news = json.dumps(news, ensure_ascii=False)
    myMaterial.add_news(accessToken, news)