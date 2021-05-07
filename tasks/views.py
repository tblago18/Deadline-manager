from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import *
from .forms import *
from .utils import Calendar
import calendar
from calendar import HTMLCalendar
import xml.etree.ElementTree as etree
from datetime import date


class CustomLogin(LoginView):
	template_name='tasks/login.html'
	fields='__all__'
	redirect_authenticated_user = True
	# success_url = reverse_lazy('list')


class RegisterView(FormView):
	template_name='tasks/register.html'
	form_class=UserCreationForm
	redirect_authenticated_user = True
	success_url=reverse_lazy('list')

	def form_valid(self, form):
		user=form.save()
		if user is not None:
			login(self.request, user)
		return super (RegisterView, self).form_valid(form)


def CalendarView(request):
	todays_date = date.today()
	year=todays_date.year
	month=int(todays_date.month)
	# month=month.capitalize() #making sure that the first letter is capitalized
	# onths_list=list(calendar.month_name)
	
	#month_number=months_list.index(month)

	#my_calendar=HTMLCalendar().formatmonth(year, month)
	print('hello')
	my_calendar=Calendar(year, month).formatmonth(withyear=True)


	context={'month':month, 'year': year, 'my_calendar':my_calendar}
	
	return render(request, 'tasks/calendar.html', context)



@login_required
def index(request):
	current_user = request.user
	tasks=Task.objects.filter(user=current_user).order_by('due_date')
	form=TaskForm()
	calendar_form=CalendarForm()
	todays_date = date.today()
	month=int(todays_date.month)
	year=todays_date.year

	if request.method=='POST':
		form=TaskForm(request.POST)
		calendar_form = CalendarForm(request.POST)
		#print('made a form')

		if form.is_valid():
			form_instance = form.save(commit=False)
			form_instance.user = current_user
			form_instance.save()
			#print('set the user', instance.user)
			return redirect('/')
		elif calendar_form.is_valid():
			#print('valid')
			year=calendar_form.cleaned_data.get("year")
			month=calendar_form.cleaned_data.get("month")
			#print(year)
		
		# else:
		# 	print(form.errors.as_data())
		# 	print('form not valid')
	my_calendar=Calendar(year, month).mark_dates(request)
	# html_calendar = html_calendar.replace("&nbsp;", " ")

	# root = etree.fromstring(html_calendar)
	# root.set("cellpadding", '5')
	# root.set("cellspacing", '2')
	# my_calendar=etree.tostring(root)

		
	
	#month=month.capitalize() #making sure that the first letter is capitalized
	#onths_list=list(calendar.month_name)
	
	#month_number=months_list.index(month)


	context={'month':month, 'year': year, 'my_calendar':my_calendar, 'tasks':tasks, 'form':form, 'calendar_form':calendar_form}
	return render(request, 'tasks/list.html', context)

@login_required
def updateTask(request, pk):
	task=Task.objects.get(id=pk)
	form = TaskForm(instance=task)
	if request.method=='POST':
		form = TaskForm(request.POST,instance=task)
		if form.is_valid():
			form.save()
		return redirect('/')
	context={'form':form}
	return render (request, 'tasks/update_task.html', context)
@login_required
def deleteTask(request, pk):
	
	item= Task.objects.get(id=pk)
	
	if request.method=='POST':
		item.delete()
		return redirect('/')
	context={'item':item}
	return render (request, 'tasks/delete.html', context)


