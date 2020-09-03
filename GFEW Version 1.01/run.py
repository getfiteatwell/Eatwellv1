from flask_app import *
import router
import user_router
import social_media_auth


if __name__=='__main__':
    #Debud mode allows you to make changes without restarting the server
    app.run(host='0.0.0.0', threaded=True)