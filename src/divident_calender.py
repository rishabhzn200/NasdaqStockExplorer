import datetime
import pandas
import requests

pandas.set_option('display.max_columns', None)

class DividendCalender:
    url = 'https://api.nasdaq.com/api/calendar/dividends'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'DNT': "1",
        'Origin': 'https://www.nasdaq.com/',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)'
    }

    def __init__(self, year, month):
        """
        Initialize the DividendCalender object.
        :param year: year int
        :param month: month int
        """

        self.year = int(year)
        self.month = int(month)

    def date_str(self, day):
        """
        Accepts a day and returns a formatted date string.
        :param day: day
        :return: formatted date string
        """

        date_obj = datetime.date(self.year, self.month, day)
        date_str = date_obj.strftime(format="%Y-%m-%d")
        return date_str

    def scraper(self, date_str):
        """
        Scrapes JSON object from page using requests module.
        :param date_str: string in yyyy-mm-dd format
        :return: Returns a JSON dictionary at a given URL.
        """

        params = {'date': date_str}
        page = requests.get(self.url, headers=self.headers, params=params)
        dictionary = page.json()
        return dictionary

    def dict_to_df(self, dicti):
        """
        Converts the JSON dictionary into a pandas dataframe
        Appends the dataframe to calendars class attribute
        :param dicti: Output from the scraper method as input.
        :return: Dataframe of stocks with that ex-dividend date
        """

        rows = dicti.get('data').get('calendar').get('rows')
        calendar = pandas.DataFrame(rows)
        return calendar

    def calendar(self, day):
        """
        Combines the scrape and dict_to_df methods
        :param day: day of the month as string or number.
        :return: Returns a JSON dictionary with keys
        """

        day = int(day)
        date_str = self.date_str(day)
        dictionary = self.scraper(date_str)
        return self.dict_to_df(dictionary)
