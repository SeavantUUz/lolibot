#coding:utf-8
from lolibot.loli import Shoujo
import unittest

signature_url = '/?signature=ea9ff9a1dc0125bd03fa83234db49e6087f05212&echostr=kotiyasanae&timestamp=1389796635&nonce=1389405641'

class Base(unittest.TestCase):
    def setUp(self):
        app = self.create_app()
        self.client = app.test_client()
        self.app = app

    def create_app(self):
        shoujo = Shoujo(token='WhiteSilkSanae')
        ## @shoujo.add_callback('text')
        ## def hello(message):
        ##     return shoujo.response(message,content='hello world')
        @shoujo.add_callback('image')
        def image(message):
            return shoujo.response(message,handler=nomodify)
        def nomodify(dic):
            # In wechat,media_id normailly is not equal
            # with msg_id.the next coding block is only a test.
            return dic

        @shoujo.add_callback('location')
        def location(message):
            label = message['label']
            x = message['x']
            y = message['y']
            scale = message['scale']
            content = u'''
            位置信息:{0}
            纬度:{1}
            经度:{2}
            缩放比例:{3}
            '''.format(label,x,y,scale)
            message['content'] = content
            return shoujo.response(message,type='text')
        
        @shoujo.add_callback('link')
        def link(message):
            title = message['title']
            description = message['description']
            url = message['url']
            content = u'''
            链接标题:{0}
            链接描述:{1}
            链接地址:{2}
            '''.format(title,description,url)
            message['content'] = content
            return shoujo.response(message,type='text')
        
        @shoujo.add_callback()
        def all(message):
            return shoujo.response(message,type='text',content='all handler')

        @shoujo.add_callback('subscribe')
        def subscribe(message):
            return shoujo.response(message,type='text',content=u'订阅成功')

        @shoujo.add_callback('text')
        def news(m):
            m['title0'] = u'哈罗'
            m['description0'] = u'测试一下使用'
            m['picurl0'] = 'http://blog.kochiya.me/avatar.png'
            m['url0'] = 'http://blog.kochiya.me'
            return shoujo.response(m,type='news',count=1)

        app = shoujo.wsgi
        return app

class Test(Base):
    def test_invalid_get(self):
        rv = self.client.get('/')
        assert rv.status_code == 400

    def test_valid_get(self):
        rv = self.client.get(signature_url)
        assert rv.status_code == 200
        assert rv.data == 'kotiyasanae'

    def test_post_text(self):
        text = '''
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[this is a test]]></Content>
        <MsgId>1234567890123456</MsgId>
        </xml>
        '''
        rv = self.client.post('/',data=text)
        assert rv.status_code == 200

    def test_post_image(self):
        text = '''
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[this is a url]]></PicUrl>
        <MsgId>1234567890123456</MsgId>
        </xml> 
        '''
        rv = self.client.post('/',data=text)
        assert rv.status_code == 200

    def test_post_location(self):
        text = '''
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[location]]></MsgType>
        <Location_X>23.134521</Location_X>
        <Location_Y>113.358803</Location_Y>
        <Scale>20</Scale>
        <Label><![CDATA[位置信息]]></Label>
        <MsgId>1234567890123456</MsgId>
        </xml> 
        '''
        rv = self.client.post('/',data=text)
        assert rv.status_code == 200

    def test_post_link(self):
        text = '''
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[link]]></MsgType>
        <Title><![CDATA[公众平台官网链接]]></Title>
        <Description><![CDATA[公众平台官网链接]]></Description>
        <Url><![CDATA[url]]></Url>
        <MsgId>1234567890123456</MsgId>
        </xml>  
        '''
        rv = self.client.post('/',data=text)
        assert rv.status_code == 200

    def test_post_no_handler(self):
        text = '''
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[LOCATION]]></MsgType>
        <Title><![CDATA[公众平台官网链接]]></Title>
        <Description><![CDATA[公众平台官网链接]]></Description>
        <Url><![CDATA[url]]></Url>
        <MsgId>1234567890123456</MsgId>
        </xml> 
        '''
        rv = self.client.post('/',data=text)
        assert rv.status_code == 200

    def test_subscribe(self):
        text='''
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <EventKey><![CDATA[qrscene_123123]]></EventKey>
        </xml>
        '''
        rv = self.client.post('/',data=text)
        assert rv.status_code == 200


if __name__ == '__main__':
    unittest.main()
