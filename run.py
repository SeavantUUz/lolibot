from loli import Robot

robot = Robot('WhiteSilkSanae')

@robot.add_callback('text')
def hello(message):
    return robot.response(message,'hello world')

@robot.add_callback('video')
def handle(message):
    dic = robot.parser(message)
    dic['url'] = 'blog.kochiya.me'
    return robot.reponse(dic)

robot.run()
