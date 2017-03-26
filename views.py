from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
#import note.sqllib as sqllib
import note.Note as Note

# Create your views here.
    
@ensure_csrf_cookie
def index(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def CheckLogin(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
        ActionInfo={}
        ActionInfo = getpost(request)
        if ("uid" in request.session) and ("name" in request.session):#是否需要验证客户端cookie？
            ActionInfo["loginstate"]=1
            ActionInfo["name"]=request.session["name"]
            ActionInfo["permissions"]=request.session["permissions"]
        else:
            ActionInfo["loginstate"]=0
        ActionInfo["state"]="success"
        return HttpResponse(json.dumps(ActionInfo)) 
        
@ensure_csrf_cookie
def submitarticle(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
        ActionInfo = getpost(request)
        if ("name" in ActionInfo) and ActionInfo["name"]!="" and ActionInfo["name"]!=None:
            (ActionInfo,logined) = checklogininfo(request,ActionInfo)
            if logined:
                ActionInfo["permissions"]=request.session["permissions"]
                info = Note.SubmitArticle(ActionInfo)
                return HttpResponse(json.dumps(info))
            else:
                return HttpResponse(json.dumps('{"state":"%s"}'%str("请重新登录")))
        else:
            logout(request)
            ActionInfo.pop('name',None)
            info = Note.SubmitArticle(ActionInfo)
            return HttpResponse(json.dumps(info))
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def editarticle(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
        ActionInfo = getpost(request)
        if ("name" in ActionInfo) and ActionInfo["name"]!=""  and ActionInfo["name"]!=None:
            (ActionInfo,logined) = checklogininfo(request,ActionInfo)
            if logined:
                ActionInfo["permissions"]=request.session["permissions"]
            else:
                del ActionInfo['name']
            info = Note.EditArticle(ActionInfo)
            return HttpResponse(json.dumps(info))
        else:
            ActionInfo.pop('name',None)
            info = Note.EditArticle(ActionInfo)
            return HttpResponse(json.dumps(info))
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def deletearticle(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST' and "uid" in request.session:
        ActionInfo = getpost(request)
        (ActionInfo,logined) = checklogininfo(request,ActionInfo)#
        if logined:
            ActionInfo["permissions"]=request.session["permissions"]
            state = Note.DeleteArticleByNameTitle(ActionInfo)
            return HttpResponse(json.dumps(state))
        return HttpResponse(json.dumps({"state":"Name err"}))
        
@ensure_csrf_cookie
def getarticle(request,keyword=None):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
        ActionInfo = getpost(request)
        (ActionInfo,logined) = checklogininfo(request,ActionInfo)
        if logined:
            ActionInfo["permissions"]=request.session["permissions"]
        else:
            ActionInfo.pop('name',None)
        article = Note.GetArticle(ActionInfo)
        return HttpResponse(json.dumps(article))
    #判断spider
    elif "spider" in request.META.get('HTTP_USER_AGENT', "").lower():
        res = Note.SpiderResponser(request.path)
        return HttpResponse(res)
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def getarticlelist(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name')
        ActionInfo = getpost(request)
        
        if "name" in ActionInfo:
            (ActionInfo,logined) = checklogininfo(request,ActionInfo)#未登录会返回公共列表
            if logined:
                ActionInfo["permissions"]=request.session["permissions"]
            else:
                ActionInfo.pop("name",None)
                logout(request)
                
        res = Note.GetArticleList(ActionInfo)#articlelist是数组        
        return HttpResponse(json.dumps(res))  
    return render(request, 'note_register.html')
    
@ensure_csrf_cookie
def login(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
        ActionInfo = getpost(request)
        res = Note.CheckUser(ActionInfo)
        if(res["state"]=="success"):
            request.session["name"] = res["name"]
            request.session["uid"] = res["uid"]
            request.session["permissions"] = res["permissions"]
            res.pop("uid")#uid 不传回客户端
        return HttpResponse(json.dumps(res)) 
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def register(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name','mail','password')
        ActionInfo = getpost(request)
        state = Note.CreateUser(ActionInfo)
        return HttpResponse(json.dumps(state)) 
    return render(request, 'note_register.html')
    
@ensure_csrf_cookie
def searcharticle(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name')
        ActionInfo = getpost(request)
        (ActionInfo,logined) = checklogininfo(request,ActionInfo)
        if logined:
            ActionInfo["permissions"]=request.session["permissions"]
            state = Note.SearchArticleList(ActionInfo)#articlelist是数组
            return HttpResponse(json.dumps(state)) 
    return render(request, 'note_index.html')
    
@ensure_csrf_cookie
def ReSetPassword(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name',"mail")
        ActionInfo = getpost(request)
        state = Note.ReCreateUserPassword(ActionInfo)
        return HttpResponse(json.dumps(state)) 
    return render(request, 'note_index.html')

@ensure_csrf_cookie
def ChangePassword(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    if request.is_ajax() and request.method == 'POST':
    #uf should have ('name',"password","newpassword")
        ActionInfo = getpost(request)
        (ActionInfo,logined)=checklogininfo(request,ActionInfo)
        if logined:
            ActionInfo["permissions"]=request.session["permissions"]
            state = Note.ChangeUserPassword(ActionInfo)
            return HttpResponse(json.dumps(state)) 
        else:
            return render(request, 'note_index.html')
    return render(request, 'note_index.html')
    
def logout(request):
    print(request.META['HTTP_X_FORWARDED_FOR'])
    request.session.pop("name","del name failed")
    request.session.pop("permissions","del permissions failed")
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