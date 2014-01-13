# coding:utf-8
import logging
import xml.etree.ElementTree as ET
class Robot(object):
    mtypes = ['text','image','voice','video','location','link','all']

    def __init__(self):
        self.logging.basicConfig(filename='lolibot.log',level=logging.DEBUG)
        self.callbacks = dict([(i,None) for i in self.mtypes])

    def add_callback(self,mtype='all'):
        try:
            assert mtype in self.mtypes
        except AssertionError:
            raise Exception("Your type won't be accepted")
        def decorator(f):
            self.callbacks[mtype] = f
        return decorator

    def callback(self,mtype):
        return self.callbacks[mtype]

    def parser(self,data):
        root = ET.fromstring(data)
        dic = dict(
                [(child.tag,self.to_unicode(child.text)) for child in root]
                )
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
        if type == 'location':
            dic['x'] = parser_data.get('Location_X')
            dic['y'] = parser_data.get('Location_Y')
            dic['scale'] = parser_data.get('Scale')
            dic['label'] = parser_data.get('Label')
        if type == 'link':
            dic['title'] = parser_data.get('Title')
            dic['description'] = parser_data.get('Description']
            dic['url'] = parser_data.get('Url')
        return dic
        


