import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

def run(address, port):
	HandlerClass = SimpleHTTPRequestHandler
	ServerClass  = BaseHTTPServer.HTTPServer
	Protocol     = "HTTP/1.0"

	if not address:
		address = '127.0.0.1'
	if not port:
		port = 8000
	else:
		port = int(port)

	server_address = (address, port)

	HandlerClass.protocol_version = Protocol
	httpd = ServerClass(server_address, HandlerClass)

	sa = httpd.socket.getsockname()
	print "Serving HTTP on", sa[0], "port", sa[1], "..."
	httpd.serve_forever()
