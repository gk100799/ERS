from django.shortcuts import render, redirect,HttpResponse  
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.dispatch import receiver
from .models import (Users,Events, Questions, SurResponse, Registers, Survey)
from django.db import connection
import datetime


# Create your views here

def logged(request):
    if request.session.get('11'):
        return True
    messages.info(request,"Please login first!")


@csrf_exempt 
def user_login(request):
    if request.session.get('11'):
        del request.session['11']
    if request.session.get('30'):    
        del request.session['30']
        # print(request.session['11'])
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cursor=connection.cursor()
        cursor.execute("SELECT password,is_admin FROM users WHERE username=%s",[username])
        context=cursor.fetchone()
        print(password, ' ', context)
        if password == context[0]:
            request.session[11]=username
            if not context[1]:
                request.session[30]=False
                return redirect('home/')
            request.session[30]=True
            return redirect('administrator/')
        else:
             messages.error(request,"Invalid username or password.")
    return render(request = request,
                template_name = "login.html/")



@csrf_exempt 
def homepage(request):
    if logged(request)==True:
        user1=request.session['11']
        print(user1)
        now = datetime.datetime.today().strftime ('%Y-%m-%d')

        upcoming = Events.objects.raw("SELECT * FROM events a WHERE date>=%s AND NOT EXISTS(SELECT * FROM registers e WHERE e.event_id=a.event_id AND e.user_id=%s)",(now,user1))
        
        upcomingR = Events.objects.raw("SELECT * FROM events a WHERE date>=%s AND EXISTS(SELECT * FROM registers e WHERE e.event_id=a.event_id AND e.user_id=%s)",(now,user1))
        
        registered = Survey.objects.raw("SELECT * FROM ers_survey WHERE username=%s AND date>=%s",(user1,now))
        
        sur = Survey.objects.raw("SELECT s.* FROM ers_survey s WHERE s.username=%s AND s.date<%s AND NOT EXISTS(SELECT * FROM sur_response r WHERE s.username=r.user_id AND s.eventid=r.event_id)",(user1,now))
        
        

        return render(request, "student.html", {'upcoming':upcoming, 'registered':registered, 'survey':sur, 'upcomingR':upcomingR,'user1':user1})  
    return redirect('/')


@csrf_exempt
def details1(request):
    if logged(request)==True:
        eventid=request.POST['event']
        request.session[12]=eventid
        return redirect('https://event-registration-and-survey.herokuapp.com/home/details')
    return redirect('/')
    
@csrf_exempt
def details(request):
    if logged(request)==True:
        eventid=request.session['12']
        user=request.session['11']
        event=Events.objects.raw("SELECT * FROM events WHERE event_id=%s",[eventid])
        return render (request, "event-des.html/",{'event':event})
    return redirect('/')

@csrf_exempt
def register(request):
    if logged(request)==True:
        #import ipdb; ipdb.set_trace()
        eventid=request.session['12']
        user=request.session['11']
        reg=Registers.objects.create(event_id=eventid,user_id=user)
        # reg.save()
        return redirect('https://event-registration-and-survey.herokuapp.com/home')
    return redirect('/')

@csrf_exempt
def details2(request):
    if logged(request)==True:
        eventid=request.POST['event']
        request.session[12]=eventid
        return redirect('https://event-registration-and-survey.herokuapp.com/home/details3')
    return redirect('/')


@csrf_exempt
def details3(request):
    if logged(request)==True:
        eventid=request.session['12']
        user=request.session['11']
        event=Events.objects.raw("SELECT * FROM events WHERE event_id=%s",[eventid])
        #if request.method=='POST':
        return render (request, "event-des1.html/",{'event':event})
    return redirect('/')

@csrf_exempt
def unregister(request):
    if logged(request)==True:
        eventid=request.session['12']
        user=request.session['11']
        cursor=connection.cursor()
        cursor.execute("DELETE FROM registers WHERE user_id=%s AND event_id=%s",(user,eventid))
        return redirect('https://event-registration-and-survey.herokuapp.com/home')
    return redirect('/')

@csrf_exempt
def survey1(request):
    if logged(request)==True:
        event_id=request.POST['event1']
        print(event_id)
        print("sdfsuydhf")
        request.session[13]=event_id
        return redirect('https://event-registration-and-survey.herokuapp.com/home/survey')
    return redirect('/')

@csrf_exempt
def survey(request):
    if logged(request)==True:
        event_id=request.session['13']
        print(event_id)
        user=request.session['11']
        questions=Questions.objects.raw("SELECT * FROM questions WHERE event_id=%s ORDER BY question_id",[event_id])
        cursor=connection.cursor()
        cursor.execute("SELECT count(*) FROM questions WHERE event_id=%s",[event_id])
        x=cursor.fetchone()
        n=x[0]
        print(n)
        if request.method == 'POST':
            if n==1:
                option1=request.POST.get('option1')
                print(option1)
                cursor=connection.cursor()
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,1,%s)',(user,event_id,option1))
                return redirect('https://event-registration-and-survey.herokuapp.com/home/')

            if n==2:
                option1=request.POST.get('option1')
                print(option1)
                option2=request.POST.get('option2')
                cursor=connection.cursor()
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,1,%s)',(user,event_id,option1))
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,2,%s)',(user,event_id,option2))
                return redirect('https://event-registration-and-survey.herokuapp.com/home/')
            if n == 3:
                option1=request.POST.get('option1')
                print(option1)
                option2=request.POST.get('option2')
                option3=request.POST.get('option3')
                cursor=connection.cursor()
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,1,%s)',(user,event_id,option1))
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,2,%s)',(user,event_id,option2))
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,3,%s)',(user,event_id,option3))
                return redirect('https://event-registration-and-survey.herokuapp.com/home/')
            
            if n == 4:
                option1=request.POST.get('option1')
                print(option1)
                option2=request.POST.get('option2')
                option3=request.POST.get('option3')
                option4=request.POST.get('option4')
                cursor=connection.cursor()
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,1,%s)',(user,event_id,option1))
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,2,%s)',(user,event_id,option2))
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,3,%s)',(user,event_id,option3))
                cursor.execute('INSERT INTO sur_response(user_id,event_id,question_id,response) VALUES (%s,%s,4,%s)',(user,event_id,option4))
                return redirect('https://event-registration-and-survey.herokuapp.com/home/')

        return render(request, "stud-survey.html/", {"questions":questions})
    return redirect('/')

@csrf_exempt
def logout_request(request):
    messages.info(request, "Logged out successfully!")
    return redirect("/")



 