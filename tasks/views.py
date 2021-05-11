from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task
from .forms import *
from .utils import Calendar
from datetime import date


class CustomLogin(LoginView):  # this is a inherited from the Django inbuilt log-in class

    template_name = 'tasks/login.html'
    fields = '__all__'
    redirect_authenticated_user = True


class RegisterView(FormView):
    template_name = 'tasks/register.html'
    form_class = UserCreationForm  # this is a inbuilt Django form for creating new users
    redirect_authenticated_user = True
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:  # checking if the user already exists
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)


@login_required  # this makes sure that you cannot access the view if you are not logged in
def main_view(request):
    current_user = request.user
    tasks = Task.objects.filter(user=current_user).order_by('due_date')  # making a list of all the tasks for the user

    new_task_form = TaskForm()  # making a form so that the user can add new tasks to the list
    calendar_form = CalendarForm()  # form for choosing what month and year the user wants to see on the calendar
    search_form = SearchForm()

    todays_date = date.today()  # the calendar is by default showing current month and year
    month = int(todays_date.month)
    year = todays_date.year

    if request.method == 'POST':
        new_task_form = TaskForm(request.POST)  # post method lets us communicate with the user trough the forms
        if new_task_form.is_valid():  # checking if the post is sending a task form
            form_instance = new_task_form.save(commit=False)
            form_instance.user = current_user
            form_instance.save()
            return redirect('/')

        elif "year" in request.POST:  # or a calendar form
            calendar_form = CalendarForm(request.POST)

            if calendar_form.is_valid():
                year = calendar_form.cleaned_data.get("year")
                month = calendar_form.cleaned_data.get("month")

        elif "search" in request.POST:  # or a search form
            search_form = SearchForm(request.POST)

            if search_form.is_valid():
                searched = request.POST['search']

                if searched != '':
                    tasks = Task.objects.filter(user=current_user, title__contains=searched).order_by('due_date')
                else:
                    tasks = Task.objects.filter(user=current_user).order_by('due_date')

    my_calendar = Calendar(year, month).mark_dates(request)  # making the calendar with all the important dates
    context = {'month': month, 'year': year, 'my_calendar': my_calendar,
               'tasks': tasks, 'new_task_form': new_task_form, 'calendar_form': calendar_form,
               'search_form': search_form}
    return render(request, 'tasks/list.html', context)


@login_required
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'form': form}
    return render(request, 'tasks/update_task.html', context)


@login_required
def delete_task(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item': item}
    return render(request, 'tasks/delete.html', context)
