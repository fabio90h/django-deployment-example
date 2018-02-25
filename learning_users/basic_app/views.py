from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm, UserForm

#for Login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(required):
    return HttpResponse("Successfully logged in!")

@login_required #this will make a user that is currently logged in to logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') #grabs the input from username
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user: #if there is a user
            if user.is_active: #if the user has an active account
                login(request,user)  #perform login
                return HttpResponseRedirect(reverse('index')) #send user to index
            else:
                return HttpResponse("Account Not Active") #send message
        else:
            print('Someone tried to login and failed')
            print('Username: {} and password {}' .format(username,password))
            return HttpResponse('invalid login details supplied')
    else:
        return render(request, 'basic_app/login.html')


def registration(request):

    register = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST) #Puts out username email and password from forms.py
        profile_form = UserProfileInfoForm(data=request.POST) #For the portfolio_site and profile_pic

        if user_form.is_valid() and profile_form.is_valid():
            #for user_form
            user = user_form.save() #save inputs
            user.set_password(user.password) #hashing the password
            user.save()
            #for profile_form
            profile = profile_form.save(commit=False) #dont comit to the data base yet to avoid colission
            profile.user = user #one to one

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            register = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'basic_app/registration.html', {'user_form':user_form, 'profile_form':profile_form, 'register': register})
