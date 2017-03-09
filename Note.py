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
    
def GetArticle(ActionInfo):#快速获取文章内容，用于主页展示和文章编辑

    try:
        ActionInfo = CheckParamet(("title","mode"),ActionInfo,("author","name"))
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"title":"Paramet Error","essay":e.err,"state":"Failed"})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"GetArticle","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"title":"GetArticle UnKnowErr","essay":"GetArticle UnKnowErr","state":"Failed"})

    #ActionInfo["title"] = CleanTitle(ActionInfo["title"])#id title共用关键字
    ActionInfo["id"] = 0
    if ActionInfo["title"].isdigit():
        ActionInfo["id"] = ActionInfo["title"]
        del ActionInfo["title"]

    try:
        article = sqllib.GetArticle(ActionInfo)
    except PermissionError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"title":"Permission Denied","essay":e.err,"state":"Failed"})
    except SqlError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"title":"No Such Title","essay":e.err,"state":"Failed"})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"GetArticle","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"title":"GetArticle UnkonwErr","essay":"GetArticle UnkonwErr","state":"Failed"})

    if article["saltpassword"] is not None:#如果有密码
        article["havepassword"]=True
        if ActionInfo["mode"]=="edit":#如果有传入密码
            article["state"]="success"
        elif ActionInfo.get("password",None) is None:#如果没有传入密码
            return {"state":"Need Password","title":"Permission Denied","essay":"Need Password"}
        elif CheckArticlePassword({"saltpassword":article["saltpassword"],"salt":article["salt"],"password":ActionInfo.get("password","None")}):#如果有传入密码
            article["state"]="success"
        else:#传入密码错误
            return {"state":"Failed","title":"Get Title Error","essay":"Get Essay Error"}
    else:
        article["havepassword"]=False
        article["state"]="success"

    del article["saltpassword"]
    del article["salt"]
    del article["uid"]
    article["lastesttime"]=article["lastesttime"].strftime('%Y-%m-%d %H:%M:%S')
    article["pubtime"]=article["pubtime"].strftime('%Y-%m-%d %H:%M:%S')
    return article

        
def SubmitArticle(ActionInfo):
    
    try:
        ActionInfo = CheckParamet(["uid","name","author","title","essay","type"],ActionInfo)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SubmitArticle","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"SubmitArticle UnKnowErr"})
    
    #检查文章种类
    try:
        if CheckTitle(ActionInfo["title"]):
            sqllib.CreatArticle (ActionInfo)
            return({"state":"success"})
        else:
            return({"state":"Title Err"})
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SubmitArticle","Info":ActionInfo,"Detial":traceback.format_exc()})
        return("未知错误")

        
def EditArticle(ActionInfo):#修改文章
#ActionInfo=('title','name','essay','permission','password')
    try:
        ActionInfo = CheckParamet(["uid","name","author","title","rawtitle","essay","type"],ActionInfo,["password"])
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"EditArticle","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"EditArticle UnKnowErr"})
        
    if "password" in ActionInfo:
        if ActionInfo["password"]==str(RESETARTCALPASSWORD):#如果取消密码
            ActionInfo["saltpassword"]=None
            ActionInfo["salt"]=None
            del ActionInfo["password"]
        else:
            ActionInfo = CreateSaltAndPassword(ActionInfo)

    try:
        if sqllib.EditArticle(ActionInfo) is True:
            return ({"state":"success"})
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return({"state": e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"EditArticle","Info":ActionInfo,"Detial":traceback.format_exc()})
        return({"state": "EditArticle UnkonwErr"})

        
def DeleteArticleByNameTitle (ActionInfo):

    try:
        ActionInfo = CheckParamet(["uid","name","author","title"],ActionInfo)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"EditArticle","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"EditArticle UnKnowErr"})

    try:
        sqllib.DeleteArticleByNameTitle(ActionInfo)
        return ({"state":"success"})
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"DeleteArticleByNameTitle","Info":ActionInfo,"Detial":traceback.format_exc()})
        return({"state":"DeleteArticle Unknow Error"})

        
