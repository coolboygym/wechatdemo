# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web


class Handle(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"

            # 首次绑定公众号时需要对签名进行验证
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "xxxxxxxx"  # 请按照公众平台官网\基本配置中信息填写

            my_list = [token, timestamp, nonce]
            my_list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, my_list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature  # 打印后台日志
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is \n", webData  # 打印后台日志
            recMsg = receive.parse_xml(webData)

            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    content = recMsg.Content
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()

            if isinstance(recMsg, receive.EventMsg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.Event == 'CLICK':
                    print 'It is a CLICK event'
                    content = u'功能正在开发中，敬请期待..'.encode('utf-8')
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()

            print "暂且不处理"
            return reply.Msg().send()

        except Exception, Argment:
            return Argment
