from nltk.tokenize import word_tokenize
import ast
from pprint import pprint

# Sample list of words
word_list = None
with open("allskills.txt") as f:
    word_list = ast.literal_eval(f.read())

jd = None


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