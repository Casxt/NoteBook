from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
#import note.sqllib as sqllib
import note.Note as Note

# Create your views here.

@ensure_csrf_cookie
def index(request):
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def CheckLogin(request):
    if request.is_ajax() and request.method == 'POST':
        userinfo={}
        dict = getpostdict(request)
        if ("uid" in request.session) and ("name" in request.session):#是否需要验证客户端cookie？
            userinfo["loginstate"]=1
            userinfo["name"]=request.session["name"]
        else:
            userinfo["loginstate"]=0
        userinfo["state"]="success"
        print(userinfo)
        return HttpResponse(json.dumps(userinfo)) 
        
@ensure_csrf_cookie
def submitartical(request):
    if request.is_ajax() and request.method == 'POST':
        dict = getpostdict(request)
        if request.session.get("name",None) == dict["name"]:#对自己
            dict["uid"]=request.session["uid"]
        elif dict["name"]=="" or dict["name"] is None:#是否为公用账户#对公用账户
            dict.pop("uid","")
        else:
            return HttpResponse('{"state":"%s"}'%str("请重新登录")) 
        info = Note.SubmitArtical(dict)
        return HttpResponse('{"state":"%s"}'%str(info))  
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def editartical(request):
    if request.is_ajax() and request.method == 'POST':
        dict = getpostdict(request)
        #print("editartical",dict)
        if ("name" in dict) and dict["name"]!="":
            (dict,logined) = checklogininfo(request,dict)
            if logined:
                info = Note.EditArtical(dict)
                return HttpResponse(json.dumps({"state":str(info)}))
            else:
                return HttpResponse(json.dumps({"state":"Need Login"}))
        else:
            info = Note.EditArtical(dict)
            return HttpResponse(json.dumps({"state":str(info)}))
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def deleteartical(request):
    if request.is_ajax() and request.method == 'POST' and "uid" in request.session:
        dict = getpostdict(request)
        (dict,logined) = checklogininfo(request,dict)#
        if logined:
            if "title" in dict:
                artical = Note.DeleteArticalByNameTitle(dict)
                print(artical)
                return HttpResponse(json.dumps({"state":artical}))
            else:
                return HttpResponse(json.dumps({"state":"Title Not Found"}))
        return HttpResponse(json.dumps({"state":"Name err"}))
        
@ensure_csrf_cookie
def getartical(request,keyword=None):
    if request.is_ajax() and request.method == 'POST':
        dict = getpostdict(request)
        (dict,iflogin) = checklogininfo(request,dict)
        print("getartical",dict)
        artical = Note.GetArtical(dict)#getartical by
        return HttpResponse(json.dumps(artical))
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def login(request):
    if request.is_ajax() and request.method == 'POST':
        print('login')
        dict = getpostdict(request)
        (Islogin,userinfo,state) = Note.CheckUser(dict)
        if(Islogin):
            request.session["name"] = userinfo["name"]
            request.session["uid"] = userinfo["uid"]
            userinfo.pop("uid")#uid 不传回客户端
        return HttpResponse(json.dumps(userinfo)) 
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def register(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name','mail','password')
        dict = getpostdict(request)
        (userinfo,state) = Note.CreateUser(dict)
        print(str(userinfo),state)
        return HttpResponse(json.dumps({'state':userinfo})) 
    return render(request, 'note_register.html')
    
@ensure_csrf_cookie
def getarticallist(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name')
        dict = getpostdict(request)
        (dict,iflogin) = checklogininfo(request,dict)#未登录会返回公共列表
        (articallist,count,state) = Note.GetArticalList(dict)#articallist是数组
        if (state is True):
            return HttpResponse(json.dumps({'state':'success','articallist':articallist,'count':count})) 
        else:
            print(articallist)
            return HttpResponse(json.dumps({'state':articallist})) 
    return render(request, 'note_register.html')
    
@ensure_csrf_cookie
def searchartical(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name')
        dict = getpostdict(request)
        if "uid" not in request.session :#未登录
            return HttpResponse(json.dumps({'state':'failed'}))
        elif ("name" not in dict) or (dict["name"]=="") or (dict["name"]==None):
            dict={}
        elif request.session.get("name",None) == dict["name"]:
            dict["uid"]=request.session["uid"]
        else:#传入了name但是和已登录的name不同
            return HttpResponse(json.dumps({'state':'failed'}))
        (articallist,state) = Note.SearchArticalList(dict)#articallist是数组
        if (state is True):
            #print(json.dumps({'state':'success','articallist':articallist}))
            return HttpResponse(json.dumps({'state':'success','keyword':dict["keyword"],'articallist':articallist})) 
        else:
            print(articallist)
            return HttpResponse(json.dumps({'state':articallist})) 
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def ReSetPassword(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name',"mail")
        dict = getpostdict(request)
        (result,state) = Note.ReCreateUserPassword(dict)
        if result:
            return HttpResponse(json.dumps({'state':"success"})) 
        else:
            print(state)
            return HttpResponse(json.dumps({'state':'failed'})) 
    return render(request, 'note_index.html')

@ensure_csrf_cookie
def ChangePassword(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name',"password","newpassword")
        dict = getpostdict(request)
        (dict,iflogin)=checklogininfo(request,dict)
        print("dict",dict)
        if iflogin:
            (result,state) = Note.ChangeUserPassword(dict)
            if result:
                return HttpResponse(json.dumps({'state':state})) 
            else:
                print(state)
                return HttpResponse(json.dumps({'state':'failed'})) 
        else:
            return render(request, 'note_index.html')
    return render(request, 'note_index.html')
    
def logout(request):
    request.session.pop("name","del name failed")
    request.session.pop("password","del password failed")
    #request.session.pop("uid","del uid failed")
    if request.is_ajax() and request.method == 'GET':
        return HttpResponse('{"info":"success"}')  
    return render(request, 'note_index.html')
    
def checklogininfo(request,dict):#检查登录信息，客户端应传回name字段,判断name字段是否一致
    if "name" in dict:
        if dict["name"]==request.session.get("name","nu"):#与session用户是否相同#对自己
            dict["uid"]=request.session["uid"]#找到uid
            return (dict,True)
        else:
            #dict.pop("name","del name failed")
            dict.pop("uid","del uid failed")
            return (dict,False)
    else:
        return (dict,False)
def getpostdict(request):#检查登录信息，客户端应传回name字段,判断name字段是否一致
    dict = {}
    for key in request.POST:
        valuelist = request.POST.get(key)
        dict[key]=valuelist
    return dict