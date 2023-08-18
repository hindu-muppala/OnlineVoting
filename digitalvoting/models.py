from django.db import models

# Create your models here.
class Candidate(models.Model):
    firstName=models.CharField(max_length=30)
    lastName=models.CharField(max_length=30,null=True)
    age=models.IntegerField()
    city=models.CharField(max_length=30,null=True)
    adhaar=models.CharField(max_length=30,null=True)
    number=models.CharField(max_length=12,default='+919989513832')
    noOfVotes=models.IntegerField(default=0)
    manifesto=models.JSONField(null=True)

class Voter(models.Model):
    firstName=models.CharField(max_length=30)
    lastName=models.CharField(max_length=30,null=True)
    adhaar=models.CharField(max_length=30,null=True)
    onlineVotingRight=models.BooleanField(default=False)
    voted=models.BooleanField(default=False)
    candidateId=models.ForeignKey(Candidate,on_delete=models.CASCADE,null=True)
    number=models.CharField(max_length=12,default='+919989513832')
#Here what is primary key
#At a time a voter should have OTP
class OTP(models.Model):
    otp=models.IntegerField()
    voter=models.ForeignKey(Candidate,on_delete=models.CASCADE,unique=True)
    time=models.DateTimeField(auto_now_add=True)
class CITY(models.Model):
    name=models.CharField(max_length=20)
    pincode=models.IntegerField(unique=True)
class Area(models.Model):
    name=models.CharField(max_length=20)
class Event():
    name=models.CharField(unique=True)
    conductTimings=models.DateTimeField()
    

