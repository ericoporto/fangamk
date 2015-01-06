import sys 
from threading import Thread
import webbrowser
import BaseHTTPServer 
import SimpleHTTPServer

serverClass=BaseHTTPServer.HTTPServer
handlerClass=SimpleHTTPServer.SimpleHTTPRequestHandler

Protocol = "HTTP/1.0"
port = 8080
ip = '127.0.0.1'
admIp = ip
admPort = 8081

new = 2 #2 goes to new tab, 0 same and 1 window.
url = "http://"+ip+":{0}".format(port)

handlerClass.protocol = Protocol
httpdGame = serverClass((ip,port), handlerClass)
httpdAdm = serverClass((admIp,admPort), handlerClass) 

sa = httpdGame.socket.getsockname()
sb = httpdAdm.socket.getsockname()
print("\n---\nServing HTTP on {0}, port {1}\n---\n".format(sa[0],sa[1]) )
print("\n---\nAdm HTTP listening on {0}, port {1}\n---\n".format(sb[0],sb[1]) )
browserOk = webbrowser.open(url,new=new)

def runGameServer():
    httpdGame.serve_forever()
    print("\nrunGameServer stopped\n")
    httpdAdm.shutdown()
    return

def runAdmServer():
    httpdAdm.handle_request()
    httpdGame.shutdown()
    print("\nrunAdmServer stopped\n")
    return

gameServerThread = Thread(target=runGameServer)
gameServerThread.daemon = True
admServerThread = Thread(target=runAdmServer)
admServerThread.daemon = True

gameServerThread.start()
admServerThread.start()
admServerThread.join()
