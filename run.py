from loli import Shoujo

robot = Shoujo('WhiteSilkSanae')

@robot.add_callback('text')
def hello(message):
    return robot.response(message,content='hello world')

## @robot.add_callback('video')
## def handle(message):
##     message['url'] = 'blog.kochiya.me'
##     return robot.reponse(message,content='hello world',handler=foo)
## 
robot.run()
