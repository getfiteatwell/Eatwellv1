from flask_app import app
import API_auth
import API_get
import API_post


if __name__=='__main__':
    #Debud mode allows you to make changes without restarting the server
    app.run(host='0.0.0.0', debug=True)