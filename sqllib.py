
#/usr/bin/python3.4
import traceback
import pymysql
import base64
import time
import json
from pprint import pprint
try:
    from note.config import *
    import note.permission as Permission
except:
    from config import *
    import permission as Permission
####################################
#
#预操作接口
#
####################################  
def api (function,**arg):#快速创建用户
    column = ('uid','name','saltpassword','mail','salt','permission','time')
    Column = str(column).replace("'","`")
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    function(cursor,**arg)
    cursor.close()
    conn.commit()
    conn.close()
    return True
    
####################################
#
#权限查询接口
#
####################################
def MixPermission(Group, Addition):
    if Group is None:    
        Group = "Default"
    per  = dict(USER_GROUP[Group])
    if Addition is None:
        return per
    else:
        Addition  = json.loads(Addition)
        per.update(Addition)
    return per
    
def GetUserPermission (cursor,uid):
    UserColumn = ('permission','group')
    SqlUserField = str(UserColumn).replace("'","`")[1:-1]
    UserSql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `uid`=%s"""
    cursor.execute(UserSql,(uid))
    value = cursor.fetchone()
    if value is not None:
        permission = dict(map(lambda x,y:[x,y],UserColumn,value))
        per = MixPermission(permission["group"],permission["permission"])
        return per
    elif value is None:
        return("No Such Uid %s"%(uid))
    else:
        return("GetUserPermission Failed")
        
def GetArticleInfo (cursor,title,uid):
    ArticleColumn = ('id','uid','blgroup','permission')
    SqlArticleField = str(ArticleColumn).replace("'","`")[1:-1]
    Sql =  """select """+SqlArticleField+""" from """+TABLE["artical"]+""" WHERE `title`=%s AND `uid`=%s"""
    cursor.execute(Sql,(title,uid))
    value = cursor.fetchone()
    if value is not None:
        ArticleInfo = dict(map(lambda x,y:[x,y],ArticleColumn,value))
        if ArticleInfo["permission"] is None:
            ArticleInfo["permission"] = {}
        else:
            ArticleInfo["permission"] = json.loads(ArticleInfo["permission"])
        UserPermission = GetUserPermission(cursor,ArticleInfo["uid"])
        UserPermission.update(ArticleInfo["permission"])
        ArticleInfo["permissions"] = UserPermission
        return ArticleInfo
    elif value is None:
        return("No Such title %s"%(title))
    else:
        return("GetArticlePermission Failed")
####################################
#
#用户操作
#
####################################      
def FastCreateUser (uf):#快速创建用户
    column = ('uid','name','saltpassword','mail','salt','permission','time')
    Column = str(column).replace("'","`")
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =   """insert into """+TABLE["user"]+" "+Column+""" values (%s,%s,%s,%s,%s,0,now())"""
    cursor.execute(sql,(uf["uid"],uf["name"],uf["saltpassword"],uf["mail"],uf["salt"]))
    cursor.close()
    conn.commit()
    conn.close()
    return True

def CreateUser (uf):#创建用户
    column = ('uid','name','mail','salt','saltpassword','lastfailedtime','time')
    Column = str(column).replace("'","`")
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =   """insert into """+TABLE["user"]+""" """+Column+""" values (%s,%s,%s,%s,%s,now(),now())"""
    cursor.execute(sql,(uf["uid"],uf["name"],uf["mail"],uf["salt"],uf["saltpassword"]))
    cursor.close()
    conn.commit()
    conn.close()
    return True

def GetUid (name,cursor,*l):#快速查询uid，permission，group,可追加字段
    uf={}
    usercolumn=['uid','name','permission','articalnum','group']
    usercolumn.extend(l)
    SqlUserField = str(usercolumn).replace("'","`")[1:-1]
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `name`=%s """
    cursor.execute(sql,(name))
    value = cursor.fetchone()
    print (value)
    if value is not None:
        uf = dict(map(lambda x,y:[x,y],usercolumn,value))
        uf["permissions"] = MixPermission(uf["group"],uf["permission"])
    elif value is None:
        return("No Such User %s"%(name))
    else:
        return("CreatArtical Failed")
    return uf
    
