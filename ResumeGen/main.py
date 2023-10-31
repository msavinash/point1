import ast
import base64
import datetime
import json
import os
from pprint import pprint
import re
import sys
import traceback

from io import BytesIO


from time import time

from flask import Flask, Response, request, jsonify, render_template, redirect, url_for, session, request
from flask_cors import CORS
from flask_oauthlib.client import OAuth

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from pdfGen import generatePdf
from jdRanking import rank
from utils import *


# Constants
OAUTH_CREDENTIALS = os.path.join("credentials", 'oauth.json')
FIRESTORE_CREDENTIALS = os.path.join("credentials", 'firestore.json')
COLLECTION_NAME = "resume-data"


# Initialize Firestore DB
firestoreCredentials = credentials.Certificate(FIRESTORE_CREDENTIALS)
app = firebase_admin.initialize_app(firestoreCredentials)
db = firestore.client()



# Load Google OAuth credentials
oauthCredentials = None
with open(OAUTH_CREDENTIALS) as f:
    oauthCredentials = json.load(f)

# Google OAuth configuration
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=oauthCredentials["web"]["client_id"],
    consumer_secret=oauthCredentials["web"]["client_secret"],
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'tailores is the best'
CORS(app)



app.jinja_env.filters['b64encode'] = b64encodeFilter
app.jinja_env.filters['format_date'] = formatDate



# Routes

@app.route('/')
def index():
    if 'google_token' in session and "email" in google.get('userinfo').data:
        return redirect("/profile")
    else:
        return redirect("/login")


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    accessToken = session.get('google_token')[0]
    revokeGoogleAccessToken(accessToken)
    session.pop('google_token', None)
    print("logout", 'google_token' in session)
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
    userEmail = google.get('userinfo').data['email']
    userExists = checkUserExists(userEmail, db, COLLECTION_NAME, google)

    if userExists:
        return redirect("/")
    else:
        return redirect("/newuser")
    

@google.tokengetter
def getGoogleOauthToken():
    return session.get('google_token')


@app.route('/profile')
def userProfile():
    if 'google_token' in session and "email" in google.get('userinfo').data:
        userEmail = google.get('userinfo').data['email']
        print("User email:", userEmail)
        if not checkUserExists(userEmail, db, COLLECTION_NAME, google):
            return redirect("/newuser")
        resumeData = getResumeData(userEmail, db, COLLECTION_NAME, google)
        pdfBytes, _ = generatePdf(resumeData)
        encodedData = base64.b64encode(pdfBytes).decode('utf-8')
        return render_template("user.html", resumeData=resumeData, encodedData=encodedData)
    else:
        return redirect("/login")


@app.route('/newuser')
def newUserIndex():
    if 'google_token' in session and "email" in google.get('userinfo').data:
        userData = google.get('userinfo').data
        email = userData["email"]
        if checkUserExists(email, db, COLLECTION_NAME, google):
            return redirect("/")    
        return render_template('newUser.html', email=userData["email"], name=userData["name"])
    else:
        return redirect("/login")


@app.route('/profile-data', methods=['POST'])
def store_user_data():
    try:
        data = request.form
        resumeDataJson = preprocessResumeData(data)
        addToFirestore(resumeDataJson, db, COLLECTION_NAME)
        return jsonify({'message': 'User data stored successfully'})

    except Exception as e:
        print("ERROR!!")
        print("Exception Type:", type(e).__name__)  # Print the type of exception
        print("Exception Message:", str(e))  # Print the error message
        print("Line Number:", sys.exc_info()[-1].tb_lineno)  # Print the line number where the exception occurred
        traceback.print_exc()  # Print the full traceback information
        return jsonify({'error': str(e)}), 500
    




@app.route('/generate_rankedpdf', methods=['POST'])
def generateRankedPdf():
    t = time()
    jd = None
    pdfBuffer = BytesIO()
    email = request.form.get('email')
    jd = request.form.get('job_description')
    highlight = request.form.get("highlight")
    onepage = request.form.get("onepage")
    print("Got request params:", time()-t, "s")
    t = time()
    resumeData = getResumeData(email, db, COLLECTION_NAME, google)
    print("Got data from Firestore:", time()-t, "s")
    t = time()
    projects = resumeData["project_experience"].copy()
    for index, project in enumerate(projects):
        projects[index] = project["title"]+" "+" ".join(project["technologies"])+" "+" ".join(project["description"])
    print("Prepped project data for ranking:", time()-t, "s")
    t = time()
    ranks, words = rank(projects, jd)
    print("Ranked projects:", time()-t, "s")
    t = time()
    rankedProjects = [resumeData["project_experience"][i] for i in ranks]
    workExperience = resumeData["work_experience"]

    for index, project in enumerate(rankedProjects):
        if type(project["description"]) == str:
            rankedProjects[index]["description"] = [project["description"]]

    if highlight == "true":
        for pIndex, project in enumerate(rankedProjects):
            for dIndex, description in enumerate(project["description"]):
                sentence = description
                for word in words:
                    pattern = re.compile(fr'\b({re.escape(word)})\b', re.IGNORECASE)
                    sentence = pattern.sub(r'<b>\1</b>', sentence)
                rankedProjects[pIndex]["description"][dIndex] = sentence


    
        for wIndex, work in enumerate(workExperience):
            for dIndex, description in enumerate(work["description"]):
                sentence = description
                for word in words:
                    pattern = re.compile(fr'\b({re.escape(word)})\b', re.IGNORECASE)
                    sentence = pattern.sub(r'<b>\1</b>', sentence)
                workExperience[wIndex]["description"][dIndex] = sentence

    resumeData["project_experience"] = rankedProjects
    resumeData["work_experience"] = workExperience
    print("Got data ready for pdf gen:", time()-t, "s")
    t = time()
    pdf_bytes = None
    if onepage == "true":
        while True:
            pdf_bytes, num_pages = generatePdf(resumeData)
            print("Num pages:", num_pages)
            if num_pages > 1:
                resumeData["project_experience"] = resumeData["project_experience"][:-1]
            else:
                break
    else:
        pdf_bytes, _ = generatePdf(resumeData)
    print("Generated PDF:", time()-t, "s")
    pdfBuffer.seek(0)
    response = Response(pdf_bytes, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
    print("Returning response")
    return response



@app.route('/checkmyuserexists', methods=['GET'])
def checkmyuserexists():
    email = request.args.get('email')
    if checkUserExists(email, db, COLLECTION_NAME, google):
        print("Found document with email:")
        return "true"
    else:
        print("Document not found for email:", email)
        return "false"




if __name__ == "__main__":
    app.run()
    # getResumeData()
