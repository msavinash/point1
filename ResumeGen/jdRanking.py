from nltk.tokenize import word_tokenize
import ast
from pprint import pprint

# Sample list of words
word_list = None
with open("allskills.txt") as f:
    word_list = ast.literal_eval(f.read())


# List of project descriptions
project_descriptions = [
    "".join(["<b>Hangman</b> - http://github.com/nickdepinet/hangman<br/>",
    "Implemented a command line hangman game engine and an artificial intelligence player in python.",
    "The AI uses letter frequencies from the English dictionary and additionally word frequencies from the ",
    "Google corpus make intelligent guesses as to the next letter."]),
    "".join(["<b>g()(\'al\')</b> - http://github.com/eatnumber1/goal<br/>",
    "Completed the first Python solution to the g()(\'al\') programming challenge. ",
    "The \"goal\" of the g()(\'al\') challenge is to enable the calling of g()(\'al\') in the source of the ",
    "language of choice with n ()'s, and to be returned the string \"goal\" with the appropriate number of \"o\"s."]),
    "".join(["<b>DrinkPi</b> - http://github.com/jeid64/drinkpi/<br/>",
    "Worked with a partner to replace a failing component in the Computer Science House drink machines. ",
    "The software controlling the machines was previously written in Java and running on Dallas TINI microcomputers. ",
    "These TINI's were failing and were no longer produced, so we re-wrote the software in Python to run on a ",
    "Raspberry Pi. The software talks to the drink server over sockets using the SUNDAY protocol, and to the drink ",
    "machine hardware using the 1-Wire protocol and a USB 1-Wire bus master."]),
    "".join(["<b>TempMon</b> - http://github.com/nickdepinet/tempmon/<br/>",
    "Implemented a temperature monitoring system for a server room using a Raspberry Pi. ",
    "The system monitors temperature using a series of DSB1820 temperature sensors. ",
    "When the temperature exceeds a set limit, an email notification is sent. ",
    "The software, including temperature reading, threading, and email notification is written in Python."]),
    "".join(["<b>Nexus Q Development</b> - http://github.com/nickdepinet/android_device_google_steelhead<br/>"]),
    "".join(["<b>CryptoGuard</b> - https://github.com/yourusername/cryptoguard<br/>",
    "Developed a secure messaging application using end-to-end encryption techniques. Implemented cryptographic algorithms such as AES-256 and RSA for message encryption and secure key exchange. The application ensures the privacy and confidentiality of user communications, making it resistant to eavesdropping and unauthorized access."])
]



jd = None

with open("sampleJD.txt", 'r', encoding='utf-8', errors='ignore') as f:
    jd = f.read()



def rank1(project_descriptions, jd):
    # Initialize a list to store the modified project descriptions
    modified_project_descriptions = []

    # Iterate through project descriptions and extract skills
    for description in project_descriptions:
        description = description.lower() # Convert text to lowercase for case-insensitive matching

        # Extract skills that are in the word_list
        present_skills = [word for word in word_list if word in description]

        # Create a dictionary for the modified project description
        modified_description = {
            "description": description,
            "skills": present_skills
        }

        # Append the modified description to the list
        modified_project_descriptions.append(modified_description)

    jd = jd.lower()
    given_skills = [word for word in word_list if word in jd]


    # Create a dictionary to store skill overlap counts
    skill_overlap_counts = {}

    # Iterate through project data and count skill overlaps
    for project in modified_project_descriptions:
        project_skills = project['skills']
        overlap_count = len(set(given_skills) & set(project_skills))
        skill_overlap_counts[project['description']] = overlap_count

    tmp = list(skill_overlap_counts.items())
    for i in range(len(tmp)):
        tmp[i] = (i, tmp[i])
    # Sort projects based on overlap count in descending order
    sorted_projects = sorted(tmp, key=lambda x: x[1][1], reverse=True)

    # Extract the ordered project descriptions
    # ordered_descriptions = [project[0] for project in sorted_projects]
    order = [project[0] for project in sorted_projects]

    # Print the ordered project descriptions
    # for index, description in enumerate(ordered_descriptions):
    #     print(f"{index + 1}. {description} (Overlap Count: {skill_overlap_counts[description]})")
    return order





import nltk
from nltk import word_tokenize, pos_tag
import re

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_nouns(text):
    """Extract all nouns from a given text."""
    
    # Remove special characters using regex
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    tokens = word_tokenize(text)
    # print("Tokens")
    # print(tokens)
    nouns = [word for word, pos in pos_tag(tokens) if pos in ['NN', 'NNS', 'NNP', 'NNPS']]
    return nouns

def rank(project_descriptions, jd):
    modified_project_descriptions = []

    # Extract proper nouns from the job description
    jd_proper_nouns = extract_nouns(jd.lower())
    # print("JD")
    # print(jd.lower())
    # print("JD Proper Nouns")
    # print(jd_proper_nouns)
    for description in project_descriptions:
        description = description.lower()

        # Extract proper nouns from the project description
        project_proper_nouns = extract_nouns(description)
        # print("Project Proper Nouns")
        # print(project_proper_nouns)

        # Create a dictionary for the modified project description
        modified_description = {
            "description": description,
            "proper_nouns": project_proper_nouns
        }

        modified_project_descriptions.append(modified_description)

    # Create a dictionary to store proper noun overlap counts
    proper_noun_overlap_counts = {}

    for project in modified_project_descriptions:
        project_proper_nouns = project['proper_nouns']
        overlap_count = len(set(jd_proper_nouns) & set(project_proper_nouns))
        proper_noun_overlap_counts[project['description']] = overlap_count

    tmp = list(proper_noun_overlap_counts.items())
    for i in range(len(tmp)):
        tmp[i] = (i, tmp[i])

    # Sort projects based on overlap count in descending order
    sorted_projects = sorted(tmp, key=lambda x: x[1][1], reverse=True)

    # Extract the ordered project descriptions
    order = [project[0] for project in sorted_projects]

    return order, jd_proper_nouns


if __name__=="__main__":
    ans = rank(project_descriptions, jd)
    pprint(ans)