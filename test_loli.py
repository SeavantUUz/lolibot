from loli import Shoujo
import unittest

signature_url = '/?signature=ea9ff9a1dc0125bd03fa83234db49e6087f05212&echostr=kotiyasanae&timestamp=1389796635&nonce=1389405641'

class Base(unittest.TestCase):
    def setUp(self):
        app = self.create_app()
        self.client = app.test_client()
        self.app = app

    def create_app(self):
        shoujo = Shoujo(token='WhiteSilkSanae')
        @shoujo.add_callback('text')
        def hello(message):
            return shoujo.response(message,content='hello world')

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

if __name__ == '__main__':
    unittest.main()
