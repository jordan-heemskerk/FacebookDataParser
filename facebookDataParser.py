#!/usr/bin/python

from bs4 import BeautifulSoup

class FacebookDataParser(object):

    """ Parse and print out your Facebook Data in a useful format.
    True to Python, this is a quick first prototype of parsing data available from a user's Facebook data download.
    It parses and formats the data's message timeline information (date and time), and prints each entry onto a new line.

    Created by:
        Erika Burdon / eburdon

    Created for:
        University of Victoria
        CSC 462: Distributed Computing
        Summer 2016

    Usage:
        Download your Facebook data; extract and move 'messages.htm' to the same folder as this file.
        Run './facebookDataParser.py >> out.txt'

    Future work:
        Implement in Go lang
        Move to hadoop cluster (e.g., make use of mapReduce) or another parallel computing algorithm to improve performance
        Add flexibility: 
            Add options to parse other data available in the download such as:
                User message content (e.g., produce data for a word cloud)
                User photo metadata
                ??
            Add option for user to specify output format (e.g., single lined, list, object)
    """

    def messageTimelineParser(self):
        # indexing constants
        WEEKDAY = 0
        MONTH = 1
        YEAR = 2

        soup = BeautifulSoup(open("messages.htm"), "lxml")

        headers = soup.findAll('div', attrs={'class':'message_header'})
        for header in headers:

            meta_date_text = header.find('span', attrs={'class':'meta'}).get_text()

            # e.g., [u'Sunday', u' April 5', u' 2015 at 8:44am PDT']
            meta_date_text = [item.strip() for item in meta_date_text.split(",")]

            meta_weekday = meta_date_text[WEEKDAY]

            # split month, date
            meta_date_text[MONTH]   = meta_date_text[MONTH].split(" ")
            meta_month              = meta_date_text[MONTH][0]
            meta_date               = meta_date_text[MONTH][1]

            # split year
            meta_date_text[YEAR]    = meta_date_text[YEAR].split(" ")
            meta_year               = meta_date_text[YEAR][0]

            # split time
            raw_time = meta_date_text[YEAR][2]
            if "pm" in raw_time:
                raw_time = raw_time.split(":")
                hour = int(raw_time[0]) + 12

                if hour >= 24:
                    hour = 00

                raw_time[0] = str(hour)

                raw_time = ":".join(raw_time)

            # save time without am/pm suffix
            meta_time = raw_time[:-2]

            # print data to file e.g., Sunday,April,5,2015,8:44
            print '%s,%s,%s,%s,%s' % (meta_weekday, meta_month, meta_date, meta_year, meta_time)

if __name__ == "__main__":
    fb = FacebookDataParser()
    fb.messageTimelineParser()
