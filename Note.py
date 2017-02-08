#正则替换/s为" "记得做
#所有传入检查name，没有name用公用账户
#传出必有name和username
#以uid作为登录凭证
#文章和标题长度限制
import hashlib
import re
import json
import time
import traceback
from pprint import pprint
#traceback.format_exc()
try:
    import note.sqllib as sqllib
    import note.mail as mail
    import note.logger as logger
    from note.config import *
    from note.spider import *
    from note.sqllib import SqlError
    from note.permission import PermissionError
    from note.mail import MailError
except Exception as e:
    import sqllib
    import mail
    import logger
    from config import *
    from spider import *
    from sqllib import SqlError
    from permission import PermissionError
    from mail import MailError

####################################
#
#异常
#
####################################  
class NoteError(Exception):
    def __init__(self,FunctionName,Massage,Info=None):  
        self.info = Info
        self.function = FunctionName
        self.err = Massage
        Exception.__init__(self)
    
def CheckUser(uf):#检查用户能否登录

    try:
        uf = CheckParamet(["name","password"],uf)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"CheckUser","Info":uf,"Detial":traceback.format_exc()})
        return ({"state":"CheckUser UnKnowErr"})
        
    try:
        userinfo = sqllib.GetLoginInfo ({'name':uf["name"]})
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":"Failed"})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"CheckUser","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"Failed"})

    shapassword = hashlib.sha256()
    shapassword.update((str(uf["password"])+userinfo['salt']).encode('utf-8'))
    t = time.mktime(userinfo["now"].timetuple())-time.mktime(userinfo["lastfailedtime"].timetuple())
    t = (t/3600)
    waitetime=WAITETIME*(WAITENUM**(userinfo["lgnfailedtimes"]-LOGINFAILEDTIMES+1))
    if userinfo["lgnfailedtimes"]>=LOGINFAILEDTIMES and t<waitetime:
        return ({"state":"Login Failed Too Many Times Try After %s Hour"%(float('%0.3f'%(waitetime-t)))})
    elif shapassword.hexdigest()==userinfo['saltpassword']:
        sqllib.CleanFailedTimes ({'name':uf["name"]})
        res = {}
        res["name"] = userinfo["name"]
        res["uid"] = userinfo["uid"]
        res["group"] = userinfo["group"]
        res["permission"] = userinfo["permission"]
        res["permissions"] = userinfo["permissions"]
        res["state"] = "success"
        return (res)
    else:
        sqllib.LoginFailed ({'name':uf["name"]})
        return ({"state":"Failed"})
    
def GetArtical(ActionInfo):#快速获取文章内容，用于主页展示和文章编辑

    try:
        ActionInfo = CheckParamet(["name","author","title"],ActionInfo)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"title":"Paramet Error","essay":e.err,"state":"Failed"})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"GetArtical","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"title":"GetArtical UnKnowErr","essay":"GetArtical UnKnowErr","state":"Failed"})

    #ActionInfo["title"] = CleanTitle(ActionInfo["title"])#id title共用关键字
    ActionInfo["id"] = 0
    if ActionInfo["title"].isdigit():
        ActionInfo["id"] = ActionInfo["title"]
    ActionInfo["mode"] = ActionInfo.get("mode",None)

    try:
        artical = sqllib.GetArtical(ActionInfo)
    except PermissionError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"title":"Permission Denied","essay":e.err,"state":"Failed"})
    except SqlError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"title":"No Such Title","essay":e.err,"state":"Failed"})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"GetArtical","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"title":"GetArtical UnkonwErr","essay":"GetArtical UnkonwErr","state":"Failed"})

    if artical["saltpassword"] is not None:#如果有密码
        if ActionInfo.get("mode",None)=="edit":#如果有传入密码
            artical["state"]="success"
        elif ActionInfo.get("password",None) is None:#如果没有传入密码
            return {"state":"Need Password","title":"Permission Denied","essay":"Need Password"}
        elif CheckArticalPassword({"saltpassword":artical["saltpassword"],"salt":artical["salt"],"password":ActionInfo.get("password","None")}):#如果有传入密码
            artical["state"]="success"
        else:#传入密码错误
            return {"state":"Failed","title":"Get Title Error","essay":"Get Essay Error"}
    else:
        artical["state"]="success"

    del artical["saltpassword"]
    del artical["salt"]
    del artical["uid"]
    artical["lastesttime"]=artical["lastesttime"].strftime('%Y-%m-%d %H:%M:%S')
    artical["pubtime"]=artical["pubtime"].strftime('%Y-%m-%d %H:%M:%S')
    return artical

        
