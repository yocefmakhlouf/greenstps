from email.mime import image
import json
from time import time
from tkinter import EXCEPTION
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from datetime import datetime
from hashlib import sha256
from django.utils import timezone
class last_users(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    date=models.DateTimeField()
    def create(user):
        return last_users.objects.update_or_create(user=user,defaults={'date':timezone.now()})

class Refresh_token(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    token = models.CharField(max_length=64)
    def create(user):
        hs = user.password+datetime.now().__str__()
        r_token = sha256(hs.encode('utf-8')).hexdigest()
        return Refresh_token.objects.update_or_create(user=user,defaults={'token':r_token})
        
class Access_token(models.Model):
    r_token = models.OneToOneField(
        Refresh_token,
        on_delete=models.CASCADE,
    )
    token = models.CharField(max_length=64)
    def create(Rtoken):
        hs = Rtoken.token+datetime.now().__str__()
        a_token = sha256(hs.encode('utf-8')).hexdigest()
        return Access_token.objects.update_or_create(r_token=Rtoken,defaults={'token':a_token})

class Data(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    taille = models.IntegerField(default=0)
    poids = models.IntegerField(default=0)
    today_steps = models.IntegerField(default=0)
    total_steps = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    categ = models.CharField(max_length=50)
    school = models.CharField(max_length=50,default='um6p')
    chat_path = models.CharField(max_length=200,blank=True,default="")
    data_path=models.CharField(max_length=200,default="",blank=True,) 

    def create(user,r):
        try:
            int(r.data["taille"])
        except:
            return "Taille error"
        try:
            int(r.data["poids"])
        except:
            return "Poids error"

        d,_=Data.objects.update_or_create(user=user,defaults={
                "taille" : int(r.data["taille"]),
                "poids":int(r.data["poids"]),
                "today_steps":0,
                "total_steps" :0,
                "age":int(r.data["age"]),
                "school" :r.data["school"],
                "categ": r.data['categ'],
                }
        )
        print(d)
        if d.chat_path and d.data_path:
            return d
        else:
            try :
                while 1:
                    data_path = get_random_string(length=25)+'.json'
                    chat_path = get_random_string(length=25)+'.json'
                    open(settings.DATA_ROOT+'jsons\\'+data_path,'r').close()
                    open(settings.DATA_ROOT+'jsons\\'+chat_path,'r').close()
            except:
                d.chat_path=chat_path
                d.data_path= data_path
                d.save()
                a=open(settings.DATA_ROOT+'jsons\\'+data_path,'w')
                b=open(settings.DATA_ROOT+'jsons\\'+chat_path,'w')
                json.dumps({"steps":{},"calories":{},"distance":{}},a)
                a.close()
                b.close()
                return d
       
class compets(models.Model):
    name = models.CharField(max_length=50)
    image = models.TextField()
    date = models.CharField(max_length=50)
    status=models.CharField(max_length=10)
    showing = models.IntegerField(default=0)
    def create(name,image,date,status,showing):
        return compets.objects.update_or_create(name=name,defaults={'image':image,'date':date,'status':status,"showing":showing})