#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, Abdurahman Hersi, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse
from urllib.parse import urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):

        #host=url

        #if("http" in url):
        adjusted_url = urlparse(url)
        host = adjusted_url.hostname
        port = adjusted_url.port
        path= adjusted_url.path
        
        #addr_info=socket.getaddrinfo(host,80, proto=socket.SOL_TCP)
        #print("came in get host port")
        #addr=addr_info[0]


       
        
        return(host,port,path)
        

    def connect(self, host, port):
        # use sockets!

        #Creating socket
        #try:
        #    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ##except socket.error as err:
          #  print "socket creation failed with error %s" %(err)
          #  sys.exit()

        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))        
        return s

    def get_code(self, data):
        return None

    def close(self):
        self.socket.close()

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        #print("came into get")
        code = 500
        body = ""

        host=url
        if("http" in url):
            adjusted_url = urlparse(url)
            host = adjusted_url.hostname


        #return all information from host to create socket
        addr= self.get_host_port(url)
        (host,port,path)= addr
        if(port==None):
            port=80
        if(len(path)==0):
            path='/'

        s= self.connect(host,port)
   
        
        info=("GET "+path+" HTTP/1.1\r\nConnection: close\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Type: application/x-www-form-urlencoded\r\nHost: "+ host+" \r\n\r\n")
        s.sendall(info.encode('utf-8'))
        #self.socket.sendall(data.encode('utf-8'))
        new_info= self.recvall(s)
        #print(new_info)
       # print("------------------------")
        aa=new_info.split('\r\n\r\n')
        #print(aa[0])
        print("----------------")
        #print(aa[1])
        print("-------------------")
        
        #print("asdfasf")
        code = int(new_info.split()[1])

        s.close()
        body=aa[1]
        #print(body)
        sys.stdout.write(body)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        host=url
        if("http" in url):
            adjusted_url = urlparse(url)
            host = adjusted_url.hostname


        #print("came into post")



        addr= self.get_host_port(url)
        (host,port,path)= addr
        if(port==None):
            port=80
        if(len(path)==0):
            path='/'

        s= self.connect(host,port)
        
        if(args):
            args=urlencode(args)
            content_length=len(args)
        else:
            args=""
            content_length=0


        info="POST "+path+" HTTP/1.1\r\nHost: "+ host+"\r\nContent-Length: "+str(content_length)+"\r\nContent-Type: application/x-www-form-urlencoded\r\nConnection: close\r\n\r\n"+args
        s.sendall(info.encode('utf-8'))
        #self.socket.sendall(data.encode('utf-8'))
        new_info= self.recvall(s)
        #print(new_info)
        #print("------------------------")
        aa=new_info.split('\r\n\r\n')
        #print(aa[0])
        #print("----------------")
        #print(aa[1])
        
        print("----------")
        #print(aa[0])
        print("----------")

        code = int(new_info.split()[1])

        s.close()
        body=aa[1]
        sys.stdout.write(body)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print("eee")
        print(client.command( sys.argv[2], sys.argv[1] ).body)
    else:
        print(client.command( sys.argv[1]))   
