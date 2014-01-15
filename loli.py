# coding:utf-8
from flask import Flask
import logging
import xml.etree.ElementTree as ET
import hashlib

class Loli(object):
    mtypes = ['text','image','voice','video','location','link','all']

    def __init__(self,token='yourToken'):
        self.logging.basicConfig(filename='lolibot.log',level=logging.DEBUG)
        self._callbacks = dict([(i,None) for i in self.mtypes])
        self.token = token

    def add_callback(self,mtype='all'):
        assert mtype in self.mtypes
        def decorator(f):
            self._callbacks[mtype] = f
        return decorator

    def callback(self,mtype):
        return self._callbacks.get(mtype)

    def response(self,msg,**kwargs):
        type = msg['type']
        msg['receiver'],msg['sender'] = msg['sender'],msg['receiver']
        template = template
        


    def parser(self,data):
        root = ET.fromstring(data)
        parser_data = dict(
                [(child.tag,self.child.text) for child in root]
                )
        dic = {}
        dic['msgid'] = parser_data.get('MsgId')
        dic['receiver'] = parser_data.get('ToUserName')
        dic['sender'] = parser_data.get('FromUserName')
        dic['type'] = type = parser_data.get('MsgType')
        dic['timestamp'] = parser_data.get('CreateTime')
        if type == 'text':
            dic['content'] = parser_data.get('Content')
        if type == 'image':
            dic['picurl'] = parser_data.get('PicUrl')
            dic['media_id'] = parser_data.get('MediaId')
        if type == 'voice':
            dic['media_id'] = parser_data.get('MediaId')
            dic['format'] = parser_data.get('Format')
        if type == 'video':
            dic['media_id'] = parser_data.get('MediaId')
            dic['th_media_id'] = parser_data.get('ThumbMediaId')
            dic['title'] = 'default title'
            dic['description'] = 'no description'
        if type == 'location':
            dic['x'] = parser_data.get('Location_X')
            dic['y'] = parser_data.get('Location_Y')
            dic['scale'] = parser_data.get('Scale')
            dic['label'] = parser_data.get('Label')
        if type == 'link':
            dic['title'] = parser_data.get('Title')
            dic['description'] = parser_data.get('Description')
            dic['url'] = parser_data.get('Url')
        return dic

    def verify(self,kwargs):
        token = self.token
        signature = kwargs.get('signature')
        timestamp = kwargs.get('timestamp')
        nonce = kwargs.get('nonce')
        echostr = kwargs.get('echostr')
        liststr = sorted([token,timestamp,nonce])
        sha1 = hashlib.sha1()
        sha1.update((''.join(liststr)).encode('utf-8'))
        hashcode = sha1.hexdigest()
        return signature == hashcode

class Shoujo(Loli):
    @property
    def wsgi(self):
        app = Flask(__name__)

        @app.route('/',methods=['GET','POST'])
        def handle():
            if request.method == "GET":
                if self.verify(request.args):
                    return request.args.get('echstr')
                else:
                    return 'signature error',400
            else:
                msg = self.parser(request.data)
                assert msg['type']
                func = self.callback(msg['type'])
                if func:
                    return func(msg)
                else:
                    raise Exception("Undefined type")
        return app

    def run(self,host='127.0.0.1',port=5000):
        self.wsgi.run(host,port)

