import requests
import json
from bs4 import BeautifulSoup
import random
import math 

class RozeeScraper:    
    # Function to return single page job information
    def getSinglePageJobsData(self, input, page_no):
        self.page_no = (int(page_no))
        # sets url
        if input == '':
            self.url = f'https://www.rozee.pk/job/jsearch/q/all/fin/1/fpn/{self.page_no}'
        else:    
            self.userInput = input.split(' ') 
            self.jobQuery = '%20'.join(self.userInput)
            self.url = f'https://www.rozee.pk/job/jsearch/q/{self.jobQuery}/fin/1/fpn/{self.page_no}' 
        
        # fetches page and filters out irrelevent information
        soup = BeautifulSoup(requests.get(self.url).text, 'lxml') 
        scriptAP = soup.find_all('script')[39].text.strip().split('apResp = ')[1]
        script = scriptAP.split('var setTooltip')[0].strip()[:-1] 
        data = json.loads(script) 
        
        # if data not found
        if data['code'] != 200:
            return [ {
                'keyword' : input,
                'job_id' : '',
                'title' : '',
                'company' : '',
                'job_type' : '',
                'skills' : [],
                'experience' : '',
                'description': '',
                'created_at': '',
                'min_salary' : 0,
                'max_salary' : 0,
                'city': '',
                'total': 0,
                'msg': '',
                'permaLink': '',
                'job_expiry_date': '',
                'status_code': data['code']
            } ]
        
        self.jobsList = []
        self.job_count = 0
        
        self.pages = data['response']['pagination']['list']
                        
        # Loop runs for each job present on the page (20 jobs per page)
        for job in data['response']['jobs']['basic']:
            
            self.job_count += 1
            
            # job data maping
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
                'keyword' : input,
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
                'city':city,
                'total': data['response']['numFound'],
                'msg': data['response']['pagination']['msg'],
                'permaLink': permaLink,
                'job_expiry_date': job_expiry_date,
                'status_code': data['code']
            }
            
            # appends the dictionary to joblist array
            self.jobsList.append(job_dict)
              
        return self.jobsList
           
    # Function to get pages
    def getPagination(self, input, page_no):
        self.page_no = (int(page_no))
        # sets url
        if input == '':
            self.url = f'https://www.rozee.pk/job/jsearch/q/all/fin/1/fpn/{self.page_no}'
        else:    
            self.userInput = input.split(' ') 
            self.jobQuery = '%20'.join(self.userInput)
            self.url = f'https://www.rozee.pk/job/jsearch/q/{self.jobQuery}/fin/1/fpn/{self.page_no}' 
        
        # fetches page and filters out irrelevent information
        soup = BeautifulSoup(requests.get(self.url).text, 'lxml') 
        scriptAP = soup.find_all('script')[39].text.strip().split('apResp = ')[1]
        script = scriptAP.split('var setTooltip')[0].strip()[:-1] 
        data = json.loads(script) 
        
        # if data not found
        if data['code'] != 200:
            return {'Error' : '404 Not Found.', 'Status Code': data['code']}
        
        pagination = data['response']['pagination']['list']
    
        return pagination
        
    # Function to get job detail of a single job
    def getJobDetail(self, jobId):
        jobDetailUrl = 'https://www.rozee.pk/services/job/jobDetail'
        payload = {'jid' : jobId}
        
        response = requests.request("POST", jobDetailUrl, data=payload)
        jobdetail = json.loads(response.text)

        if jobdetail['code'] != 200:
            return {'Error' : 'Data not found.', 'Status Code' : jobdetail['code']}

        title = jobdetail['subDetail']['title']
        displayDate = jobdetail['subDetail']['displayDate']
        applyBy =  jobdetail['subDetail']['applyBy']
        
        if jobdetail['subDetail']['req_experience'] == "":
            experience = "Fresh"
        else:
             experience = jobdetail['subDetail']['req_experience']
        
        degreeTitle = jobdetail['subDetail']['degreeTitle']
        education = jobdetail['subDetail']['education']
        min_salary = jobdetail['subDetail']['salary_range_from']
        max_salary = jobdetail['subDetail']['salary_range_to']
        salary_duration = jobdetail['subDetail']['salary_duration']
        
        if min_salary == "0" or min_salary == "":
            min_salary = "Flexible"
        
        skills = []
        
        for skill in jobdetail['subDetail']['skillListing']:
            skills.append(skill['skill'])
            
        soup = BeautifulSoup(jobdetail['subDetail']['type_exact'], 'lxml')
        
        job_type = soup.get_text()    
        industryName = jobdetail['subDetail']['industryName']
        job_shift = jobdetail['subDetail']['jbTypeDetail']
        careerLevel = jobdetail['subDetail']['careerLevel']
        jobCatagory = jobdetail['subDetail']['displayCatName'] 
        description = jobdetail['subDetail']['description']
        permaLink = 'https://www.rozee.pk/' + jobdetail['subDetail']['rozeePermaLink']
        
        detail_dict = {
            'title' : title,
            'displayDate' : displayDate,
            'applyBy' : applyBy,
            'experience' : experience,
            'degreeTitle' : degreeTitle,
            'education' : education,
            'min_salary' : min_salary,
            'max_salary' : max_salary,
            'salary_duration' : salary_duration,
            'skills' : skills,
            'industryName' : industryName,
            'job_shift' : job_shift,
            'job_type' : job_type,
            'careerLevel' : careerLevel,
            'jobCatagory' : jobCatagory,
            'permaLink': permaLink,
            'description' : description,
        }
        
        return detail_dict
    
    # Function to fetch chart details for skills
    def getSkillChartDetails(self):
        chartUrl = "https://www.rozee.pk/job/jsearch/q/all/fin/1"
        soup = BeautifulSoup(requests.get(chartUrl).text, 'lxml') 
        scriptAP = soup.find_all('script')[39].text.strip().split('apResp = ')[1]
        script = scriptAP.split('var setTooltip')[0].strip()[:-1] 
        data = json.loads(script) 
        
        # if data not found
        if data['code'] != 200:
            return {'Error' : '404 Not Found.', 'Status Code': data['code']}
        
        facets = data['response']['facets']
    
        labels = []
        data = []
    
        chartInfo = {}
        chartData = []
        
        facet = facets[5]['data']

        for index in range(0, 8):
            if ('Communication' in facet[index]['label']):
                continue
            
            chartInfo = {
                'label' : facet[index]['label'].split(' '),
                'data' : facet[index]['count']
            }
            
            chartData.append(chartInfo)
            
        random.shuffle(chartData)
            
        for info in chartData:
            labels.append(info['label'])    
            data.append(info['data'])
        
        return {
            'labels' : labels,
            'data' : data
        }
        
    # Function to get chart details for field
    def getFieldChartDetails(self):
        chartUrl = "https://www.rozee.pk/job/jsearch/q/all/fin/1"
        soup = BeautifulSoup(requests.get(chartUrl).text, 'lxml') 
        scriptAP = soup.find_all('script')[39].text.strip().split('apResp = ')[1]
        script = scriptAP.split('var setTooltip')[0].strip()[:-1] 
        data = json.loads(script) 
        
        # if data not found
        if data['code'] != 200:
            return {'Error' : '404 Not Found.', 'Status Code': data['code']}
        
        facets = data['response']['facets']
    
        labels = []
        data = []
    
        chartInfo = {}
        chartData = []
        
        facet = facets[0]['data']

        for index in range(0, 6):
            chartInfo = {
                'label' : facet[index]['label'].split(' '),
                'data' : facet[index]['count']
            }
            
            chartData.append(chartInfo)
            
        random.shuffle(chartData)
            
        for info in chartData:
            labels.append(info['label'])    
            data.append(info['data'])
        
        return {
            'labels' : labels,
            'data' : data
        }

    def getPageMeta(self, input):
        self.page_no = 0
        # sets url
        if input == '':
            self.url = f'https://www.rozee.pk/job/jsearch/q/all/fin/1/fpn/{self.page_no}'
        else:    
            self.userInput = input.split(' ') 
            self.jobQuery = '%20'.join(self.userInput)
            self.url = f'https://www.rozee.pk/job/jsearch/q/{self.jobQuery}/fin/1/fpn/{self.page_no}' 
        
        # fetches page and filters out irrelevent information
        soup = BeautifulSoup(requests.get(self.url).text, 'lxml') 
        scriptAP = soup.find_all('script')[39].text.strip().split('apResp = ')[1]
        script = scriptAP.split('var setTooltip')[0].strip()[:-1] 
        data = json.loads(script)
        
        final_array = []
        test = []
        
        for facet in data['response']['facets']:
            if not 'id' in facet['data'][0].keys():
                continue
            nested_array = []
            
            for facet_data in facet['data']:
                fkey = facet['meta']['fkey']
                label = facet_data['label']
                id = facet_data['id']
                count = str(facet_data['count'])
                
                # if id == fkeyid:
                #     isChecked = 'checked'
                # else:
                #     isChecked = ''
                
                facet_dict = {
                    'fkey' : fkey,
                    'label' : label,
                    'id' : id,
                    'count' : count,
                    # 'checked': isChecked
                }
                
                nested_array.append(facet_dict)
            
            test.append({'title': facet['meta']['blkTitle'],'data' : nested_array})
        return test
    
    def getFilteredJobsData(self, input, page_no, fkey_id, fkey):
            self.page_no = (int(page_no))
            # sets url
            if input == '':
                self.url = f'https://www.rozee.pk/job/jsearch/q/all/fin/1/fpn/{self.page_no}/{fkey}/{fkey_id}'
            else:    
                self.userInput = input.split(' ') 
                self.jobQuery = '%20'.join(self.userInput)
                self.url = f'https://www.rozee.pk/job/jsearch/q/{self.jobQuery}/fin/1/fpn/{self.page_no}/{fkey}/{fkey_id}' 
            
            # fetches page and filters out irrelevent information
            soup = BeautifulSoup(requests.get(self.url).text, 'lxml') 
            scriptAP = soup.find_all('script')[39].text.strip().split('apResp = ')[1]
            script = scriptAP.split('var setTooltip')[0].strip()[:-1] 
            data = json.loads(script) 
            
            # if data not found
            if data['code'] != 200:
                return [ {
                    'keyword' : input,
                    'job_id' : '',
                    'title' : '',
                    'company' : '',
                    'job_type' : '',
                    'skills' : [],
                    'experience' : '',
                    'description': '',
                    'created_at': '',
                    'min_salary' : 0,
                    'max_salary' : 0,
                    'city': '',
                    'total': 0,
                    'msg': '',
                    'permaLink': '',
                    'job_expiry_date': '',
                    'status_code': data['code']
                } ]
            
            self.jobsList = []
            self.job_count = 0
            
            self.pages = data['response']['pagination']['list']
                            
            # Loop runs for each job present on the page (20 jobs per page)
            for job in data['response']['jobs']['basic']:
                
                self.job_count += 1
                
                # job data maping
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
                    'keyword' : input,
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
                    'city':city,
                    'total': data['response']['numFound'],
                    'msg': data['response']['pagination']['msg'],
                    'permaLink': permaLink,
                    'job_expiry_date': job_expiry_date,
                    'status_code': data['code']
                }
                
                # appends the dictionary to joblist array
                self.jobsList.append(job_dict)
                
            return self.jobsList
        
    def getFilteredPagination(self, input, page_no, fkey_id, fkey):
            self.page_no = (int(page_no))
            # sets url
            if input == '':
                self.url = f'https://www.rozee.pk/job/jsearch/q/all/fin/1/fpn/{self.page_no}/{fkey}/{fkey_id}'
            else:    
                self.userInput = input.split(' ') 
                self.jobQuery = '%20'.join(self.userInput)
                self.url = f'https://www.rozee.pk/job/jsearch/q/{self.jobQuery}/fin/1/fpn/{self.page_no}/{fkey}/{fkey_id}' 
            
            # fetches page and filters out irrelevent information
            soup = BeautifulSoup(requests.get(self.url).text, 'lxml') 
            scriptAP = soup.find_all('script')[39].text.strip().split('apResp = ')[1]
            script = scriptAP.split('var setTooltip')[0].strip()[:-1] 
            data = json.loads(script) 
            
            # if data not found
            if data['code'] != 200:
                return {'Error' : '404 Not Found.', 'Status Code': data['code']}
            
            pagination = data['response']['pagination']['list']
        
            return pagination

if __name__ == '__main__':
    scraper = RozeeScraper()
    # scraper.getSinglePageJobsData('', 0)
    # scraper.getJobDetail(1464917)

## ---------- Put this code before return statement in getSinglePageJobsData to update page_information.json file ------------ ##
# with open('json/page_information.json', 'w') as f:
#     json.dump(data, f, indent = 2)

## ---------- Put this code before return statement in getSinglePageJobsData to update jobs_data.json file ------------ ##
# with open('json/jobs_data.json', 'w') as f:
#     json.dump({'User Input' : input, 'pages' : len(self.pages) - 2,'jobs' : self.jobsList, 'Status Code' : data['code']}, f, indent = 2)

## ---------- Put this code before return statement in getJobDetail to update jobdetail.json file ------------ ##
# with open('json/jobdetail.json', 'w') as f:
#     json.dump(jobdetail, f, indent = 2)