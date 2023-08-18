from django.urls import path 
from . import views
urlpatterns=[
    path("",views.intro,name="intro"),
     path("voting", views.dynamicCandidates, name="index"),
     path("login",views.login),
     path("candidatelogin",views.create_candidate),
     path("otp",views.otp_verify),
     path("form",views.form),
     path("Success",views.Success),
     path("tovote",views.finalVoting),
     path("setCookie",views.set_cookie),
]
