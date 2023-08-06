import asyncio
from aiohttp import web
import requests
import os
import socket
import time
import sys
from GinVPN.AES import AES
import socket, string, random, requests,threading, queue



aes=None
def format_response(r):
    byte_string=b''
    byte_string+=r.status_code.to_bytes(2, byteorder='big')+b' '
    byte_string+=r.url.encode('utf-8')+b' '
    for h in r.headers:
        #print(h, r.headers[h])
        byte_string+=b'<h>'+h.encode('utf-8')+b':'+ r.headers[h].encode('utf-8')
    byte_string+=b'<b>'+r.content
    return byte_string
def make_request(req_type, req_url, headers_dict, req_body):
    r=None
    if(req_type==b'GET'):
        r = requests.get(req_url, data=req_body,headers=headers_dict)
    elif(req_type==b'POST'):
        r = requests.post(req_url, data=req_body,headers=headers_dict)
    elif(req_type==b'HEAD'):
        r = requests.head(req_url, headers=headers_dict)
    elif(req_type==b'PUT'):
        r = requests.put(req_url, data=req_body,headers=headers_dict)
    elif(req_type==b'DELETE'):
        r = requests.delete(req_url, data=req_body,headers=headers_dict)
    elif(req_type==b'OPTIONS'):
        r = requests.options(req_url, data=req_body,headers=headers_dict)
    return r
async def recv_msg(request):
    msg=await request.read()
    req=aes.decrypt(msg)
    print(req)
    req_type=req.split(b' ')[0]
    req_url=req.split(b' ')[1].decode('utf-8')
    r=b''.join(req.split(b' ')[2:]).split(b'<b>')
    req_headers=r[0].split(b'<h>')[1:]
    req_body=b''.join(r[1:])
    headers_dict={}
    for h in req_headers:
        headers_dict[h.split(b':')[0]]=h.split(b':')[1]
    r=make_request(req_type, req_url, headers_dict, req_body)
    b=aes.encrypt(format_response(r),False)
    print(len(b))
    if r!=None:
        return web.Response(status=200,body=bytes(b), headers={'zander-approved':'yes', 'Content-Length':str(len(b))})
    else:
        return web.Response(status=500,text="Server Error", headers={'zander-approved':'yes'})

    #return web.Response(status=500, text='GinVPN has encountered an error')
        

def main():
    key="Vrz19NDnmgmqvJw0fm4R3Zadi7OLLVoA"
    global aes
    aes=AES.AES(key,14)
    app = web.Application()
    app.router.add_route('POST', '/', recv_msg)
    loop = asyncio.get_event_loop()
    f = loop.create_server(app.make_handler(), '0.0.0.0', os.environ.get('PORT', '5000'))
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
if __name__ == "__main__":
    main()