def GetName (uid,cursor,*l):#快速查询uid，permission，group
    uf={}
    usercolumn=['uid','name','permission','articalnum','group']
    usercolumn.extend(l)
    SqlUserField = str(usercolumn).replace("'","`")[1:-1]
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `uid`=%s """
    cursor.execute(sql,(uid))
    value = cursor.fetchone()
    if value is not None:
        uf = dict(map(lambda x,y:[x,y],usercolumn,value))
        uf["permissions"] = MixPermission(uf["group"],uf["permission"])
    elif value is None:
        return("No Such Uid %s"%(name))
    else:
        return("CreatArtical Failed")
    return uf

def GetUserInfo (ActionInfo):#获取user信息
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    value = GetUid (ActionInfo["name"],cursor,"mail")
    cursor.close()
    conn.commit()
    conn.close()
    return value
    
def GetLoginInfo (uf):#登录查询用
    #id,uid,name
    logincolumn=('uid','name','salt','saltpassword','permission','group','lgnfailedtimes','lastfailedtime')
    SqlUserField = str(logincolumn).replace("'","`")[1:-1]
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `name`=%s OR `mail`=%s """
    cursor.execute(sql,(uf["name"],uf["name"]))
    value = cursor.fetchone()
    sql =  """select now()"""
    cursor.execute(sql)
    time = cursor.fetchone()[0]#fetchone返回结果数组，取第一个元素
    print(time)
    cursor.close()
    conn.commit()
    conn.close()
    if value is None:
        return None
    d = dict(map(lambda x,y:[x,y],logincolumn,value))
    d["now"] = time
    d['permissions'] = MixPermission(d['group'], d['permission'])
    return d
    
def LoginFailed (uf):#登录失败计数
    #id,uid,name
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """update """+TABLE["user"]+""" SET `lgnfailedtimes`=(`lgnfailedtimes`+1),`lastfailedtime`=now() WHERE `name`=%s """
    print(uf["name"])
    print(cursor.execute(sql,(uf["name"])))
    cursor.close()
    conn.commit()
    conn.close()
    return True
    
def CleanFailedTimes (uf):#登录成功清除计数
    #name
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """update """+TABLE["user"]+""" SET `lgnfailedtimes`=0,`lastfailedtime`=now() WHERE `name`=%s """
    print(sql)
    cursor.execute(sql,(uf["name"]))
    cursor.close()
    conn.commit()
    conn.close()
    return True

def ResetPassword (uf):#重置密码
    #id,uid,name
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """update """+TABLE["user"]+""" SET `salt`=%s,`saltpassword`=%s WHERE `uid`=%s """
    cursor.execute(sql,(uf["salt"],uf["saltpassword"],uf["uid"]))
    cursor.close()
    conn.commit()
    conn.close()
    return True
    
####################################
#
#文章操作
#
####################################
def GetRemark (uid,title,cursor,*l):#快速查询remark 等
    ActionInfo={}
    usercolumn=['remark','permission']
    usercolumn.extend(l)
    SqlUserField = str(usercolumn).replace("'","`")[1:-1]
    sql =  """select """+SqlUserField+""" from """+TABLE["artical"]+""" WHERE `uid`=%s AND `title`=%s"""
    cursor.execute(sql,(uid,title))
    value = cursor.fetchone()
    if value is not None:
        ActionInfo = dict(map(lambda x,y:[x,y],usercolumn,value))
    elif value is None:
        return("No Such Uid %s Title %s"%(uid,title))
    else:
        return("GetRemark Failed")
    return ActionInfo
    
def b64(text):
    if text is None:
        return None
    bytesString = text.encode("utf-8")
    encodestr = base64.b64encode(bytesString)
    return (encodestr.decode())
    
def FastCreatArtical (ActionInfo):#快速创建文章
    Articalcolumn = ('uid','title','permission','essay','pubtime','lastesttime')
    ArticalColumn = str(Articalcolumn).replace("'","`")
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    #创建文章
    ArticleSql = """insert into """+TABLE["artical"]+""" """+ArticalColumn+""" values (%s,%s,%s,%s,now(),now())"""
    cursor.execute(ArticleSql,(ActionInfo.get("uid",PUBLICUSER),ActionInfo["title"],ActionInfo.get("permission",0),ActionInfo["essay"]))
    UserSql = """update """+TABLE["user"]+""" set `articalnum`=(`articalnum`+1) where `uid`=%s"""
    cursor.execute(UserSql,(ActionInfo.get("uid",PUBLICUSER)))
    cursor.close()
    conn.commit()
    conn.close()
    return True

