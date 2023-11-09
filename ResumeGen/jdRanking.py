from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
import ast
from pprint import pprint

import pickle

# # Sample list of words
# word_list = None
# with open("allskills.txt") as f:
#     word_list = ast.literal_eval(f.read())

jd = None


def getSkillsInJD(jd):
    # print("JD")
    # print(jd)
    jd = jd.replace('/', ' ')
    jdtoke = word_tokenize(jd.lower())
    # print("JD Tokenized")
    # print(jdtoke)
    # skills = None
    # with open("linkedinskill", 'r', encoding='utf-8', errors='ignore') as f:
    #     skills = list(map(lambda x: x.strip().lower(), f.readlines()))
    # # split multiple word skills
    # allskills = set()
    # for skill in skills:
    #     allskills.update(skill.split())

    # # remove stop words using nltk
    # stop_words = set(stopwords.words('english'))
    # allskills = allskills.difference(stop_words)

    # pickle.dump(allskills, open("allskills.pkl", "wb"))

    allskills = pickle.load(open("allskills.pkl", "rb"))

    # pprint(skills)
    jd = " ".join(jdtoke)
    jd = " "+jd+" "
    jdSkills = []
    for skill in allskills:
        if " "+skill+" " in jd:
            jdSkills.append(skill)
    return jdSkills






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
    # print(project_descriptions)
    # Extract proper nouns from the job description
    jd_skills = getSkillsInJD(jd)
    # print("JD")
    # print(jd.lower())
    # print("JD Proper Nouns")
    # print("SKILLS")
    # print(jd_skills)
    for description in project_descriptions:
        description = description.lower()

        # Extract proper nouns from the project description
        project_tokens = word_tokenize(description)
        # print("Project Proper Nouns")
        # print(project_proper_nouns)

        # Create a dictionary for the modified project description
        modified_description = {
            "description": description,
            "tokens": project_tokens
        }

        modified_project_descriptions.append(modified_description)
    # print(modified_project_descriptions)

    # Create a dictionary to store proper noun overlap counts
    proper_noun_overlap_counts = {}

    for project in modified_project_descriptions:
        project_tokens = project['tokens']
        overlap_count = len(set(jd_skills) & set(project_tokens))
        proper_noun_overlap_counts[project['description']] = overlap_count

    tmp = list(proper_noun_overlap_counts.items())
    for i in range(len(tmp)):
        tmp[i] = (i, tmp[i])

    # Sort projects based on overlap count in descending order
    sorted_projects = sorted(tmp, key=lambda x: x[1][1], reverse=True)

    # Extract the ordered project descriptions
    order = [project[0] for project in sorted_projects]
    # print(jd_skills)
    return order, jd_skills





def rank_stash(project_descriptions, jd):
    modified_project_descriptions = []
    # print(project_descriptions)
    # Extract proper nouns from the job description
    jd_proper_nouns = extract_nouns(jd.lower())
    # print("JD")
    # print(jd.lower())
    # print("JD Proper Nouns")
    print(jd_proper_nouns)
    jdSkills = getSkillsInJD(jd)
    print("JD Skills")
    print(jdSkills)
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
    # print(modified_project_descriptions)

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