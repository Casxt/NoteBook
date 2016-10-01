#正则替换/s为" "记得做
#所有传入检查name，没有name用公用账户
#传出必有name和username
#以uid作为登录凭证
#文章和标题长度限制
import hashlib
import re
import json
import time
try:
    import note.sqllib as sqllib
    import note.mail as mail
    from note.config import *
except Exception as e:
    print (e)
    import sqllib
    import mail
    from config import *

def GetArtical(uf):#快速获取文章内容，用于主页展示和文章编辑
    uf["title"] = CleanTitle(uf["title"])#id title共用关键字
    uf["id"] = 0
    if uf["title"].isdigit():
        uf["id"] = uf["title"]
    #uf["uid"] = uf.get("uid",PUBLICUSER)
    uf["name"] = uf.get("name",PUBLICUSER)
    if uf["name"] != PUBLICUSER and uf["iflogin"]==False:
        return ARTICALNEEDRIGHT
    try:
        artical = sqllib.GetArtical(uf)
        #print("GetArtical",artical)
    except Exception as e:    
        print("GetArtical",e)
        return ("Note.GetArtical UnkonwErr")
    if artical is None:
        return {"title":None,"essay":None,"state":"Failed"}
    if artical["saltpassword"] is not None:#如果有密码
        if uf.get("mode",None)=="edit" and uf["uid"]==artical["uid"]:#如果有传入密码
            artical["state"]="success"
        elif uf.get("password",None) is None:#如果没有传入密码
            return {"state":"Need Password"}
        elif CheckArticalPassword({"saltpassword":artical["saltpassword"],"salt":artical["salt"],"password":uf.get("password","None")}):#如果有传入密码
            artical["state"]="success"
        else:#传入密码错误
            return {"state":"Failed"}
    else:
        artical["state"]="success"
    del artical["saltpassword"]
    del artical["salt"]
    del artical["uid"]
    artical["lastesttime"]=artical["lastesttime"].strftime('%Y-%m-%d %H:%M:%S')
    artical["pubtime"]=artical["pubtime"].strftime('%Y-%m-%d %H:%M:%S')
    return artical
    
def CheckUser(uf):#检查用户能否登录
    name = uf["name"].lower()
    password = uf["password"]
    info = {}
    if CheckUserName(name):
        userinfo = sqllib.GetLoginInfo ({'name':name})
        if userinfo is None:
            state = "Failed"
            stateinfo = "ERROR UserName"
            islogin = False
        else:
            shapassword = hashlib.sha256()
            shapassword.update((str(password)+userinfo['salt']).encode('utf-8'))
            t = time.mktime(userinfo["now"].timetuple())-time.mktime(userinfo["lastfailedtime"].timetuple())
            t = (t/3600)
            waitetime=WAITETIME*(WAITENUM**(userinfo["lgnfailedtimes"]-LOGINFAILEDTIMES+1))
            if userinfo["lgnfailedtimes"]>=LOGINFAILEDTIMES and t<waitetime:
                state = "Login Failed Too Many Times Try After %s Hour"%(float('%0.3f'%(waitetime-t)))
                print (state)
                stateinfo = "Login Failed Too Many Times"
                islogin = False
            elif shapassword.hexdigest()==userinfo['saltpassword']:
                sqllib.CleanFailedTimes ({'name':name})
                state = "success"
                stateinfo = "success"
                islogin = True
                info["uid"] = userinfo["uid"]
                info["name"] = userinfo["name"]
            else:
                sqllib.LoginFailed ({'name':name})
                state = "Failed"
                stateinfo = "Password Error"
                islogin = False
    else:
        state = "Failed"
        stateinfo = "Check Name Failed"
        islogin = False
    info["state"]=state
    return (islogin,info,stateinfo)

def CheckArticalPassword(af):#发现文章有密码之后的操作
    shapassword = hashlib.sha256()
    shapassword.update((str(af["password"])+af['salt']).encode('utf-8'))
    if shapassword.hexdigest()==af['saltpassword']:
        return True
    else:
        return False
def SubmitArtical(af):
#af=('title','name','essay','right','blgroup','password','prikey','pubkey')
    af["title"] = CleanTitle(af["title"])
    af["essay"] = CleanArtical(af["essay"])
    af["uid"] = af.get("uid",PUBLICUSER)
    if af["type"] not in ARTICALTYPELIST:
        return (ARTICLETYPEERR)
    if "password" in af:
        af = CreateSaltAndPassword(af)
    try:
        if CheckTitle(af["title"]):
            sqllib.CreatArtical (af)
            return({"state":"success"})
        else:
            return({"state":"Title Err"})
    except Exception as e:
        print(e)
        if ("Duplicate entry" in str(e)):
            return({"state":"标题重复"})
        return("未知错误")
            
