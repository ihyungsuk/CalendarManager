from selenium import webdriver
from bs4 import BeautifulSoup
from tkinter import *

from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build

creds_filename = 'credentials_mine.json' # 사용자 구글API ID json 파일을 저장
scopes = ['https://www.googleapis.com/auth/calendar'] # scopes에 권한 저장

flow = InstalledAppFlow.from_client_secrets_file(creds_filename, scopes) ##########
creds = flow.run_local_server(port=0) #############################################
service = build('calendar', 'v3', credentials=creds) ############################## service를 이용해 credential_mine.json 사용자의 구글캘린더에 접근


class Assignment: # 과제 객체
    def __init__(self, subject, ox, title, date, deadline, teacher):
        self._subject = subject # 과제 과목
        self._ox = ox # 과제 제출여부
        self._title = title #과제 제목
        self._date = date #과제 기한 날짜
        self._deadline = deadline #과제 기한 시간
        self._teacher = teacher #과제를 내신 선생님
        self.__check = 0 # 유효성 검사할 때 사용

    def append_to_calendar(self): # 자신을 구글 캘린더에 이벤트로 추가
        self.__event = { # 자신을 이벤트로 추가할 형식
            'summary': self._title,  # 일정 제목
            'description': "untill "+self._deadline[:5]+' '+self._subject+' by'+self._teacher, # 일정 설명
            'start': {  # 시작 날짜
                'date': self._date,
                'timeZone': 'Asia/Seoul', #시간 기준 장소
            },
            'end': {  # 종료 날짜
                'date': self._date,
                'timeZone': 'Asia/Seoul',
            },
            'colorId': 1 if self._ox else 4 # 제출했을 시 파란색, 제출하지 않았을 시 빨간색
        }

        self.__event = service.events().insert(calendarId='primary', body=self.__event).execute() # 자신을 구글 캘린더에 이벤트로 추가
        print('Event created: %s' % (self.__event.get('htmlLink'))) ## 이벤트로 추가했음을 알리고 추가한 이벤트의 링크 출력

    def return_text(self): # tkinter button의 command로 쓸 함수
        self._key = self._ent.get() # key에 entry에 입력된 문자열을 저장
        self._root.destroy() # tkinter root 파괴

    def show_tkinter(self, txt): #tkinter 화면을 제공해주는 함수
        self._key = ''
        self._root = Tk()  # 메인 창 생성
        self._root.title('Calendar Manager')  # 창의 제목 설정
        self._root.geometry('1000x500+200+200')  # 너비x높이+x좌표+y좌표
        self._label = Label(self._root, text=self._title + '\n' + self._teacher +
                            '\n' + self._date + '\n' + self._deadline + '\n\n' + txt)
        self._label.pack(padx=20, pady=50)
        self._ent = Entry(self._root)
        self._ent.pack()
        self._btn = Button(self._root, text='확인', command=self.return_text)
        self._btn.pack()
        self._root.mainloop()

    def change_deadline(self): # 과제의 제출기한 수정 함수
        print()
        print(self._title, self._teacher, self._date, self._deadline)
        self.show_tkinter('Do you want to change deadline? (yes/no)') # key에 yes 또는 no 저장
        if(self._key == 'yes'): # 제출기한을 바꾸어 이벤트로 추가하고 싶은 경우
            self.show_tkinter('new date? (form: yyyy-mm-dd. ex-->2020-02-04)') # 바꿀 제출기한 날짜 설정
            self._new_date = self._key

            self.show_tkinter('new deadline? (form: hh:mm:ss ex-->08:59:11)') # 바꿀 제출기한 시간 설정
            self._new_deadline = self._key

            if str(type(self._new_date)) != """<class 'str'>""":############################################여기서부터
                self.__check = 1
            elif len(self._new_date) != 10:
                self.__check = 1
            elif self._new_date[4] != '-' or self._new_date[7] != '-':
                self.__check = 1
            elif '2021' < self._new_date[:4] or self._new_date[:4] < '2020':
                self.__check = 1
            elif self._new_date[5:7] > '12' or self._new_date[5:7] < '01':
                self.__check = 1
            elif self._new_date[8:10] > '31' or self._new_date[8:10] < '01':
                self.__check = 1 ###########################################################################여기까지 new_date 유효성 검사

            if self.__check == 0: # 유효성 검사 통과 시 변경
                self._date = self._new_date

            self.__check = 0 ############################################################################### 여기서부터
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
            elif self._new_deadline[6:8] > '99' or self._new_deadline[6:8] < '00':
                self.__check = 1 ########################################################################### 여기까지 new_deadline 유효성 검사

            if self.__check == 0: # 유효성 검사 통과 시 변경
                self._deadline = self._new_deadline


