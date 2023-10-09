from flask import Flask, redirect, url_for, render_template, session, request
from flask_oauthlib.client import OAuth
import requests
import json
import pymongo


mongo_uri = "mongodb+srv://msavinash1139:point1@cluster0.opvthne.mongodb.net/point1?retryWrites=true&w=majority"
collection_name = "user_profiles"
def check_user_exists(search_email):
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database()
    collection = db[collection_name]
    query = {"email_id": search_email}
    result = collection.find_one(query)
    print(result)
    client.close()
    if result:
        return True
    else:
        return False

def getResumeData(search_email):
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database()
    collection = db[collection_name]
    query = {"email_id": search_email}
    result = collection.find_one(query)
    client.close()
    return result

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

cred = None
with open("cred.json") as f:
    cred = json.load(f)

# Google OAuth configuration
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=cred["web"]["client_id"],
    consumer_secret=cred["web"]["client_secret"],
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    # if 'google_token' in session:
    #     user_email = google.get('userinfo').data['email']
    #     data = getResumeData(user_email)
    #     return render_template('user.html', data=data)
    # user_email = "msavinash1139@gmail.com"
    # data = getResumeData(user_email)
    return render_template('newUser.html')


@app.route('/newuser')
def newUserIndex():
    if 'google_token' in session:
        return render_template('newUser.html')

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    
    session['google_token'] = (response['access_token'], '')
    print(session['google_token'])
    # Get user info from Google
    user_email = google.get('userinfo').data['email']
    # print(user_info.data['email'])
    
    # Check if the user exists on your backend using the user_info
    # You can make an API call to /checkuser or perform any necessary checks here
    
    # return redirect(url_for('index'))
    user_exists = check_user_exists(user_email)

    if user_exists:
        # User exists, render user.html
        # return render_template('user.html')
        return redirect("/")
    else:
        # New user, render newUser.html
        # return render_template('newUser.html')
        return redirect("/newuser")
    


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run()
