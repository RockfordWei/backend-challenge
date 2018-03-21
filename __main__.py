# Ada Support Backend Developer Challenge
# Solution by Rocky Wei March 21, 2018

from adachat import ChatManager
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import traceback
from urllib.parse import urlparse

# default server port
port = 8181

# start a singleton instance because it would load a sqlite3 database /tmp/chat.db by default
chat = ChatManager()
        
class WebServer(BaseHTTPRequestHandler):
    # a very basic http request handler implementation
    
    def setHeader(self, code):
        # assuming this server would serve json only
        self.send_response(code)
        self.send_header('Content-Type', 'text/json')
        self.end_headers()
        
    def do_POST(self):
        # post request, mandated by the challenge
        if self.path == '/messages/':
            pass
        else:
            self.setHeader(404)
            return
        
        # get the upload json content, assuming utf-8 
        # could be decoded to any other encodings
        source = self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8")
        
        # placeholder for error returns
        err = { "error": 0 }
        try:
            # log the chat content
            chat.append(source)
        except:
            err["error"] = "%s" % (sys.exc_info()[0])
            err["trace"] = traceback.format_exc()
            
        self.setHeader(200)
        # respond to the client
        self.wfile.write(bytes(json.dumps(err), 'utf-8'))
        
    def do_GET(self):
        # on get method, however, for testing purposes, 
        # it is providing an express way to generate a valid conversation id

        if self.path == '/':
            # by default, simply allocate a conversation id for testing
            ret = {"id": ChatManager.allocate_conversation_id()}
            self.setHeader(200)
            self.wfile.write(bytes(json.dumps(ret), 'utf-8'))
            return

        # mandated by the challenge
        uri = '/conversations/'
        if self.path.startswith(uri):
            self.setHeader(200)
            pass
        else:
            self.setHeader(404)
            return

        ret = None
        try:
            # parse the conversation id
            id = self.path[len(uri):]
            
            # perform the query
            ret = chat.query(id)
        except:
            err = {"error": "%s" % sys.exc_info()[0], "trace": traceback.format_exc()}
            ret = json.dumps(err)
            
        # send back the history
        self.wfile.write(bytes(ret, 'utf-8'))
        
# start the server by the above settings
chat_server = HTTPServer(('', port), WebServer)

print(chat.now(), "Server %d starts\n" % port)

try:
    chat_server.serve_forever()
except KeyboardInterrupt:
    pass

# cleaning up
chat_server.server_close()
print(chat.now(), "Server %d closed\n" % port)
chat = None
chat_server = None