class GroupAssignment(Assignment): # 조별과제
    def __init__(self, subject, ox, title, date, deadline, teacher):
        super().__init__(subject, ox, title, date, deadline, teacher)
        self.show_tkinter('Enter leader: ') # 조장 설정
        self._leader = self._key

        self.show_tkinter('Enter group members(띄어쓰기로 구분): ') #조원 설정
        self._member = self._key.split()

    def append_to_calendar(self): # 상속한 연산의 오버라이딩
        self.__description = "until " + \
            self._deadline[:5]+' '+self._subject+' by'+self._teacher
        self.__description += '\n' + "Leader: " + self._leader + '\n' # description에 조장 정보 추가
        for i in self._member:
            self.__description += i+' ' # description에 조원 정보 추가. 이후로는 동일
        self.__event = {
            'summary': self._title,  # 일정 제목
            # 'location': '집', # 일정 장소
            'description': self.__description,  # 일정 설명
            'start': {  # 시작 날짜
                'date': self._date,
                'timeZone': 'Asia/Seoul',
            },
            'end': {  # 종료 날짜
                'date': self._date,
                'timeZone': 'Asia/Seoul',
            },
            'colorId': 1 if self._ox else 5
        }

        self.__event = service.events().insert(calendarId='primary', body=self.__event).execute()
        print('Event created: %s' % (self.__event.get('htmlLink')))


driver = webdriver.Chrome('chromedriver.exe') # selenium 패키지에서 사용할 driver 설정
driver.implicitly_wait(3) # 페이지 이동 전마다 3초씩 대기
driver.get('https://go.sasa.hs.kr/auth') # 달빛학사 로그인 페이지로 이동

driver.find_element_by_name('id').send_keys('1948') # 달빛학사 아이디 입력
driver.find_element_by_name('passwd').send_keys('gktlqkf491!!') # 달빛학사 비밀번호 입력
driver.find_element_by_xpath('/html/body/div/div[2]/form/div[3]/div[3]/input').click() # 확인 버튼 클릭
driver.get('https://go.sasa.hs.kr/board/searchCOR') # 제출모음 게시판 클릭

source = driver.page_source # 현재 driver가 있는 페이지의 페이지정보 따오기
soup = BeautifulSoup(source, "html.parser") # beautifulsoup4 설정
tmp = soup.select("table.CORtable0 > tbody > tr > td") # beautifulsoup4를 이용해 제출모음 게시판의 숨겨짐되지 않은 표의 텍스트 크롤링

l = [] # 크롤링한 데이터 저장할 리스트
for i in tmp:
    l.append(i.text) # 크롤링한 텍스트 데이터 저장

idx = 0 ################################################### 크롤링한 데이터 처리하기 위한 변수들
subject = ''#############################################
ox = ''##################################################
title = ''###############################################
date = ''################################################
deadline = ''############################################
month = ''###############################################
day = ''#################################################
teacher = ''#############################################
asm_list = [] # 과제 인스턴트 리스트

for i in l: #################################################### 크롤링한 데이터 처리
    i = i.strip()
    if idx % 6 == 0:
        # print("subject:", i)
        subject = i
    elif idx % 6 == 1:
        if i == '제출함':
            ox = 1
        else:
            ox = 0
        # print("ox:", ox)
    elif idx % 6 == 2:
        pnt = i[:3]
        length = len(i)
        for j in range(1, length-2):
            if i[j:j+3] == pnt:
                i = i[:j-1]
                break
        # print("title:", i)
        title = i
    elif idx % 6 == 3:
        month = i[2:4]
        day = i[5:7]
        deadline = i[8:13]+":00"
        date = "2020-"+month+"-"+day
        # print("time:", date, deadline)
    elif idx % 6 == 4:
        # print("teacher:", i)
        teacher = i
    elif idx % 6 == 5:
        check = 0
        pnt = '[자료]'
        length = len(title)
        for j in range(length-3):
            if title[j:j+4] == pnt: ################ 과제 제목에 [자료]가 있을 경우 check = 1
                check = 1
                break
        if check == 0:
            asm = Assignment(subject, ox, title, date, deadline, teacher) # check = 0일 경우 개인과제로 인스턴트 생성
            asm_list.append(asm) # 리스트에 인스턴트 추가
        else:
            asm = GroupAssignment(subject, ox, title, date, deadline, teacher) # check = 1일 경우 조별과제로 인스턴트 생성
            asm_list.append(asm) # 리스트에 인스턴트 추가
    idx += 1

deadline_parameter = 1 # 제출기한 변경할지 안할지 표시하는 변수

key = ''  #############################################################################################3 제출기한 변경할 과제 있는지 입력받기 위한 tkinter
root = Tk() #####################################################################################
root.title('Calendar Manager')  #################################################################
root.geometry('1000x500+200+200')################################################################
label = Label(root, text='Are there events that you want to change deadline? (yes/no)')##########
label.pack(padx=20, pady=50)#####################################################################
ent = Entry(root)################################################################################
ent.pack()#######################################################################################


def return_text(): # tkinter button에 쓸 command 함수
    global key, root, ent
    key = ent.get()
    root.destroy()


btn = Button(root, text='확인', command=return_text)
btn.pack()
root.mainloop()
if key == 'no': # 변경할 과제 없다고 답했을 경우
    deadline_parameter = 0
for i in asm_list:
    if deadline_parameter == 1: # 변경할 과제 있다고 답했을 경우
        i.change_deadline() #과제마다 기한변경 메소드 실행
    i.append_to_calendar() # 과제마다 구글 캘린더에 이벤트로 추가
