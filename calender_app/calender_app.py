import time
import httplib2
import os
import pytz    # $ pip install pytz
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
# from dateutil import tz
import datetime
import sys
# sudo pip install --upgrade google-api-python-client
from apiclient import discovery as disbuild
import math
path_ = os.path.join(os.getcwd(), "va", "calender_app")
print(path_)
sys.path.append(path_)


class calender_app:

    def __init__(self):
        #     this class has the goal to make an meeting with people on a picked time.
        # --noauth_local_webserver

        try:
            import argparse
            self.flags = argparse.ArgumentParser(
                parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None
        self.flags.noauth_local_webserver = True
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/calendar-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/calendar'
        self.CLIENT_SECRET_FILE = 'client_secret_VA.json'
        self.APPLICATION_NAME = 'Google Calendar make event'
        self.credentials = self.get_credentials()
        http = self.credentials.authorize(httplib2.Http())
        self.service = disbuild.build('calendar', 'v3', http=http)
        self.datetime_ = datetime.datetime
        self.c_local_tz = pytz.timezone("Europe/Amsterdam")
        self.email_ids = None
        self.end_ = None
        self.start = None
        self.adam_loc = {'devoteam.com_3137303633363931363234@resource.calendar.google.com': 'BLACKROOM',
                         'devoteam.com_31343433383535383433@resource.calendar.google.com': 'WHITEROOM',
                         'devoteam.com_3233373832363736313031@resource.calendar.google.com': 'BOARDROOM'}

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_dir = os.path.join(os.getcwd(), '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'VA_credential.json')
        client_secret_dir = os.path.join(
            credential_dir, self.CLIENT_SECRET_FILE)

        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                client_secret_dir, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            print("copy the site and aprove the things it asks")
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def main(self, names=['tako tabak', 'roger van daalen'], appointment_within_days=8, length_meeting=30,
             start_search="none", location='Adam'):

        normal_hours = [self.datetime_.strptime("08:29:00", '%H:%M:%S'
                                                ).replace(year=2018
                                                          ).astimezone(pytz.utc),
                        # .replace(tzinfo = self.c_local_tz),
                        self.datetime_.strptime("17:30:00", '%H:%M:%S'
                                                ).replace(year=2018
                                                          ).astimezone(pytz.utc)]

        self.email_ids = self.get_id(names)
        if start_search is "none" or start_search is "nu":
            now = datetime.datetime.now(pytz.utc)
        else:
            print("alt start time not yet implemented")
            now = datetime.datetime.now(pytz.utc)
        # self.get_events( email_ids[0], now, number = 10)
        within_days = datetime.timedelta(appointment_within_days)
        end_of_period = now + within_days
        freebusy = self.find_free(self.email_ids, now, end_of_period)

        if location is 'Adam':
            location_id = list(self.adam_loc.keys())
            # print(location_id)
        freebusy_loc = self.find_free(location_id, now, end_of_period)

        # start_time = time.time()
        # prep while-loop
        current_start_time = self.make_quarter(datetime.datetime.now(pytz.utc))
        end_meeting = current_start_time + \
            datetime.timedelta(0, length_meeting * 60)
        possible = False
        # print("start end ", current_start_time, end_of_period, "first line in while")
        while not possible and current_start_time < end_of_period:
            possible = True
            current_start_time, end_meeting = self.check_for_end_week_day(current_start_time,
                                                                          length_meeting,
                                                                          normal_hours)
            for id in self.email_ids:
                busy, freebusy[id], next_free = self.check_free(freebusy[id], current_start_time,
                                                                end_meeting, id)
                if busy:
                    possible = False
                    current_start_time = next_free
                    current_start_time, end_meeting = self.check_for_end_week_day(current_start_time,
                                                                                  length_meeting,
                                                                                  normal_hours)

                    break

            if possible:
                # find location
                possible = False
                next_free_loc = []
                for loc in location_id:
                    busy, freebusy_loc[loc], next_free_ = self.check_free(freebusy_loc[loc],
                                                                          current_start_time,
                                                                          end_meeting,
                                                                          self.adam_loc[loc])

                    if not busy:
                        possible = True
                        self.loc = {"email": loc, "name": self.adam_loc[loc]}
                        break
                    next_free_loc.append(next_free_.astimezone(pytz.utc))

                if not possible:
                    # find earliest next time a room is free
                    now = datetime.datetime.now(pytz.utc)
                    # print(next_free_loc, now)
                    next_free = min(dt for dt in next_free_loc)
                    current_start_time, end_meeting = self.check_for_end_week_day(next_free,
                                                                                  length_meeting,
                                                                                  normal_hours)
            # print("start end ", current_start_time, end_of_period, "last line in while")

        if current_start_time > end_of_period:
            print("not found")
            return 0, 0

        print("found meeting utc time", current_start_time, "till", end_meeting)
        self.start, self.end_ = current_start_time.astimezone(
            self.c_local_tz), end_meeting.astimezone(self.c_local_tz)
        print("found meeting time", self.start, "till", self.end_)

        return self.start, self.end_

    def check_for_end_week_day(self, current_start_time, length_meeting, normal_hours):
        end_meeting = current_start_time + \
            datetime.timedelta(0, length_meeting * 60)

        if end_meeting.time() > normal_hours[1].time():
            current_start_time = current_start_time + datetime.timedelta(1)
            current_start_time = current_start_time.replace(hour=normal_hours[0].hour,
                                                            minute=normal_hours[0].minute)
            end_meeting = current_start_time + \
                datetime.timedelta(0, length_meeting * 60)
            print("too late")
        if end_meeting.weekday() > 4:
            print("next week")
            current_start_time = current_start_time + \
                datetime.timedelta(7 - end_meeting.weekday())
            current_start_time = current_start_time.replace(hour=normal_hours[0].hour,
                                                            minute=normal_hours[0].minute)
            end_meeting = current_start_time + \
                datetime.timedelta(0, length_meeting * 60)
        return current_start_time, end_meeting

    def find_free(self, list_id, now, end_of_period):

        now = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_ = end_of_period.strftime('%Y-%m-%dT%H:%M:%SZ')

        resp_loc = self.service.freebusy().query(body={"timeMin": now,
                                                       "timeMax": end_,
                                                       "items": [{'id': id} for id in list_id]}
                                                 ).execute()
        # print("resp_loc", resp_loc['calendars'])
        return resp_loc['calendars']

    def check_free(self, freebusy_id, current_start_time, end_meeting, name='unknown'):
        busy = False
        next_free = None
        # freebusy_id['busy'][0]['']
        # print(freebusy_id['busy'][0], len(freebusy_id['busy']), range(1))
        for i in range(len(freebusy_id['busy'])):
            start_dt = self.datetime_.strptime(freebusy_id['busy'][i]["start"],
                                               '%Y-%m-%dT%H:%M:%SZ').astimezone(pytz.utc)
            end_dt = self.datetime_.strptime(freebusy_id['busy'][i]["end"],
                                             '%Y-%m-%dT%H:%M:%SZ').astimezone(pytz.utc)

            if end_meeting > start_dt and current_start_time < end_dt:

                # print(freebusy_id['busy'][i])
                busy = True
                next_free = self.make_quarter(end_dt)
                print(name, "can not do ", current_start_time,
                      end_meeting, "next (s)he can is:", next_free)
                break

        return busy, freebusy_id, next_free

    def get_id(self, names):
        # big assumtion that all the people are from devoteam
        id_list = []
        for id in names:
            id_list.append(id.replace(" ", ".") + "@devoteam.com")
        return id_list

    def get_events(self, id, now, number=10):
        event_list = []
        eventsResult = self.service.events().list(calendarId=id, timeMin=now.isoformat() + "Z",
                                                  maxResults=str(number), singleEvents=True,
                                                  orderBy='startTime').execute()

        events = eventsResult.get('items', [])
        print("\n", id)
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end_ = event['end'].get('dateTime', event['end'].get('date'))

            if 'visibility' in event and event['visibility'] == 'private':
                name = 'private'
            else:
                name = event['summary']
            print(start, end_, name)
            event_list.append((start, end_, name))

        return event_list

    def meeting_to_string(self, start=None):
        if start is None:
            start = self.start
        day_int = start.strftime('%j')
        print("debug start-local", start)
        if day_int == datetime.datetime.utcnow().strftime('%j'):
            day_str = "vandaag"
        elif day_int == (datetime.datetime.utcnow() +
                         datetime.timedelta(1)).strftime('%j'):
            day_str = "morgen"
        else:
            delta_days = int(day_int) - \
                int(datetime.datetime.now(pytz.utc).strftime('%j'))
            print(delta_days)
            day_str = "over " + str(delta_days) + \
                " dagen op " + start.strftime("%A")

        time_str = str(start.strftime("%H")) + ":" + str(start.strftime("%M"))
        print("debug meetning string ", day_str, time_str)
        return day_str, time_str

    def make_name(self):
        return "Meeting with " + " & ".join([id.split(".")[0] for id in self.email_ids])

    def make_event(self, name=None, location='Adam'):
        """ makes an event

        """
        if name is None:
            name = self.make_name()
        if location is 'Adam':
            location = "Devoteam, Paasheuvelweg 26, 1105 BJ Amsterdam-Zuidoost, Netherlands, " + \
                self.loc['name']
            self.email_ids.append(self.loc['email'])

        # + datetime.timedelta(0, self.start.utcoffset().total_seconds())
        start = self.start
        # + datetime.timedelta(0, self.end_.utcoffset().total_seconds())
        end_ = self.end_
        event = {
            'summary': name,
            'location': location,
            'description': 'An event created by the Devoteam Virtual Agent.',
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': str(start.tzinfo),
            },
            'end': {
                'dateTime': end_.isoformat(),
                'timeZone': str(end_.tzinfo),
            },
            'guestsCanModify': [
                False
            ],
            'attendees': [{'email': id} for id in self.email_ids],
            'reminders': {
                'useDefault': True,
            },
        }
        print(event)
        event = self.service.events().insert(calendarId='primary',
                                             body=event,
                                             sendNotifications=True
                                             ).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return event.get('htmlLink'), event

    def make_quarter(self, time):
        # 15 minutes * 60 seconds = 900 seconds
        t = self.datetime_(2018, 1, 1, 0, 0).astimezone(
            pytz.utc)  # only deltatime has total_seconds()
        round_quarters = math.ceil((time - t).total_seconds() / 900)
        return t + datetime.timedelta(0, round_quarters * 900)


if __name__ == '__main__':

    cal = calender_app()
    start, end_ = cal.main()
    print(cal.meeting_to_string(start, end_))
    link, event = cal.make_event()
