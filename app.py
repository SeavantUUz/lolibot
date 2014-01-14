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
        if verity(request.args):
            return request.args.get('echostr')
        else:
            return 'signature error',400
    else:
        msg = parser(request.data)
        return echo(msg)


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



def to_unicode(data):
    if isinstance(data,unicode):
        return data
    elif isinstance(data,int):
        return unicode(data)
    else:return data.decode('utf-8')