def SubmitArtical(ActionInfo):
    
    try:
        ActionInfo = CheckParamet(["uid","name","author","title","essay","type"],ActionInfo)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SubmitArtical","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"SubmitArtical UnKnowErr"})
    
    #检查文章种类
    try:
        if CheckTitle(ActionInfo["title"]):
            sqllib.CreatArtical (ActionInfo)
            return({"state":"success"})
        else:
            return({"state":"Title Err"})
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SubmitArtical","Info":ActionInfo,"Detial":traceback.format_exc()})
        return("未知错误")

        
def EditArtical(ActionInfo):#修改文章
#ActionInfo=('title','name','essay','permission','password')
    try:
        ActionInfo = CheckParamet(["uid","name","author","title","rawtitle","essay","type"],ActionInfo,["password"])
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"EditArtical","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"EditArtical UnKnowErr"})
        
    if "password" in ActionInfo:
        if ActionInfo["password"]==str(RESETARTCALPASSWORD):#如果取消密码
            ActionInfo["saltpassword"]=None
            ActionInfo["salt"]=None
            del ActionInfo["password"]
        else:
            ActionInfo = CreateSaltAndPassword(ActionInfo)

    try:
        if sqllib.EditArtical(ActionInfo) is True:
            return ({"state":"success"})
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return({"state": e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"EditArtical","Info":ActionInfo,"Detial":traceback.format_exc()})
        return({"state": "EditArticle UnkonwErr"})

        
def DeleteArticalByNameTitle (ActionInfo):

    try:
        ActionInfo = CheckParamet(["uid","name","author","title"],ActionInfo)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"EditArtical","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"EditArtical UnKnowErr"})

    try:
        sqllib.DeleteArticalByNameTitle(ActionInfo)
        return ({"state":"success"})
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"DeleteArticalByNameTitle","Info":ActionInfo,"Detial":traceback.format_exc()})
        return({"state":"DeleteArtical Unknow Error"})

        
def GetArticalList(ActionInfo):

    try:
        ActionInfo = CheckParamet(["uid","name","author"],ActionInfo,["page","eachpage","order"])
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"GetArticalList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"GetArticalList UnKnowErr"})

    try:
        res = sqllib.GetArticalList (ActionInfo)
        count = res["count"]
        result = res["result"]
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return {'state':'false','articallist':e.err,'count':0}
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"GetArticalList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return {'state':'GetArticalList','articallist':e.err,'count':0}
    for artical in result:
        artical["lastesttime"]=artical["lastesttime"].strftime('%Y-%m-%d %H:%M:%S')
        artical["pubtime"]=artical["pubtime"].strftime('%Y-%m-%d %H:%M:%S')
        if artical["saltpassword"]==None:
            artical["password"]=0
        else:
            artical["password"]=1
        del artical["saltpassword"]
    return {'state':'success','articallist':result,'count':count}


def SpiderResponser(url):
    s = r'^\/(([\S\s]+?)\/)?(([\S\s]+?)\/)?$'
    try:
        a = re.match(s, url).groups()#1,3
    except:
        print(traceback.format_exc())
    if (a[1] != "list"):
        return GetSpiderArticle(a[1],a[3])
    elif (a[1] == "list"):
        pass
        
def GetSpiderArticle(user,title):
    if title is None:
        title = user
        user = PUBLICUSER
    af = {
        "mode":"GetArticle",
        "title":title,
        "name":user,
        "iflogin":False
    }
    res = GetArtical(af)
    return APIDERARTICLE.format(res["title"],res["essay"])
    
#保密性需求，是否要开放列表？
def GetSpiderArticleList(list,user):
    if user is None:
        user = PUBLICUSER
    af = {
        "mode":"GetArticleList",
        "name":user,
        "iflogin":False
    }
    res = GetArticalList(af)
    return 0
    
