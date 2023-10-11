from flask import Flask, Response, request
from io import BytesIO
from pdfGen import generate_print_pdf
from jdRanking import rank
import ast
import pymongo
from time import time


app = Flask(__name__)

mongo_uri = "mongodb+srv://msavinash1139:point1@cluster0.opvthne.mongodb.net/point1?retryWrites=true&w=majority"
collection_name = "user_profiles"

def getResumeData(search_email):
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database()
    collection = db[collection_name]
    query = {"email_id": search_email}
    result = collection.find_one(query)
    # if result:
    #     print("Found document with email:", result)
    # else:
    #     print("Document not found for email:", search_email)
    client.close()
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
    print("Got request params:", time()-t, "ms")
    t = time()
    # projects = ast.literal_eval(projects)
    resumeData = getResumeData(email)
    print("Got data from MongoDB:", time()-t, "ms")
    t = time()
    resumeData = convert_newlines_to_list(resumeData)
    print("Converted new lines to lists:", time()-t, "ms")
    t = time()
    projects = resumeData["project_experience"]
    for index in range(len(projects)):
        projects[index] = str(projects[index])
    print("Prepped project data for ranking:", time()-t, "ms")
    t = time()
    ranks = rank(projects, jd)
    print("Ranked projects:", time()-t, "ms")
    t = time()
    rankedProjects = [projects[i] for  i in ranks]
    # print(rankedProjects)
    # print(type(rankedProjects))
    # print(rankedProjects)
    resumeData["project_experience"] = rankedProjects
    for index in range(len(resumeData["project_experience"])):
        resumeData["project_experience"][index] = ast.literal_eval(resumeData["project_experience"][index])
    # print(resumeData["project_experience"])
    print("Got data ready for pdf gen:", time()-t, "ms")
    t = time()
    pdf_bytes = generate_print_pdf(resumeData)
    print("Generated PDF:", time()-t, "ms")
    # Serve the generated PDF as a response
    pdf_buffer.seek(0)
    response = Response(pdf_bytes, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
    print("Returning response")
    return response



if __name__ == "__main__":
    app.run()
    # getResumeData()
