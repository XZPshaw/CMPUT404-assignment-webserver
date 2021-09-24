#  coding: utf-8 
import socketserver
import os
import urllib.parse
import datetime
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/



#https://emalsha.wordpress.com/2016/11/24/how-create-http-server-using-python-socket-part-ii/
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        self.str_data = self.data.decode('utf-8')
        #print("decoded request:\n",self.str_data)

        method = self.str_data.splitlines()[0].split()[0]
        relativePath = self.str_data.splitlines()[0].split()[1]


        base_dir = "www"
        file_path = os.path.abspath(base_dir) + relativePath
        #print(file_path)
        if method == 'GET' :
            content_type = ''
            #print("relativePath",relativePath.split('/'))
            if not relativePath.endswith("/") and '.' not in relativePath.split('/')[-1]:
                response = self.status301Res(relativePath)


            elif relativePath[-1] == '/' and ".css" not in relativePath and ".html" not in relativePath:
                file_path += 'index.html'
                
                try :
                    #print("final path:",file_path)
                    target_file = open(file_path,'r')
                    content_file = target_file.read()
                except FileNotFoundError:
                    response = self.status404Res()
                else:
                    target_file.close()
                    content_type = 'text/html'
                    response = self.status200Res(content_type,content_file)
            else:
                try:
                    #print("path:",file_path)
                    target_file = open(file_path,'r')
                    content_file = target_file.read()
                except FileNotFoundError:
                    response = self.status404Res()
                else:
                    target_file.close()
                    if (".css" in relativePath.split('/')[-1]):
                        #print("css here")
                        content_type = 'text/css'
                    elif (".html" in relativePath.split('/')[-1]):
                        #print("html here")
                        content_type = 'text/html'

                    response = self.status200Res(content_type,content_file)
        else:
            response = self.status405Res()

        #https://stackoverflow.com/questions/10114224/how-to-properly-send-http-response-with-python-using-socket-library-only/10114266
        #print(response)
        self.request.sendall(bytearray(response,'utf-8'))

    def status301Res(self,relativePath):
        '''
        res = "HTTP/1.1 301 Moved Permanently\r\n"
        res += "Content-Type: text/html\r\n"
        #res += "Content-Length: 0\r\n"
        res += "Connection: close\r\n"
        targetLocation = relativePath+"/"
        res += "Location: %s"%targetLocation
        '''

        res = "HTTP/1.1 301 Moved Permanently\r\n"
        res += "Date:"
        res += datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        res += "\r\n"
        res += "Connection: close\r\n"
        targetLocation = relativePath+"/"
        res += "Location: %s"%targetLocation
        res +="\r\n"
        res += "Content-Length: 0\r\n"
        res += "Content-Type: text/html\r\n\r\n"
        
        return res
        


        #self.request.sendall(response)


    def status200Res(self,content_type,content_file):

        
        res = "HTTP/1.1 200 OK\r\n"
        res += "Date:"
        res += datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        res += "\r\n"
        res += "Connection: close\r\n"
        res += "Content-Lenghth: %s\r\n"% str(len(content_file))
        res += "Content-Type:%s"%content_type
        res +="\r\n\r\n"
        res += content_file
        res += "\r\n"

        #print(res)
                                              
        #res = "HTTP/1.1 200 OK\r\n" + "Content-Type:%s\r\n\r\n"%content_type + content_file + "\r\n"
        return res
    def status404Res(self):
        res = "HTTP/1.1 404 Not Found\r\n"
        #res += "Content-Type: text/html\r\n"
        res += "Date:"
        res += datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        res += "\r\n"
        res += "Connection: close\r\n"
        res += "Content-Type: text/html\r\n\r\n"

        return res
    def status405Res(self):
        res = "HTTP/1.1 405 Method Not Allowed\r\n"
        res += "Date:"
        res += datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        res += "\r\n"
        res += "Connection: close\r\n"
        res += "Content-Type: text/html\r\n\r\n"
        return res


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
