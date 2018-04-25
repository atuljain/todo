from __future__ import unicode_literals

import sys,json
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import Context, RequestContext, loader
from django.template.loader import get_template, render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from models import Task
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def index(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            context = {}
            template = loader.get_template('login.html')
            return HttpResponse(template.render(context,request))
        if request.method == 'POST':
            username = str(request.POST.get('username'))
            password = str(request.POST.get('password'))
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/home')
                else:
                    return HttpResponse(json.dumps({
                        "status": "error",
                        "message": "Invalid Username or password."
                    }))
            else:
                return HttpResponse(json.dumps({
                    "status": "error",
                    "message": "Provide username or password."
                }))
    else:
        return HttpResponseRedirect('/home')

@login_required
def app_logout(request):
    logout(request)
    response = HttpResponseRedirect('/')
    return response

@login_required
def home(request):
    if request.method == 'GET':
        order_by = request.GET.get('order_by')
        search_title = request.GET.get('search_title')

        if search_title:
            tasks = Task.objects.filter(title__startswith=search_title).exclude(state='delete')
        elif order_by:
            tasks = Task.objects.all().order_by(order_by).exclude(state='delete')
        else:
            tasks = Task.objects.all().exclude(state='delete')
        paginator = Paginator(tasks, 5)
        page = request.GET.get('page')
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tasks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tasks = paginator.page(paginator.num_pages)
        context = {
            'tasks':tasks,
            'state':['pending'],
            'host':request.META['HTTP_HOST']
            }
        template = loader.get_template('home.html')
        return HttpResponse(template.render(context, request))
    if request.method == 'POST':
        title = request.POST.get("title", 0)
        if len(title)  == 0:
            return HttpResponse(json.dumps({
                'status': 'ok',
                'message': 'Our support team will get back to you.'
            }))
        parent_task = request.POST.get("parent_task", "")
        due_date = request.POST.get("due_date", "")
        if parent_task:
            parent = Task.objects.get(id=parent_task)
            task = Task.objects.create(title=title,parent_task=parent,due_date=due_date,state="pending",user=request.user)
        else:
            task = Task.objects.create(title=title,due_date=due_date,state="pending",user=request.user)
        return HttpResponseRedirect('/home')

# Soft delete for task to make there state in delete 
@login_required
def task_delete(request):
    if request.method == 'POST':
        task_id = request.POST.get("task_id")
        if task_id:
            try:   
                task = Task.objects.get(id=task_id)
                task.state='delete'
                task.save()
                return HttpResponseRedirect('/home')
            except:
                return HttpResponse("Task id is not found")
        else:
            return HttpResponse("Task id is null")


def permannat_delete_task():
    # today datetime object
    today = datetime.datetime.now()
    # get 15 days before date
    old = today-timedelta(days=15)
    # delete those task which is updated to delete state before old date
    task = Task.objects.filter(updated_at__lte=today,state='delete').delete()
    return 'deleted'
