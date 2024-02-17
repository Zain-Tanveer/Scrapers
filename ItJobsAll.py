import requests
import json
import csv
from bs4 import BeautifulSoup

class ITJobs:
    url = 'https://www.rozee.pk/job/jsearch/q/all/fin/1'

    def getData(self, url):
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'lxml')
        scriptAP = soup.find_all('script')[39].text.strip().split('apResp = ')[1]
        script = scriptAP.split('var setTooltip')[0].strip()[:-1]
        data = json.loads(script)
        return data

    def getNextPage(self, data):
        page = data['response']['pagination']['list'][-1]
        if page['lang'] == 'Next':
            page_no = page['fpn']
            newUrl = f"{self.url}/fpn/{page_no}"
            return newUrl
        else:
            return
    
    def getAllJobs(self):
        self.jobsList = []
        self.job_count = 0
        self.page_no = 0
        while True:
            data = self.getData(self.url)
            self.page_no += 1  
            print(f'''You're on page {self.page_no}!''')

            for job in data['response']['jobs']['basic']:
            
                self.job_count += 1
                
                # job data mapping
                job_id = job['jid']
                title = job['title']
                company = job['company']
                job_type = job['type']
                description = job['description']
                created_at = job['created']
                city = job['city']
                job_expiry_date = job['applyBy']
                permaLink = 'https://www.rozee.pk/' + job['rozeePermaLink']
                
                if job['experience_text'] == "":
                    experience = "Fresh"
                else:
                    experience = job['experience_text']

                
                # skills, min_salary and max_salary are optional on rozee.pk
                if not 'skills' in job.keys():
                    skills = ''
                else:
                    skills = job['skills']
                    
                if not 'salaryN_exact' in job.keys():
                    min_salary = 0
                else:
                    min_salary = job['salaryN_exact']
                
                if not 'salaryT_exact' in job.keys():
                    max_salary = 0
                else:
                    max_salary = job['salaryT_exact']
                
                # creates a job dictionary
                job_dict = {
                    'job_id' : job_id,
                    'title' : title,
                    'company' : company,
                    'job_type' : job_type,
                    'skills' : skills,
                    'experience' : experience,
                    'description': description,
                    'created_at': created_at,
                    'min_salary' : min_salary,
                    'max_salary' : max_salary,
                    'city': city,
                    'total': data['response']['numFound'],
                    'msg': data['response']['pagination']['msg'],
                    'permaLink': permaLink,
                    'job_expiry_date': job_expiry_date,
                    'status_code': data['code']
                }
                # appends the dictionary to joblist array
                self.jobsList.append(job_dict)
                        
            self.url = self.getNextPage(data)
            if not self.url:
                print('No more pages left.')
                self.url = "https://www.rozee.pk/job/jsearch/q/all/fin/1"
                break
                
            print('Fetching next page. Please wait a few seconds...\n')
        
        print(f'\nTotal Jobs : {self.job_count}')
        return self.jobsList
   
## TO POPULATE THE 'all_jobs.json' FILE IN THE 'json' FOLDER UNCOMMENT THE ##
## CODE BELOW AND DO THE FOLLOWING COMMAND IN TERMINAL 'python ItAllJobs.py' ##
    
# if __name__ == '__main__':
#     fAll = ITJobs()
    
#     with open('json/all_jobs.json', 'w') as f:
#         json.dump(fAll.getAllJobs(), f, indent = 2)