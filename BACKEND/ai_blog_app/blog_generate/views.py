
from django.shortcuts import render,redirect
# We import render() to send an HTML page as a response to the browser.
# redirect is used in Django to navigate the user to another URL after an action is completed.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


from django.contrib.auth.decorators import login_required
# "contributed modules" (built-in extra features)
# This decorator is used to allow only logged-in users to access a page.
# login_required redirects unauthenticated users to LOGIN_URL, which is a Django setting written in capital letters because it is a configuration constant.

from django.views.decorators.csrf import csrf_exempt
# You are importing a decorator that turns OFF CSRF protection for a view.
# Django normally checks every POST request for a CSRF token. soo disable it coz javascript does not generate csrf token
# It disables CSRF security check for that view.
# No CSRF check → request allowed directly
# JavaScript usually does not send CSRF token automatically.
# Because sometimes CSRF protection is not practical or not needed (especially in APIs).


from django.http import JsonResponse
# It is used to send data from Django backend → frontend in JSON format.

import json




# Create your views here.(it is a function)
# We pass request to the function, but it is not just a normal argument — it is an object.
# Request is an object that contains user data sent from browser to Django server.
@login_required
def index(request):
    
    return render(request,'FRONTEND/index.html') # Here Template Engine Starts To Search For The HTML file

#render() finds the HTML template, processes it, and sends its content as an HTTP response—not the template name string."


@csrf_exempt
def generate_blog(request):

    if request.method=="POST":
        
        try:
            data=json.loads(request.body)
            # This line reads data sent from frontend (request) and converts it into a Python dictionary.

            links_yt=data['link']

            return JsonResponse({'content':links_yt})
        
        except(KeyError,json.JSONDecodeError):
            # KeyError----Happens when key does not exist in dictionary.
            # JSONDeocdeError-----Happens when JSON data is invalid.
            return JsonResponse({'error':'Invalid data sent'},status=400)
        

        #get yt title
        
        #get transcript

        #use OpenAI to generate the blog

        #save blog article to database

        # return blog article as a response



    else:
        return JsonResponse({'error':'Invalid Request Method'},status=405)


def user_login(request):

    if request.method=='POST': #here post mean user click submit----POST means data is sent to the server when user submits something.

        username=request.POST['username']  
        # is used to get data sent from a form when user submits it using POST method.
        password=request.POST['password']

        #Checking Datbase Matching or Not....
        user=authenticate(request, username=username ,password=password)

        if user is not None:

            login(request,user)
            # request helps Django check user session, security, and authentication process properly.

            return redirect('/')
        
        else:
            error_message='Invalid Username Or Password'

            return render(request,'FRONTEND\login.html',{'error_message': error_message})

        


    

    return render(request,'FRONTEND\login.html')


def user_signup(request):

# request.POST is used in Django to access form data sent using the POST method.

    if request.method=='POST':

        username= request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirm_password']

        # checking the password and confirm_password are same are not then saves the user and logged in
        if password==confirmpassword:
            
            try:

                #  Create user and save password in database ORM Runs Here to store data automatically
                # create_user() creates a new record (row) in the User table, not a column.
                user=User.objects.create_user(username,email,password)
                user.save()

                #  Auto login
                login(request,user) 

                #  Redirect to home
                return redirect('/')
            
            except:
                error_message='Errorn In Creating The Account'

                return render(request,'FRONTEND\Signup.html',{'error_message':error_message})


        else:
           error_message='Password Not Matched'

           return render(request,'FRONTEND\Signup.html',{'error_message':error_message}) # here we render again the page to show the error



    return render(request,'FRONTEND\Signup.html')





def user_logout(request):

    logout(request)

    return redirect("/")


