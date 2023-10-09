from flask import Flask, request, jsonify, render_template
import json
from pprint import pprint
import pymongo
import traceback
from flask import Flask, redirect, url_for, render_template, session, request
from flask_oauthlib.client import OAuth
import requests
import json
import pymongo

 
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

from flask import request


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


def convert_to_resume_data(data):
    # Helper function to extract data from the ImmutableMultiDict
    def extract_data(prefix, keys):
        extracted_data = {}
        for key in keys:
            full_key = f"{key}"
            if full_key in data:
                extracted_data[key] = data[full_key]
        return extracted_data

    # Helper function to extract list data from the ImmutableMultiDict
    def extract_list_data(prefix, keys):
        extracted_data = []
        i = 0
        while True:
            item_data = {}
            found = False
            for key in keys:
                full_key = f"{prefix}[{i}][{key}]"
                if key == "technologies":
                    # Handle multiple project technologies
                    technologies = data.getlist(full_key)
                    if technologies:
                        item_data[key] = technologies
                        found = True
                else:
                    if full_key in data:
                        item_data[key] = data[full_key]
                        found = True
            if not found:
                break
            extracted_data.append(item_data)
            i += 1
        return extracted_data

    # Extracting data
    resume_data = extract_data("", ["name", "phone_number", "email_id", "linkedin_link", "objective"])
    resume_data["work_experience"] = extract_list_data("work_experience", ["title", "company", "from", "to", "description"])
    resume_data["project_experience"] = extract_list_data("project_experience", ["title", "technologies", "description"])
    resume_data["education"] = extract_list_data("education", ["degree", "major", "university", "from", "to"])
    resume_data["technical_skills"] = {
        "languages": data.getlist("technical_skills_languages[]"),
        "developer_tools": data.getlist("technical_skills_developer_tools[]"),
        "technologies_and_frameworks": data.getlist("technical_skills_technologies_and_frameworks[]")
    }

    return resume_data



mongo_uri = "mongodb+srv://msavinash1139:point1@cluster0.opvthne.mongodb.net/point1?retryWrites=true&w=majority"
collection_name = "user_profiles"


def sendToMongo(data):
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database()
    collection = db[collection_name]
    insert_result = collection.insert_one(data)
    if insert_result.acknowledged:
        print("Data inserted successfully with ObjectId:", insert_result.inserted_id)
    else:
        print("Data insertion failed")
    client.close()




mongo_uri = "mongodb+srv://msavinash1139:point1@cluster0.opvthne.mongodb.net/point1?retryWrites=true&w=majority"
collection_name = "user_profiles"
# def getResumeData():
#     search_email = "msavinash1139@gmail.com"
#     client = pymongo.MongoClient(mongo_uri)
#     db = client.get_database()
#     collection = db[collection_name]
#     query = {"email_id": search_email}
#     result = collection.find_one(query)
#     client.close()
#     return result



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

# @app.route('/landingpage')
# def landingPage():
#     return render_template("landingPage.html")

@app.route('/useprofile')
def userProfile():
    user_email = google.get('userinfo').data['email']
    data = getResumeData(user_email)
    # print(data)
    return render_template("user.html", data=data)


@app.route('/')
def index():
    if 'google_token' in session and "email" in google.get('userinfo').data:
        return redirect("/useprofile")
    else:
        return redirect("/login")
        # user_email = google.get('userinfo').data['email']
        # data = getResumeData(user_email)
        # return render_template('user.html', data=data)
    # user_email = "msavinash1139@gmail.com"
    # data = getResumeData(user_email)
    # return render_template('newUser.html')



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
 


@app.route('/profile-data', methods=['POST'])
def store_user_data():
    try:
        data = request.form
        resume_data_json = convert_to_resume_data(data)
        print("SENDING")
        pprint(resume_data_json)
        sendToMongo(resume_data_json)
        return jsonify({'message': 'User data stored successfully'})

    except Exception as e:
        print("ERROR!!")
        print("Exception Type:", type(e).__name__)  # Print the type of exception
        print("Exception Message:", str(e))  # Print the error message
        print("Line Number:", sys.exc_info()[-1].tb_lineno)  # Print the line number where the exception occurred
        traceback.print_exc()  # Print the full traceback information
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()