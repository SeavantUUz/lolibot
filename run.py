import loli

robot = loli.Shoujo('WhiteSilkSanae')

@robot.add_callback('text')
def hello(message):
    return robot.response(message,content='hello world')

@robot.add_callback('image')
def image(message):
    return robot.reponse(message)

robot.run()
