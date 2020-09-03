from flask_app import *
import router


if __name__=='__main__':
    #Debud mode allows you to make changes without restarting the server
    app.run(host='0.0.0.0', port=5001, threaded=True)