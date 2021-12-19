from logging import log
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.contrib import messages
from firebase_admin import storage
import os

from pyrebase.pyrebase import Auth
###############


firebaseConfig = {
    'apiKey': "AIzaSyAHzA488bj7dLD28vnLFqOHSOk-hKh9XiA",
    'authDomain': "userprofile-ef6fa.firebaseapp.com",
    'projectId': "userprofile-ef6fa",
    'storageBucket': "userprofile-ef6fa.appspot.com",
    'messagingSenderId': "312343457692",
    'appId': "1:312343457692:web:2e0e345c2afd2f40456259",
    'measurementId': "G-NK1M19KN5S",
    'databaseURL':"https://userprofile-ef6fa-default-rtdb.firebaseio.com/"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
#cred = credentials.Certificate("/home/RoadwayExpress/onbusiness/userprofile-ef6fa-f44430a31c39.json")
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/RoadwayExpress/onbusiness/userprofile-ef6fa-f44430a31c39.json"

cred = credentials.Certificate("/home/yuvaraj/algofocus/onbusiness/userprofile-ef6fa-f44430a31c39.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "userprofile-ef6fa-f44430a31c39.json"

firebase_admin.initialize_app(cred)

#################

# Create your views here.
def Login(request):
    if request.method =='POST':
        if 'login' in request.POST:
            try:
                email=request.POST['log_email']
                password=request.POST['log_password']
               
                

                #user = auth.create_user_with_email_and_password(email, password)
                #print(email)
                #print("Successfully logged in!")
                #localId = auth.get_account_info(user['idToken'])['users'][0]['localId']
                
                login = auth.sign_in_with_email_and_password(email, password)
                localId = auth.get_account_info(login['idToken'])['users'][0]['localId']
                request.session['localId']=localId
                request.session['session_mail']=email
                return redirect(Dashboard)
                #email = auth.get_account_info(login['idToken'])['users'][0]['email']
                #print(email)
            except:
                messages.info(request, 'Invalid email or password :(') 
                print("Invalid email or password")
                return redirect(Login)

        if 'register' in request.POST:
            username=request.POST['username']
            email=request.POST['email']
            password1=request.POST['password1']
            password2=request.POST['password2']
            if password1==password2:
                try:
                    user = auth.create_user_with_email_and_password(email, password1)
                    localId = auth.get_account_info(user['idToken'])['users'][0]['localId']

                    db = firestore.Client()
                    doc_ref = db.collection('users').document(email)
                    doc_ref.set({
                        "name": username,
                        "email":email,
                        "password":password1,
                        "localId":localId,
                        "DOB":"",
                        "address":"",
                        "profile":"https://www.pngfind.com/pngs/m/676-6764065_default-profile-picture-transparent-hd-png-download.png",
                    })
                    messages.info(request, 'Account created successfully :)') 
                    print("Account created")
                    return redirect(Login)
                except:
                    messages.info(request, 'Email already exist :(') 
                    print("mail exist")
                    return redirect(Login)

            else:
                messages.info(request, 'Password is not matching') 
                print("pass not matching")
                return redirect(Login)
                
    return render(request,'user_page/sign_up.html')
    
    #print("dashboard")
    
def forgot_password(request):
    
    if request.method =='POST':
        try:
            email=request.POST['reset_email']
            auth.send_password_reset_email(email)
            messages.info(request, 'Reset link will be send your mail')
            return redirect(Login)
        except:
            messages.info(request, 'Enter a valid email') 
            return redirect(Login)
    return render(request,'user_page/forgot_page.html')


def Dashboard(request):
    
    db = firestore.Client()
    localId=request.session['localId']
    mail=request.session['session_mail']
    
    storage=firebase.storage()
    #storage.child('/profiles/image').put(image)
    #links=storage.child('/profiles/image').get_url(localId)
    #and 'docfile' in request.FILES:
    print(auth.current_user)
    if request.method =='POST':
        if 'update' in request.POST:
            print('inner if')
            fname=request.POST['fname']
            dob=request.POST['dob']
            address=request.POST['address']
            email=request.POST['email']
            password=request.POST['password']

            if 'docfile' in request.FILES:
                profile_photo = request.FILES['docfile']
                name=str(profile_photo)
                storage.child(name).put(profile_photo)
                links=storage.child(name).get_url(localId)
            else:
                file=request.POST['file_name']
                print(file)
                links=file

            doc_ref = db.collection('users').document(mail)
            doc_ref.set({
                "name": fname,
                "localId":localId,
                "DOB":dob,
                "email":email,
                "password":password,
                "address":address,
                "profile":links,
            })
            messages.info(request, 'Your details are updated') 
            data={'DOB': dob, 'profile': '', 'name': fname, 'address': address,'email':email,"profile":links}
            return render(request,'user_page/dashboard.html',{"details":data})
    print('outer')
    doc_ref = db.collection('users').where("localId","==",localId).stream()
    details={}
    for doc in doc_ref:
        details = doc.to_dict()
    '''
    except KeyError as e:
        details=None
        messages.info(request, 'Please login with valid account')
        return redirect(Login) 
        
    '''
    return render(request,'user_page/dashboard.html',{"details":details})


def signout(request):
   
    try:
        del request.session['localId']
        del request.session['session_mail']
        messages.info(request, 'Bye! Bye!')
        return redirect(Login)
    except KeyError:
        return redirect(Login)
     
    





'''
  var storage = firebase.storage();
  var file=document.getElementById("files").files[0];
  var storageref=storage.ref();
  var thisref=storageref.child(file.name).put(file);
  thisref.on('state_changed',function(snapshot) {
  console.log('Done');
'''