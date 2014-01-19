lolibot
=======

lolibot是一个微信消息处理框架,目前依赖于flask

安装
------
目前lolibot只托管在github上,通过`git clone`方式安装
`git clone https://github.com/SeavantUUz/lolibot.git`

环境
------
目前lolibot依赖于flask进行路由分发和wsgi支持
```
virtualenv env
source env/bin/activate
pip install flask
```

Hello World
-------
最简单的消息处理，对所有收到的消息(任意类型)，回复Hello World
```python
from lolibot.loli import Shoujo
shoujo = Shoujo('yourToken')
@shoujo.add_callback()
def all(message):
    return shoujo.response(message,content='Hello World')
shoujo.run()
```

文档
------
http://blog.kochiya.me/www/posts/Lolibot.html
