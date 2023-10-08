from flask import Flask, request, jsonify, render_template
import json
from pprint import pprint
import pymongo
import traceback
 
app = Flask(__name__)
 
from flask import request

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
def getResumeData():
    search_email = "msavinash1139@gmail.com"
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



@app.route('/')
def hello_world():
    data = getResumeData()
    # print(data)
    return render_template("toggleTest.html", data=data)
 


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