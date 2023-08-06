from django.shortcuts import render,redirect
from django.db import connection
from django.contrib import messages as msg
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from .middleware import settoken
from .models import *
from . import models as m
from datetime import datetime
import re 
import jwt

#Patterns for validation
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
# username_pattern = r'^[a-zA-Z0-9_-]{3,16}$'

cursor=connection.cursor()


#Register
def register(request):
    if request.method =="POST":
        #requesting data from html page
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        password=request.POST.get("pass")
        
        #Searching if email is already registered or not
        cursor.callproc('SP_user_registry_get_by_email',[email])
        dup_res=cursor.fetchall()
        cursor.nextset()
        
        #Validation & duplicate handling
        if len(dup_res)==0:
            if re.match(email_pattern,email):
                if re.match(password_pattern,password):
                    hased_pass=make_password(password)
                    cursor.callproc('SP_user_registry_insert',[fname,lname,email,hased_pass])
                    cursor.nextset()
                    msg.success(request,"Registered Successfully")
                    return render(request,'login.html')    
                else:
                    msg.warning(request,"Password should be Aplha-numeric with atleast 1 uppercase character and no special character")
                    return render(request,'reg.html')
            else:
                msg.warning(request,"Invalid Email pattern")
                return render(request,'reg.html')
        else:
            msg.warning(request,"Email Already Exit")
            return render(request,'reg.html')
    else:
        return render(request,'reg.html')


