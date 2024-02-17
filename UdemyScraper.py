import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

import requests
import wget
import zipfile
import os
class UdemyScraper:
        def downloadChromeDriver(self):
                # get the latest chrome driver version number
                url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
                response = requests.get(url)
                version_number = response.text

                # build the donwload url
                download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"

                # download the zip file using the url built above
                latest_driver_zip = wget.download(download_url,'chromedriver.zip')

                # extract the zip file
                with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
                        zip_ref.extractall('') # you can specify the destination folder path here
                # delete the zip file downloaded above
                os.remove(latest_driver_zip)
                
        def defineHeadlessHeaders(self):
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            self.options = webdriver.ChromeOptions()
            self.options.headless = True
            self.options.add_argument(f'user-agent={user_agent}')
            self.options.add_argument("--window-size=1920,1080")
            self.options.add_argument('--ignore-certificate-errors')
            self.options.add_argument('--allow-running-insecure-content')
            self.options.add_argument("--disable-extensions")
            self.options.add_argument("--proxy-server='direct://'")
            self.options.add_argument("--proxy-bypass-list=*")
            self.options.add_argument("--start-maximized")
            self.options.add_argument('--disable-gpu')
            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome(options=self.options)
        
        def getCourses(self, courseName):
                self.courseName = courseName.split(' ') 
                self.courseQuery = '+'.join(self.courseName)
                page_url = f"https://www.udemy.com/courses/search/?src=ukw&q={self.courseQuery}"
                self.driver.get(page_url)
                time.sleep(2)
                
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                self.driver.quit()
                
                courses = soup.find_all(attrs={'query' : courseName})
                course_list = []
                
                for course in courses:
                        course_url = '{0}{1}'.format('https://www.udemy.com', course.a['href'])
                        course_title = course.a.contents[0]                        
                        course_headline = course.select("[class*='course-headline']")[0].text
                        author = course.select("[class*='course-card-instructor']")[0].text
                        course_rating = course.select("[class*='rating-number']")[0].text
                        number_of_ratings = course.select("[class*='reviews-text']")[0].text[1:-1]
                        course_details = course.find_all('span', class_='course-card-details')
                        course_length = course_details[0].text
                        number_of_lectures = course_details[1].text
                        difficulty = course_details[2].text   

                        course_dict = {
                        'course_url' : course_url,
                        'course_title' : course_title,
                        'course_headline' : course_headline,
                        'author' : author,
                        'course_rating' : course_rating,
                        'number_of_ratings' : number_of_ratings,
                        'course_length'  : course_length,
                        'number_of_lectures' : number_of_lectures,
                        'difficulty' : difficulty,
                        }
                        course_list.append(course_dict)
                        break

                return {'courses' : course_list}
    

## TO DOWNLOAD THE LATEST CHROME DRIVER UNCOMMENT THE CODE BELOW ##
## AND DO THE FOLLOWING COMMAND IN TERMINAL 'python UdemyScraper.py' ##

# if __name__=='__main__':
#         scraper = UdemyScraper()
#         scraper.downloadChromeDriver()

# if __name__=='__main__':
#         scraper = UdemyScraper()
#         scraper.defineHeadlessHeaders()
#         courses = scraper.getCourses("python")
#         print(courses)