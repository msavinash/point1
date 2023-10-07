

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template
from flask import Flask, request, jsonify
import json
from pprint import pprint
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.



from flask import request

def convert_to_json(data):
    # data = request.form

    # Extracting personal information
    personal_info = {
        "name": data.get("name"),
        "phone_number": data.get("phone_number"),
        "email_id": data.get("email_id"),
        "linkedin_link": data.get("linkedin_link"),
        "objective": data.get("objective")
    }

    # Extracting work experience
    work_experience_titles = data.getlist("work_experience_title[]")
    work_experience_companies = data.getlist("work_experience_company[]")
    work_experience_from_dates = data.getlist("work_experience_from[]")
    work_experience_to_dates = data.getlist("work_experience_to[]")
    work_experience_descriptions = data.getlist("work_experience_description[]")

    work_experiences = []
    for title, company, from_date, to_date, description in zip(work_experience_titles, work_experience_companies, work_experience_from_dates, work_experience_to_dates, work_experience_descriptions):
        work_experiences.append({
            "title": title,
            "company": company,
            "from": from_date,
            "to": to_date,
            "description": description.splitlines()  # Splitting description by lines to get a list
        })

    # Extracting project experience
    project_experience_titles = data.getlist("project_experience_title[]")
    project_experience_technologies = [tech.split(",") for tech in data.getlist("project_experience_technologies[]")]
    project_experience_descriptions = data.getlist("project_experience_description[]")

    project_experiences = []
    for title, technologies, description in zip(project_experience_titles, project_experience_technologies, project_experience_descriptions):
        project_experiences.append({
            "title": title,
            "technologies": technologies,
            "description": description.splitlines()
        })

    # Extracting education
    education_degrees = data.getlist("education_degree[]")
    education_majors = data.getlist("education_major[]")
    education_universities = data.getlist("education_university[]")
    education_from_dates = data.getlist("education_from[]")
    education_to_dates = data.getlist("education_to[]")

    educations = []
    for degree, major, university, from_date, to_date in zip(education_degrees, education_majors, education_universities, education_from_dates, education_to_dates):
        educations.append({
            "degree": degree,
            "major": major,
            "university": university,
            "from": from_date,
            "to": to_date
        })

    # Extracting technical skills
    technical_skills = {
        "languages": data.get("technical_skills_languages").split(","),
        "developer_tools": data.get("technical_skills_developer_tools").split(","),
        "technologies_and_frameworks": data.get("technical_skills_technologies_and_frameworks").split(",")
    }

    # Combining all data into the final structure
    resume_data = {
        "name": personal_info["name"],
        "phone_number": personal_info["phone_number"],
        "email_id": personal_info["email_id"],
        "linkedin_link": personal_info["linkedin_link"],
        "objective": personal_info["objective"],
        "work_experience": work_experiences,
        "project_experience": project_experiences,
        "education": educations,
        "technical_skills": technical_skills
    }

    return resume_data

# Call the function to get the JSON structure
# resume_data_json = convert_to_json()
# print(resume_data_json)










from collections import defaultdict

def convert_to_resume_data(data):
    resume_data = {}
    work_experience = defaultdict(dict)
    project_experience = defaultdict(dict)
    education = defaultdict(dict)
    technical_skills = defaultdict(list)

    for key, value in data.items():
        if "[" in key and "]" in key:
            section, index, subkey = key.split('[')[0], key.split('[')[1].split(']')[0], key.split('[')[2].split(']')[0]
            
            if section == "work_experience":
                if subkey not in work_experience[index]:
                    work_experience[index][subkey] = []
                work_experience[index][subkey].append(value)
            elif section == "project_experience":
                if subkey not in project_experience[index]:
                    project_experience[index][subkey] = []
                project_experience[index][subkey].append(value)
            elif section == "education":
                if subkey not in education[index]:
                    education[index][subkey] = []
                education[index][subkey].append(value)
            elif section == "technical_skills":
                technical_skills[subkey].append(value)
        else:
            resume_data[key] = value

    print("!"*100)
    print(work_experience)

    resume_data["work_experience"] = [dict(val) for val in work_experience.values()]
    resume_data["project_experience"] = [dict(val) for val in project_experience.values()]
    resume_data["education"] = [dict(val) for val in education.values()]
    resume_data["technical_skills"] = dict(technical_skills)

    return resume_data





from werkzeug.datastructures import ImmutableMultiDict

def convert_to_resume_data2(data):
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
    print("ON HERE!!!!!!!!!!!!!!!!!!")
    pprint(resume_data)
    resume_data["work_experience"] = extract_list_data("work_experience", ["title", "company", "from", "to", "description"])
    resume_data["project_experience"] = extract_list_data("project_experience", ["title", "technologies", "description"])
    resume_data["education"] = extract_list_data("education", ["degree", "major", "university", "from", "to"])
    resume_data["technical_skills"] = {
        "languages": data.getlist("technical_skills_languages[]"),
        "developer_tools": data.getlist("technical_skills_developer_tools[]"),
        "technologies_and_frameworks": data.getlist("technical_skills_technologies_and_frameworks[]")
    }

    return resume_data


# # Example usage
# data = ImmutableMultiDict([...])  # Your data here
# resume_data = convert_to_resume_data(data)
# print(resume_data)





import pymongo

# Replace these with your MongoDB connection details
mongo_uri = "mongodb+srv://msavinash1139:point1@cluster0.opvthne.mongodb.net/point1?retryWrites=true&w=majority"
collection_name = "user_profiles"


def sendToMongo(data):
    # JSON data to be stored
    # resume_data_json = convert_to_json(data)

    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_uri)

    # Access the desired database and collection
    db = client.get_database()
    collection = db[collection_name]

    # Insert the JSON data into the collection
    insert_result = collection.insert_one(data)

    # Check if the insertion was successful
    if insert_result.acknowledged:
        print("Data inserted successfully with ObjectId:", insert_result.inserted_id)
    else:
        print("Data insertion failed")

    # Close the MongoDB connection
    client.close()

import traceback

@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return render_template("test.html")
    # return render_template("bubbleTest.html")
 


@app.route('/profile-data', methods=['POST'])
def store_user_data():
    try:
        # Get the form data from the request
        data = request.form
        print(data)
        resume_data_json = convert_to_resume_data2(data)
        print("BEFORE SENDING")
        pprint(resume_data_json)
        sendToMongo(resume_data_json)

        pprint(resume_data_json)
        # # Convert the form data to a JSON object
        # user_data = {
        #     'name': data['name'],
        #     'email': data['email']
        #     # Add more fields as needed
        # }

        # # Store the user data as a JSON object in a file
        # with open('user_data.json', 'w') as json_file:
        #     json.dump(user_data, json_file)
        print("done!!!")
        return jsonify({'message': 'User data stored successfully'})

    except Exception as e:
        print("ERROR!!")
        print("Exception Type:", type(e).__name__)  # Print the type of exception
        print("Exception Message:", str(e))  # Print the error message
        print("Line Number:", sys.exc_info()[-1].tb_lineno)  # Print the line number where the exception occurred
        traceback.print_exc()  # Print the full traceback information
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()