# coding:utf-8
from flask import Flask,request
import logging
import hashlib
import xml.etree.ElementTree as ET

logging.basicConfig(filename='lolibot.log',level=logging.DEBUG)

app = Flask(__name__)

logging.debug('----------DEBUG BEGINING!----------')
@app.route('/',methods=['GET','POST'])
def get():
    if request.method == 'GET':
        if request.args:
            return verity(request.args)
        else:
            return 'hello sanae'
    else:
        msg = parser(request.data)
        return echo(msg)

def verity(kwargs):
        token     = 'WhiteSilkSanae'
        signature = kwargs.get('signature')
        timestamp = kwargs.get('timestamp')
        nonce     = kwargs.get('nonce')
        echostr   = kwargs.get('echostr')
        liststr   = [token,timestamp,nonce]
        liststr.sort()
        sha1      = hashlib.sha1()
        hashcode  = sha1.update(''.join(liststr))
        logging.info("
            token:{0}\n
            signature:{1}\n
            timestamp:{2}\n
            nonce:{3}\n
            echostr:{4}\n
            hashcode:{5}
           ".format(token,signature,timestamp,nonce,echostr,hashcode)) 
        logging.debug('----------DEBUG ENDING----------')
        if signature == hashcode.hexdigest():
            return True
        else:
            return False

def echo(dictionary):
    TEMPLATE = to_unicode('''
    <xml>
        <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
        <FromUserName><![CDATA[{ToUserName}]]></FromUserName> 
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[{MsgType}]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        <FuncFlag>1</FuncFlag>
    </xml>
    ''')
    return TEMPLATE.format(**dictionary)

def parser(data):
    root = ET.formstring(data)
    msg = dict(
        [(child.tag,to_unicode(child.text)) for child in root]
        )
    return msg


def to_unicode(data):
    if isinstance(data,unicode):
        return data
    elif isinstance(data,int):
        return unicode(data)
    else:return data.decode('utf-8')
