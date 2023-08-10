import datetime
from dateutil.relativedelta import relativedelta
import pytz

class QueryTime():

    """
    Usage:
        Decide the start time and the end time wether was in the summer time or the winter time.

        Summer time: 
                     To begin at the first day of October on every year. (as well as the end of the winter time.);
                     The first sunday in October on every year.
                     The date of Ocotber 1st plus the days between the first sunday

        Winter time: 
                     To begin at the first day of Aril on every year. (as well as the end of the summer time.);
                     The first sunday in April on every year.
                     The date of April 1st plus the days between the first sunday

        Return the start date and the end date which are to be paramaters.
    """

    def get_first_sunday_in_october(self,year):
        
        october_1st = datetime.datetime(year=year, month=10, day=1)

        day_of_week = october_1st.weekday()

        days_until_sunday = 6 - day_of_week

        first_sunday = (october_1st + datetime.timedelta(days=days_until_sunday)).date()

        return first_sunday


    def get_first_sunday_in_april(self,year):


        april_1st = datetime.datetime(year=year, month=4, day=1)

        day_of_week = april_1st.weekday()

        days_until_sunday = 6 - day_of_week

        first_sunday = (april_1st + datetime.timedelta(days=days_until_sunday)).date()

        return first_sunday

    def start_time(self,n: int):

        """
            n =
                7: one week;
                14: two week...
        """
        
        time_zone = pytz.timezone('Australia/Melbourne')

        aus_now = datetime.datetime.now(time_zone)

        date = aus_now.date() + relativedelta(days= -aus_now.weekday()-n)

        year = date.year

        get_first_sunday_in_april = self.get_first_sunday_in_april(year)

        get_first_sunday_in_october = self.get_first_sunday_in_october(year)

        if get_first_sunday_in_april <= date <= get_first_sunday_in_october:

            time = f'{date} 14:00:00'

        else:

            time = f'{date} 13:00:00'

        return time

    def end_time(self):

        time_zone = pytz.timezone('Australia/Melbourne')

        aus_now = datetime.datetime.now(time_zone)

        date = aus_now.date() + relativedelta(days= -aus_now.weekday()-1)

        year = date.year

        get_first_sunday_in_april = self.get_first_sunday_in_april(year)

        get_first_sunday_in_october = self.get_first_sunday_in_october(year)

        if get_first_sunday_in_april <= date <= get_first_sunday_in_october:

            time = f'{date} 14:00:00'

        else:
            
            time = f'{date} 13:00:00'

        return time


    def formatted_today(self):

        today = datetime.datetime.today()

        today_line = today.strftime('%Y-%m-%d')

        today_fit = today.strftime("%Y%m%d")

        return {
                    'today_line': today_line,
                    'today_fit': today_fit
               }
