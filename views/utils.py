import models
from app import app,db,cfg
import flask
import os

def session_check(request):
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if cfg['cookie_name'] in request.cookies:
        id = request.cookies.get(cfg['cookie_name'])
    else:
        res = db.select(table='users',fields=['id'],params={'ip':ip})
        if res:
            id=res.id
        else:
            return models.User(ip=ip)        
    res = models.User(id=id)
    if res.ip!=ip:
        res.ip = ip
        res.update()
    if res.banned:
        return
    return res


def restrict_check(request,board):
    user = session_check(request)
    if not user:
        return 
    res = db.select(table='restrictions',fields=['timestamp'],params={'id':user.id,'board':board.name})
    if res:
        return
    else:
        return 1    


def allowed_file(file):
    file.seek(0, os.SEEK_END)
    return file.filename.split('.')[-1] in cfg['allowed_exts'] and file.tell()<=int(cfg['max_image_size'])*1024*1024


def response(code,message,user):
    if str(code)[0]=='2':
        status = 'success'
    else:
        status = 'error'   
    return flask.make_response(flask.jsonify({'code':code,'status':status,'content':message,'user':user.__dict__}),code)
    