def CreatArtical (ActionInfo):#创建文章
    Articalcolumn = ('title','uid','name','essay','type','tag','permission','blgroup','salt','saltpassword','remark','pubtime','lastesttime')
    ArticalColumn = str(Articalcolumn).replace("'","`")
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    #获取用户信息,鉴权
    uf = GetName (ActionInfo["uid"],cursor)
    if uf is None:
        cursor.close()
        conn.commit()
        conn.close()
        return("No Such User %s"%(ActionInfo["uid"]))
        
    ActionInfo.update(uf)

    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)

    Per = Permission.CreateArticle(ActionInfo,ActionInfo["authorInfo"])
    print(Per)
    if Per is True:
        #创建文章
        ArticleSql = """insert into """+TABLE["artical"]+""" """+ArticalColumn+""" values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())"""
        cursor.execute(ArticleSql,(ActionInfo["title"],ActionInfo["authorInfo"]["uid"],ActionInfo["name"],ActionInfo["essay"],ActionInfo.get("type",DEFAULTARTICALTYPE),ActionInfo.get("tag",None),ActionInfo.get("permission",None),ActionInfo.get("blgroup",None),ActionInfo.get("salt",None),ActionInfo.get("saltpassword",None),ActionInfo.get("remark",None)))
        #若上句执行错误则不会执行下句
        UserSql = """update """+TABLE["user"]+""" set `articalnum`=(`articalnum`+1) where `uid`=%s"""
        cursor.execute(UserSql,(ActionInfo["uid"]))
    else:
        cursor.close()
        conn.commit()
        conn.close()
        return(Per)
    cursor.close()
    conn.commit()
    conn.close()
    return True    

def EditArtical (ActionInfo):
    ARTICALFIELD=('title','essay','type','tag','permission','blgroup','salt','saltpassword','remark')
    #拼接set语句
    SetUpdateColumn = ""
    SetUpdateInfo=[]
    for key in ARTICALFIELD:
        if key in ActionInfo:
            SetUpdateColumn = SetUpdateColumn+"`"+str(key)+"`=%s,"
            SetUpdateInfo.append(ActionInfo[key])
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    #获取用户信息,鉴权
    if "uid" not in ActionInfo:#没有uid就用name获取
        ActionInfo.update(GetUid(ActionInfo['name'],cursor))
        
    ActionInfo.update(GetName(ActionInfo['uid'],cursor))
    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)

    ArticleInfo = GetArticleInfo(cursor,ActionInfo['title'],ActionInfo["authorInfo"]["uid"])
    pprint(ArticleInfo)
    t = Permission.EditArticle(ActionInfo,ArticleInfo)
    SetUpdateInfo.append(ActionInfo["authorInfo"]["uid"])
    SetUpdateInfo.append(ActionInfo["rawtitle"])
    sql = """update """+TABLE["artical"]+""" set """+SetUpdateColumn+"""`lastesttime`=now() where `uid`=%s AND `title`=%s"""
    num = cursor.execute(sql,SetUpdateInfo)
    if num>1:
        #一次更新多条！
        print("EditArtical Err！！",sql)
        return False
    cursor.close()
    conn.commit()
    conn.close()
    if num==1:
        return True
    else:
        return num
        
def DeleteArticalByNameTitle (ActionInfo):#必须登陆后才能删除，必须带uid
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    uf = GetUid(ActionInfo['name'],cursor)
    
    ActionInfo.update(uf)
    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)
    ArticleInfo = GetArticleInfo(cursor,ActionInfo['title'],ActionInfo['authorInfo']['uid'])
    
    Per = Permission.DeleteArticle(ActionInfo,ArticleInfo)
    if Per is True:
        #DELETE FROM 表名称 WHERE 列名称 = 值
        ArticleSql =  """DELETE from """+TABLE["artical"]+""" WHERE `uid`=%s AND `title`=%s """
        values = cursor.execute(ArticleSql,(ActionInfo["uid"],ActionInfo["title"]))
        UserSql = """update """+TABLE["user"]+""" set `articalnum`=(`articalnum`-1) where `uid`=%s"""
        cursor.execute(UserSql,(ActionInfo["uid"]))
    else:
        value = 0
    cursor.close()
    conn.commit()
    conn.close()
    return values
        
