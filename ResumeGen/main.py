from flask import Flask, Response, request
from io import BytesIO
from pdfGen import generate_print_pdf
from jdRanking import rank
import ast


app = Flask(__name__)

resumeData = {"name": "Avinash Mangalore Suresh", "phone_number":"530-551-2854",
            "email_id": "msavinash1139@gmail.com", "linkedin_link": "linkedin.com/in/avinash-m-s",
            "objective":'''To contribute my extensive skills and experience in full stack development, cloud technologies and unit testing
to drive innovation and deliver reliable solutions in a dynamic and collaborative environment''',
            "work_experience":[
                {
                    "title":"Software Developer Intern",
                    "company":"Wolters Kluwer Health",
                    "from":"June 2023", "to": "Aug 2023",
                    "description":['''Achieved 80% code coverage enhancement for C# projects through test writing using Nunit during internship.''',
                                '''Spearheaded Jenkins-based builds and leveraged OpenCover for accurate code coverage analysis, resulting in substantial improvement in C# project code coverage.''',
                                '''Utilized Cobertura to generate comprehensive code coverage reports, highlighting the impact on software quality'''
                                ]
                },
                {
                    "title": "Software Development Engineer",
                    "company": "Amadeus Software Labs",
                    "from": "Aug 2021",
                    "to": "Aug 2022",
                    "description": [
                        "Developed Python scripts for PostgreSQL to automate database operations, improving efficiency and fixing errors in database migration and data transformation tasks.",
                        "Analyzed Collibra workflows to identify issues with workflow failure and update business logic behind workflows to stay up to date with the data governance policies.",
                        "Managed data governance operations including data asset import and workflow deployment through Collibra for over 400 users, ensuring data integrity and governance for critical data processes."
                    ]
                },
                {
                    "title": "Software Developer Intern",
                    "company": "Amadeus Software Labs",
                    "from": "Jan 2021",
                    "to": "May 2021",
                    "description": [
                        "Led collaboration efforts with cross-functional teams to seamlessly integrate an in-house software testing application with a ticketing application through SOAP APIs, leading to a 30% improvement in ticketing speed.",
                        "Enhanced in-house testing app's UI with Angular.js, introducing new features for smoother navigation.",
                        "Developed backend support using Spring Java, integrating SOAP APIs to service the front end app."
                    ]
            }
            ],
            "project_experience":[
                {
                "title":"Hotel Amenities Management System",
                "technologies": ["Java", "Spring", "Cassandra", "Javascript", "React"],
                "description": [
                                '''Implemented the backend using Java and Spring, following the Model-View-Controller (MVC) architecture.''',
                                '''Utilized Cassandra to store and manage data related to customer requests, amenities, availability and priority.''',
                                '''Designed a user-friendly interface for customers to manage their tickets using React'''
                                ]
                },
                {
                    "title": "Movie Ticketing Application",
                    "technologies": ["Python", "AWS Lambda", "S3", "DynamoDB", "API Gateway"],
                    "description": [
                        "Created serverless Python APIs for ticket management on AWS Lambda, resulting in 30% faster development time.",
                        "Configured AWS Application Gateway to seamlessly integrate with the ticketing application.",
                        "Implemented data storage and retrieval using DynamoDB for JSON objects ensuring data consistency and durability."
                    ]
                },
                {
                    "title": "RideShare API Development",
                    "technologies": ["Docker", "Python", "AWS EC2", "RabbitMQ"],
                    "description": [
                        "Designed REST APIs for a ride share service in a team of 3 peers, using Flask with Python for backend development.",
                        "Hosted the REST API across different Docker containers located across different EC2 Linux instances with an AWS Elastic Load Balancer, ensuring high availability and fault tolerance for the application.",
                        "Integrated RabbitMQ with the application to ensure synchronization in a distributed database service, allowing for efficient communication between different components of the system and ensuring data consistency."
                    ]
                },
                {
                    "title": "Accommate - Accommodation Posting Board",
                    "technologies": ["Python", "Flask", "NLP"],
                    "description": [
                        "Performed ETL and annotated posting text information for over 100+ postings to create a high-quality training dataset.",
                        "Developed pipelines using the NLTK libraries to perform named entity recognition with an accuracy of over 90%.",
                        "Moved the extracted information into MongoDB database and integrated it with a web application built using Flask-Python, resulting in an increased response time of 30% and improved data accessibility for over 1000 users."
                    ]
                },
                {
                    "title": "MLTool",
                    "technologies": ["Python", "Scikit-Learn", "Flask", "Vue"],
                    "description": [
                        "Implemented a RESTful API using Flask-Python to handle machine learning tasks, hosted on Pythonanywhere.",
                        "Utilized Vue.js to create a dynamic user interface, with features such as live model training progress updates.",
                        "Incorporated ML model selection and hyperparameter tuning capabilities to improve model accuracy and performance."
                    ]
                }
            ],
            "education":[
                {
                    "degree": "M.S",
                    "major": "Computer Science",
                    "university":"San Jose State University",
                    "from": "Aug 2022",
                    "to": "May 2024"
                },
                {
                    "degree": "B.Tech",
                    "major": "Computer Science",
                    "university":"PES University",
                    "from": "Aug 2017",
                    "to": "May 2021"
                }
            ],
            "technical_skills":{
                "languages": ["Python", "Java", "C", "HTML/CSS", "JavaScript", "SQL", "Go", "C#"],
                "developer_tools": ["Visual Studio", "Eclipse", "Google Cloud Platform", "AWS", "Jenkins"],
                "technologies_and_frameworks": ["Flask", "Spring", ".NET", "Angular.js", "React"]
            }
        }



