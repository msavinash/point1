from flask import Flask, Response, request
from io import BytesIO
from pdfGen import generate_print_pdf
from jdRanking import rank
import ast
import pymongo
from time import time
import datetime
from flask_cors import CORS


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

import re



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)

mongo_uri = "mongodb+srv://msavinash1139:point1@cluster0.opvthne.mongodb.net/point1?retryWrites=true&w=majority"
collection_name = "user_profiles"


# UserReg modules

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






























# ResumeGen modules
def format_date(date_str):
    try:
        from_date = date_str.split('-')
        year, month = int(from_date[0]), int(from_date[1])
        month_name = datetime.date(year, month, 1).strftime('%B')
        if len(month_name)>4:
            month_name = month_name[:3]
        return f"{month_name} {year}"
    except Exception as e:
        return date_str

app.jinja_env.filters['format_date'] = format_date


client = pymongo.MongoClient(mongo_uri)
db = client.get_database()
collection = db[collection_name]
# collection.create_index([("email_id", pymongo.ASCENDING)])

def getResumeData(search_email):
    query = {"email_id": search_email}
    result = collection.find_one(query)
    # if result:
    #     print("Found document with email:", result)
    # else:
    #     print("Document not found for email:", search_email)
    # client.close()
    return result


def convert_newlines_to_list(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_newlines_to_list(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = convert_newlines_to_list(item)
    elif isinstance(data, str):
        if '\n' in data:
            data = data.split('\n')
    return data









# UserReg routes
@app.route('/profile')
def userProfile():
    if 'google_token' in session and "email" in google.get('userinfo').data:
        user_email = google.get('userinfo').data['email']
        data = getResumeData(user_email)
        # print(data)
        return render_template("user.html", data=data)
    else:
        return redirect("/login")

    


@app.route('/')
def index():
    if 'google_token' in session and "email" in google.get('userinfo').data:
        return redirect("/profile")
    else:
        return redirect("/login")
    



@app.route('/newuser')
def newUserIndex():
    if 'google_token' in session and "email" in google.get('userinfo').data:
        print(session['google_token'])
        user_email = google.get('userinfo').data
        print(user_email)
        return render_template('newUser.html')
    else:
        return redirect("/login")
        # user_email = google.get('userinfo').data['email']
        # data = getResumeData(user_email)
        # return render_template('user.html', data=data)

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
    






################################################################################################################################################################



# ResumeGen routes
@app.route('/')
def hello_world():
    return 'Hello, World!'


# @app.route('/generate_rankedpdf', methods=['POST'])
@app.route('/generate_getrankedpdf', methods=['GET'])
def generate_getrankedpdf():
    jd = None
    with open("sampleJD.txt", 'r', encoding='utf-8', errors='ignore') as f:
        jd = f.read()
    # Create an in-memory PDF
    pdf_buffer = BytesIO()
    email = "msavinash1139@gmail.com"
    print("Got email:", email)
    # jd = request.form.get('job_description')
    print("Got JD:")
    # projects = ast.literal_eval(projects)
    resumeData = getResumeData(email)
    resumeData = convert_newlines_to_list(resumeData)
    projects = resumeData["project_experience"]
    for index in range(len(projects)):
        projects[index] = str(projects[index])
    ranks = rank(projects, jd)
    rankedProjects = [projects[i] for  i in ranks]
    resumeData["project_experience"] = rankedProjects
    for index in range(len(resumeData["project_experience"])):
        resumeData["project_experience"][index] = ast.literal_eval(resumeData["project_experience"][index])
    pdf_bytes = generate_print_pdf(resumeData)

    # Serve the generated PDF as a response
    pdf_buffer.seek(0)
    response = Response(pdf_bytes, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
    print("Returning response")
    return response

@app.route('/generate_rankedpdf', methods=['POST'])
# @app.route('/generate_rankedpdf', methods=['GET'])
def generate_rankedpdf():
    t = time()
    jd = None
    with open("sampleJD.txt", 'r', encoding='utf-8', errors='ignore') as f:
        jd = f.read()
    # Create an in-memory PDF
    pdf_buffer = BytesIO()
    # rankedProjects = request.json.get('data', [])
    # rankedProjects = json.loads(request.form.get('data'))
    email = request.form.get('email')
    print("Got email:", email)
    jd = request.form.get('job_description')
    print("Got JD:", jd)
    highlight = request.form.get("highlight")
    print("GOT HIGHLIGHT!!!!", highlight)
    print("Got request params:", time()-t, "s")
    t = time()
    # projects = ast.literal_eval(projects)
    resumeData = getResumeData(email)
    print("Got data from MongoDB:", time()-t, "s")
    t = time()
    resumeData = convert_newlines_to_list(resumeData)
    pprint(resumeData)
    print("Converted new lines to lists:", time()-t, "s")
    t = time()
    projects = resumeData["project_experience"].copy()
    # print(projects)
    for index, project in enumerate(projects):
        projects[index] = project["title"]+" ".join(project["technologies"])+" ".join(project["description"])
    print("Prepped project data for ranking:", time()-t, "s")
    t = time()
    ranks, words = rank(projects, jd)
    # print(ranks)
    # print(resumeData["project_experience"])
    print("Ranked projects:", time()-t, "s")
    t = time()
    rankedProjects = [resumeData["project_experience"][i] for i in ranks]

    for index, project in enumerate(rankedProjects):
        if type(project["description"]) == str:
            rankedProjects[index]["description"] = [project["description"]]

    print("Got words", words)
    if highlight == "true":
        for pIndex, project in enumerate(rankedProjects):
            for dIndex, description in enumerate(project["description"]):
                sentence = description
                for word in words:
                    # Create a regex pattern that matches the word case-insensitively
                    pattern = re.compile(fr'\b({re.escape(word)})\b', re.IGNORECASE)
                    sentence = pattern.sub(r'<b>\1</b>', sentence)
                print(rankedProjects[pIndex]["description"])
                print(rankedProjects[pIndex]["description"][dIndex])
                rankedProjects[pIndex]["description"][dIndex] = sentence

    # print(rankedProjects)
    # print(type(rankedProjects))
    # print(rankedProjects)
    resumeData["project_experience"] = rankedProjects
    # for index in range(len(resumeData["project_experience"])):
    #     resumeData["project_experience"][index] = ast.literal_eval(resumeData["project_experience"][index])
    # # print(resumeData["project_experience"])
    # print(resumeData)
    print("Got data ready for pdf gen:", time()-t, "s")
    t = time()
    pdf_bytes = generate_print_pdf(resumeData)
    print("Generated PDF:", time()-t, "s")
    # Serve the generated PDF as a response
    pdf_buffer.seek(0)
    response = Response(pdf_bytes, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
    print("Returning response")
    return response



@app.route('/checkmyuserexists', methods=['GET'])
def checkmyuserexists():
    email = request.args.get('email')
    print("Got email:", email)
    result = getResumeData(email)
    if result:
        print("Found document with email:", result)
        return "true"
    else:
        print("Document not found for email:", email)
        return "false"
    return "NULL"




if __name__ == "__main__":
    app.run()
    # getResumeData()
