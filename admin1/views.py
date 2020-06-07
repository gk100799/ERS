from django.shortcuts import render
from ers.models import (Users,Events, Questions, SurResponse, viewresponse,count,Response)
from django.shortcuts import render, redirect,HttpResponse  
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import datetime
from django.db import connection
from django.conf import settings
from django.http import JsonResponse
from django.core import serializers
import json


# Create your views here.
def adminpage(request):
    now = datetime.datetime.today().strftime ('%Y-%m-%d')
    print(now)
    events=Events.objects.raw("SELECT * FROM events WHERE date>=%s",[now])
    survey=Events.objects.raw("SELECT * FROM events WHERE date<%s",[now])
    students=Users.objects.raw("SELECT * FROM users")
    return render(request, "admin.html", {'events':events,'survey':survey,'students':students})


@csrf_exempt
def createevent(request):
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        data = request.POST
        id1 = request.POST['event_id']
        event_name = data['event_name']
        description = data['description']
        organizers = data['organizers']
        venue = data['venue']
        time = data['time']
        limit = data['limit']
        fee = data['fee']
        date = data['date']
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO events (event_id,event_name,description,organizers,venue,limit_max,fee,time,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (id1,event_name,description,organizers,venue,limit,fee,time,date))
            messages.success(request, 'Successfully created the Event !')
        return redirect("https://event-registration-and-survey.herokuapp.com/administrator/#events")
    #return render(request, "event-create (Final).html")
    return render(request = request,
                template_name = "event-create (Final).html/")




@csrf_exempt
def modifyevent1(request):
    #import ipdb; ipdb.set_trace()
    context = {}
    event_id = request.POST.get('editevent',None)
    request.session[0]=event_id
    return redirect('https://event-registration-and-survey.herokuapp.com/administrator/edit-event')
 
@csrf_exempt
def modifyevent(request):
    eventid=request.session['0']
    print(eventid)
    event=Events.objects.raw("SELECT * FROM events WHERE event_id=%s",[eventid])
    #print(event.event_name)
    #import ipdb; ipdb.set_trace() 
    print(event) 
    if request.method == 'POST':
        data = request.POST
        id1 = request.POST['event_id']
        event_name = data['event_name']
        description = data['description']
        organizers = data['organizers']
        venue = data['venue']
        time = data['time'] 
        limit = data['limit']
        fee = data['fee']
        date = data['date']
        with connection.cursor() as cursor:
            cursor.execute("UPDATE events SET event_id=%s,event_name=%s,description=%s,organizers=%s,venue=%s,time=%s,limit_max=%s,fee=%s,date=%s WHERE event_id=%s",(id1,event_name,description,organizers,venue,time,limit,fee,date,id1))  
        messages.success(request, 'Successfully modified the Event !')
        return redirect("https://event-registration-and-survey.herokuapp.com/administrator/#events")
    #return render(request, "event-create (Final).html")
    return render(request,"modify.html/", {'event':event})


@csrf_exempt
def deleteevent(request):
    eventid=request.POST['delete']
    cursor=connection.cursor()
    cursor.execute("DELETE FROM registers WHERE event_id=%s",[eventid])
    cursor.execute("DELETE FROM questions WHERE event_id=%s",  [eventid])
    cursor.execute("DELETE FROM sur_response WHERE event_id=%s",  [eventid])
    cursor.execute("DELETE FROM events WHERE event_id=%s",[eventid])
    messages.success(request, 'Succesfully deleted the event',)
    return redirect("https://event-registration-and-survey.herokuapp.com/administrator/#events")

@csrf_exempt
def createsurvey1(request):
    eventid = request.POST.get('editsurvey',None)
    request.session[2]=eventid
    return redirect('https://event-registration-and-survey.herokuapp.com/administrator/edit-survey')

@csrf_exempt 
def createsurvey(request):
    eventid=request.session['2']
    print(eventid)
    survey=Questions.objects.raw("SELECT * FROM questions WHERE event_id=%s ORDER BY question_id ",[eventid])
    #if request.method == 'POST':
    return render(request,"survey-creation.html/", {'survey':survey})

@csrf_exempt    
def addsurvey(request):
    eventid=request.session['2']
    data=request.POST
    question=data['q1']
    questionid=data['question_id']
    op1=data['op1']
    op2=data['op2']
    op3=data['op3']
    op4=data['op4']
    cursor=connection.cursor()
    cursor.execute("CALL insques(%s,%s,%s,%s,%s,%s,%s);",(eventid,questionid,question,op1,op2,op3,op4))
    #cursor.execute("INSERT INTO questions(event_id,question_id,question,option1,option2,option3,option4) VALUES (%s,%s,%s,%s,%s,%s,%s)",(eventid,questionid,question,op1,op2,op3,op4))
    return redirect("https://event-registration-and-survey.herokuapp.com/administrator/edit-survey")


@csrf_exempt
def deletequestion(request):
    if request.method == 'POST':
        #import ipdb; ipdb.set_trace()
        eventid = request.session['2']
        questionid = request.POST['delete']
        print(questionid,eventid ,"is it")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM questions WHERE question_id=%s AND event_id=%s", (questionid, eventid))
        messages.success(request, 'Succesfully deleted the question')
        return redirect("https://event-registration-and-survey.herokuapp.com/administrator/edit-survey")



