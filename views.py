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
        ActionInfo={}
        ActionInfo = getpost(request)
        if ("uid" in request.session) and ("name" in request.session):#是否需要验证客户端cookie？
            ActionInfo["loginstate"]=1
            ActionInfo["name"]=request.session["name"]
        else:
            ActionInfo["loginstate"]=0
        ActionInfo["state"]="success"
        return HttpResponse(json.dumps(ActionInfo)) 
        
@ensure_csrf_cookie
def submitartical(request):
    if request.is_ajax() and request.method == 'POST':
        ActionInfo = getpost(request)
        if ("name" in ActionInfo) and ActionInfo["name"]!="" and ActionInfo["name"]!=None:
            (ActionInfo,logined) = checklogininfo(request,ActionInfo)
            if logined:
                info = Note.SubmitArtical(ActionInfo)
                return HttpResponse(json.dumps(info))
            else:
                return HttpResponse(json.dumps('{"state":"%s"}'%str("请重新登录")))
        else:
            logout(request)
            ActionInfo.pop('name',None)
            info = Note.SubmitArtical(ActionInfo)
            return HttpResponse(json.dumps(info))
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def editartical(request):
    if request.is_ajax() and request.method == 'POST':
        ActionInfo = getpost(request)
        if ("name" in ActionInfo) and ActionInfo["name"]!=""  and ActionInfo["name"]!=None:
            (ActionInfo,logined) = checklogininfo(request,ActionInfo)
            if logined:
                info = Note.EditArtical(ActionInfo)
                return HttpResponse(json.dumps(info))
            else:
                return HttpResponse(json.dumps({"state":"Need Login"}))
        else:
            ActionInfo.pop('name',None)
            info = Note.EditArtical(ActionInfo)
            return HttpResponse(json.dumps(info))
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def deleteartical(request):
    if request.is_ajax() and request.method == 'POST' and "uid" in request.session:
        ActionInfo = getpost(request)
        (ActionInfo,logined) = checklogininfo(request,ActionInfo)#
        if logined:
            if "title" in ActionInfo:
                state = Note.DeleteArticalByNameTitle(ActionInfo)
                return HttpResponse(json.dumps({"state":state}))
            else:
                return HttpResponse(json.dumps({"state":"Title Not Found"}))
        return HttpResponse(json.dumps({"state":"Name err"}))
        
@ensure_csrf_cookie
def getartical(request,keyword=None):
    if request.is_ajax() and request.method == 'POST':
        ActionInfo = getpost(request)
        (ActionInfo,logined) = checklogininfo(request,ActionInfo)
        if not logined:
            ActionInfo.pop('name',None)
        artical = Note.GetArtical(ActionInfo)#getartical by
        return HttpResponse(json.dumps(artical))
    #判断spider
    elif "spider" in request.META.get('HTTP_USER_AGENT', "").lower():
        res = Note.SpiderResponser(request.path)
        return HttpResponse(res)
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def getarticallist(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name')
        ActionInfo = getpost(request)
        
        if "name" in ActionInfo:
            (ActionInfo,logined) = checklogininfo(request,ActionInfo)#未登录会返回公共列表
            if not logined:
                ActionInfo.pop("name",None)
                logout(request)
                
        (articallist,count,state) = Note.GetArticalList(ActionInfo)#articallist是数组        
        if (state is True):
            return HttpResponse(json.dumps({'state':'success','articallist':articallist,'count':count})) 
        else:
            return HttpResponse(json.dumps({'state':articallist})) 
    return render(request, 'note_register.html')
    
@ensure_csrf_cookie
def login(request):
    if request.is_ajax() and request.method == 'POST':
        ActionInfo = getpost(request)
        (Islogin,ActionInfo,state) = Note.CheckUser(ActionInfo)
        if(Islogin):
            request.session["name"] = ActionInfo["name"]
            request.session["uid"] = ActionInfo["uid"]
            request.session["permissions"] = ActionInfo["permissions"]
            ActionInfo.pop("uid")#uid 不传回客户端
        return HttpResponse(json.dumps(ActionInfo)) 
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def register(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name','mail','password')
        ActionInfo = getpost(request)
        (ActionInfo,state) = Note.CreateUser(ActionInfo)
        return HttpResponse(json.dumps({'state':ActionInfo})) 
    return render(request, 'note_register.html')
    
@ensure_csrf_cookie
def searchartical(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name')
        ActionInfo = getpost(request)
        if "uid" not in request.session :#未登录
            return HttpResponse(json.dumps({'state':'failed'}))
        elif ("name" not in ActionInfo) or (ActionInfo["name"]=="") or (ActionInfo["name"]==None):
            ActionInfo={}
        elif request.session.get("name",None) == ActionInfo["name"]:
            ActionInfo["uid"]=request.session["uid"]
        else:#传入了name但是和已登录的name不同
            return HttpResponse(json.dumps({'state':'failed'}))
        (articallist,state) = Note.SearchArticalList(ActionInfo)#articallist是数组
        if (state is True):
            return HttpResponse(json.dumps({'state':'success','keyword':ActionInfo["keyword"],'articallist':articallist})) 
        else:
            return HttpResponse(json.dumps(articallist)) 
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def ReSetPassword(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name',"mail")
        ActionInfo = getpost(request)
        (result,state) = Note.ReCreateUserPassword(ActionInfo)
        if result:
            return HttpResponse(json.dumps({'state':"success"})) 
        else:
            return HttpResponse(json.dumps({'state':'failed'})) 
    return render(request, 'note_index.html')

@ensure_csrf_cookie
def ChangePassword(request):
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name',"password","newpassword")
        ActionInfo = getpost(request)
        (ActionInfo,iflogin)=checklogininfo(request,ActionInfo)
        if iflogin:
            (result,state) = Note.ChangeUserPassword(ActionInfo)
            if result:
                return HttpResponse(json.dumps({'state':state})) 
            else:
                return HttpResponse(json.dumps({'state':'failed'})) 
        else:
            return render(request, 'note_index.html')
    return render(request, 'note_index.html')
    
def logout(request):
    request.session.pop("name","del name failed")
    request.session.pop("permissions","del password failed")
    request.session.pop("uid","del uid failed")
    if request.is_ajax() and request.method == 'GET':
        return HttpResponse('{"info":"success"}')  
    return render(request, 'note_index.html')
    
def checklogininfo(request,ActionInfo):#检查登录信息，客户端应传回name字段,判断name字段是否一致
    if "name" in ActionInfo and "name" in request.session :
        if ActionInfo["name"]==request.session["name"]:#与session用户是否相同#对自己
            ActionInfo["uid"]=request.session["uid"]#找到uid
            ActionInfo["iflogin"]=True
            return (ActionInfo,True)
        else:
            #ActionInfo.pop("name","del name failed")
            ActionInfo.pop("uid","del uid failed")
            ActionInfo["iflogin"]=False
            return (ActionInfo,False)
    else:
        ActionInfo["iflogin"]=False
        return (ActionInfo,False)
def getpost(request):#检查登录信息，客户端应传回name字段,判断name字段是否一致
    ActionInfo = {}
    for key in request.POST:
        valuelist = request.POST.get(key)
        ActionInfo[key]=valuelist
    return ActionInfo