from django.shortcuts import render


# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth,Group
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone

from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.decorators import api_view,parser_classes
# Create your views here.
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def login ( request ) :
   return Response({"status":False,"message":"noooooooooo"})
    # print("this is, next=",request.GET.get('next'))
    # if request.method == 'POST' :
    #    username = request . POST [ 'username' ]
    #    password = request . POST [ 'password' ]
    #    user = auth.authenticate( username=username , password = password)
    #    if user is not None :
    #        auth.login (request,user )
    #        print("valid user")
    #        uname=request.user.get_username()
    #        if len(uname)>8:
    #                 uname=uname[0:7]
    #                 uname=uname+".."
    #        request.session['uname']=uname
    #        nm=request.session['uname']
    #        print(nm)
         
    #        #print(request. META['HTTP_REFERER'])
          
    #        """if request. META['HTTP_REFERER']:
    #             h=request. META['HTTP_REFERER']
    #             r=h.split("=")
    #             print(r)
    #             print("have a next parameter")
    #             return redirect (r[1]) """
    #        if request.POST.get("next"):
    #             print(request.POST.get("next")) 
               
             
    #             return redirect (request.POST.get("next"))
    
          
    #        return redirect ( "main" )

           
    #    else :
    #         print("invalid user")
    #         messages.info ( request , ' invalid credentials ' )
    #         return redirect( 'login' )
    # return render ( request , 'accounts/login.html' )



def logout(request):
    auth.logout(request)
    return redirect("main")