def EditArtical(af):#修改文章
#af=('title','name','essay','right','blgroup','password','prikey','pubkey')
    af["rawtitle"] = CleanTitle(af["rawtitle"])
    af["title"] = CleanTitle(af["title"])
    af["essay"] = CleanArtical(af["essay"])
    if af["type"] not in ARTICALTYPELIST:
        return (ARTICLETYPEERR)
    if "password" in af:
        if af["password"]==str(RESETARTCALPASSWORD):#如果取消密码
            print("resetpassword")
            af["saltpassword"]=None
            af["salt"]=None
            del af["password"]
        else:
            af = CreateSaltAndPassword(af)
    if ("name" not in af) or (af["name"]=="") or (af["name"]==None):#必须有name字段，登录验证由session处理
        af["name"]=PUBLICUSER
        af["uid"]=PUBLICUSER
    if CheckUserName(af["name"]) and CheckTitle(af["title"]):
        try:
            if sqllib.EditArtical(af) is True:
                return ({"state":"success"})
        except Exception as e:
            if ("Duplicate entry" in str(e)):
                return({"state":"标题重复"})
            return("未知错误")

def DeleteArticalByNameTitle (af):
    af["title"] = CleanTitle(af["title"])
    if "uid" in af:#必须有uid字段，登录验证由session处理
        try:
            sqllib.DeleteArticalByNameTitle(af)
            return "success"
        except Exception as e:
            print("DeleteArticalByNameTitle",e)
            return(str(e))
    return "Failed"
    
def GetArticalList(af):
    if "uid" not in af:#必须有uid字段否则视为未登录，登录验证由session处理
        af["name"]=PUBLICUSER
        af["uid"]=PUBLICUSER
    if ("page" not in af) or (int(af["page"])<1):
        af["page"] = 1
    else:
        af["page"] = int(af["page"])
    if ("eachpage" not in af):
       af["eachpage"] = EACHPAGENUM
    if CheckUserName(af["name"]):
        try:
            result = sqllib.GetArticalList (af)
            count = sqllib.CountArticalList (af)
        except Exception as e:
            print(e)
            return("GetArticalList未知错误",0,False)
        for artical in result:
            artical["lastesttime"]=artical["lastesttime"].strftime('%Y-%m-%d %H:%M:%S')
            artical["pubtime"]=artical["pubtime"].strftime('%Y-%m-%d %H:%M:%S')
            if artical["saltpassword"]==None:
                artical["password"]=0
            else:
                artical["password"]=1
            del artical["saltpassword"]
        #print(result)
        return(result,count,True)
    else:
        return("Name Err",0,False)
        
def SearchArticalList(af):
    if "name" not in af:#必须有name字段否则视为未登录，登录验证由session处理
        af["name"]=PUBLICUSER
        af["uid"]=PUBLICUSER
    af["keyword"] = af["keyword"].strip()
    if CheckUserName(af["name"]) and CheckKeyWord(af["keyword"]):
        try:
            result = sqllib.SearchArtical (af)
            for artical in result:
                artical["lastesttime"]=artical["lastesttime"].strftime('%Y-%m-%d %H:%M:%S')
                artical["pubtime"]=artical["pubtime"].strftime('%Y-%m-%d %H:%M:%S')
                if artical["name"]==PUBLICUSER:
                    del artical["name"]
            return(result,True)
        except Exception as e:
            print(e)
            return("SearchArticalList未知错误",False)
    else:
        return("Failed",False)
        
def CreateUser(uf):#生成用户，生成uid，生成盐
    import uuid
    #uf should have ('uid','name','mail','salt','saltpassword')
    uf["name"] = uf["name"].lower()
    uf["mail"] = uf["mail"].lower()
    if CheckUserName(uf['name']) and CheckUserPassword(uf['password']) and CheckUserMail(uf['mail']):
        t = str(int(time.time()))
        #生成salt
        salt = hashlib.sha256()
        salt.update((uf['password'][0:5]+t+uf['name'][0:4]).encode('utf-8'))
        uf["salt"] = salt.hexdigest()
        #生成hash256password
        hash256password = hashlib.sha256()
        hash256password.update((uf['password']).encode('utf-8'))
        uf['hash256password'] = hash256password.hexdigest()
        #生成saltpassword
        saltpassword = hashlib.sha256()
        saltpassword.update((uf['hash256password']+uf["salt"]).encode('utf-8'))
        uf['saltpassword'] = saltpassword.hexdigest()
        #生成uid
        uf['uid'] = str(uuid.uuid3(uuid.uuid1(), uf['mail']))
        try:
            info = sqllib.CreateUser(uf)
            mail.Send(uf["mail"],MAIL_TITLE_SIGNIN,MAIL_ARTICAL_SIGNIN)
            return ("success",info)
        except Exception as e:
            err = str(e)
            if "Duplicate entry" in err:
                if "name" in err:
                    return ("Name Already Exist",False)
                elif "mail" in err:
                    return ("Mail Already Exist",False)
                else:
                    print(err)
                    return (err,False)
            else:
                print(e)
                return (e,False)
    else:
        return ("Name Or Password Err",False)

