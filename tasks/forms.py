from django import forms
import datetime
from datetime import date

from .models import *


def year_choices():
    return [(y, y) for y in range(datetime.date.today().year, datetime.date.today().year + 10)]


def month_choices():
    return [(m, m) for m in range(1, 13)] 


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["user"]  # we do not want the user to be able to set who is the user for security so we are hiding this field
        fields = '__all__'
        widgets = {'due_date': DateInput()}


class CalendarForm(forms.Form):
    year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=date.today().year)
    month = forms.TypedChoiceField(coerce=int, choices=month_choices, initial=date.today().month)


class SearchForm(forms.Form):
    search = forms.CharField(required=False)