def GetArtical (ActionInfo):#直接获取文章信息
    Articalcolumn=('id','uid','name','title','essay','type','tag','permission','blgroup','pubtime','lastesttime','salt','saltpassword')
    ArticalColumn = str(Articalcolumn).replace("'","`")[1:-1]
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    ######
    #拼接索搜语句
    ######
    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)
    ActionInfo.update(GetName(ActionInfo['uid'],cursor))
    #pprint(ActionInfo)
    ArticleInfo = GetArticleInfo(cursor,ActionInfo['title'],ActionInfo["authorInfo"]["uid"])
    if ActionInfo["mode"] == "edit":
        Per = Permission.EditArticle(ActionInfo,ArticleInfo)
    else:
        Per = Permission.ReadArticle(ActionInfo,ArticleInfo)
    if Per is True:
        sql =  """select """+ArticalColumn+""" from """+TABLE["artical"]+""" WHERE `name`=%s AND  (`id`=%s OR `title`=%s)"""
        cursor.execute(sql,(ActionInfo["author"],ActionInfo.get("id",None),ActionInfo.get("title",None)))
        value = cursor.fetchone()
        cursor.close()
        conn.commit()
        conn.close()
        if value is not None:
            d = dict(zip(Articalcolumn,value))
            return d
        else:
            return None
    else:
        return None

def GetArticalList (ActionInfo):#获取文章列表
    #ActionInfo应有page一项,eachpage
    Articalcolumn=('id','name','title','type','tag','saltpassword','permission','blgroup','pubtime','lastesttime')#,'essay'
    ArticalColumn = str(Articalcolumn).replace("'","`")[1:-1]
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    
    ######
    #拼接索搜语句
    ######
    
    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)
    ActionInfo.update(GetName(ActionInfo['uid'],cursor))
    #pprint(ActionInfo)
    Per = Permission.ReadArticleList(ActionInfo,ActionInfo["authorInfo"])
    
    if Per is True:
        sql =  """select """+ArticalColumn+""" from """+TABLE["artical"]+""" WHERE `uid`=%s ORDER BY `id` DESC Limit %s,%s """
        cursor.execute(sql,(ActionInfo["authorInfo"]["uid"],(ActionInfo["page"]-1)*ActionInfo["eachpage"],ActionInfo["eachpage"]))
        values = cursor.fetchall()
        CountSql =  """select COUNT(*) from """+TABLE["artical"]+""" WHERE `uid`=%s"""
        cursor.execute(CountSql,(ActionInfo["authorInfo"]["uid"]))
        num = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        res = {"result":[]}
        res["count"] = num
        for value in values:
            d = dict(zip(Articalcolumn,value))
            d["ifpassword"] = False if (d["saltpassword"]==None) else True
            res["result"].append(d)
        return res
    else:
        cursor.close()
        conn.commit()
        conn.close()
        return None
        
def CountArticalList (ActionInfo):#获取用户文章数目#废弃
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """select COUNT(*) from """+TABLE["artical"]+""" WHERE `uid`=%s"""
    cursor.execute(sql,(ActionInfo["uid"]))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return values
    
def SearchArtical (ActionInfo):#简单搜索#必须保证搜索词为关键词用单个空格分开的形式
    #搜索权限设计？
    Articalcolumn=('id','name','title','essay','type','permission','blgroup','pubtime','lastesttime')
    ArticalColumn = str(Articalcolumn).replace("'","`")[1:-1]
    ######
    #拼接索搜语句
    #登录才能使用
    #是否能全局搜索？暂定不能
    ######
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    if "uid" not in ActionInfo:
        ActionInfo["uid"]=GetUid (ActionInfo.get("name",PUBLICUSER),cursor)["uid"]
    keyword = '%'+ActionInfo['keyword'].replace(" ","%")+'%'
    sql =  """select """+ArticalColumn+""" from """+TABLE["artical"]+""" WHERE ( `uid`=%s OR `uid`=%s ) AND 
    `saltpassword` is NULL AND ( `essay` LIKE %s OR  `title` LIKE %s) LIMIT 0,20"""
    cursor.execute(sql,(ActionInfo["uid"],PUBLICUSER,keyword,keyword))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    result = []
    for value in values:
        result.append(dict(zip(Articalcolumn,value)))
    return result

