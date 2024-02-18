# Scrapers

It is a backend server developed in [python][python]. It was part of my final year project. The main focus of this project was to create web scrapers for scraping data from [rozee.pk][rozeepk] and [CodeAcademy][codeacademy]. You can hit the APIs in main.py or individually run each scraper file to see their working. Jobs were scraped from [rozee.pk][rozeepk] and courses were scraped from [CodeAcademy][codeacademy].

While working on this project I also implement a scraper for [Udemy][udemy] but since udemy has way too many security implementations it was not possible with [BeautifulSoup4][beautifulsoup] so I had to use [Selenium][selenium] web driver. The UdemyScraper uses a method known as headless scraping but it is very slow and was not optimal for my final year project. So I decided to scrap courses from [CodeAcademy][codeacademy] instead.

**NOTE**: The rozee scraper will only target IT jobs available on rozee.pk.

**NOTE**: These scrapers were written in november, 2022. If the websites that these scrapers target have made changes in their HTML structure, then the scrapers will break.

## Installation

Before running the code, you need to install the latest version of python. It is better if you watch a guide on how to install python and run python code is VS Code.

Afterward you need to run the following commands, these are all of the libraries used in this project.

```sh
pip install requests
pip install beautifulsoup4
pip install selenium
pip install lxml
pip install fastapi
pip install uvicorn
```

To run the server on a local environment do

```
uvicorn main:app --reload
```

# How it works

The rozee scraper targets a variable known as 'apResp' in a script tag. This 'apResp' variable has all of the necessary information display on the page.
The codeacademy scraper targets html elements.
The udemy scraper uses selenium to load the page so that all the data that is displayed using javascript can be loaded. It then gets the page source and closes the web browser. Just like the codeacademy scraper, it targets the htmls element to scrap relevant data.

## License

NONE

[//]: # "These are reference links used in the body of this note and get stripped out when the markdown processor does its job."
[angular]: https://angular.io/
[nodejs]: https://nodejs.org/en
[python]: https://www.python.org/
[express]: https://expressjs.com/
[multer]: https://www.npmjs.com/package/multer
[cyclic]: https://www.cyclic.sh/
[mongodb]: https://www.mongodb.com/
[railway]: https://railway.app/
[rozeepk]: https://www.rozee.pk/
[codeacademy]: https://www.codecademy.com/
[udemy]: https://www.udemy.com/
[selenium]: https://www.selenium.dev/documentation/webdriver/
[beautifulsoup]: https://beautiful-soup-4.readthedocs.io/en/latest/
[scrapers]: https://github.com/Zain-Tanveer/Scrapers
[uploadfile]: https://github.com/Zain-Tanveer/upload-file-api
[linkapi]: https://github.com/Zain-Tanveer/Link-API
[cloudinary]: https://cloudinary.com/
[cloudinarylibrary]: https://www.npmjs.com/package/cloudinary
[careerhub]: https://github.com/Zain-Tanveer/CareerHub-Backend
