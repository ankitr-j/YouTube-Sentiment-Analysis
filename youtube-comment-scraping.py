from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
from nltk_tester import sentiment_analyzer

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
# options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
driver = webdriver.Chrome(options=options)

# URL of the YouTube video
url = 'https://www.youtube.com/watch?v=__eiQumLOEo'

# Open the YouTube video page
driver.maximize_window()
driver.get(url)
# Scroll to load comments
time.sleep(8)  # Wait for the page to load
driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight/3);")
time.sleep(1)  # Wait for comments to load

# Scroll multiple times to load more comments
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1)

# Get page source after scrolling
page_source = driver.page_source
driver.quit()


# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')
comments = soup.find_all('span', class_="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap")
with open('comments.txt', 'w', encoding='utf-8') as file:
    file.write(str(comments))

comments_sentences = []

for comment in comments:
    comments_sentences.append(comment.text.strip())

VIDEO_DESCRIPTION = comments_sentences.pop()
VIDEO_DATE = comments_sentences.pop() +" "+ comments_sentences.pop()
comments_sentences.pop()
VIEWS = comments_sentences.pop()
comments_sentences.pop()
LIKES = comments_sentences.pop()

# for i in range(len(comments_sentences)):
#     print("Comment Number : ",i ," Comment :-", comments_sentences[i])

# print("Video description = ", VIDEO_DESCRIPTION)
# print("Video Date :-", VIDEO_DATE)
# print("Views :-", VIEWS)
# print("Likes :-", LIKES)

analyzer = sentiment_analyzer()
negative = 0
positive = 0
neutral = 0
for comment in comments_sentences:
    sentiment = analyzer.analyse_sentiment(comment)
    negative+= sentiment["neg"]
    positive+= sentiment["pos"]
    neutral+= sentiment["neu"]

    # polarity += sentiment.polarity
    # subjectivity += sentiment.subjectivity

print("Positive :", positive,",", "Negative : ", negative, "Neutral : ", neutral)
print("Total Comments :", len(comments_sentences))
# Close the WebDriver
