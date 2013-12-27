# coding:utf-8
from flask import Flask,request
import hashlib
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def get():
    if request.method == 'GET':
        return verity(request.args)
    else:
        msg = parser(request.data)
        return echo(msg)

def verity(kwargs):
        token     = 'AprocySanae'
        signature = kwargs.get('signature')
        timestamp = kwargs.get('timestamp')
        nonce     = kwargs.get('nonce')
        echostr   = kwargs.get('echostr')
        liststr   = [token,timestamp,nonce]
        liststr.sort()
        sha1      = hashlib.sha1()
        hashcode  = sha1.update(''.join(liststr))
        if signature == hashcode.hexdigest():
            return echostr
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
        
if __name__ == "__main__":
    app.run()
