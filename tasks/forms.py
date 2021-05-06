from django import forms
from django.forms import ModelForm
import calendar
import datetime
from datetime import date

from .models import *

def year_choices():
    return [(r,r) for r in range(2010, datetime.date.today().year+10)]
def month_choices():
	return [(r,r) for r in range(1, 13)]
class DateInput(forms.DateInput):
	input_type='date'

class TaskForm(forms.ModelForm):
	class Meta:
		model=Task
		exclude = ["user"]
		fields='__all__'
		widgets={'due_date': DateInput()}

class CalendarForm(forms.Form):

	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=date.today().year)
	month= forms.TypedChoiceField(coerce=int, choices=month_choices, initial=date.today().month)
	
