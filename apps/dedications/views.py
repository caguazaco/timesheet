from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .models import Occupation, Task, UserTask
from .forms import OccupationForm
from decouple import config

from static.py.utils import billing_period, format_dates

CUTOFF_DAY = config('CUTOFF_DAY', cast = int)
[lower_date, today] = billing_period(CUTOFF_DAY)

# Create your views here.
@login_required
def home(request):
    occupations = list_occupations(request.user, today)
    tasks = list_user_active_tasks(request.user)

    if request.method == 'GET':
        context = {
            'cutoff_day': CUTOFF_DAY, # To share the CUTOFF_DAY environment variable with the JavaScript scripts
            'occupations': occupations,
            'tasks': tasks
        }
    else:
        form = OccupationForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('home')
        else:
            context['form'] = form
    
    return render(request, 'home.html', context)

@login_required
def record(request):
    occupations = list_occupations(request.user, lower_date)
    
    context = {
        'cutoff_day': CUTOFF_DAY, # To share the CUTOFF_DAY environment variable with the JavaScript scripts
        'occupations': occupations
    }

    return render(request, 'record.html', context)

def list_occupations(user, day):
    occupations = Occupation.objects.filter(users = user.id, date__gte = day).order_by('-date', '-start_time')
    occupations = format_dates(occupations) # Adjusts the format of date and time fields

    dates = list(set(Occupation.objects.filter(users = user.id, date__gte = day).order_by('-date').values_list('date', flat = True)))

    return occupations

def list_user_active_tasks(user):
    user_tasks_ids = UserTask.objects.filter(users = user.id, is_active = True).values_list('tasks_id', flat = True).distinct()
    tasks = Task.objects.filter(id__in = user_tasks_ids, is_active = True)

    return tasks

@login_required
def edit_occupation(request, id):
    occupation = Occupation.objects.get(id = id)
    selected_task = Task.objects.get(id = occupation.tasks.id)
    other_tasks = list_user_active_tasks(request.user).exclude(id = occupation.tasks.id)
    
    if request.method == 'GET':
        form = OccupationForm(instance = occupation)
        
        context = {
            'cutoff_day': CUTOFF_DAY, # To share the CUTOFF_DAY environment variable with the JavaScript scripts
            'form': form,
            'selected_task': selected_task,
            'other_tasks': other_tasks
        }
    else:
        form = OccupationForm(request.POST, instance = occupation)
        
        if form.is_valid():
            form.save()
            
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return redirect('home')
        else:
            context = {
                'cutoff_day': CUTOFF_DAY, # To share the CUTOFF_DAY environment variable with the JavaScript scripts
                'form': form,
                'selected_task': selected_task,
                'all_tasks': other_tasks
            }
        
    return render(request, 'edit_occupation.html', context)

def delete_occupation(request, id):
    occupation = Occupation.objects.get(id = id)
    occupation.delete()

    return redirect('home')

def logout(request):
    logout(request)
    
    return redirect('/')