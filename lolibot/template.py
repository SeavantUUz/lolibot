#coding:utf-8
import re
class Template(object):
    def _common(self,sub_template):
        u'''所有模板共有的公共部分'''
        return '''
<xml>
    <ToUserName><![CDATA[{receiver}]]></ToUserName>
    <FromUserName><![CDATA[{sender}]]></FromUserName>
    <CreateTime>{timestamp}</CreateTime>
    <MsgType><![CDATA[{type}]]></MsgType>
''' + sub_template + \
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
    def news(self,count):
        u'''news模板，实现很麻烦，需要传入的值很多而且需要标注，通常情况不推荐'''
        sub_template = self.generateNews(count)
        return self._common(sub_template)

    def generateNews(self,count):
        temps = []
        template = '''
    <item>
    <Title><![CDATA[{title}]]></Title> 
    <Description><![CDATA[{description}]]></Description>
    <PicUrl><![CDATA[{picurl}]]></PicUrl>
    <Url><![CDATA[{url}]]></Url>
    </item> 
'''
        for i in range(count):
            localTemp = template
            temps.append(self.multiple_replace(localTemp,i))
            print i
        sub_template = ''.join(temps)
        sub_template= '<ArticleCount>{0}</ArticleCount>\n<Articles>{1}\n</Articles>\n'.format(count,sub_template)
        return sub_template

    def multiple_replace(self,text,count):
        u'''替换字典标志……把title自动替换成title1,title2这样'''
        pat = re.compile(r'\{(.+?)\}')
        def one_replace(match):
            return '{'+match.group(1)+str(count)+'}'
        return pat.sub(one_replace,text)