def GetArticleList(ActionInfo):

    try:
        ActionInfo = CheckParamet(["uid","name"],ActionInfo,["page","eachpage","order","author"])
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"GetArticleList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"GetArticleList UnKnowErr"})

    try:
        res = sqllib.GetArticleList (ActionInfo)
        count = res["count"]
        result = res["result"]
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return {'state':e.err}
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"GetArticleList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return {'state':'GetArticleList UnKnowErr'}
    for article in result:
        article["lastesttime"]=article["lastesttime"].strftime('%Y-%m-%d %H:%M:%S')
        article["pubtime"]=article["pubtime"].strftime('%Y-%m-%d %H:%M:%S')
        if article["saltpassword"]==None:
            article["password"]=0
        else:
            article["password"]=1
        del article["saltpassword"]
    return {'state':'success','articlelist':result,'count':count}


def SpiderResponser(url):
    s = r'^\/(([\S\s]+?)\/)?(([\S\s]+?)\/)?$'
    a = re.match(s, url).groups()#1,3
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
    res = GetArticle(af)
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
    res = GetArticleList(af)
    return 0
    
def SearchArticleList(ActionInfo):

    try:
        ActionInfo = CheckParamet(("uid","name","keyword"),ActionInfo,("page","eachpage","order","author"))
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({"state":e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SearchArticleList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({"state":"SearchArticleList UnKnowErr"})
        
    ActionInfo["keyword"] = ActionInfo["keyword"].strip()
    try:
        result = sqllib.SearchArticle (ActionInfo)
        for article in result:
            article["lastesttime"]=article["lastesttime"].strftime('%Y-%m-%d %H:%M:%S')
            article["pubtime"]=article["pubtime"].strftime('%Y-%m-%d %H:%M:%S')
            if article["name"]==PUBLICUSER:
                del article["name"]
        return({'state':'success','keyword':ActionInfo["keyword"],'articlelist':result})
    except (SqlError,PermissionError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return({'state':e.err,'keyword':ActionInfo["keyword"]})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SearchArticleList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return({'state':'SearchArticleList UnknowErr','keyword':ActionInfo["keyword"]})
        
def CreateUser(ActionInfo):#生成用户，生成uid，生成盐
    import uuid
    
    try:
        ActionInfo = CheckParamet(["name","mail","password","group"],ActionInfo)
    except NoteError as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return ({'state':e.err})
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"SearchArticleList","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({'state':"SearchArticleList UnKnowErr"})
    
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
        mail.Send(ActionInfo["mail"],MAIL_TITLE_SIGNIN,MAIL_ARTICLE_SIGNIN)
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
        try:
            info = sqllib.GetUserInfo (ActionInfo)
            info["password"] = ActionInfo["newpassword"]
            info = CreateSaltAndPassword(info)
            mail.Send(info["mail"],MAIL_TITLE_CGPASSWORD,MAIL_ARTICLE_CGPASSWORD)
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

    try:
        info = sqllib.GetUserInfo(ActionInfo)
    except (SqlError,PermissionError,MailError) as e:
        logger.Record("INFO",e.err,{"Function":e.function,"Info":e.info})
        return {'state':e.err}
    except Exception as e:
        logger.Record("ERROR",str(e),{"Function":"ReCreateUserPassword","Info":ActionInfo,"Detial":traceback.format_exc()})
        return ({'state':"ReCreateUserPassword UnKnowErr"})
        
    if ActionInfo["mail"] == info["mail"]:
        newpassword = str(uuid.uuid3(uuid.uuid1(), ActionInfo['mail']))
        info["password"] = newpassword
        info = CreateSaltAndPassword(info)
        try:
            mail.Send(ActionInfo["mail"],MAIL_TITLE_RSPASSWORD,MAIL_ARTICLE_RSPASSWORD%(newpassword))
            sqllib.ResetPassword (info)#重置密码
            sqllib.CleanFailedTimes (info)#清空登录计数
            return {'state':"success"}
        except (SqlError,PermissionError,MailError) as e:
            return {'state':e.err}
        except Exception as e:
            logger.Record("ERROR",str(e),{"Function":"ReCreateUserPassword","Info":ActionInfo,"Detial":traceback.format_exc()})
            return ({'state':"ReCreateUserPassword UnKnowErr"})
    else:
        return {'state':"Mail Not Match"}

# def CleanTitle(Title):
    # Title = re.sub(r'\s',' ', Title)
    # Title.replace("<","").replace(">","")
    # return Title

# def CleanArticle(Article):
    # Article.replace("<script","").replace("script>","")
    # Article.replace("<iframe","").replace("iframe>","")
    # Article.replace("<link","")
    # Article.replace("<style","").replace("style>","")
    # Article.replace("<frameset","").replace("frameset>","")
    # return Article

        
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

def CheckUserGroup(Group):#检查用户组
    if Group in USER_GROUP:
        return True
    else:
        return False
        
def CheckTitle(Title):
    ForBidden = r'[\\#\$\?<>]'
    Allow = r'^\S[\S\s]{%s,%s}$'%(MIN_TITLE_LENGTH-1,MAX_TITLE_LENGTH-1)
    if re.match(ForBidden, Title) or not re.match(Allow, Title):
        return CheckArticleId(Title)
    else:
        return True

def CheckArticleId(Id):
        return Id.isdigit()
        
def CheckEssay(Essay):
    ForBidden = r'((<script)|(script>)|(<iframe)|(iframe>)|(<link)|(<style)|(style>)|(<frameset)|(frameset>))'
    Allow = r'^[\S\s]{%s,%s}$'%(MIN_ESSAY_LENGTH,MAX_ESSAY_LENGTH)
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
    if Type in ARTICLETYPELIST:
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

def CheckMode(Mode):
    if Mode in MODE_LIST:
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
        "group":CheckUserGroup,
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
        "id":CheckArticleId,
        "mode":CheckMode
    }
    ResInfo = {}
    
    if "essay" in ParametKeySet:#必须有name字段，登录验证由session处理
        if CheckFunction["essay"](ActionInfo["essay"]) is True:
            ResInfo["essay"] = ActionInfo["essay"]
            ParametKeySet.remove("essay")
        else:
            raise NoteError("CheckParamet","IllLegal Paramet 'essay'",{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
                
    if "name" in ParametKeySet:#必须有name字段，登录验证由session处理
        if  "name" in ActionInfo: 
            if CheckFunction["name"](ActionInfo["name"].lower()) is True:
                ResInfo["name"] = ActionInfo["name"].lower()
                ParametKeySet.remove("name")
            else:
                raise NoteError("CheckParamet","IllLegal Paramet 'name':'%s'"%(ActionInfo["author"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            if "name" in OptionalParametKeySet:
                ActionInfo["name"]=PUBLICUSER
                ActionInfo["uid"]=PUBLICUSER
            else:
                raise NoteError("CheckParamet","Missing Paramet 'name'",{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
                
    if "author" in ParametKeySet:
        if  "author" in ActionInfo:
            if CheckFunction["author"](ActionInfo["author"].lower()) is True:
                ResInfo["author"] = ActionInfo["author"].lower()
                ParametKeySet.remove("author")
            else:
                raise NoteError("CheckParamet","IllLegal Paramet 'author':'%s'"%(ActionInfo["author"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            if "author" in OptionalParametKeySet:
                ActionInfo["author"]=PUBLICUSER
            else:
                raise NoteError("CheckParamet","Missing Paramet 'author'",{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
    
    if "group" in ParametKeySet:
        if  "group" in ActionInfo:
            if CheckFunction["group"](ActionInfo["group"]) is True:
                ResInfo["group"] = ActionInfo["group"]
                ParametKeySet.remove("group")
            else:
                raise NoteError("CheckParamet","IllLegal Paramet 'group':'%s'"%(ActionInfo["group"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            if "group" in OptionalParametKeySet:
                ActionInfo["group"]=DEFAULT_GROUP
            else:
                raise NoteError("CheckParamet","Missing Paramet 'group'",{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
    
    if "mail" in ParametKeySet:
        if  "mail" in ActionInfo:
            if CheckFunction["mail"](ActionInfo["mail"].lower()) is True:
                ResInfo["mail"] = ActionInfo["mail"].lower()
                ParametKeySet.remove("mail")
            else:
                raise NoteError("CheckParamet","IllLegal Paramet 'mail':'%s'"%(ActionInfo["mail"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            if "mail" in OptionalParametKeySet:
                raise NoteError("CheckParamet","Missing Paramet %s"%(str(e)),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
            else:
                raise NoteError("CheckParamet","Missing Paramet %s"%(str(e)),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
                    
    if "uid" in ParametKeySet:#必须有name字段，登录验证由session处理
        if  "uid" in ActionInfo:
            if CheckFunction["uid"](ActionInfo["uid"]) is True:
                ResInfo["uid"] = ActionInfo["uid"]
                ParametKeySet.remove("uid")
            else:
                raise NoteError("CheckParamet","IllLegal Paramet 'uid'",{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            if "uid" in OptionalParametKeySet:
                raise NoteError("CheckParamet","Need to Login")
                #要不要允许默认值?
            else:
                raise NoteError("CheckParamet","Need to Login")


    if "page" in ParametKeySet:
        if "page" in ActionInfo:
            if CheckFunction["page"](ActionInfo["page"]) is True:
                ResInfo["page"] = int(ActionInfo["page"])
                ParametKeySet.remove("page")
            else:
                raise NoteError("CheckParamet","IllLegal Paramet 'page':'%s'"%(ActionInfo["page"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            if "page" in OptionalParametKeySet:
                ResInfo["page"] = 1
            else:
                raise NoteError("CheckParamet","Missing Paramet 'page'",{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})

    if "eachpage" in ParametKeySet:
        if "eachpage" in ActionInfo:
            if CheckFunction["eachpage"](ActionInfo["eachpage"]) is True:
                ResInfo["eachpage"] = int(ActionInfo["eachpage"])
                ParametKeySet.remove("eachpage")
            else:
                raise NoteError("CheckParamet","IllLegal Paramet 'eachpage':'%s'"%(ActionInfo["eachpage"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            if "eachpage" in OptionalParametKeySet:
                ResInfo["eachpage"] = EACHPAGENUM
            else:
                raise NoteError("CheckParamet","Missing Paramet 'eachpage'",{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})

    if "order" in ParametKeySet:
        if "order" in ActionInfo:
            if CheckFunction["order"](ActionInfo["order"]) is True:
                ResInfo["order"] = ActionInfo["order"]
                ParametKeySet.remove("order")
            else:
                raise NoteError("CheckParamet","IllLegal Paramet 'order':'%s'"%(ActionInfo["order"]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        else:
            if "order" in OptionalParametKeySet:
                ResInfo["order"] = "DESC"
            else:
                raise NoteError("CheckParamet","Missing Paramet 'order'",{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
            
    for Key in ParametKeySet:
        try:
            if CheckFunction[Key](ActionInfo[Key]) is True:
                ResInfo[Key] = ActionInfo[Key]
            else:
                if Key!="essay":
                    raise NoteError("CheckParamet","IllLegal Paramet '%s':'%s'"%(Key,ActionInfo[Key]),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
                else:
                    raise NoteError("CheckParamet","IllLegal Paramet '%s'"%(Key),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
        except KeyError as e:
            if Key in OptionalParametKeySet:
                pass
            else:
                raise NoteError("CheckParamet","Missing Paramet '%s'"%(Key),{"ActionInfo":ActionInfo,"ParametKeySet":ParametKeySet})
            
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

def CheckArticlePassword(ActionInfo):#发现文章有密码之后的操作
    shapassword = hashlib.sha256()
    shapassword.update((str(ActionInfo["password"])+ActionInfo['salt']).encode('utf-8'))
    if shapassword.hexdigest()==ActionInfo['saltpassword']:
        return True
    else:
        return False