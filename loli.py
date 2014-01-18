# coding:utf-8
from flask import Flask,request
import logging
import xml.etree.ElementTree as ET
import hashlib
from template import Template
from utils import to_unicode

__all__ = ['Loli','Shoujo']

class Loli(object):
    mtypes = ['text','image','voice','video','location','link','scan','subscribe','unsubscribe','CLICK','LOCATION','all']
    logging.basicConfig(filename='lolibot.log',level=logging.DEBUG)

    def __init__(self,token='yourToken',logging=True):
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
        ## msg is parsed and your handled data.Actually,it is a dict.
        ## Your could specify a type by assign.ex response(type='music').I list all legal types.
        '''
        ex: response(message,type='yourType')
        optional kwargs:
        type='legal_types',content='yourContent',handler=foo,count=1 
        ps:when type is news,the count kwarg is nessceary
        support types:
        text,image,voice,video,music,news
        '''
        msg['receiver'],msg['sender'] = msg['sender'],msg['receiver']
        legal_types = ['text','music','image','voice','video','news']

        ## get some kwargs ##
        # key word content ---- which force type to textand return a static string
        if kwargs.get('type'):
            type = kwargs.get('type')
        else:type = msg['type']
        # charge receiver and sender
        if not type in legal_types:
            raise Exception("Illgal type!You could only choose one type from legal_types!") 
        if kwargs.get('content'):
            msg['type'] = type = 'text'
            msg['content'] = to_unicode(kwargs.get('content'))
        # key word handler ---- which is a function object,accept a dict and return a modified dict
        if kwargs.get('handler'):
            msg = kwargs.get('handler')(msg)
        ## more kwargs ##

        if not type == 'news':
            template = to_unicode(getattr(Template(),type))
        else:
            count = kwargs.get('count')
            if count:
                temp = Template() 
                # some codes 
            else:
                raise Exception('When type is set to news,the count kwarg is necessary!')

        logging.info(template.format(**msg))
        try:
            retdata = template.format(**msg)
        except:
            raise Exception("You did't pass enough args or pass wrong args,please check args which template needed.Read template.py maybe inspire your mind")
        return retdata
        
    def parser(self,data):
        root = ET.fromstring(data)
        parser_data = dict(
                [(child.tag,to_unicode(child.text)) for child in root]
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
            # the MsgId in there is not MediaId which
            # should be sent
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
        if type == 'event':
            dic['event_key'] = parser_data.get('EventKey')
            dic['type'] = parser_data.get('Event')
            dic['ticket'] = parser_data.get('Ticket')
            ## LOCATION type has some extra values
            dic['latitude'] = parser_data.get('Latitude')
            dic['longitude'] = parser_data.get('Longitude')
            dic['precision'] = parser_data.get('Precision')
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

    def handlerAll(self,message):
        return self.response(message,type='text',content=u"Sorry,I don't have a specially callback function could handle your meesage's type now. ")

    def handlerUnknown(self,message):
        return self.response(message,type='text',content=u"Sorry,I could not recognize this message's type.Maybe the API of wechat has updated.Post a issue on github is a recommended way.")

class Shoujo(Loli):
    @property
    def wsgi(self):
        app = Flask(__name__)

        @app.route('/',methods=['GET','POST'])
        def handle():
            '''your should never care the sender and receiver and never care get or post --- unless you know what do you do'''
            if request.method == "GET":
                if request.args != {} and self.verify(request.args):
                    return request.args.get('echostr')
                else:
                    return 'signature error',400
            else:
                msg = self.parser(request.data)
                assert msg['type']
                func = self.callback(msg['type'])
                if func:
                    return func(msg)
                else:
                    if msg['type'] in self.mtypes:
                        foo = self.callback('all')
                        if foo:
                            return foo(msg)
                        else:return self.handlerAll(msg)
                    else:
                        else:return self.handlerUnknown(msg)
        return app

    def run(self,host='127.0.0.1',port=5000):
        self.wsgi.run(host,port)

