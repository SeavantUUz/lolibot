from loli import Robot

robot = Robot('WhiteSilkSanae')

@robot.add_callback('text')
def hello(message):
    return robot.response(message)

@robot.add_callback('video')
def handle(message):
    message['url'] = 'blog.kochiya.me'
    return robot.reponse(message,content='hello world',handler=foo)

robot.run()
