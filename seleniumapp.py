from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tabulate import tabulate
from selenium.common.exceptions import NoSuchElementException
import sqlite3
conn = sqlite3.connect("test.db")

c = conn.cursor()


sql = ''' INSERT INTO emp(name,year,link)
              VALUES(?,?,?) '''



#
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# , options=chrome_options
driver = webdriver.Chrome(executable_path="./chromedriver.exe")
url = "https://www.honourpoint.in"
driver.get(url)
flag= True
m=200
i=0
while(flag):

    time.sleep(1)
    try:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[2]/div/div[7]/div/div/div/div/div/div/div/a").click()

    except NoSuchElementException as e:
        print(e)
        print("Got stuck at", i)

    i+=1

    if(i>m):
        flag=False

time.sleep(10)


posts= driver.find_elements_by_class_name("hp-profile-item")
print(i)

print()

#sequel
print("Processing data")
j=0
for post in posts:
    j+=1
    if(j>150):
        nam = post.find_element_by_class_name("hp-profile-title").text

        yr = post.find_element_by_class_name("hp-profile-publish-date").text
        lin = post.find_element_by_class_name("hp-profile-image").find_element_by_tag_name("img").get_attribute("src")
        data = (nam,yr,lin)

        c.execute(sql,data)
        conn.commit()


print("finished")
