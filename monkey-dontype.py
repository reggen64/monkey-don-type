#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bstml
import time
import sys

chr_to_type=0
total_time=0
if(len(sys.argv)==3):
        if(sys.argv[1]=='--wpm'):
                chr_to_type=5*int(sys.argv[2])
        elif(sys.argv[1]=='-t'):
                total_time=sys.argv[2]
                chr_to_type=300
elif(len(sys.argv)==5):
        total_time=int(sys.argv[4])
        chr_to_type=int(total_time*int(sys.argv[2])/12)
else:
        print('Please specify --wpm (-t also if you want to)')
        exit(1)
print("Total time:", str(total_time))
print("Characters to type:", chr_to_type)



s=Service("") #####Insert location of chromedriver here
driver = webdriver.Chrome(service=s)
driver.get("https://monkeytype.com/")
time.sleep(5)
time_button=driver.find_element(By.XPATH, '//*[@id="testConfig"]/div/div[5]/div[5]')
time_button.click()
time_input=driver.find_element(By.XPATH, '/html/body/div[7]/div/div/input')
time_input.send_keys(Keys.BACK_SPACE+str(total_time))
time_ok_button=driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[4]')
time_ok_button.click()

char_typed=0
finished=0
word_input = driver.find_element(By.ID, "wordsInput")

time.sleep(10)

while(not finished):
    html_code=driver.page_source
    soup=bstml(html_code, "html.parser")
    words=soup.find_all("div", {"class": "word"})
    wordlist=[]
    for i in range(len(words)):
                st=bstml(str(words[i]), "html.parser")
                word=''
                for j in st.find_all("letter", class_=None):
                        k=bstml(str(j), "html.parser")
                        word=word+k.letter.contents[0]
                if(word):
                        wordlist.append(word)
    print(wordlist)
    print(len(wordlist))
    for i in wordlist:
        for j in i:
            word_input.send_keys(j)
            char_typed=char_typed+1
            if(char_typed==chr_to_type):
                finished=1
                break
        if(char_typed==chr_to_type):
            finished=1
            break
        word_input.send_keys(' ')
        char_typed=char_typed+1
        if(char_typed==chr_to_type):
            finished=1
            break

if(finished):
    print("Mission successful!")
time.sleep(500)
driver.close()
exit(0)
