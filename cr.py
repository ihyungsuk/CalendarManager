from selenium import webdriver
from bs4 import BeautifulSoup
import time

from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
import datetime

creds_filename = 'credentials_mine.json'
scopes = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(creds_filename, scopes)
creds = flow.run_local_server(port=0)
service = build('calendar', 'v3', credentials=creds)
today = datetime.date.today().isoformat()

class Assignment:
    def __init__(self, subject, ox, title, date, endtime, teacher):
        self._subject = subject
        self._ox = ox
        self._title = title
        self._date = date
        self._endtime = endtime
        self._teacher = teacher
        self.__check = 0
    def append_to_calendar(self):
        self.__event = {
                'summary': self._title, # 일정 제목
                # 'location': '집', # 일정 장소
                'description': "untill "+self._endtime[:5]+' '+self._subject+' by'+self._teacher, # 일정 설명
                'start': { # 시작 날짜
                    'date': self._date, 
                    'timeZone': 'Asia/Seoul',
                },
                'end': { # 종료 날짜
                    'date': self._date, 
                    'timeZone': 'Asia/Seoul',
                },
                'colorId': 1 if self._ox else 4
            }

        self.__event = service.events().insert(calendarId='primary', body=self.__event).execute()
        print('Event created: %s' % (self.__event.get('htmlLink')))
    def change_due(self, new_date, new_endtime):
        if str(type(new_date)) != """<class 'str'>""":
            self.__check = 1
        elif len(new_date) != 10:
            self.__check = 1
        elif new_date[4] != '-' or new_date[7] != '-':
            self.__check = 1
        elif '2021' < new_date[:4] or new_date[:4] < '2020':
            self.__check = 1
        elif new_date[5:7] > '12' or new_date[5:7] < '01':
            self.__check = 1
        elif new_date[8:10]>'31' or new_date[8:10] < '01':
            self.__check = 1

        if self.__check == 0:
            self._date = new_date

        self.__check = 0
        if str(type(new_endtime)) != """<class 'str'>""":
            self.__check = 1
        elif len(new_endtime) != 8:
            self.__check = 1
        elif new_endtime[2] != ':' or new_endtime[5] != ':':
            self.__check = 1
        elif '23' < new_endtime[:2] or new_endtime[:2] < '00':
            self.__check = 1
        elif new_endtime[3:5] > '59' or new_endtime[3:5] < '00':
            self.__check = 1
        elif new_endtime[6:8]>'99' or new_endtime[6:8] < '00':
            self.__check = 1
        
        if self.__check==0:
            self._endtime = new_endtime



class GroupAssignment(Assignment):
    def __init__(self, subject, ox, title, date, endtime, teacher):
        super().__init__(subject, ox, title, date, endtime, teacher)
        print(self._title, self._teacher, self._date, self._endtime)
        self._leader = input("Leader:")
        self._member = input("Group members: ").split()
    def append_to_calendar(self):
        self.__description = "untill "+self._endtime[:5]+' '+self._subject+' by'+self._teacher
        self.__description += '\n' + "Leader: " + self._leader + '\n'
        for i in self._member:
            self.__description += i+' ' 
        self.__event = {
                'summary': self._title, # 일정 제목
                # 'location': '집', # 일정 장소
                'description': self.__description, # 일정 설명
                'start': { # 시작 날짜
                    'date': self._date, 
                    'timeZone': 'Asia/Seoul',
                },
                'end': { # 종료 날짜
                    'date': self._date, 
                    'timeZone': 'Asia/Seoul',
                },
                'colorId': 1 if self._ox else 5
            }

        self.__event = service.events().insert(calendarId='primary', body=self.__event).execute()
        print('Event created: %s' % (self.__event.get('htmlLink')))

driver = webdriver.Chrome('C:\\Users\\형석\\Documents\\GitHub\\CalendarManager\\chromedriver.exe')
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
date = ''
endtime =''
month=''
day=''
teacher = ''
asm_list = []

for i in l:
    i = i.strip()
    if idx%6==0:
        # print("subject:", i)
        subject = i
    elif idx%6==1:
        if i=='제출함':
            ox = 1
        else:
            ox = 0
        # print("ox:", ox)
    elif idx%6==2:
        pnt = i[:3]
        length = len(i)
        for j in range(1, length-2):
            if i[j:j+3] == pnt:
                i = i[:j-1]
                break
        # print("title:", i)
        title = i
    elif idx%6==3:
        month = i[2:4]
        day = i[5:7]
        endtime = i[8:13]+":00"
        date = "2020-"+month+"-"+day
        # print("time:", date, endtime)
    elif idx%6==4:
        # print("teacher:", i)
        teacher = i
    elif idx%6==5:
        check = 0
        pnt = '[자료]'
        length = len(title)
        for j in range(length-3):
            if title[j:j+4] == pnt:
                check = 1
                break
        if check==0:
            asm = Assignment(subject, ox, title, date, endtime, teacher)
            asm_list.append(asm)
        else:
            asm = GroupAssignment(subject, ox, title, date, endtime, teacher)
            asm_list.append(asm)
    idx +=1

for i in asm_list:
    i.change_due('2020-12-03', '13:00:00')
    i.append_to_calendar()




