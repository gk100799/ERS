from django.contrib.auth.models import User
from django.shortcuts import render, redirect,HttpResponse  
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.decorators import login_required
from .models import (ERSEvent, ERSQuestion, ERSSurvey)
from django.db import connection
# Create your views here.
# def index(request):
#     # import ipdb; ipdb.set_trace()
#     return render(request, "addUser.html")
 

    #@csrf_exempt
def addUser(request):
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        data = request.POST 
        username=data['username']
        email=data['email']
        password=data['password']
        firstname=data['firstname']
        lastname=data['lastname']
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.is_staff=True
        user.save()
        print(connection.queries)
        return HttpResponse("Hurray!! You're registered!")
    return render(request = request,
                template_name = "addUser.html/")


    #adduser = ERSUser.objects.create(username=data['username'], password=data['password'], email=data['email'], firstname=data['firstname'], lastname=data['lastname'], branch=data['branch'], phone=data['phone'])
    #adduser.save()

# def loginpage(request):
#     return render(request, "login.html")
@csrf_exempt
def user_login(request):
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User= authenticate(request,username=username, password=password)
        print(connection.queries)
        if User is not None:
            login(request, User)
            if not User.is_staff:
                return redirect('home/')
            return redirect('admin1/')
        else:
             messages.error(request,"Invalid username or password.")
    return render(request = request,
                template_name = "login.html/")


# def login_request(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             #username = request.POST('username')
#             #password = request.POST('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)

#                 messages.info(request, f"You are now logged in as {username}")
#                 return redirect('home/')
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request = request,
#                     template_name = "login.html/",
#                     context={"form":form})


@login_required(login_url='/')
def homepage(request):
    return render(request, "student.html")  

@login_required(login_url='/')
def adminpage(request):
    return render(request, "admin.html")
       
@login_required(login_url='/')
def gaandupage(request):
    return render(request, "event-create (Final).html")

@login_required(login_url='/')
@csrf_exempt
def createevent(request):
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        data = request.POST
        id1 = request.POST.get('event_id')
        event_name = data.get('event_name')
        description = data.get('description')
        organizers = data.get('organizers')
        venue = data.get('venue')
        time = data.get('time')
        limit = data.get('limit')
        fee = data.get('fee')
        date = data.get('date')
        question = ERSEvent(id = id1, event_name = event_name, description = description, organizers = organizers, venue = venue, time = time, limit = limit, fee = fee, date = date)
        question.save()
        return HttpResponse("<h1 style='color:red'>Hurray!! Event created</h1>")
    #return render(request, "event-create (Final).html")
    return render(request = request,
                template_name = "event-create (Final).html/")   


@login_required(login_url='/')
@csrf_exempt
def modifyevent(request):
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        data = request.POST
        id1 = request.POST.get('event_id')
        event_name = data.get('event_name')
        description = data.get('description')
        organizers = data.get('organizers')
        venue = data.get('venue')
        time = data.get('time')
        limit = data.get('limit')
        fee = data.get('fee')
        date = data.get('date')
        question = ERSEvent(id = id1, event_name = event_name, description = description, organizers = organizers, venue = venue, time = time, limit = limit, fee = fee, date = date)
        question.save()
        return HttpResponse("Hurray!! Event edited")
    #return render(request, "event-create (Final).html")
    return render(request = request,
                template_name = "modify.html/") 



def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")


# @receiver(user_logged_in)
# def sig_user_logged_in(sender, user, request, **kwargs):
#     request.session['isLoggedIn'] = True
#     request.session['isAdmin'] = user.is_superuser
#     #request.session['team'] = user.teams
#     request.session['username'] = user.username
#     isLoggedIn = request.session.get('isLoggedIn',False)
#     isAdmin = request.session.get('isAdmin',False)
#     # team =request.session.get('team','')
#     username = request.session.get('username','')
#     return render(
#         request,
#         'login.html',
#         context = {'isLoggedIn':isLoggedIn,'isAdmin':isAdmin,'username':username},
#     )