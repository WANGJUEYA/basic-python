import json

import tornado.ioloop
import tornado.web


def dash(template, image):
    result = len(template) + len(image)
    return str(result)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """get请求"""
        template = self.get_argument('template', '')
        image = self.get_argument('image', '')
        result = dash(template, image)
        self.write(result)

    def post(self):
        '''post接口， 获取参数'''
        body = self.request.body
        json_obj = json.loads(body)
        result = dash(json_obj['template'], json_obj['image'])
        self.write(result)


application = tornado.web.Application([(r"/dash", MainHandler), ])

if __name__ == "__main__":
    application.listen(8832)
    tornado.ioloop.IOLoop.instance().start()
