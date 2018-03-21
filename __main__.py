from adachat import ChatManager
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import traceback
from urllib.parse import urlparse

port = 8181
chat = ChatManager()
        
class WebServer(BaseHTTPRequestHandler):
    
    def setHeader(self, code):
        self.send_response(code)
        self.send_header('Content-Type', 'text/json')
        self.end_headers()
        
    def do_POST(self):
        if self.path == '/messages/':
            pass
        else:
            self.setHeader(404)
            return
            
        source = self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8")
        err = { "error": 0 }
        try:
            chat.append(source)
        except:
            err["error"] = "%s" % (sys.exc_info()[0])
            err["trace"] = traceback.format_exc()
            
        self.setHeader(200)
        self.wfile.write(bytes(json.dumps(err), 'utf-8'))
        
    def do_GET(self):
        if self.path == '/':
            # by default, simply allocate a conversation id for testing
            ret = {"id": ChatManager.allocate_conversation_id()}
            self.setHeader(200)
            self.wfile.write(bytes(json.dumps(ret), 'utf-8'))
            return

        uri = '/conversations/'
        if self.path.startswith(uri):
            self.setHeader(200)
            pass
        else:
            self.setHeader(404)
            return

        ret = None
        try:
            id = self.path[len(uri):]
            ret = chat.query(id)
        except:
            err = {"error": "%s" % sys.exc_info()[0], "trace": traceback.format_exc()}
            ret = json.dumps(err)
            
        self.wfile.write(bytes(ret, 'utf-8'))
        
chat_server = HTTPServer(('', port), WebServer)
print(chat.now(), "Server %d starts\n" % port)

try:
    chat_server.serve_forever()
except KeyboardInterrupt:
    pass

chat_server.server_close()
print(chat.now(), "Server %d closed\n" % port)
chat = None
chat_server = None