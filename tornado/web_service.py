import tornado.web
import logging
import string
import os
import sys
# from predict import predict
import predicter

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)
# 给logger添加handler
logger.addHandler(ch)


def work(text):
    if text is None:
        return 0.
    else:
        return predicter.predict(text)


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        p = work(text)
        self.write(p)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        text = self.get_argument('text')
        if text !='':
            p = work(text)
            print(p[0][0])
            dig = p * 100
            if p[0][0] >0.5:
                prob = "%.2f%%" %(dig)
                result = "Screened feature is within O&M UI scope, chance is around "+ prob
            else:
                result = "Screened feature may NOT be in O&M UI's scope"
        else:
            result = "Please insert functional description"
        self.render('index2.html',text=text,result='{0}'.format(result))



application=tornado.web.Application(handlers=[(r"/", MainHandler),(r'/demo', IndexHandler)],
                                    template_path=os.path.join(os.path.dirname(__file__), "templates"),
                                    static_path =os.path.join(os.path.dirname(__file__), "statics"),debug = True
                                    )


if __name__=='__main__':
    if len(sys.argv)<2:
        port=8410
    else:
        port=string.atoi(sys.argv[1])


application.listen(port)
logger.info('Starting server:port=%d, use <Ctrl-C> to stop' % port)
tornado.ioloop.IOLoop.instance().start()
