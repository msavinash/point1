

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
        resume_data_json = convert_to_json(data)


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
        print(e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()