import xml.etree.ElementTree as etree
from datetime import datetime
from calendar import HTMLCalendar
from .models import Task


class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None):
        
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def mark_dates(self, request):
        
        html_calendar = self.formatmonth(self.year, self.month)  # produce the basic html calendar

        # fetching all the tasks for this year and month and for this user so we can mark it on the calendar
        tasks = Task.objects.filter(user=request.user, due_date__year=self.year, due_date__month=self.month,
                                    complete=False)

        dates_to_mark = []  # extracting only the dates

        for task in tasks:
            dates_to_mark.append(task.due_date.day)

        today = datetime.today()

        html_calendar = html_calendar.replace("&nbsp;", " ")
        root = etree.fromstring(html_calendar)
        root.set("cellpadding", '5')  # styling the html calendar table
        root.set("cellspacing", '2')
        root.set("border", "3")

        for elem in root.findall("*//td"):  # looping the html calendar table by cell/date

            try:

                if int(elem.text) in dates_to_mark:
                    
                   elem.set('bgcolor', "pink")
              

                # highlighting today's day on the calendar
                if int(elem.text) == today.day and self.month == today.month and self.year == today.year:
                    elem.text = "*" + elem.text + "*"

            except:
                pass

        my_calendar = etree.tostring(root)

        return my_calendar