#Login Authorization
def auth(request):
    if request.method =="POST":
        email=request.POST.get("email")
        password=request.POST.get("pass")
        
        #Email exist or not
        cursor.callproc('SP_user_registry_get_by_email',[email])
        res=cursor.fetchall()
        cursor.nextset()
        id =res[0][0]
        #Authenticating
        cursor.callproc('SP_Custom_token_get_by_user_id',[id])
        sign=cursor.fetchall()
        cursor.nextset()
        # print(sign)

        if len(sign)!=0:
            if sign[0][4]==None:        
                token=sign[0][2]
                settoken(token)
                return redirect("/todo")
            else:
                if len(res)!=0:
                    ret_id=res[0][0]#Retriving Id from 0th column
                    ret_name=res[0][1]#Retriving First Name from 1th column
                    ret_email=res[0][3]#Retriving email from 3rd column
                    ret_pass=res[0][4]#Retrivinf password from 4th column
                    # print(ret_pass)
                    if check_password(password,ret_pass):
                        
                        #Token Generation
                        payload={
                            'id':ret_id,
                            'email':ret_email,
                            'name':ret_name,
                            'time':datetime.utcnow().isoformat()
                        }
                        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                        settoken(token)

                        #inserting in sigin table
                        cursor.callproc('SP_Custom_token_signin_insert',[ret_id,token])
                        cursor.nextset()

                        return redirect ('/todo')
                    else:
                        msg.warning(request,'Invalid Password')
                        return render(request,'login.html')    
                else:
                    msg.warning(request,'Email is not registered')
                    return render(request,'login.html')
        else:
            if len(res)!=0:
                ret_id=res[0][0]#Retriving Id from 0th column
                ret_name=res[0][1]#Retriving First Name from 1th column
                ret_email=res[0][3]#Retriving email from 3rd column
                ret_pass=res[0][4]#Retrivinf password from 4th column
                print(ret_pass)
                if check_password(password,ret_pass):
                    
                    #Token Generation
                    payload={
                        'id':ret_id,
                        'email':ret_email,
                        'name':ret_name,
                        'time':datetime.utcnow().isoformat()
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    settoken(token)

                    #inserting in sigin table
                    cursor.callproc('SP_Custom_token_signin_insert',[ret_id,token])
                    cursor.nextset()

                    return redirect ('/todo')
                else:
                    msg.warning(request,'Invalid Password')
                    return render(request,'login.html')    
            else:
                msg.warning(request,'Email is not registered')
                return render(request,'login.html')    
    else:
        return render(request,"login.html")

def add_todo_page(request):
    verify_token=request.META.get('HTTP_AUTHORIZATION')
    if verify_token:
        try:
            jwt_token = verify_token.split(' ')[1]
            #Decoding JWT    
            decoded=jwt.decode(jwt_token,settings.SECRET_KEY,algorithms=['HS256'])
            id=decoded['id']
            print(id)
        except:
            msg.warning(request,"Please Sign-in")
            return render(request,"login.html")
        cursor.callproc('SP_Custom_token_get_by_user_id',[id])
        res=cursor.fetchall()
        cursor.nextset()
        signout=res[0][4]
        print(signout)
        
        if signout==None:
            if request.method=="POST":
                tilte=request.POST.get("title")
                category=request.POST.get("category")
                desc=request.POST.get("desc")
                cursor.callproc("SP_todo_insert",[id,tilte,category,desc]) 
                return redirect("/todo")
            else:
                return render (request,"add_todo.html")
        else:
            msg.warning(request,'Please Sign-in')
            return render(request,'login.html')
    else:
        msg.warning(request,'Please Sign-in')
        return render(request,'login.html')

#Todo-List
def todo_list(request):
   
    verify_token=request.META.get('HTTP_AUTHORIZATION')
    if verify_token:
        try:
            jwt_token = verify_token.split(' ')[1]
            #Decoding JWT    
            decoded=jwt.decode(jwt_token,settings.SECRET_KEY,algorithms=['HS256'])
            id=decoded['id']
            name=decoded['name']
            print(id)
        except:
            msg.warning(request,'Please Sign-in')
            return render(request,'login.html')
        cursor.callproc('SP_Custom_token_get_by_user_id',[id])
        res=cursor.fetchall()
        cursor.nextset()
        signout=res[0][4]
        print(signout)

        if signout==None:
           cursor.callproc('SP_todo_get_by_user_id',[id])
           value=cursor.fetchall()
           cursor.nextset()
           todos = [
            {'id':row[0],'Title': row[2], 'category': row[3], 'Descbribe': row[4], 'Status': row[5]}
            for row in value
            ]
           return render(request,'todo.html',{'li':todos,'name':name})

        else:
            msg.warning(request,'Please Sign-in')
            return render(request,'login.html')
    else:
        msg.warning(request,'Please Sign-in')
        return render(request,'login.html')


def update(request,id):
    verify_token=request.META.get('HTTP_AUTHORIZATION')
    if verify_token:
        try:
            jwt_token = verify_token.split(' ')[1]
            #Decoding JWT    
            decoded=jwt.decode(jwt_token,settings.SECRET_KEY,algorithms=['HS256'])
            us_id=decoded['id']
        except:
            msg.warning(request,'Please Sign-in')
            return render(request,"login.html")
        if request.method=="POST":
            tilte=request.POST.get("title")
            category=request.POST.get("category")
            desc=request.POST.get("desc")
            status=request.POST.get("status")
            cursor.callproc("SP_todo_update",[us_id,tilte,category,desc,status,id]) 
            return redirect("/todo")
        else:
            cursor.callproc('SP_todo_get_by_id',[id])
            res=cursor.fetchall()
            cursor.nextset()
            todos = [
            {'id':row[0],'Title': row[2], 'category': row[3], 'Descbribe': row[4], 'Status': row[5]}
            for row in res
            ]
            return render(request,'update.html',{'li':todos,'id':id})
    else:
        msg.warning(request,'Please Sign-in')
        return render(request,'login.html')


def completed(request,id):
    verify_token=request.META.get('HTTP_AUTHORIZATION')
    if verify_token:
        try:
            jwt_token = verify_token.split(' ')[1]
            #Decoding JWT    
            decoded=jwt.decode(jwt_token,settings.SECRET_KEY,algorithms=['HS256'])
            us_id=decoded['id']
        except:
            msg.warning(request,"Please Sign-in")
            return render(request,'login.html')
        cursor.callproc('SP_todo_update_completed',[id])
        cursor.nextset()
        return redirect("/todo")
    else:
        msg.warning(request,"Please Sign-in First")
        return render(request,'login.html')

def delete(request,id):
    verify_token=request.META.get('HTTP_AUTHORIZATION')
    print(verify_token)
    if verify_token:
        try:
            jwt_token = verify_token.split(' ')[1]
            #Decoding JWT    
            decoded=jwt.decode(jwt_token,settings.SECRET_KEY,algorithms=['HS256'])
            us_id=decoded['id']
        except:
            msg.warning(request,"Please Sign-in First")
            return render(request,'login.html')
        cursor.callproc('SP_todo_delete',[id])
        cursor.nextset()
        return redirect('/todo')
    else:
        msg.warning(request,"Please Sign-in First")
        return render(request,'login.html')

#Logout
def Logout(request):
    verify_token=request.META.get('HTTP_AUTHORIZATION')
    print(verify_token)
    if verify_token:
        try:
            jwt_token = verify_token.split(' ')[1]
            #Decoding JWT    
            decoded=jwt.decode(jwt_token,settings.SECRET_KEY,algorithms=['HS256'])
            id=decoded['id']
        except:
            msg.warning(request,"Please Sign-in First")
            return render(request,'login.html')
        settoken(" ")
        cursor.callproc('SP_Custom_token_signout_update',[id,jwt_token])
        return render(request,'login.html')
    else:
        msg.warning(request,"Please Sign-in First")
        return render(request,'login.html')