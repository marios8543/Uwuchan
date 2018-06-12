from app import app,cfg

if __name__=='__main__' and cfg['dry_run']=='false':
    app.run(debug=True)
