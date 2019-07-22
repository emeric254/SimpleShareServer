import os
import tornado.ioloop
import tornado.web
import tornado.httpserver

FILES = './files'

MAX_FILE_SIZE = 1073741824  # 1 gio


class FilesHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({
            'files': os.listdir(FILES)
        })

    def post(self):
        form_file = self.request.files.get('file_uploaded')
        if not form_file:
            self.set_status(400)
            return

        form_file = form_file[0]
        if not form_file:
            self.set_status(400)
            return

        file_path = os.path.join(FILES, form_file.get('filename'))
        with open(file_path, mode='wb') as file:
            file.write(form_file.get('body'))

        self.redirect('/', permanent=False)


def make_app():
    return tornado.web.Application([
        (r'/', tornado.web.RedirectHandler, {"url": "/index.html"}),
        (r'/(index\.html)', tornado.web.StaticFileHandler, {'path': '.'}),
        (r'/(favicon\.ico)', tornado.web.StaticFileHandler, {'path': '.'}),
        (r'/files', FilesHandler),
        (r'/files/(.*)', tornado.web.StaticFileHandler, {'path': FILES})
    ])


if __name__ == "__main__":
    if not os.path.isdir(FILES):
        os.mkdir(FILES)
    app = make_app()
    server = tornado.httpserver.HTTPServer(app, max_buffer_size=MAX_FILE_SIZE)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    tornado.ioloop.IOLoop.current().start()
