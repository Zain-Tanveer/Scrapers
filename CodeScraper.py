import requests
from bs4 import BeautifulSoup

class CodeScraper:
    url = 'https://www.codecademy.com/search?query='
    
     # returns courses
    def getCourses(self, course):
        url = self.getUrl(course)
        soup = self.getPageSource(url)
                
        courses = soup.select("ol[class*='gamut-1yv0cql']")
        course_list = []

        # mapping course data
        for course in courses:
            course_title = course.h3.text
            difficulty = course.select_one("span[class*='1131uxx']").text
            description = course.select_one("span[class*='fo958g']").text.strip()

            course_url = '{0}{1}'.format('https://www.codecademy.com', course['href'])
            
            if course.select_one("span[class*='1wx7f9v']") == None:
                lessons = ''
            else:
                lessons = course.select_one("span[class*='1wx7f9v']").b.text
            
            if course.select_one("span[class*='19dl2hr']") == None:
                extras = ''
            else:
                extras = course.select_one("span[class*='19dl2hr']").text
            
            course_dict = {
                'course_url' : course_url,
                'course_title' : course_title,
                'difficulty' : difficulty,
                'description' : description,
                'lessons' : lessons,
                'extras' : extras
            }
            
            course_list.append(course_dict)
        
        return course_list
    
    # creates Url
    def getUrl(self, course):
        course = course.split(' ') 
        query = '%20'.join(course)
        url = self.url + query    
        return url
    
    # get data from page
    def getPageSource(self, url):
        # fetches complete page source 
        soup = BeautifulSoup(requests.get(url).text, 'lxml') 
        return soup
        
        
if __name__=='__main__':
    obj = CodeScraper()
    courses = obj.getCourses('java')
    print(courses)