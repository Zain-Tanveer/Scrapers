# pip install requests
# pip install beautifulsoup4
# pip install selenium
# pip install lxml
# pip install nltk
# pip install wget

# pip install fastapi
# pip install uvicorn (for live server)

from ItJobsAll import ITJobs
from fastapi import FastAPI, Request
from NLPSkillFinder import NLPSkillFinder
from RozeeScraper import RozeeScraper
from CodeScraper import CodeScraper
from UdemyScraper import UdemyScraper

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs = RozeeScraper()
courses = CodeScraper()
nlp = NLPSkillFinder()
itJobs = ITJobs()

@app.get("/api/jobs") # we will also pass page_no= as query params from frontend
async def getJobsData(userInput, page_no):
    return jobs.getSinglePageJobsData(userInput, page_no)

@app.get("/api/filteredJobs") # we will also pass page_no= as query params from frontend
async def getJobsData(userInput, page_no, fkey_id, fkey):
    return jobs.getFilteredJobsData(userInput, page_no, fkey_id, fkey)

@app.get("/api/pagemeta")  # we will also pass page_no= as query params from frontend
async def getJobsData(userInput):
    return jobs.getPageMeta(userInput)

@app.get("/api/jobdetail")
async def getJobDetail(jobId): # we will need to pass jobId from frontend
    return jobs.getJobDetail(jobId)

@app.get("/api/pagination")
async def getJobDetail(userInput, page_no): # we will need to pass jobId and keyword from frontend
    return jobs.getPagination(userInput, page_no)

@app.get("/api/filteredPagination")
async def getJobDetail(userInput, page_no, fkey_id, fkey): # we will need to pass jobId and keyword from frontend
    return jobs.getFilteredPagination(userInput, page_no, fkey_id, fkey)

@app.get('/api/chartdetails/skills')
async def getChartsData():
    return jobs.getSkillChartDetails()

@app.get('/api/chartdetails/fields')
async def getChartsData():
    return jobs.getFieldChartDetails()

@app.get("/api/courses")
async def getCourses(course):
    return courses.getCourses(course)

@app.post("/api/findKeywords")
async def getKeywords(request: Request):
    req = await request.json()
    return nlp.compare_job_skills(req['data'])

@app.get("/api/getAllJobs")
async def getAllJobs():
    return itJobs.getAllJobs()

# uvicorn main:app --reload (to open up live server)