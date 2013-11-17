#! /usr/bin/env python
# coding=utf-8
__author__ = 'yl'
#using bottle here, a python web framework
from bottle import *
import hashlib
import xml.etree.ElementTree as ET
import urllib2
import json

app = Bottle()
 
@app.get("/")
def check_signature():
    #check whether the token is valid
    token = "thuhelper" #set your token here
    signature = request.GET.get('signature', None)  
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    if hashstr == signature:
        return echostr
    else:
        return None
 
def parse_msg():
    #"parse the command sent from wechat"
    recvmsg = request.body.read()  
    root = ET.fromstring(recvmsg)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg
 
def set_content():
    content = "Text message for wechat test"
    return content
  
@app.post("/")
def response_msg():
    msg = parse_msg()
    #handle text message
    textTpl = """<xml>
             <ToUserName><![CDATA[%s]]></ToUserName>
             <FromUserName><![CDATA[%s]]></FromUserName>
             <CreateTime>%s</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[%s]]></Content>
             <FuncFlag>0</FuncFlag>
             </xml>"""
    content = set_content()
    if msg['Content'] == "hi":
      echostr = textTpl % (
                           msg['FromUserName'], msg['ToUserName'], str(int(time.time())),
                           content)
      return echostr
    else:
      echostr = textTpl % (
                           msg['FromUserName'], msg['ToUserName'], str(int(time.time())),
                           'hi')
      return echostr
 
#call bae serive
from bae.core.wsgi import WSGIApplication
#create application
application = WSGIApplication(app)