from flask import Flask
import json
import pbot_orm

app = Flask(__name__)
cfg = json.loads(open("config.json","r").read())
name = cfg['site_name']
db = pbot_orm.ORM(host=cfg['db_host'],
    username=cfg['db_user'],password=cfg['db_pass'],
    database=cfg['db_database'])
app.config['MAX_CONTENT_PATH'] = cfg['max_image_size']*1024*1024

from views.site_views import *
if cfg['enable_api']=='true':
    from views.api_views import *
from views.admin_views import *