####################################
#
#初始化表
#
####################################
def DefineUserTable ():#取得查询所需的关键字
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =   """CREATE TABLE `"""+TABLE["user"]+"""` ( 
            `id`  int NOT NULL AUTO_INCREMENT ,
            `uid`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `name`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `mail`  varchar(50) CHARACTER SET utf8 NOT NULL  ,
            `salt`  text CHARACTER SET utf8 NOT NULL ,
            `saltpassword`  text CHARACTER SET utf8 NOT NULL ,
            `permission`  text CHARACTER SET utf8 NULL,
            `articalnum`  int DEFAULT 0 ,
            `lgnfailedtimes`  int DEFAULT 0 ,
            `group`  text CHARACTER SET utf8 NULL ,
            `remark`  text CHARACTER SET utf8 NULL ,
            `lastfailedtime`  datetime NULL ,
            `time`  datetime NULL ,
            UNIQUE INDEX (uid),
            UNIQUE INDEX (name),
            UNIQUE INDEX (mail),
            PRIMARY KEY (`id`)
            )"""
            #`prikey`  text CHARACTER SET utf8 NULL ,
            #`pubkey`  text CHARACTER SET utf8 NULL ,
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    return True
def DefineArticalTable ():#文章表
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =   """CREATE TABLE `"""+TABLE["artical"]+"""` (
            `id`  bigint NOT NULL AUTO_INCREMENT ,
            `uid`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `name`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `title`  varchar(100) CHARACTER SET utf8 NOT NULL ,
            `essay`  longtext CHARACTER SET utf8 NOT NULL ,
            `type`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `tag`  text CHARACTER SET utf8 NULL ,
            `permission`  text CHARACTER SET utf8 NULL ,
            `blgroup`  varchar(255) CHARACTER SET utf8 NULL ,
            `salt`  text CHARACTER SET utf8 NULL ,
            `saltpassword`  text CHARACTER SET utf8 NULL ,
            `remark`  text CHARACTER SET utf8 NULL ,
            `pubtime`  datetime NOT NULL ,
            `lastesttime`  datetime NOT NULL ,
            UNIQUE KEY(`uid`, `title`) ,
            INDEX (`uid`),
            INDEX (`title`),
            INDEX (`blgroup`),
            FOREIGN KEY (`uid`) REFERENCES `"""+TABLE["user"]+"""` (`uid`),
            PRIMARY KEY (`id`)
            )"""
            #`pubkey`  text CHARACTER SET utf8 NULL ,
            #`prikey`  text CHARACTER SET utf8 NULL ,
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    return True
def DefineArticalSearchTable ():#文章查询表
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =   """CREATE TABLE `"""+TABLE["search"]+"""` (
            `id`  bigint NOT NULL AUTO_INCREMENT ,
            `uid`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `b64title`  varchar(255) CHARACTER SET utf8 NOT NULL ,
            `b64essay`  longtext CHARACTER SET utf8 NOT NULL ,
            `b64tag`  text CHARACTER SET utf8 NULL ,
            `permission`  int DEFAULT 0,
            `blgroup`  varchar(255) CHARACTER SET utf8 NULL ,
            `b64remark`  text CHARACTER SET utf8 NULL ,
            `pubtime`  datetime NOT NULL ,
            `lastesttime`  datetime NOT NULL ,
            INDEX (`uid`),
            INDEX (`blgroup`),
            FULLTEXT (`b64title`),
            FULLTEXT (`b64essay`),
            FULLTEXT (`b64tag`),
            PRIMARY KEY (`id`)
            )
            ENGINE=MyISAM"""
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    return True