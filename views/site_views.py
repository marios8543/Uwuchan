from app import app,db,cfg,name
import models
import flask
import base64

@app.route('/image/<id>')
@app.route('/image/<id>.<ext>')
def image(id=0,ext=0):
    res = models.Image(id=id)
    if not res:
        return flask.make_response(flask.jsonify({'code':'404','status':'error','content':'Image not found'}),404)
    response = flask.make_response(res.data)
    response.headers.set('Content-Type', 'image/{}'.format(res.type))
    response.headers.set('Content-Disposition', 'attachment', filename='{}.{}'.format(res.og_name,res.type))
    return response