def SearchArticalList(ActionInfo):

    try:
        ActionInfo = CheckParamet(["uid","name","author"],ActionInfo,["page","eachpage","order"])
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SearchArticalList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"SearchArticalList UnKnowErr"})
        
    ActionInfo["keyword"] = ActionInfo["keyword"].strip()
    try:
        result = sqllib.SearchArtical (ActionInfo)
        for artical in result:
            artical["lastesttime"]=artical["lastesttime"].strftime('%Y-%m-%d %H:%M:%S')
            artical["pubtime"]=artical["pubtime"].strftime('%Y-%m-%d %H:%M:%S')
            if artical["name"]==PUBLICUSER:
                del artical["name"]
        return({'state':'success','keyword':ActionInfo["keyword"],'articallist':result})
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return({'state':e.err,'keyword':ActionInfo["keyword"]})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SearchArticalList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return({'state':'SearchArticalList UnknowErr','keyword':ActionInfo["keyword"]})
        
def CreateUser(ActionInfo):#生成用户，生成uid，生成盐
    import uuid
    
    try:
        ActionInfo = CheckParamet(["name","mail","password"],ActionInfo)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({'state':e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SearchArticalList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({'state':"SearchArticalList UnKnowErr"})
    
    #ActionInfo should have ('uid','name','mail','salt','saltpassword')
    #ActionInfo["name"] = ActionInfo["name"].lower()
    #ActionInfo["mail"] = ActionInfo["mail"].lower()
    
    t = str(int(time.time()))
    #生成salt
    salt = hashlib.sha256()
    salt.update((ActionInfo['password'][0:5]+t+ActionInfo['name'][0:4]).encode('utf-8'))
    ActionInfo["salt"] = salt.hexdigest()
    #生成hash256password
    hash256password = hashlib.sha256()
    hash256password.update((ActionInfo['password']).encode('utf-8'))
    ActionInfo['hash256password'] = hash256password.hexdigest()
    #生成saltpassword
    saltpassword = hashlib.sha256()
    saltpassword.update((ActionInfo['hash256password']+ActionInfo["salt"]).encode('utf-8'))
    ActionInfo['saltpassword'] = saltpassword.hexdigest()
    #生成uid
    ActionInfo['uid'] = str(uuid.uuid3(uuid.uuid1(), ActionInfo['mail']))
    try:
        mail.Send(ActionInfo["mail"],MAIL_TITLE_SIGNIN,MAIL_ARTICAL_SIGNIN)
        info = sqllib.CreateUser(ActionInfo)
        return ({'state':"success"})
    except (SqlError,PermissionError,MailError) as e:
        return ({'state':e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"CreateUser","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({'state':"CreateUser UnkonwErr"})

def ChangeUserPassword(ActionInfo):#更改密码，要求登录
    #ActionInfo should have name password newpassword
    try:
        ActionInfo = CheckParamet(["name","password","newpassword"],ActionInfo)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({'state':e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"ChangeUserPassword","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({'state':"ChangeUserPassword UnKnowErr"})
        
    userinfo = CheckUser(ActionInfo)
    if userinfo["state"] == "success":
        info = sqllib.GetUserInfo (ActionInfo)
        info["password"] = ActionInfo["newpassword"]
        info = CreateSaltAndPassword(info)
        try:
            mail.Send(info["mail"],MAIL_TITLE_CGPASSWORD,MAIL_ARTICAL_CGPASSWORD)
            sqllib.ResetPassword (info)
            return {'state':"success"}
        except (SqlError,PermissionError,MailError) as e:
            return {'state':e.err}
        except Exception as e:
            logger.Record("ERROR",str(e),{"Function":"ChangeUserPassword","Info":ActionInfo,"Detial":traceback.format_exc()})
            return ({'state':"ChangeUserPassword UnKnowErr"})
    else:
        return {'state':userinfo["state"]}

def ReCreateUserPassword(ActionInfo):#重置密码用户名
    import uuid
    #ActionInfo should have ('uid','name','mail','salt','saltpassword')
    try:
        ActionInfo = CheckParamet(["name","mail"],ActionInfo)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({'state':e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"ChangeUserPassword","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({'state':"ChangeUserPassword UnKnowErr"})


    info = sqllib.GetUserInfo (ActionInfo)
    if ActionInfo["mail"] == info["mail"]:
        newpassword = str(uuid.uuid3(uuid.uuid1(), ActionInfo['mail']))
        info["password"] = newpassword
        info = CreateSaltAndPassword(info)
        try:
            mail.Send(ActionInfo["mail"],MAIL_TITLE_RSPASSWORD,MAIL_ARTICAL_RSPASSWORD%(newpassword))
            sqllib.ResetPassword (info)#重置密码
            sqllib.CleanFailedTimes (info)#清空登录计数
            return {'state':"success"}
        except (SqlError,PermissionError,MailError) as e:
            return {'state':e.err}
    else:
        return {'state':"Mail Not Match"}

def CleanTitle(Title):
    Title = re.sub(r'\s',' ', Title)
    Title.replace("<","").replace(">","")
    return Title

def CleanArtical(Artical):
    Artical.replace("<script","").replace("script>","")
    Artical.replace("<iframe","").replace("iframe>","")
    Artical.replace("<link","")
    Artical.replace("<style","").replace("style>","")
    Artical.replace("<frameset","").replace("frameset>","")
    return Artical

        
def CheckUserName(Name):#检查用户名是否合法
    s = r'^[a-zA-Z][0-9a-zA-Z@.\-]{4,29}$'
    if re.match(s, Name):
        return True
    else:
        return False

def CheckUserId(uid):#检查用户名是否合法
        return True

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

def CheckTitle(Title):
    ForBidden = r'[\\#\$\?<>]'
    Allow = r'[\S\S]{%s,%s}'%(MIN_TITLE_LENGTH,MAX_TITLE_LENGTH)
    if re.match(ForBidden, Title) or not re.match(Allow, Title):
        return CheckArticleId(Title)
    else:
        return True

def CheckArticleId(Id):
        return Id.isdigit()
        
def CheckEssay(Essay):
    ForBidden = r'[(<script)(script>)(<iframe)(iframe>)(<link)(<style)(style>)(<frameset)(frameset>)]'
    Allow = r'[\S\S]{%s,%s}'%(MIN_ESSAY_LENGTH,MAX_ESSAY_LENGTH)
    if re.match(ForBidden, Essay) or not re.match(Allow, Essay):
        return False
    else:
        return True
        
def CheckKeyWord(KeyWord):
    s = r'[`=\/]'
    if re.match(s, KeyWord) or len(KeyWord.replace(" ",""))<MINSEARCHLENGTH or len(KeyWord.replace(" ",""))>MAXSEARCHLENGTH:
        return False
    else:
        return True  

def CheckArticleType(Type):
    if Type in ARTICALTYPELIST:
        return True
    else:
        return False
        
def CheckArticleListOrder(Order):
    if Order in ("ASC","DESC"):
        return True
    else:
        return False

def CheckArticleListPage(Page):
    if Page.isdigit() is True:
        return True
    else:
        return False
       
def CheckArticleListEachPage(EachPage):
    if EachPage.isdigit() is True and int(EachPage)<=MAX_EACHPAGE_NUM and int(EachPage)>=MIN_EACHPAGE_NUM:
        return True
    else:
        return False
       
def CheckParamet(ParametKeyList,ActionInfo,OptionalParametKeyList=[]):
    ParametKeySet = set(ParametKeyList+OptionalParametKeyList)
    OptionalParametKeySet = set(OptionalParametKeyList)
    CheckFunction = {
        "uid":CheckUserId,
        "name":CheckUserName,
        "author":CheckUserName,
        "title":CheckTitle,
        "rawtitle":CheckTitle,
        "essay":CheckEssay,
        "password":CheckUserPassword,
        "newpassword":CheckUserPassword,
        "mail":CheckUserMail,
        "keyword":CheckKeyWord,
        "type":CheckArticleType,
        "page":CheckArticleListPage,
        "eachpage":CheckArticleListEachPage,
        "order":CheckArticleListOrder,
        "id":CheckArticleId
    }
    ResInfo = {}
    if "name" in ParametKeySet:#必须有name字段，登录验证由session处理
        if  "name" not in ActionInfo:
            ActionInfo["name"]=PUBLICUSER
            ActionInfo["uid"]=PUBLICUSER
        else:
            if CheckFunction["name"](ActionInfo["name"].lower()) is True:
                ResInfo["name"] = ActionInfo["name"].lower()
                ParametKeySet.remove("name")
            else:
                if "name" not in OptionalParametKeySet:
                    raise NoteError("CheckParamet","IllLegal Paramet 'name':'%s'"%(ActionInfo["name"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
    
    if "author" in ParametKeySet:
        if  "author" not in ActionInfo:
            ActionInfo["author"]=PUBLICUSER
        else:
            if CheckFunction["author"](ActionInfo["author"].lower()) is True:
                ResInfo["author"] = ActionInfo["author"].lower()
                ParametKeySet.remove("author")
            else:
                if "author" not in OptionalParametKeySet:
                    raise NoteError("CheckParamet","IllLegal Paramet 'author':'%s'"%(ActionInfo["author"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
    
    if "mail" in ParametKeySet:
        if  "mail" not in ActionInfo:
            raise NoteError("CheckParamet","Missing Paramet %s"%(str(e)),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            if CheckFunction["mail"](ActionInfo["mail"].lower()) is True:
                ResInfo["mail"] = ActionInfo["mail"].lower()
                ParametKeySet.remove("mail")
            else:
                if "mail" not in OptionalParametKeySet:
                    raise NoteError("CheckParamet","IllLegal Paramet 'mail':'%s'"%(ActionInfo["mail"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
                    
    if "uid" in ParametKeySet:#必须有name字段，登录验证由session处理
        if  "uid" not in ActionInfo:
            raise NoteError("CheckParamet","Need to Login")
        else:
            if CheckFunction["uid"](ActionInfo["uid"]) is True:
                ResInfo["uid"] = ActionInfo["uid"]
                ParametKeySet.remove("uid")
            else:
                if "uid" not in OptionalParametKeySet:
                    raise NoteError("CheckParamet","IllLegal Paramet 'uid'",{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})

    if "page" in ParametKeySet:
        if "page" in ActionInfo:
            if CheckFunction["page"](ActionInfo["page"]) is True:
                ResInfo["page"] = int(ActionInfo["page"])
                ParametKeySet.remove("page")
            else:
                if "page" not in OptionalParametKeySet:
                    raise NoteError("CheckParamet","IllLegal Paramet 'page':'%s'"%(ActionInfo["page"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            ResInfo["page"] = 1
        
    if "eachpage" in ParametKeySet:
        if "eachpage" in ActionInfo:
            if CheckFunction["eachpage"](ActionInfo["eachpage"]) is True:
                ResInfo["eachpage"] = int(ActionInfo["eachpage"])
                ParametKeySet.remove("eachpage")
            else:
                if "eachpage" not in OptionalParametKeySet:
                    raise NoteError("CheckParamet","IllLegal Paramet 'eachpage':'%s'"%(ActionInfo["eachpage"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            ResInfo["eachpage"] = EACHPAGENUM

    if "order" in ParametKeySet:
        if "order" in ActionInfo:
            if CheckFunction["order"](ActionInfo["order"]) is True:
                ResInfo["order"] = ActionInfo["order"]
                ParametKeySet.remove("order")
            else:
                if "order" not in OptionalParametKeySet:
                    raise NoteError("CheckParamet","IllLegal Paramet 'order':'%s'"%(ActionInfo["eachpage"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            ResInfo["order"] = "DESC"
            
    for Key in ParametKeySet:
        try:
            if CheckFunction[Key](ActionInfo[Key]) is True:
                ResInfo[Key] = ActionInfo[Key]
            else:
                raise NoteError("CheckParamet","IllLegal Paramet ‘%s'"%(Key),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        except KeyError as e:
            if Key not in OptionalParametKeySet:
                raise NoteError("CheckParamet","Missing Paramet %s"%(str(e)),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        except Exception as e:
            print(traceback.format_exc())
            Info = {"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet}
            logger.Record("ERROR",str(e),{"Function":"CheckParamet","Info":Info,"Detial":traceback.format_exc()})
            raise NoteError("CheckParamet","CheckParamet UnknowErr",Info)
            
    return (ResInfo)
        
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

def CheckArticalPassword(ActionInfo):#发现文章有密码之后的操作
    shapassword = hashlib.sha256()
    shapassword.update((str(ActionInfo["password"])+ActionInfo['salt']).encode('utf-8'))
    if shapassword.hexdigest()==ActionInfo['saltpassword']:
        return True
    else:
        return False