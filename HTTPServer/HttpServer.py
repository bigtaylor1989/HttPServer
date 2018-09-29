#coding=utf-8
'''
name:fuji
time:2018-9-29
email:770313592@qq.com
'''
from socket import *
import sys
import re
from threading import Thread
from setting import *
import time

class HTTPServer(object):
    def __init__(self,addr = ('0.0.0.0',80)):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
        self.bind(addr)

    def bind(self,addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)

    #Http服务器启动
    def server_forever(self):
        self.sockfd.listen(10)
        print('Listen the porr %d ...'%self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            print('Connect from ',addr)
            handle_client = Thread(target = self.handle_request,args = (connfd,))
            handle_client.setDaemon(True)
            handle_client.start()

    def handle_request(self,connfd):
        #接收浏览器请求
        request = connfd.recv(4096)
        request_lines = request.splitlines()
        #获取请求行
        request_line = request_lines[0].decode()

        #正则提取请求方法和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern,request_line).groupdict()
        except:
            response_headers = "HTTP/1.1 500 Server Error\r\n"
            response_headers += '\r\n'
            response_body = "Server Error"
            response = response_headers + response_body
            connfd.send(response.encode())
            return

        #将请求发给frame得到返回数据结果
        status,response_body = self.send_request(env['METHOD'],env['PATH'])

        #根据响应码组织响应头内容
        response_headers = self.get_headers(status)
        #将结果组织为http　response 发送给客户端
        response = response_headers + response_body
        connfd.send(response.encode())
        connfd.close()

    #和框架frame交互发送request 获取response
    def send_request(self,method,path):
        s = socket()
        s.connect(frame_addr)
        #向webframe发送method 和 path
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        status = s.recv(1024).decode()
        response_body = s.recv(4096 * 10).decode()
        return status,response_body
    def get_headers(self,status):
        if status == '200':
            response_headers = 'HTTP/1.1 200 ok\r\n'
            response_headers += '\r\n'
        elif status == '404':
            response_headers = 'HTTP/1.1 404 Not Found\r\n'
            response_headers += '\r\n'
        return response_headers


if __name__ == '__main__':
    httpd = HTTPServer(ADDR)
    httpd.server_forever()

# 00000000001
# 00000000010
# 01010000011
# 11111010000


# 00000000000
# 11111010000