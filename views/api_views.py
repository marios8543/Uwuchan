from app import app,db,cfg,name
import models
from views import utils
import flask
import os
request = flask.request

@app.route('/')
def index():
    user = utils.session_check(request)
    if user.fng:
        resp = utils.response(200,'Registered')
        resp.set_cookie(cfg['cookie_name'],user.id,user)
        return resp
    else:
        return utils.response(200,'Welcome Back!',user)

@app.route('/api/make_post',methods=['POST','GET'])
def make_post():
    board = models.Board(request.args.get('board'))
    user = utils.session_check(request)
    if not user or user.fng:
        return utils.response(403,'You have been banned or have never visited before. If its the latter visit home first.',user)
    if not board.name:
       return utils.response(400,'That board does not exist.',user)        
    if not utils.restrict_check(request,board):
        return utils.response(403,'You have been banned from posting in this board.',user)  
    subject = request.form['subject'][:int(cfg['max_subject_length'])]
    comment = request.form['comment'][:int(cfg['max_comment_length'])]
    if 'subject' in request.form:
        subject = request.form['subject'][:int(cfg['max_subject_length'])]
    else:
        subject = ''    
    if 'file' in request.files:
        file = request.files['file']
        if not utils.allowed_file(file):
            return utils.response(400,'The image is of an unacceptable format or too large.',user)
        img = models.Image(file=file)
        if not img:
            return utils.response(500,'Something went wrong. Try again later',user)
    else:
        img = models.Image(dummy=True)
        img.id = 0
    post = models.Post(board=board,author=user,subject=subject,comment=comment,image=img.id)
    if post:
        return utils.response(201,post.dictate(),user)
    else:
        return utils.response(500,'Something went wrong. Try again later.',user)


@app.route('/api/get_post')
def get_post():
    user = utils.session_check(request)
    if not user or user.fng:
        return utils.response(403,'You have been banned or have never visited before. If its the latter visit home first.',user)
    board = models.Board(request.args.get('board'))
    if not board.name:
       return utils.response(400,'That board does not exist.',user)
    res = models.Post(board=board,id=request.args.get('id'))
    if res.board:
        return utils.response(200,res.dictate(),user)
    else:
        return utils.response(404,'That post does not exit',user)


@app.route('/api/add_comment',methods=['POST','GET'])
def add_comment():
    user = utils.session_check(request)
    board = models.Board(request.args.get('board'))
    post = models.Post(id=request.args.get('post'),board=board)
    if 'subject' in request.form:
        subject = request.form['subject'][:int(cfg['max_subject_length'])]
    else:
        subject = ''    
    comment = request.form['comment'][:int(cfg['max_comment_length'])]    
    if not user or user.fng:
        return utils.response(403,'You have been banned or have never visited before. If its the latter visit home first.',user)
    if not board.name:
        return utils.response(404,'That board does not exist.',user)
    if not utils.restrict_check(request,board):
        return utils.response(403,'You have been banned from posting in this board.',user)
    post = models.Post(id=request.args.get('post'),board=board)    
    if not post.board:
        return utils.response(404,'That post does not exist.',user)
    if post.thread==0:
        thread = post.id
    else:
        thread = post.thread 
    if 'file' in request.files:
        file = request.files['file']
        if not utils.allowed_file(file):
            return utils.response(400,'The image is of an unacceptable format or too large.',user)
        img = models.Image(file=file)
        if not img:
            return utils.response(500,'Something went wrong. Try again later',user)
    else:
        img = models.Image(dummy=True)
        img.id = 0
    comment = ">>{}\n{}".format(post.id,comment)
    post = models.Post(board=board,author=user,subject=subject,comment=comment,image=img.id,thread=thread)
    if post:
        return utils.response(201,post.dictate(),user)
    else:
        return utils.response(500,'Something went wrong. Try again later.',user)


@app.route('/api/get_boards')
def get_boards():
    user = utils.session_check(request)
    if not user or user.fng:
        return utils.response(403,'You have been banned or have never visited before. If its the latter visit home first.',user)
    arr = []        
    res = db.selectmany(table='boards',fields=['name','color','pinned'])
    for r in res:
        arr.append(r.__dict__)
    return utils.response(200,arr,user)


@app.route('/api/get_posts')
def get_posts():
    user = utils.session_check(request)
    if not user or user.fng:
        return utils.response(403,'You have been banned or have never visited before. If its the latter visit home first.',user)
    board = models.Board(request.args.get('board'))
    if not board.name:
        return utils.response(404,'That board does not exist.',user)
    limit = int(request.args.get('limit'))
    if limit>int(cfg['post_pull_limit']):
        return utils.response(400,'You can only pull {} posts per request'.format(cfg['post_pull_limit']),user)
    posts = models.get_posts(board,limit,dicc=True)
    return utils.response(200,posts,user)