import pymongo

# Replace these with your MongoDB connection details
mongo_uri = "mongodb+srv://msavinash1139:point1@cluster0.opvthne.mongodb.net/point1?retryWrites=true&w=majority"
collection_name = "user_profiles"
def getResumeData(search_email):
    # search_email = "msavinash1139@gmail.com"  # Replace with the email you want to search for

    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_uri)

    # Access the desired database and collection
    db = client.get_database()
    collection = db[collection_name]

    # Create a query to find the document with the specified email
    query = {"email_id": search_email}

    # Retrieve the document with the specified email
    result = collection.find_one(query)

    if result:
        print("Found document with email:", result)
    else:
        print("Document not found for email:", search_email)

    # Close the MongoDB connection
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
    # rankedProjects = request.json.get('data', [])
    # rankedProjects = json.loads(request.form.get('data'))
    email = "msavinash1139@gmail.com"
    print("Got email:", email)
    # jd = request.form.get('job_description')
    print("Got JD:", jd)
    # projects = ast.literal_eval(projects)
    resumeData = getResumeData(email)
    resumeData = convert_newlines_to_list(resumeData)
    projects = resumeData["project_experience"]
    for index in range(len(projects)):
        projects[index] = str(projects[index])
    ranks = rank(projects, jd)
    rankedProjects = [projects[i] for  i in ranks]
    # print(rankedProjects)
    # print(type(rankedProjects))
    # print(rankedProjects)
    resumeData["project_experience"] = rankedProjects
    for index in range(len(resumeData["project_experience"])):
        resumeData["project_experience"][index] = ast.literal_eval(resumeData["project_experience"][index])
    # print(resumeData["project_experience"])
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
    # projects = ast.literal_eval(projects)
    resumeData = getResumeData(email)
    resumeData = convert_newlines_to_list(resumeData)
    projects = resumeData["project_experience"]
    for index in range(len(projects)):
        projects[index] = str(projects[index])
    ranks = rank(projects, jd)
    rankedProjects = [projects[i] for  i in ranks]
    # print(rankedProjects)
    # print(type(rankedProjects))
    # print(rankedProjects)
    resumeData["project_experience"] = rankedProjects
    for index in range(len(resumeData["project_experience"])):
        resumeData["project_experience"][index] = ast.literal_eval(resumeData["project_experience"][index])
    # print(resumeData["project_experience"])
    pdf_bytes = generate_print_pdf(resumeData)

    # Serve the generated PDF as a response
    pdf_buffer.seek(0)
    response = Response(pdf_bytes, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
    print("Returning response")
    return response



if __name__ == "__main__":
    app.run()
    # getResumeData()
