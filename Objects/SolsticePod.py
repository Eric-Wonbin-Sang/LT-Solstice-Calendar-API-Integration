import datetime
import time

from Objects import CalendarItem


class SolsticePod:

    def __init__(self, **kwargs):

        self.ip_address = kwargs.get("ip_address")
        self.calendar_id = kwargs.get("calendar_id")
        self.service = kwargs.get("service")

        self.calendar_item_list = self.get_calendar_item_list()

    def get_event_list(self):
        events_result = self.service.events().list(calendarId=self.calendar_id,
                                                   timeMin=datetime.datetime.utcnow().isoformat() + 'Z',
                                                   # 'Z' for UTC time
                                                   maxResults=10,
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def get_calendar_item_list(self):

        curr_date = datetime.datetime.now()
        now = curr_date.isoformat() + 'Z'
        utc_now = time.strptime(now[0:16], '%Y-%m-%dT%H:%M')
        epoch_now = int(time.mktime(utc_now))
        now_local = time.localtime(epoch_now)

        # Get future event info using calendarID
        event_list = self.get_event_list()
        if not event_list:
            print('No upcoming events found.')
        calendar_item_list = []
        for e_i, event in enumerate(event_list[:3]):

            calendar_item = CalendarItem.CalendarItem(event=event)
            if epoch_now > calendar_item.epoch_end or calendar_item.start_local.tm_mday != now_local.tm_mday:
                break

            calendar_item_list.append(calendar_item)

        return calendar_item_list

    def get_calendar_dict_list(self):
        return [calendar_item.get_solstice_calendar_dict(calendar_item_index=e_i)
                for e_i, calendar_item in enumerate(self.calendar_item_list)]


def get_solstice_pod_list(calendar_info, service):
    solstice_pod_list = []
    for ip_address in calendar_info.ip_id_dict:
        solstice_pod_list.append(
            SolsticePod(
                ip_address=ip_address.strip(),
                calendar_id=calendar_info.ip_id_dict[ip_address],
                service=service
            )
        )
    return solstice_pod_list
