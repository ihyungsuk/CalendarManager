from selenium import webdriver
from bs4 import BeautifulSoup
import time

class Assignments:
    cnt = 0
    def __init__(self, subject, ox, title, due, teacher):
        self.subject = subject
        self.ox = ox
        self.title = title
        self.due = due
        self.teacher = teacher

driver = webdriver.Chrome('/home/ihyungsuk/codes/chromedriver')
driver.implicitly_wait(3)
driver.get('https://go.sasa.hs.kr/auth')

driver.find_element_by_name('id').send_keys('1948')
driver.find_element_by_name('passwd').send_keys('gktlqkf491!!')
driver.find_element_by_xpath('/html/body/div/div[2]/form/div[3]/div[3]/input').click()
driver.get('https://go.sasa.hs.kr/board/searchCOR')

source = driver.page_source
soup = BeautifulSoup(source, "html.parser")
tmp = soup.select("table.CORtable0 > tbody > tr > td")

l =[]
for i in tmp:
    l.append(i.text)

idx = 0
subject = ''
ox = ''
title = ''
due = ''
teacher = ''
asm_list = []

for i in l:
    i = i.strip()
    if idx%6==0:
        print("subject:", i)
        subject = i
    elif idx%6==1:
        if i=='제출함':
            ox = 1
        else:
            ox = 0
        print("ox:", ox)
    elif idx%6==2:
        pnt = i[:3]
        length = len(i)
        for j in range(1, length):
            if i[j:j+3] == pnt:
                i = i[:j-1]
                break
        print("title:", i)
        title = i
    elif idx%6==3:
        print("due:", i)
        due = i
    elif idx%6==4:
        print("teacher:", i)
        teacher = i
    elif idx%6==5:
        asm = Assignments(subject, ox, title, due, teacher)
        asm_list.append(asm)
    idx +=1

for i in asm_list:
    print("subject:", i.subject)
    print("ox:", i.ox)
    print("title:", i.title)
    print("due", i.due)
    print("teacher", i.teacher)

'div.p_inr > div.p_info > a > span'

# print(title.text)

