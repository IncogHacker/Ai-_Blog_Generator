
from django.core import exceptions
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

from pytube import YouTube


from django.conf import settings
# It lets you access your Django project settings (settings.py) inside your code.

from openai import OpenAI
import json
import os
import assemblyai as aai  
#as aai gives a short nickname (alias) to the module.
# ✅ AssemblyAI is a speech AI service that converts voice/audio into text using artificial intelligence.



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

            print(f"Your Link is--{links_yt}")

            # return JsonResponse({'content':links_yt})
        
        except(KeyError,json.JSONDecodeError):
            # KeyError----Happens when key does not exist in dictionary.
            # JSONDeocdeError-----Happens when JSON data is invalid.

            
            return JsonResponse({'error':'Invalid data sent'},status=400)
        
            

        #get yt title
        Store=youtube_get_Link_data(links_yt)
        # print(f"Your Title is {Store}")
        
        #get transcript
        after_transcribe=get_transcription(links_yt)
        if not after_transcribe:
            return JsonResponse({'error':"Failed To get Transcript"},status=500)

        #use OpenAI to generate the blog
        generated_blog = generate_blog_from_transcriber(after_transcribe)
        if not generated_blog:
           return JsonResponse({'error':"Failed To Generate The Blog Article"},status=500)
        

        #save blog article to database

        # return blog article as a response
        return JsonResponse({'content':generated_blog})



    else:
        return JsonResponse({'error':'Invalid Request Method'},status=405)
    
#--------------------------------------------------------------------------------------------------------------------------------------------

# Getting Youtube link Data like title ,stream,views,thumbnail etc.....


def youtube_get_Link_data(link):

    try:

       Store_link = YouTube(link) # Creates YouTube object with video data.

       print(f"pytube_is_working--{Store_link}\n")

       Title_yt=Store_link.title

       print(f"Title is fetched --{Title_yt}")

       return Title_yt 
    
    except Exception as e:
        print(f"Your error in Get_link_Data----{e}")

        return None

    

# ---------------------------------------------------------------------------------------------------------------------------------------------
#Here we Are getting vedio to Audio to text speech 
def download_audio(link):

    try:
        
        Store_link = YouTube(link)
        
        audio=Store_link.streams.filter(only_audio=True).first()
        # This gets the audio stream (sound only) from a YouTube video using PyTube and first means format which is available at the top.

        out_file=audio.download(output_path=settings.MEDIA_ROOT)
        # This downloads the audio file and saves it in your media folder.

        # audio.download() → downloads file

        # output_path → where to save file

        # settings.MEDIA_ROOT → your media folder path

        
        base, ext=os.path.splitext(out_file)

        new_file=base + '.mp3'
        os.rename(out_file ,new_file)

        return new_file
    
    except Exception as e:

        print(f"Audio text is Not Generating----{e}")
        



def get_transcription(link):

    try:
            audio_file=download_audio(link)

            print(f"Here is audio_file After Download--{audio_file}\n")

            if not audio_file:
                return None

            #setting API key of Assembly Ai
            aai.settings.api_key=os.environ.get("ASSEMBLY_API_KEY")

            if not os.environ.get("ASSEMBLY_API_KEY"):
                print("Assembly Key Is Not present")
                return None
            # It sets your AssemblyAI API key so your program can use AssemblyAI services.
            # aai → AssemblyAI library

            # settings.api_key → where AssemblyAI stores your API key

            # You are giving the key to AssemblyAI.



            # Creates a Transcriber object.
            transcriber=aai.Transcriber()
            # Transcriber = machine that converts speech to text
            # It has methods like:

            # .transcribe()

            # .upload()

            # .submit()

            transcript=transcriber.transcribe(audio_file)
            # This tells AssemblyAI:--Convert audio to text

            return transcript.text
    
    except Exception as e:
        print(f"Transcription Error--{e}")

# ---------------------------------------------------------------------------------------------------------------------------------
#Transcript → Prompt → OpenAI → Blog content → Return

def generate_blog_from_transcriber(transcript):

    client=OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    if not os.environ.get("OPENAI_API_KEY"):
        print("OPEN_API--KEY --NOT FOUND")
        return None
    # System → get API key → connect OpenAI → store in client

    prompt=f"Based On th following transcript from a Youtube Video, write a comphrensive blog article, write it based on transcript but dont make it look like a youtube vedio make it look like a blog article:\n\n{transcript}\n\n Article"

    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=1000  #1000 tokens ≈ ~700–800 words.

    )

    return response.choices[0].message.content


#-----------------------------------------------------------------------------------------------------------------------------------


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

            return render(request,'FRONTEND/login.html',{'error_message': error_message})

        


    

    return render(request,'FRONTEND/login.html')


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

                return render(request,'FRONTEND/Signup.html',{'error_message':error_message})


        else:
           error_message='Password Not Matched'

           return render(request,'FRONTEND/Signup.html',{'error_message':error_message}) # here we render again the page to show the error



    return render(request,'FRONTEND/Signup.html')





def user_logout(request):

    logout(request)

    return redirect("/")


