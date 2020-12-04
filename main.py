from selenium import webdriver
from bs4 import BeautifulSoup
from tkinter import *

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
    def __init__(self, subject, ox, title, date, deadline, teacher):
        self._subject = subject
        self._ox = ox
        self._title = title
        self._date = date
        self._deadline = deadline
        self._teacher = teacher
        self.__check = 0
    def append_to_calendar(self):
        self.__event = {
                'summary': self._title, # 일정 제목
                # 'location': '집', # 일정 장소
                'description': "untill "+self._deadline[:5]+' '+self._subject+' by'+self._teacher, # 일정 설명
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

    def return_text(self):
        self._key, self._root
        self._key = self._ent.get()
        self._root.destroy()
    def show_tkinter(self, txt):
        self._key = ''
        self._root = Tk() # 메인 창 생성
        self._root.title('Calendar Manager') #창의 제목 설정
        self._root.geometry('1000x500+200+200') # 너비x높이+x좌표+y좌표
        self._label = Label(self._root, text=self._title +'\n' + self._teacher+'\n' + self._date + '\n' + self._deadline + '\n\n' + txt)
        self._label.pack(padx=20, pady=50)
        self._ent = Entry(self._root)
        self._ent.pack()
        self._btn = Button(self._root, text='확인', command=self.return_text)
        self._btn.pack()
        self._root.mainloop()

    def change_deadline(self):
        print()
        print(self._title, self._teacher, self._date, self._deadline)
        self.show_tkinter('Do you want to change deadline? (yes/no)')
        if(self._key == 'yes'):
            self.show_tkinter('new date? (form: yyyy-mm-dd. ex-->2020-02-04)')
            self._new_date = self._key

            self.show_tkinter('new deadline? (form: hh:mm:ss ex-->08:59:11)')
            self._new_deadline = self._key

            if str(type(self._new_date)) != """<class 'str'>""":
                self.__check = 1
            elif len(self._new_date) != 10:
                self.__check = 1
            elif self._new_date[4] != '-' or self._new_date[7] != '-':
                self.__check = 1
            elif '2021' < self._new_date[:4] or self._new_date[:4] < '2020':
                self.__check = 1
            elif self._new_date[5:7] > '12' or self._new_date[5:7] < '01':
                self.__check = 1
            elif self._new_date[8:10]>'31' or self._new_date[8:10] < '01':
                self.__check = 1

            if self.__check == 0:
                self._date = self._new_date

            self.__check = 0
            if str(type(self._new_deadline)) != """<class 'str'>""":
                self.__check = 1
            elif len(self._new_deadline) != 8:
                self.__check = 1
            elif self._new_deadline[2] != ':' or self._new_deadline[5] != ':':
                self.__check = 1
            elif '23' < self._new_deadline[:2] or self._new_deadline[:2] < '00':
                self.__check = 1
            elif self._new_deadline[3:5] > '59' or self._new_deadline[3:5] < '00':
                self.__check = 1
            elif self._new_deadline[6:8]>'99' or self._new_deadline[6:8] < '00':
                self.__check = 1

            if self.__check==0:
                self._deadline = self._new_deadline

class GroupAssignment(Assignment):
    def __init__(self, subject, ox, title, date, deadline, teacher):
        super().__init__(subject, ox, title, date, deadline, teacher)
        self.show_tkinter('Enter leader: ')
        self._leader = self._key

        self.show_tkinter('Enter group members(띄어쓰기로 구분): ')
        self._member = self._key.split()

    def append_to_calendar(self):
        self.__description = "until "+self._deadline[:5]+' '+self._subject+' by'+self._teacher
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

driver = webdriver.Chrome('chromedriver.exe')
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
deadline =''
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
        deadline = i[8:13]+":00"
        date = "2020-"+month+"-"+day
        # print("time:", date, deadline)
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
            asm = Assignment(subject, ox, title, date, deadline, teacher)
            asm_list.append(asm)
        else:
            asm = GroupAssignment(subject, ox, title, date, deadline, teacher)
            asm_list.append(asm)
    idx +=1

deadline_parameter = 1

key = ''
root = Tk() # 메인 창 생성
root.title('Calendar Manager') #창의 제목 설정
root.geometry('1000x500+200+200') # 너비x높이+x좌표+y좌표
label = Label(root, text='Are there events that you want to change deadline? (yes/no)')
label.pack(padx=20, pady=50)
ent = Entry(root)
ent.pack()
def return_text():
    global key, root, ent
    key = ent.get()
    root.destroy()
btn = Button(root, text='확인', command=return_text)
btn.pack()
root.mainloop()
if key=='no':
    deadline_parameter = 0
for i in asm_list:
    if deadline_parameter == 1:
        i.change_deadline()
    i.append_to_calendar()




