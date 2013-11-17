wechatDemo
==========

A python demo for wechat platform, based on bottle web framework and BAE service.

app.conf:
    handle url request
    
bottle.py:
    python web framework
    
index.py:
    verify validity and parse the message from weixin, then send text message to user through bae
    you can visit http://mp.weixin.qq.com/wiki/index.php?title=%E9%A6%96%E9%A1%B5 for more wechat API
