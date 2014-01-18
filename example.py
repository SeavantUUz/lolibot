from lolibot.loli import Shoujo
shoujo = Shoujo('yourToken')

@shoujo.add_callback()
def all(message):
    return shoujo.response(message,type='text',content='all handler')

@shoujo.add_callback('text')
def news(m):
    m['title0'] = u'哈罗'
    m['description0'] = u'测试一下使用'
    m['picurl0'] = 'http://blog.kochiya.me/avatar.png'
    m['url0'] = 'http://blog.kochiya.me'
    return shoujo.response(m,type='news',count=1)

@shoujo.add_callback('image')
def image(message):
    def image(message):
    return shoujo.response(message,handler=nomodify)

def nomodify(dic):
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

@shoujo.add_callback('subscribe')
def subscribe(message):
    return shoujo.response(message,type='text',content=u'订阅成功')
