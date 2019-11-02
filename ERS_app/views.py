from django.contrib.auth.models import User
from django.shortcuts import render, redirect,HttpResponse  
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    # import ipdb; ipdb.set_trace()
    return render(request, "addUser.html")


    #@csrf_exempt
def addUser(request):
    #import ipdb; ipdb.set_trace()
    data = request.POST
    username=data['username']
    email=data['email']
    password=data['password']
    firstname=data['firstname']
    lastname=data['lastname']
    user = User.objects.create_user(username, email, password)
    user.first_name = firstname
    user.last_name = lastname
    user.save()
    return HttpResponse("Hurray!! You're registered!")

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
        if User is not None:
            login(request, User)
            return redirect('home/')
        else:
             messages.error(request, "Invalid username or password.")
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
    return render(request, "home.html")   



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