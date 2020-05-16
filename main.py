import requests
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import hashlib

import SolsticePod

from General import Constants


def get_password(ip_address):
    # Return empty string if clear-text password is empty
    if Constants.admin_password is None:
        return ''

    stats_url = 'http://{}/api/stats?password={}'.format(ip_address, Constants.admin_password)
    rc = requests.get(stats_url)
    request_config = eval(rc.text)
    version = request_config.get('m_serverVersion')

    # Return a SHA1-hashed password string if Pod version < 4.1
    if float(version[0:3]) < 4.1:
        return hashlib.sha1(Constants.admin_password.encode('utf-8')).hexdigest()
    return Constants.admin_password


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

    credentials = get_credentials()
    service = build('calendar', 'v3', http=credentials.authorize(Http()))

    for solstice_pod in SolsticePod.get_solstice_pod_list():

        calendar_item_list = solstice_pod.get_calendar_item_list(service=service)
        for i, calendar_item in enumerate(calendar_item_list):
            print(i, calendar_item)

        calendar_dict_list = [calendar_item.get_solstice_calendar_dict(calendar_item_index=e_i)
                              for e_i, calendar_item in enumerate(calendar_item_list)]

        requests.post(
            'http://{}/api/calendar/set'.format(solstice_pod.ip_address),
            json={
                'password': get_password(solstice_pod.ip_address),
                'calendarItems': calendar_dict_list
            }
        )


main()