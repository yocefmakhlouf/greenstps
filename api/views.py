from ast import operator
from dataclasses import field
from datetime import datetime
from hashlib import sha256
from urllib import response
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import json
from api.models import Data
from api.models import Access_token, Refresh_token,compets
from datetime import datetime as DT,timedelta

from api.models import last_users
class getuserchat(APIView):
    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            dts={}
            if request.data["index"] == 'all' :
                a=Access_token.objects.get(token = t)
                ps=User.objects.get(username='polesport')
                if a.r_token.user ==  ps:
                    for i in last_users.objects.order_by('date')[::-1]:
                        dts[i.user.username]=i.date.strftime("%d-%m-%y  %H:%M")
            return Response(dts,status=200)
        except Exception as e:
            print(e)
            return Response({"Error":"Error while processing demand"},status=422)
class LDAPLogin(APIView):
    """
    Class to authenticate a user via LDAP and
    then creating a login session
    """
    authentication_classes = ()

    def post(self, request):
        """
        Api to login a user
        :param request:
        :return:
        """
        user_obj = authenticate(username=request.data['username'],
                                password=request.data['password'])
        '''if user_obj is None:
            User.objects.create_user(request.data['username'],password=request.data['password'])
        user_obj = authenticate(username=request.data['username'],
                               password=request.data['password'])'''
        #token = Token.objects.get_or_create(user=user_obj)
        if user_obj:
            login(request, user_obj,backend='django.contrib.auth.backends.ModelBackend')
            RefreshToken.for_user(user_obj)
            r_token,_ = Refresh_token.create(user_obj)
            a_token,_ = Access_token.create(r_token)
            content = {'refresh':str(r_token.token),'access': a_token.token}
        else :
            return Response({"Error":"Invalid credentials"},status=422)

        
        return Response(content, status=200)
class connect(APIView):
    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            a=Access_token.objects.get(token = t)
            if a.r_token.token ==  request.data["token"]:
                return Response({},status=200)
            return Response({"Error":"Invalid credentials"},status=422)
        except:
            return Response({"Error":"Error while processing demand"},status=422)
class logout(APIView):
    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            a=Access_token.objects.get(token = t)
            if a.r_token.token ==  request.data["token"]:
                Access_token.objects.get(token=t).delete()
                Refresh_token.objects.get(token=request.data["token"]).delete()
                return Response({},status=200)
            return Response({"Error":"Invalid credentials"},status=422)
        except:
            return Response({"Error":"Error while processing demand"},status=422)
class geteventdata(APIView):
    fields=["name","date","status","showing"]

    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            dts={}
            if request.data["event"]:
                a=Access_token.objects.get(token = t)
                ps=User.objects.get(username='polesport')
                if a.r_token.user ==  ps:
                    d=compets.objects.get(name=request.data["event"])
                    for f in geteventdata.fields:
                        dts[f]=getattr(d,f)
            return Response(dts,status=200)
        except Exception as e:
            print(e)
            return Response({"Error":"Error while processing demand"},status=422)
