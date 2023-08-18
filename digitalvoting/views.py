from django.shortcuts import render,redirect
from django.http import JsonResponse
from  onlinevoting.models import Candidate,Voter
from twilio.rest import Client
from dotenv import load_dotenv
from django.http import HttpResponse
from cryptography.fernet import Fernet
key=Fernet.generate_key()
load_dotenv()
import random
import logging
import json
import os
def login(request): #login render
    return render(request,'login.html')
def intro(request):
    return render(request,'intro.html')
def otp_verify(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})

        # Access the JSON data
        firstName = json_data.get('firstName')
        secondName = json_data.get('secondName')
        adhaarNumber = json_data.get('adhaarNumber')
        OTP = random.randint(1000001, 10000000)
        logger = logging.getLogger(__name__)
        logger.info(f"Phone number: {request.POST}")
        all_objects = Voter.objects.all()
        a=False
        for i in all_objects:
            if i.adhaar==adhaarNumber and i.firstName==firstName and i.lastName==secondName and i.voted==False and i.onlineVotingRight:
                phone=i.number
                account_sid = os.getenv('account_sid')
                auth_token =os.getenv('auth_token')
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                                        body=f'One time {OTP} valid for 5 minutes',
                                        from_=os.getenv('phNo'),
                                        to=phone
                                    )
                a=True
        if a==False:
            return JsonResponse({"verification":"faliure"})
        return JsonResponse({"verification": f"{OTP}"})
    
    return JsonResponse({"verification":"faliure"})

def create_candidate(request):   
    if request.method == 'POST':
        first_name = request.POST.get('fn')
        last_name = request.POST.get('ln')
        adhaar_number = request.POST.get('an')
        address_1 = request.POST.get('c')
        address_2 = request.POST.get('s')
        value1 = request.POST.get('v1')
        value2 = request.POST.get('v2')
        value3 = request.POST.get('v3')
        logger = logging.getLogger(__name__)
        logger.info(f"Phone number: {first_name}")
        all_objects = Voter.objects.all()
        all_objects2=Candidate.objects.all()
        a=False
        for i in all_objects:
            if i.adhaar==adhaar_number and i.firstName==first_name and i.lastName==last_name:
                a=True
            if a==True:
                for j in all_objects2:
                    if j.adhaar==adhaar_number:
                        a=False
        if a==False:
            return redirect("http://localhost:8000/form")
        new_candidate=Candidate(firstName=first_name,lastName=last_name,age="30",city=address_1,values=value1+' '+value2+' '+value3,adhaar=adhaar_number,number="+919989513832")
        new_candidate.save()  
        return redirect("http://localhost:8000/Success")
    
    return redirect("http://localhost:8000/form")
def set_cookie(request):
    if request.method == 'POST':
        logger = logging.getLogger(__name__)
       # logger.info(f"Phone number: {json.loads(request.body)}")
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})
        try:
            f=Fernet(key)
            adhaarNumber = json_data.get('adhaarNumber')
           # logger.info(f"Phone number: {adhaarNumber}+{f}")
            token=f.encrypt(adhaarNumber.encode())
            logger.info(f"Phone number: {adhaarNumber}+{f}+{token}")
            response = HttpResponse("Cookie set successfully!")  
            response.set_cookie('n', f'{token}', max_age=3600, secure=True, httponly=True)
            logger.info("Yaa encrypted")
        except:
            return HttpResponse("Error")
        return response
    return HttpResponse("Error")
def dynamicCandidates(request):
        # Get the JSON data from the request body
        # cookie validation vundalee
        # here I should get the keys also
    cookie_value = request.COOKIES.get('n', None)
    if cookie_value!=None :
            all_objects = Candidate.objects.all()
            a = {}
            for j, candidate in enumerate(all_objects):
                a[j] = {
                'firstName': candidate.firstName,
                'lastName': candidate.lastName,
                'values': candidate.values,
             }
            return render(request, 'voting.html', {'candidates': a})
    
    return redirect('http://localhost:8000/login')

def form(request):
    return render(request,'formC.html')
def Success(request):
    return render(request,'sucess.html')
def finalVoting(request):
    return render(request,'sucess.html')
