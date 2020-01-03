from selenium import webdriver
from bs4 import BeautifulSoup  # bs4 is the module and BeautifulSoup is the class
import time
import webbrowser
import os
# functions that allow us to interact and get OS information and even control processes up to a limit.
import lxml
# lxml is a Python library which allows for easy handling of XML and HTML, can also be used for web scraping.
# Beautiful Soup relies on a parser, the default is lxml
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#specifying-the-parser-to-use

pages =['ConsultNexus']  # list of pages to scrape
if not os.path.exists("FacebookPages"):
    os.mkdir("FacebookPages")

for page in pages:
    driver = webdriver.Chrome(r"C:/Users/iiitb/Desktop/zense/chromedriver.exe")  # making an instance of ChromeDriver
    driver.get('https://www.facebook.com/' + page + '/posts')

    # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
    # try replacing with above code
    # Ways to scroll down a page : by pixel, based on element, till the end
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")  # get total scroll height
    counter = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down to the bottom
        # methods of Javascript but driver object allows us to use in Python
        time.sleep(SCROLL_PAUSE_TIME)  # wait for page to load
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break;

        last_height = new_height

    html = driver.page_source  # get the HTML source code
    soup = BeautifulSoup(html, "lxml")  # creating an object called soup of the BeautifulSoup class
    # html.parser can also be used as parser

    f = open('./FacebookPages/' + page + ".html", 'w', encoding="utf-8")
    f.write("<html>\n<title> " + page + " </title>\n")
    f.write("<head><link rel='stylesheet' href='Check.css'></head><body>")

    count = 1  # represents number of posts
    posts = soup.findAll("div", {"class": "_5pcr userContentWrapper"})
    # traverses the tree and finds all the Tag and NavigableString objects that match the criteria we give
    # division or section in a HTML page
    # findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)
    # findAll it returns a list

    '''for post in posts:
        if count % 2 == 1:
            f.write("<div odd>")
        else:
            f.write("<div even>")'''

    for post in posts:
        f.write("<div>")

        f.write("<a href = 'https://m.facebook.com/" + post.find('a', {'class': '_5pcq'})['href'] + "' target=\"_blank\">")
        # target="_blank" : the linked document will open in a new tab
        f.write('<p>' + str(count) + '</p></a>')

        count = count + 1

        image = post.find("img", {"class": "scaledImageFitWidth img"})

        if image is not None:
            f.write("<img src = " + image['src'] + ">")

        post_description = post.find("div", {"class": lambda value: value and value.startswith("_5pbx userContent")})
        if post_description is not None:
            f.write("<p>" + post_description.text + "</p><br>")

        '''comments = post.findAll("span", {"class": "UFICommentBody"})
        # UFI = Universal Feedback Interface
        if comments is not None:
            f.write("<p><b>Comments:</b>")
            for comment in comments:
                f.write("<li>" + comment.text + "</li>")
            f.write("<br></p>")'''

        f.write("</div>")

    f.write("</body>")
    f.write("</html>")
    f.close()
    webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open('C:/Users/iiitb/Desktop/zense/FacebookPages/' + page + '.html')
    break
