


from __future__ import print_function
import threading

from datetime import datetime, timedelta,timezone
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from time import sleep

from googlemeet import google_join, zoom_join

SCOPES = ['https://www.googleapis.com/auth/calendar']



class Join:
    def __init__(self, platform,url, isOrganizer, username):
  
        if platform == 'Google':
            google_join(url,isOrganizer,username)
        elif platform == 'Zoom':
            zoom_join(url, isOrganizer,username)


def get_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds



def get_meeting_info():
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
   
    now = datetime.now(timezone.utc).isoformat()
    now_plus_window = (datetime.now(timezone.utc) + timedelta(hours=5)).isoformat()
  
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=now_plus_window, maxResults=8, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])


    for event in events:

        # Extract start time and convert to datetime
        start_time = datetime.strptime(event['start'].get('dateTime', event['start'].get('date')), '%Y-%m-%dT%H:%M:%S%z')


        
        next_timestamp = start_time.timestamp()
        now_timestamp = datetime.now().timestamp()

        
        if next_timestamp > now_timestamp:
            platform = None

            organizer_email = event.get('organizer', {}).get('email', '')
            meet_link = None
           
            if 'conferenceData' in event:
                if 'meet' in event['conferenceData'].get('entryPoints')[0].get('uri'):
                    meet_link = event['hangoutLink']

                    platform = 'Google'
                   
            elif 'description' in event and 'zoom' in event['description']:

                meet_link = event['location']
  

                platform = 'Zoom'
           
            if meet_link is None:
                continue
            
            title = event.get('summary') or "No title"

            return (platform, start_time, next_timestamp, title , meet_link, organizer_email)

    # No upcoming events found
    return (None,None, None, None, None, None)


def open_meeting_in_browser(meet_link, platform, organizer_email):

    email = 'eduarhidalgo1010@gmail.com'
    username = "eduar"
    if email == organizer_email : 
        isOrganizer = True
    else:
        isOrganizer = False

    Join(platform, meet_link, isOrganizer,username)

def main():
 
    while True:
        sleep(1)
        now = datetime.now()
        now_timestamp = now.timestamp()
        (platform, next_time, next_timestamp, meeting_name, meet_link, organizer) = get_meeting_info()
        # platform = "Google"
     
        if not platform:
            print("No upcoming meetings in your calendar for the next 5 hour.")
            continue
        time_diff_seconds = next_timestamp - now_timestamp

        minutes, seconds = divmod(int(time_diff_seconds), 60)
        
        if 20 < time_diff_seconds <= 60:
            minutes, seconds = divmod(int(time_diff_seconds), 60)
            print(f"Next meeting({meeting_name}) starts in {seconds} seconds. Join here: {meet_link}")
        elif time_diff_seconds <= 20:
            print(f"New meeting({meeting_name}) has started! Joining ...")

            try :
                meeting = threading.Thread(target=open_meeting_in_browser(meet_link, platform, organizer),args=())
                meeting.start()
                meeting.join()
            except:
                pass
           
            print("Meeting joined, Searching a next meeting...")
            sleep(30)
        else :
            print(f"Next meeting({meeting_name}) starts in {minutes} minutes and {seconds} seconds.")
            



if __name__ == '__main__':

    while(1):
        try: 
            main()
        except Exception as error:
            print(error)
            sleep(10)