def ChangeUserPassword(uf):#更改密码，要求登录
    #uf should have name password newpassword
    uf["name"] = uf["name"].lower()
    (Islogin,userinfo,state) = CheckUser(uf)
    if Islogin:
        info = sqllib.GetUserInfo (uf)
        info["password"] = uf["newpassword"]
        info = CreateSaltAndPassword(info)
        sqllib.ResetPassword (info)
        mail.Send(info["mail"],MAIL_TITLE_CGPASSWORD,MAIL_ARTICAL_CGPASSWORD)
        return (True,"success")
    else:
        print("ChangeUserPassword",Islogin,userinfo,state)
        return (False,"Name Or Password err")
      
def ReCreateUserPassword(uf):#重置密码用户名
    import uuid
    #uf should have ('uid','name','mail','salt','saltpassword')
    uf["name"] = uf["name"].lower()
    uf["mail"] = uf["mail"].lower()
    #print("ReCreateUserPassword",uf)
    if CheckUserName(uf["name"]) and CheckUserMail(uf["mail"]):
        info = sqllib.GetUserInfo (uf)
        if uf["mail"] == info["mail"]:
            newpassword = str(uuid.uuid3(uuid.uuid1(), uf['mail']))
            info["password"] = newpassword
            info = CreateSaltAndPassword(info)
            sqllib.ResetPassword (info)#重置密码
            mail.Send(uf["mail"],MAIL_TITLE_RSPASSWORD,MAIL_ARTICAL_RSPASSWORD%(newpassword))
            sqllib.CleanFailedTimes (info)#清空登录计数
            return (True,"success")
        else:
            return (False,"Mail Not Match")
    else:
        return (False,"Name wrong")
        
def CheckUserName(Name):#检查用户名是否合法
    s = r'^[a-zA-Z][0-9a-zA-Z@.\-]{4,29}$'
    if re.match(s, Name):
        return True
    else:
        return False

def CheckUserPassword (Password):#检查密码是否合法
    s = r'^[0-9a-zA-Z@.\-\_\#\$\^\&\*]{6,128}$'
    if re.match(s, Password):
        return True
    else:
        return False   

def CheckUserMail(Mail):#检查邮箱是否合法
    s = r'^[0-9a-zA-Z][0-9a-zA-Z\-]{0,}@[0-9a-zA-Z.\-]+?.[a-zA-Z.]+[a-zA-Z]$'
    if re.match(s, Mail):
        return True
    else:
        return False

def CleanTitle(Title):
    Title = re.sub(r'/s',' ', Title)
    Title.replace("<","").replace(">","")
    return Title
    

def CheckTitle(Title):
    s = r'[\\#\$\?<>]'
    if re.match(s, Title):
        return False
    else:
        return True
        
def CheckKeyWord(KeyWord):
    s = r'[`=]'
    if re.match(s, KeyWord) or len(KeyWord.replace(" ",""))<3:
        return False
    else:
        return True  
def CleanArtical(Artical):
    Artical.replace("<script","").replace("script>","")
    Artical.replace("<iframe","").replace("iframe>","")
    Artical.replace("<link","")
    Artical.replace("<style","").replace("style>","")
    Artical.replace("<frameset","").replace("frameset>","")
    return Artical

def SendMail(mail):
    pass
    return True

def CreateSaltAndPassword(af):#重新生成salt和密码
    #password uid/name
    t = str(int(time.time()))
    #生成salt
    salt = hashlib.sha256()
    salt.update((af['password'][0:5]+t+af.get('uid',af["name"])[0:4]).encode('utf-8'))
    af["salt"] = salt.hexdigest()
    #生成hash256password
    hash256password = hashlib.sha256()
    hash256password.update((af['password']).encode('utf-8'))
    af['hash256password'] = hash256password.hexdigest()
    #生成saltpassword
    saltpassword = hashlib.sha256()
    saltpassword.update((af['hash256password']+af["salt"]).encode('utf-8'))
    af['saltpassword'] = saltpassword.hexdigest()
    return af