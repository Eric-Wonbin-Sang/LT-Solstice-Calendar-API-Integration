import requests
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import hashlib

from Objects import SolsticePod, CalendarInfo

from General import Constants


def is_valid_ip(calendar_info, ip_address):
    admin_password = calendar_info.param_dict["Solstice Password"]
    stats_url = 'http://{}/api/stats?password={}'.format(ip_address, admin_password)
    try:
        rc = requests.get(stats_url)
        return True
    except:
        return False


def get_password(calendar_info, ip_address):

    admin_password = calendar_info.param_dict["Solstice Password"]

    # Return empty string if clear-text password is empty
    if admin_password is None:
        return ''

    stats_url = 'http://{}/api/stats?password={}'.format(ip_address, admin_password)
    rc = requests.get(stats_url)
    request_config = eval(rc.text)
    version = request_config.get('m_serverVersion')

    # Return a SHA1-hashed password string if Pod version < 4.1
    if float(version[0:3]) < 4.1:
        return hashlib.sha1(admin_password.encode('utf-8')).hexdigest()
    return admin_password


def get_credentials():
    store = file.Storage(Constants.calendar_api_token_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(
            Constants.google_calendar_credentials_path,
            scope='https://www.googleapis.com/auth/calendar.events.readonly'
        )
        credentials = tools.run_flow(flow, store)
    return credentials


def main():

    calendar_info = CalendarInfo.CalendarInfo()

    credentials = get_credentials()
    service = build('calendar', 'v3', http=credentials.authorize(Http()))

    for solstice_pod in SolsticePod.get_solstice_pod_list(calendar_info=calendar_info, service=service):

        if is_valid_ip(calendar_info, solstice_pod.ip_address):
            requests.post(
                'http://{}/api/calendar/set'.format(solstice_pod.ip_address),
                json={
                    'password': get_password(calendar_info, solstice_pod.ip_address),
                    'calendarItems': solstice_pod.get_calendar_dict_list()
                }
            )

            for i, calendar_item in enumerate(solstice_pod.calendar_item_list):
                print(i, calendar_item)
        else:
            print(solstice_pod.ip_address, "is not valid")


main()
