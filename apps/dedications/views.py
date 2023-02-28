from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .models import Occupation, Task, UserTask
from .forms import OccupationForm
from decouple import config

from static.py.utils import billing_period, format_dates

CUTOFF_DAY = config('CUTOFF_DAY', cast = int)
[today, lower_date] = billing_period(CUTOFF_DAY)

# Create your views here.
@login_required
def home(request):
    occupations = list_occupations(request, today)
    tasks = list_user_active_tasks(request)

    context = {
        'cutoff_day': CUTOFF_DAY, # To share the CUTOFF_DAY environment variable with the JavaScript scripts
        'occupations': occupations,
        'tasks': tasks
    }
    
    form = OccupationForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        
        return redirect('home')
    
    context['form'] = form

    return render(request, 'home.html', context)

@login_required
def record(request):
    occupations = list_occupations(request, lower_date)
    dates = list_unique_dates(request, lower_date)

    context = {
        'cutoff_day': CUTOFF_DAY, # To share the CUTOFF_DAY environment variable with the JavaScript scripts
        'occupations': occupations,
        'dates': dates
    }
    
    form = OccupationForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        
        return redirect('record')
    
    context['form'] = form

    return render(request, 'record.html', context)

def list_occupations(request, day):
    occupations = Occupation.objects.filter(users = request.user.id, date__gte = day).order_by('-date', '-start_time')
    occupations = format_dates(occupations) # Adjusts the format of date and time fields

    return occupations

def list_unique_dates(request, day):
    dates = list(set(Occupation.objects.filter(users = request.user.id, date__gte = day).order_by('-date').values_list('date', flat = True)))

    return dates

def list_user_active_tasks(request):
    user_tasks_ids = UserTask.objects.filter(users = request.user.id, is_active = True).values_list('id', flat = True)
    tasks = Task.objects.filter(id__in = user_tasks_ids, is_active = True)

    return tasks

@login_required
def edit_occupation(request, id):
    occupation = Occupation.objects.get(id = id)
    form = OccupationForm(request.POST or None, instance = occupation)
    
    if form.is_valid():
        form.save()
        
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return redirect('home')

    context = {
        'cutoff_day': CUTOFF_DAY, # To share the CUTOFF_DAY environment variable with the JavaScript scripts
        'form': form
    }
        
    return render(request, 'edit_occupation.html', context)

def delete_occupation(request, id):
    occupation = Occupation.objects.get(id = id)
    occupation.delete()

    return redirect('home')

def logout(request):
    logout(request)
    
    return redirect('/')