class getevent(APIView):
    def validate(date_text):
        try:
            DT.strptime(date_text, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            dts={}
            if request.data["index"] == 'all' :
                a=Access_token.objects.get(token = t)
                ps=User.objects.get(username='polesport')
                if a.r_token.user ==  ps:
                    for i in compets.objects.order_by('date'):
                        dts[i.name]={"image":i.image,"date":i.date}
            return Response(dts,status=200)
        except Exception as e:
            print(e)
            return Response({"Error":"Error while processing demand"},status=422)
class setevent(APIView):
    def validate(date_text):
        try:
            DT.strptime(date_text, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            dts={}
            if request.data["image"] and request.data["name"] and setevent.validate(request.data["date"]) and (request.data["status"] in ["Ongoing","Over","Coming"]) :
                a=Access_token.objects.get(token = t)
                ps=User.objects.get(username='polesport')
                if a.r_token.user ==  ps:
                    a,_=compets.create(request.data["name"],request.data["image"],request.data["date"],request.data["status"],0)
                    print(a)
            return Response(dts,status=200)
        except Exception as e:
            print(e)
            return Response({"Error":"Error while processing demand"},status=422)
class send(APIView):
    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            dts={}
            if request.data["username"] and request.data["message"]:
                a=Access_token.objects.get(token = t)
                ps=User.objects.get(username='polesport')
                if a.r_token.user ==  ps:
                    d=Data.objects.get(user=User.objects.get(username=request.data["username"]))
                    f=open(settings.DATA_ROOT+'jsons\\'+d.chat_path)
                    j= json.load(f)
                    j[len(j)+1]={"sender":request.data["message"]}
                    f.close()
                    f=open(settings.DATA_ROOT+'jsons\\'+d.chat_path,'w')
                    json.dump(j,f)
                    f.close()
                    last_users.create(User.objects.get(username=request.data["username"]))
            return Response(dts,status=200)
        except Exception as e:
            print(e)
            return Response({"Error":"Error while processing demand"},status=422)
class GetmData(APIView):
    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            dts={}
            if request.data["username"]:
                a=Access_token.objects.get(token = t)
                ps=User.objects.get(username='polesport')
                if a.r_token.user ==  ps:
                    d=Data.objects.get(user=User.objects.get(username=request.data["username"]))
                    f=open(settings.DATA_ROOT+'jsons\\'+d.chat_path)
                    j= json.load(f)
                    l=sorted(map(int,j.keys()))[::-1]
                    lenght=30
                    if len(l)<30:
                        lenght=len(l) 
                    for i in range(-1,-lenght-1,-1):
                        dts[i]=j[str(l[i])]
                    f.close()
            return Response(dts,status=200)
        except Exception as e:
            print(e)
            return Response({"Error":"Error while processing demand"},status=422)
class GetuData(APIView):
    fields=["categ","school","taille","poids","total_steps"]
    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            dts={}
            if request.data["username"]:
                dts={"user" :request.data["username"], }
                a=Access_token.objects.get(token = t)
                ps=User.objects.get(username='polesport')
                if a.r_token.user ==  ps:
                    d=Data.objects.get(user=User.objects.get(username=request.data["username"]))
                    for f in GetuData.fields:
                        dts[f]=getattr(d,f)
            return Response(dts,status=200)
        except Exception as e:
            print(e)
            return Response({"Error":"Error while processing demand"},status=422)
class GetData(APIView):
    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            datas={"steps":{},"distance":{},"calories":{}}
            if request.data["username"]:
                a=Access_token.objects.get(token = t)
                ps=User.objects.get(username='polesport')
                if a.r_token.user ==  ps:
                    d=Data.objects.get(user=User.objects.get(username=request.data["username"]))
                    f=open(settings.DATA_ROOT+'jsons\\'+d.data_path)
                    j= json.load(f)
                    for type in ['steps','calories','distance']:
                        if request.data[type] != 2:
                            days = request.data[type]*23 + 7
                            for i in range(days,0,-1):
                                date=(DT.now()-timedelta(days=i)).strftime("%d:%m")
                                if date in j[type]:
                                    datas[type][date]=j[type][date]
                                else:
                                    j[type][date]=0
                                    datas[type][date]=j[type][date]
                        else :
                            for i in range(12,0,-1):
                                date=(DT.now()-timedelta(i*30)).strftime("%m:%y")
                                if date in j[type]:
                                    datas[type][date]=j[type][date]
                                else:
                                    j[type][date]=0
                                    datas[type][date]=j[type][date]
                    f.close()
                    f=open(settings.DATA_ROOT+'jsons\\'+d.data_path,'w')
                    json.dump(j,f)
                    f.close()
            return Response(datas,status=200)
        except Exception as e:
            print(e)
            return Response({"Error":"Error while processing demand"},status=422)
class register(APIView):
    def post(self,request):
        t= str(request.headers["Authorization"])
        try : 
            a=Access_token.objects.get(token = t)
            print(Data.create(a.r_token.user,r=request))
            return Response(status=200)
        except:
            return Response({"Error":"Error while processing demand"},status=422)
    
class gets_steps(APIView):
    def get(self,request):
        t= str(request.headers["Authorization"])
        try : 
            a=Access_token.objects.get(token = t)
            t=0
            for u in Data.objects.all():
                t+=u.total_steps
            return Response({'total steps':str(t)},status=200)
        except:
            return Response({"Error":"Error while processing demand"},status=422)    

class GetUsers(APIView):
    def get(self,request):
        t= str(request.headers["Authorization"])
        try : 
            a=Access_token.objects.get(token = t)
            ps=User.objects.get(username='polesport')
            datas={}
            if a.r_token.user ==  ps:
                for data in Data.objects.all():
                    if data.user != ps:
                       datas[data.user.username]={"school":data.school,"today steps":data.today_steps}
            return Response(datas,status=200)
        except:
            return Response({"Error":"Error while processing demand"},status=422)
    

class LDAPLogout(APIView):
    """
    Class for logging out a user by clearing his/her session
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Api to logout a user
        :param request:
        :return:
        """
        logout(request)
        data={'detail': 'User logged out successfully'}
        return Response(data, status=200)