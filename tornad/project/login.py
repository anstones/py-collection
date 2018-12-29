import time

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado import gen
from setting import settings
from tornado.options import define, options
from data.user_modules import User, session

define('port', default=8000, help='run port', type=int)


class AuthError(Exception):  # 自定义异常
    def __init__(self, msg):
        super(AuthError, self).__init__(msg)


class IndexHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        username = 'no'
        self.render('sqlalchemy.html', username=username)


class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html', error=None)

    def post(self):
        if self._check_argeument():
            try:
                self._create_user()
                self.render('login.html', error='注册成功，请登录')
            except AuthError as e:
                self.render('register.html', error=e)
            except Exception as e:
                self.render('register.html', error=e)
        else:
            self.render('register.html', error='您输入的用户名或密码格式有误')

    def _check_argeument(self):
        username = self.get_argument('name', '')
        passwd = self.get_argument('password1', '')
        if len(username) < 4 or len(passwd) < 6:
            return False
        if len(username) <= 10 and len(passwd) <= 10:
            return True
        else:
            return False

    def _create_user(self):
        if self.get_argument('password1', '') != self.get_argument('password2', ''):
            raise AuthError('两次输入的密码不同')
        if User.by_name(self.get_argument('name', '')):
            raise AuthError('用户名已经被注册 ，请更换后重试。')

        user = User()
        user.username = self.get_argument('name', '')
        user.password = self.get_argument('password1', '')
        session.add(user)
        session.commit()


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        username = 'no'
        self.render('login.html', error=None)

    def post(self):
        username = User.by_name(self.get_argument('name', ''))
        passwd = self.get_argument('password', '')
        if username and username[0].password == passwd:
            print('ok')
            self.render('sqlalchemy.html',
                        username=username[0].username)
        else:
            self.render('login.html', error='登录失败,请检查用户名或密码后重试。')


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/login', LoginHandler),
            (r'/register', RegisterHandler),
            (r'/static/*.png',tornado.web.StaticFileHandler,{"path":settings['static_path']})
        ],
        debug=True,  # 非常重要 存盘就自动应用在 server
        template_path='templates',  # html文件的文件夹
        static_path='static',
        autoescape=None,  # 关闭自动转义
    )
    # 以下是固定的 记住就行
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
