import time


class CalendarItem:

    def __init__(self, event):

        self.event = event

        self.start = self.get_start()
        self.end = self.get_end()

        # Event start time in necessary formats
        self.utc_start = time.strptime(self.start[0:16], '%Y-%m-%dT%H:%M')  # Correctly formatted UTC start time
        self.epoch_start = int(time.mktime(self.utc_start))  # Epoch timestamp of UTC start time
        self.start_local = time.localtime(self.epoch_start)  # Local time of event

        # Event end time in necessary formats
        self.utc_end = time.strptime(self.end[0:16], '%Y-%m-%dT%H:%M')  # Correctly formatted UTC end time
        self.epoch_end = int(time.mktime(self.utc_end))  # Epoch timestamp of UTC end time

        self.organizer = self.get_organizer()
        self.name = self.get_name()

    def get_start(self):
        start = self.event['start'].get('dateTime', self.event['start'].get('date'))
        if len(start) <= 10:  # Account for all day events
            start = start + 'T00:00:00'
        return start

    def get_end(self):
        end = self.event['end'].get('dateTime', self.event['end'].get('date'))
        if len(end) <= 10:  # Account for all day events
            end = end + 'T23:59:00'
        return end

    def get_organizer(self):
        organizer = self.event['organizer'].get('displayName')
        # G Suite user calendars don't include organizer.displayName unless user has associated G+ account
        if str(organizer) == 'None':
            organizer = ''
        return organizer

    def get_name(self):
        return self.event['summary']

    def get_solstice_calendar_dict(self, calendar_item_index):
        return {
            'id': str(calendar_item_index),
            'startTime': self.epoch_start,
            'endTime': self.epoch_end,
            'title': self.name,
            'organizer': self.organizer
        }

    def __str__(self):
        return "name:\t{}\n\torg:\t{}\n\tstart:\t{}\n\tend:\t{}".format(
            self.name,
            self.organizer,
            self.start,
            self.end
        )
