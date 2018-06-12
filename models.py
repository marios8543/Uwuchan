from app import db
from datetime import datetime
import json
import hashlib
from random import randint
from app import db
from flask import jsonify
import os
import base64

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def make_hash(*args,length=64):
    tobehashed = ''
    for arg in args:
        tobehashed = tobehashed+str(arg)
    tobehashed = tobehashed.encode("utf-8")
    hash_object = hashlib.sha256(tobehashed)
    return hash_object.hexdigest()[:length]

def random(dig):
    size = "0"
    while len(size)<=dig:
        size = size+'0'
    return randint(int('1'+size),int('1'+size+'0'))

class User():
    id=""
    ip=""
    first_login=""
    banned=0
    restrictions=[]
    admin = 0
    fng = 0

    def __init__(self,id=0,ip=0,dummy=False):
        if dummy==True:
            return
        if ip!=0 and id==0:
            self.ip = ip
            self.first_login = get_timestamp()
            self.id = make_hash(ip,self.first_login)            
            db.insert(table='users',values={
                'id':self.id,
                'first_login':self.first_login            
            })
            self.fng = 1
            return
        res = db.select(table='users',fields=['banned','first_login','admin'],params={'id':id})
        self.id = id
        self.ip = ip
        self.first_login = res.first_login
        self.banned = int(res.banned)
        self.admin = int(res.admin)
        #self.restrictions = db.selectmany(table='restrictions',fields=['board','timestamp'],params={'id':self.id,'valid':'1'})
        
    def update(self):
        db.update(table='users',values={
            'last_login':self.last_login,
            'banned':self.banned,
            'admin':self.admin
        },params={'ip':self.ip})
        return 1

    def ban(self,duration=0):
        db.update(table='users',values={'banned':'1'},params={'ip':self.ip})
        if duration>0:
            db.db.execute("""
            CREATE EVENT `%sban` 
            ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL %s HOUR
            ON COMPLETION NOT PRESERVE
            DO BEGIN
	            UPDATE users SET banned=0 WHERE ip=%s
            END;
            """,(self.ip,duration,self.ip,))
        return 1

    def restrict(self,board,duration=0):
        db.insert(table='restrictions',values={'id':self.id,'board':board.name})
        if duration>0:
            db.db.execute("""
            CREATE EVENT `%srestriction%s` 
            ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL %s HOUR
            ON COMPLETION NOT PRESERVE
            DO BEGIN
	            DELETE FROM restrictions WHERE ip=%s AND board=%s
            END;
            """,(self.ip,board.name,duration,self.ip,board.name,))
        return 1    


class Board():
    name=""
    color="#DCDCDC"
    pinned_post=0
    admins = []

    def __init__(self,name,dummy=False):
        if dummy==True:
            return
        res = db.select(table='boards',fields=['color','pinned','admins'],params={'name':name})
        if not res:
            return
        self.name = name
        self.color = res.color
        self.pinned_post = res.pinned
        self.admins = json.loads(res.admins)

    def add_admin(self,user):
        admins = json.loads(db.select(table='boards',fields=['admins'],params={'name':self.name}))
        if user.id in admins:
            return 1       
        admins.append(user.id)
        db.update(table='boards',values={'admins':admins},params={'name':self.name})
        return 1

    def remove_admin(self,user):
        admins = json.loads(db.select(table='boards',fields=['admins'],params={'name':self.name}))          
        admins.remove(user.id)
        db.update(table='boards',values={'admins':admins},params={'name':self.name})
        return 1

class Image():
    def __init__(self,id=0,file=0,dummy=False):
        if dummy==True:
            return
        if id==0:
            file.seek(0, os.SEEK_END)
            self.timestamp = get_timestamp()
            self.og_name = '.'.join(file.filename.split('.')[:-1])
            self.size = file.tell()
            self.type = file.filename.split('.')[-1]
            self.id = make_hash(self.timestamp,self.og_name,self.size)
            file.seek(0)
            self.data = file.read()
            db.insert(table='images',values={
                'id':self.id,
                'og_name':self.og_name,
                'type':self.type,
                'size':self.size,
                'data':self.data
            },norm=False)
            return
        else:
            res=db.select(table='images',fields=['id','timestamp','og_name','type','size','data'],params={'id':id},norm=False)
            self.id = id
            self.timestamp = res
            self.og_name = res.og_name.decode("utf-8")
            self.type = res.type.decode("utf-8")
            self.size = res.size
            self.data = res.data


class Post():
    id = ""
    author = 0
    board = ""
    timestamp = ""
    subject = ""
    comment = ""
    image = 0
    thread = 0

    def __init__(self,board=0,author=0,subject=0,comment=0,image=0,thread=0,id=0,timestamp=0,dummy=False):
        if dummy==True:
            return
        if type(board)==str:
            board = Board(board)
        if id==0:
            self.author = author
            self.board = board
            self.subject = subject
            self.comment = comment
            self.image = image
            self.thread = thread
            self.id = random(8)
            self.timestamp = get_timestamp()
            if db.insert(table='posts',values={
                'id':self.id,
                'board':self.board.name,
                'author':self.author.id,
                'timestamp':self.timestamp,
                'subject':self.subject,
                'text':self.comment,
                'image':self.image,
                'thread':self.thread
            }):
                return
        else:
            res=db.select(table='posts',fields=[
            'author','timestamp',
            'board','thread',
            'subject','text','image'],params={
                'id':id,
                'board':board.name
            })
            if not res:
                return
            self.id = id
            self.author = User(id=res.author)
            self.board = board
            self.timestamp = res.timestamp
            self.thread = int(res.thread)
            self.subject = res.subject
            self.comment = res.text
            if res.image!='0':
                self.image = Image(id=res.image.decode("utf-8"))

    def dictate(self):
        if self.image:
            img='/image/'+str(self.image)
        else:
            img=0   
        return {
            'id':self.id,
            'timestamp':self.timestamp,
            'board':self.board.name,
            'thread':int(self.thread),
            'subject':self.subject,
            'comment':self.comment,
            'image':img
        }     


def get_posts(board,limit,dicc=False):
    ret = []
    res = db.selectmany(table='posts',fields=['id'],params={'board':board.name})
    for r in res:
        p=Post(id=r.id,board=board.name)
        if dicc:
            ret.append(p.dictate())
        else:
            ret.append(p)           
    return ret[:limit]
