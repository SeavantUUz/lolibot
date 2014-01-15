#coding:utf-8
class Template(object):
    def _common(self,sub_template):
        u'''所有模板共有的公共部分'''
        return '''
<xml>
    <ToUserName><![CDATA[{receiver}]]></ToUserName>
    <FromUserName><![CDATA[{sender}]]></FromUserName>
    <CreateTime>{timestamp}</CreateTime>
    <MsgType><![CDATA[{type}]]></MsgType>
''' \     
  + sub_template + \
'</xml>'

    @property
    def text(self):
        u'''最简单的text模板,只需要有一个content信息的传入就好，不传入的话，就是echo'''
        sub_template = '''
    <Content><![CDATA[{content}]]></Content>
'''
        return self._common(sub_template)

    @property
    def image(self):
        u'''tencent没有提供image的url,只能返回media_id'''
        sub_template = '''
    <Image>
    <MediaId><![CDATA[{media_id}]]></MediaId>
    </Image>
'''
        return self._common(sub_template)

    @property
    def voice(self):
        u'''单纯传入media_id就好'''
        sub_template = '''
    <Voice>
    <MediaId><![CDATA[{media_id}]]></MediaId>
    </Voice>
'''
        return self._common(sub_template)

    @property
    def video(self):
        u'''video模板,需要传入的字典中有media_id,title,description等信息'''
        sub_template = '''
    <Video>
    <MediaId><![CDATA[{media_id}]]></MediaId>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    </Video>  
'''
        return self._common(sub_template)

    @property
    def music(self):
        u'''music模板,需要传入的字典中有title,description,musurl,hq_musqurl,media_id等信息'''
        sub_template = '''
    <Music>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    <MusicUrl><![CDATA[{musurl}]]></MusicUrl>
    <HQMusicUrl><![CDATA[{hq_musurl}]]></HQMusicUrl>
    <ThumbMediaId><![CDATA[{media_id}]]></ThumbMediaId>
    </Music>
'''
        return self._common(sub_template)

## 暂时不支持news的发送
## to be continue