@csrf_exempt
def registrants1(request):
    request.session[5]=request.POST['registrants']
    return redirect("https://event-registration-and-survey.herokuapp.com/administrator/registrants")
 


@csrf_exempt
def registrants(request):
    eventid=request.session['5']
    print(eventid)
    students=Users.objects.raw("SELECT u.*, r.event_id, r.registered_on FROM users u JOIN registers r ON u.username=r.user_id AND event_id=%s",[eventid])
    cursor = connection.cursor()
    cursor.execute("SELECT count FROM count WHERE event_id=%s",[eventid])
    count=cursor.fetchone()
    if count:
        count=count[0]
        print(count)
        return render(request,"stud-list.html",{'students':students,'count':count})
    else:
        messages.info(request,"No students registered yet!")
        return redirect('https://event-registration-and-survey.herokuapp.com/administrator/#events')


@csrf_exempt
def response1(request):
    request.session[4]=request.POST['responseid']
    print(request.session[4])
    return redirect("https://event-registration-and-survey.herokuapp.com/administrator/response")


def merge(list1, list2): 
      
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
    return merged_list 

@csrf_exempt 
def response(request):
    #import ipdb; ipdb.set_trace()
    eventid=request.session['4']
    #return render(request, "survey-results-display.html",test1={'events':test})
    cursor=connection.cursor()


    cursor.execute("SELECT option,count,TRUNC(percent,2) as percent  FROM response WHERE event_id=%s and question_id=1",[eventid])
    options1 = cursor.fetchall()
    option1=list(map(list, options1))
    print(option1)

    cursor.execute("SELECT option,count,TRUNC(percent,2) as percent  FROM response WHERE event_id=%s and question_id=2",[eventid])
    options2 = cursor.fetchall()
    option2=list(map(list, options2))
    print(option2)

    cursor.execute("SELECT option,count,TRUNC(percent,2) as percent  FROM response WHERE event_id=%s and question_id=3",[eventid])
    options3 = cursor.fetchall()
    option3=list(map(list, options3))
    print(option3)

    cursor.execute("SELECT option,count,TRUNC(percent,2) as percent  FROM response WHERE event_id=%s and question_id=4",[eventid])
    options4 = cursor.fetchall()
    option4=list(map(list, options4))
    print(option4)

    cursor.execute("SELECT question FROM questions WHERE event_id=%s ORDER BY question_id ASC",[eventid])
    questions=cursor.fetchall()
    questions1=list(map(list, questions))
    print(questions1)
    return render(request, "survey-results-display.html",{'events':questions,'options1':options1,'options2':options2,'options3':options3})
    

@csrf_exempt
def addstudent(request):
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        data = request.POST 
        username=data['usn']
        email=data['email']
        password=data['password']
        firstname=data['firstname']
        lastname=data['lastname']
        #is_staff=data['is_staff']
        phone=data['phone']
        branch=data['branch']
        with connection.cursor() as cursor:
            #cursor.execute("INSERT INTO ers_admin(username,email,password,first_name,last_name,phone) VALUES (%s,%s,%s,%s,%s,%s)", (username,email,password,firstname,lastname,phone))
            cursor.execute("INSERT INTO users(username,email,password,first_name,last_name,branch,phone) VALUES (%s,%s,%s,%s,%s,%s,%s)", (username,email,password,firstname,lastname,branch,phone))
        print(connection.queries)
        messages.success(request,'Student added successfully!')
        return redirect("https://event-registration-and-survey.herokuapp.com/administrator/#students")
    return render(request = request,
                template_name = "create-student.html/")


    
    
@csrf_exempt 
def modifystudent1(request):
    #import ipdb; ipdb.set_trace()
    context = {}
    username = request.POST.get('editstudent',None)
    request.session[1]=username
    return redirect('https://event-registration-and-survey.herokuapp.com/administrator/edit-student')



@csrf_exempt
def modifystudent(request):
    studentid=request.session['1']
    print(studentid)
    user=Users.objects.raw("SELECT * FROM users WHERE username=%s",[studentid])
    #print(event.event_name)
    #import ipdb; ipdb.set_trace() 
    print(user)
    if request.method == 'POST':
        data=request.POST
        username=data['usn']
        email=data['email']
        password=data['password']
        firstname=data['firstname']
        lastname=data['lastname']
        #is_staff=data['is_staff']
        phone=data['phone']
        branch=data['branch']
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET username=%s,email=%s,password=%s,first_name=%s,last_name=%s,phone=%s,branch=%s WHERE username=%s",(username,email,password,firstname,lastname,phone,branch,username))  
        messages.success(request, 'Successfully modified the Event !')
        return redirect("https://event-registration-and-survey.herokuapp.com/administrator/#students")
    #return render(request, "event-create (Final).html")
    return render(request,"modify-student.html/", {'user':user})


    
@csrf_exempt
def deletestudent(request):
    studentid=request.POST['delete']
    print(studentid +' is deleted')
    cursor=connection.cursor()
    cursor.execute("DELETE FROM users WHERE username=%s",[studentid])
    messages.success(request, 'Succesfully deleted student')
    return redirect("https://event-registration-and-survey.herokuapp.com/administrator/#students")