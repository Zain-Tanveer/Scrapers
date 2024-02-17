from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from keywords import skill_keywords

class NLPSkillFinder:

    # process the job description.
    def prepare_job_desc(self, desc):
        # tokenize description.
        tokens = word_tokenize(desc)

        # Parts of speech (POS) tag tokens.
        token_tag = pos_tag(tokens)

        # Only include some of the POS tags.
        include_tags = ['VBN', 'VBD', 'JJ', 'JJS', 'JJR', 'CD', 'NN', 'NNS', 'NNP', 'NNPS']
        filtered_tokens = [tok.lower() for tok, tag in token_tag if tag in include_tags]

        return set(filtered_tokens)

    def compare_job_skills(self, data):
        skills_skill_list = []
        return_skills = []

        skill_lowercase = [skill.lower() for skill in skill_keywords]
        skill_keywords_set = set([tok for tok in skill_lowercase])

        match_skills = self.prepare_job_desc(data)
        skills_desc_set = match_skills

        # check if the keywords are in the job description. Look for exact match by token.
        skills_skill_words = skill_keywords_set.intersection(skills_desc_set)

        # check if longer keywords (more than one word) are in the job description. Match by substring.
        # label the job descriptions without any skill keywords.
        if len(skills_skill_words) == 0:
            skills_skill_list.append('nothing specified')

        skills_skill_list += list(skills_skill_words)
        return_skills += list(skills_skill_list)

        return return_skills

# if __name__=='__main__':
#     nlp = NLPSkillFinder()
#     print(nlp.compare_job_skills('Hi my name is zain. I am a web developer.'))
#     print(nlp.compare_job_skills("node js, express, mysql, python"))
#     print(nlp.compare_job_skills("Hello everyone, My name is Zain. I'm studying at the University of Lahore for a Bachelors degree in Computer Science. I have ample experience in C++ programming and strong concepts of OOP. I recently fell in love with web development and I'm aspiring to be a full stack web developer. I have worked on multiple projects through-out my degree mainly involving C++ and recently using HTML, CSS, JS, and PHP or LARAVEL."))
#     print(nlp.compare_job_skills("Experienced Software Engineer with a demonstrated history of Learning industry-standard skills. Skilled in Javascript, Node.js, Typescript, GraphQl, PHP, Laravel and Angular. Strong engineering professional with studies focused on Software Engineering."))