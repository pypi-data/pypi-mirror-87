from datetime import datetime, timedelta

class HunDate:
    def __init__(self):
        self.now = datetime.now()

    def today(self):
        date = self.now.strftime('%Y-%m-%d')
        return date

    def today_plus_1day(self):
        date = self.now + timedelta(days=1)
        date = date.strftime('%Y-%m-%d')
        return date

    def time(self):
        date_time = self.now.strftime('%Y-%m-%d %H:%M:%S')
        return date_time

    def minus_day(self, day):
        minus_day = self.now - timedelta(days=day)
        minus_day = minus_day.strftime('%Y-%m-%d')
        return minus_day

    def now_timestamp(self, days=0):
        t = self.now - timedelta(days=days)
        return int(t.timestamp()*1000)

    def get_timestamp(self, date):
        try:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        except:
            date = date + " 00:00:00"
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        return int(date.timestamp()*1000)
