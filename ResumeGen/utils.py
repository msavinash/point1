
import base64
import datetime


def b64encodeFilter(s):
    return base64.b64encode(s).decode("utf-8")



def checkUserExists(search_email, db, COLLECTION_NAME, google):
    doc_ref = db.collection(COLLECTION_NAME).document(search_email)
    try:
        doc = doc_ref.get()
        if doc.exists:
            # print(f'Document data: {doc.to_dict()}')
            return True
        else:
            print('Document does not exist')
            return False
    except google.cloud.exceptions.NotFound:
        print('Document not found')
        return False
    


def getResumeData(search_email, db, COLLECTION_NAME, google):
    doc_ref = db.collection(COLLECTION_NAME).document(search_email)
    try:
        doc = doc_ref.get()
        if doc.exists:
            # print(f'Document data: {doc.to_dict()}')
            return doc.to_dict()
        else:
            print('Document does not exist')
            return False
    except google.cloud.exceptions.NotFound:
        print('Document not found')
        return False
    


def preprocessResumeData(data):
    # Helper function to extract data from the ImmutableMultiDict
    def extract_data(prefix, keys):
        extracted_data = {}
        for key in keys:
            full_key = f"{key}"
            if full_key in data:
                extracted_data[key] = data[full_key]
                
        return extracted_data

    # Helper function to extract list data from the ImmutableMultiDict
    def extractListData(prefix, keys):
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
                elif key == "description":
                    # print("FOUND DESCRIPTION")
                    # print(full_key)
                    if full_key in data:
                        description = data[full_key].splitlines()
                        item_data[key] = description
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
    resume_data["work_experience"] = extractListData("work_experience", ["title", "company", "from", "to", "description"])
    resume_data["project_experience"] = extractListData("project_experience", ["title", "technologies", "description"])
    resume_data["education"] = extractListData("education", ["degree", "major", "university", "from", "to"])
    resume_data["technical_skills"] = {
        "languages": data.getlist("technical_skills_languages[]"),
        "developer_tools": data.getlist("technical_skills_developer_tools[]"),
        "technologies_and_frameworks": data.getlist("technical_skills_technologies_and_frameworks[]")
    }
    return resume_data




def formatDate(date_str):
    try:
        from_date = date_str.split('-')
        year, month = int(from_date[0]), int(from_date[1])
        month_name = datetime.date(year, month, 1).strftime('%B')
        if len(month_name)>4:
            month_name = month_name[:3]
        return f"{month_name} {year}"
    except Exception as e:
        return date_str
    


def addToFirestore(data, db, COLLECTION_NAME):
    doc_ref = db.collection(COLLECTION_NAME).document(data["email_id"])
    doc_ref.set(data)


import requests

def make_google_api_request(access_token):
    # Define the API endpoint you want to access
    api_url = 'https://www.googleapis.com/oauth2/v2/userinfo'

    # Set up the headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the authenticated request
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # Successful response, parse the data
        data = response.json()
        print(data)
        return data
    else:
        print("ERROR!!")
        # Handle errors
        error_message = response.text
        print(f"The API responded with: {error_message}")
        return error_message
