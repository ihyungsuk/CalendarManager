from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
import datetime

# # SCOPES = ['https://www.googleapis.com/auth/calendar']
# # creds_filename = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

# # http_auth = creds_filename.authorize(Http())
# # service = build('calendar', 'v3', http=http_auth)

today = datetime.date.today().isoformat()

creds_filename = 'credentials_mine.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(creds_filename, SCOPES)
creds = flow.run_local_server(port=0)
service = build('calendar', 'v3', credentials=creds)

event = {
        'summary': '객지테스트', # 일정 제목
        'location': '집', # 일정 장소
        'description': '제발되어라', # 일정 설명
        'start': { # 시작 날짜
            'dateTime': "2020-12-03"+"T00:00:00", 
            'timeZone': 'Asia/Seoul',
        },
        'end': { # 종료 날짜
            'dateTime': "2020-12-03"+"T00:00:00", 
            'timeZone': 'Asia/Seoul',
        },
        'recurrence': [
        ],
        'attendees': [
        ],
        'reminders': { # 알림 설정
            'useDefault': False,
            'overrides': [
            ],
        },
    }

# calendarId : 캘린더 ID. primary이 기본 값입니다.
event = service.events().insert(calendarId='primary', body=event).execute()
print('Event created: %s' % (event.get('htmlLink')))

# colors = service.colors().get().execute()

# Print available calendarListEntry colors.
# for id, color in colors['calendar'].iteritem():
#     print('colorId: %s' % id)
#     print('Background: %s' % color['background'])
#     print('Foreground: %s' % color['foreground'])
# # Print (available event colors.
# for color in colors['event']:
#     print('colorId: %s' % id)
#     print('Background: %s' % color['background'])
#     print('Foreground: %s' % color['foreground'])