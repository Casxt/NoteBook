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
#异常
#
####################################  
class SqlError(Exception):
    def __init__(self,FunctionName,Massage, Info=None):  
        self.info = Info
        self.function = FunctionName
        self.err = Massage
        Exception.__init__(self)
    
####################################
#
#权限查询接口
#
####################################
def MixPermission(Group, Addition):
    if Group is None or Group not in USER_GROUP:    
        Group = DEFAULT_GROUP
    per  = dict(USER_GROUP[Group])
    if Addition is None:
        return per
    else:
        Addition = json.loads(Addition)
        per.update(Addition)
    return per

def MixArticlePermission(Group, Addition):
    if Group is None or Group not in ARTICLE_GROUP:    
        Group = DEFAULT_ARTICLE_GROUP
    per  = dict(ARTICLE_GROUP[Group])
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
        Userinfo = dict(map(lambda x,y:[x,y],UserColumn,value))
        per = MixPermission(Userinfo["group"],Userinfo["permission"])
        return per
    elif value is None:
        raise SqlError("GetUserPermission","No Such Uid %s"%(uid))
    else:
        raise SqlError("GetUserPermission","Unknow Error")
        
def GetArticleInfo (cursor,title,uid):
    ArticleColumn = ('id','uid','name','group','permission')
    SqlArticleField = str(ArticleColumn).replace("'","`")[1:-1]
    if not title.isdigit():
        Sql =  """select """+SqlArticleField+""" from """+TABLE["article"]+""" WHERE `title`=%s AND `uid`=%s"""
    else:
        Sql =  """select """+SqlArticleField+""" from """+TABLE["article"]+""" WHERE `id`=%s AND `uid`=%s"""
    cursor.execute(Sql,(title,uid))
    value = cursor.fetchone()
    if value is not None:
        ArticleInfo = dict(map(lambda x,y:[x,y],ArticleColumn,value))
        per = MixArticlePermission(ArticleInfo["group"],ArticleInfo["permission"])
        UserPermission = GetUserPermission(cursor,ArticleInfo["uid"])
        UserPermission.update(per)
        ArticleInfo["permissions"] = UserPermission
    else:
        raise SqlError("GetArticleInfo","No Such Article %s"%(title))
    return ArticleInfo
    
####################################
#
#开关操作
#
####################################      
def SqlOpen():
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    return (conn,cursor)

def SqlClose(conn,cursor):
    cursor.close()
    conn.commit()
    conn.close()
    return None
    
####################################
#
#用户操作
#
####################################      
def CreateUser (uf):#创建用户
    column = ['uid','name','mail','salt','saltpassword','group','lastfailedtime','time']
    Column = "("+str(column).replace("'","`")[1:-1]+")"
    (conn,cursor) = SqlOpen()
    try:
        sql =   """insert into """+TABLE["user"]+""" """+Column+""" values (%s,%s,%s,%s,%s,now(),now())"""
        cursor.execute(sql,(uf["uid"],uf["name"],uf["mail"],uf["salt"],uf["saltpassword"],uf["group"]))
    except pymysql.err.IntegrityError as e:
        err = str(e)
        if "Duplicate entry" in err:
            if "name" in err:
                raise SqlError("CreateUser","Name:%s Already Exist"%(uf["name"]),uf)
            elif "mail" in err:
                raise SqlError("CreateUser","Mail:%s Already Exist"%(uf["mail"]),uf)
        else:
            raise SqlError("CreateUser",traceback.format_exc(),ActionInfo)
    finally:
        SqlClose(conn,cursor)
    return True

def GetUid (name,cursor,*l):#快速查询uid，permission，group,可追加字段
    uf={}
    usercolumn=['uid','name','permission','articlenum','group']
    usercolumn.extend(l)
    SqlUserField = str(usercolumn).replace("'","`")[1:-1]
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `name`=%s """
    cursor.execute(sql,(name))
    value = cursor.fetchone()
    if value is not None:
        uf = dict(map(lambda x,y:[x,y],usercolumn,value))
        uf["permissions"] = MixPermission(uf["group"],uf["permission"])
    else:
        raise SqlError("GetUid","No Such UserName:%s"%(name))
    return uf
    
def GetName (uid,cursor,*l):#快速查询uid，permission，group
    uf={}
    usercolumn=['uid','name','permission','articlenum','group']
    usercolumn.extend(l)
    SqlUserField = str(usercolumn).replace("'","`")[1:-1]
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `uid`=%s """
    cursor.execute(sql,(uid))
    value = cursor.fetchone()
    if value is not None:
        uf = dict(map(lambda x,y:[x,y],usercolumn,value))
        uf["permissions"] = MixPermission(uf["group"],uf["permission"])
    else:
        raise SqlError("GetName","No Such Uid:%s"%(uid))
    return uf

def GetUserInfo (ActionInfo):#获取user信息
    (conn,cursor) = SqlOpen()
    value = GetUid (ActionInfo["name"],cursor,"mail")
    SqlClose(conn,cursor)
    return value
    
def GetLoginInfo (ActionInfo):#登录查询用
    #id,uid,name
    logincolumn=['uid','name','salt','saltpassword','permission','group','lgnfailedtimes','lastfailedtime']
    SqlUserField = str(logincolumn).replace("'","`")[1:-1]
    (conn,cursor) = SqlOpen()
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `name`=%s OR `mail`=%s """
    cursor.execute(sql,(ActionInfo["name"],ActionInfo["name"]))
    value = cursor.fetchone()
    sql =  """select now()"""
    cursor.execute(sql)
    time = cursor.fetchone()[0]#fetchone返回结果数组，取第一个元素
    SqlClose(conn,cursor)
    if value is None:
        raise SqlError("GetLoginInfo","No Such User %s"%(name),ActionInfo)
    else:
        d = dict(map(lambda x,y:[x,y],logincolumn,value))
        d["now"] = time
        d['permissions'] = MixPermission(d['group'], d['permission'])
    return d
    
def LoginFailed (ActionInfo):#登录失败计数
    #id,uid,name
    (conn,cursor) = SqlOpen()
    sql =  """update """+TABLE["user"]+""" SET `lgnfailedtimes`=(`lgnfailedtimes`+1),`lastfailedtime`=now() WHERE `name`=%s """
    cursor.execute(sql,(ActionInfo["name"]))
    SqlClose(conn,cursor)
    return True
    
def CleanFailedTimes (uf):#登录成功清除计数
    #name
    (conn,cursor) = SqlOpen()
    sql =  """update """+TABLE["user"]+""" SET `lgnfailedtimes`=0,`lastfailedtime`=now() WHERE `name`=%s """
    cursor.execute(sql,(uf["name"]))
    SqlClose(conn,cursor)
    return True

def ResetPassword (uf):#重置密码
    #id,uid,name
    (conn,cursor) = SqlOpen()
    sql =  """update """+TABLE["user"]+""" SET `salt`=%s,`saltpassword`=%s WHERE `uid`=%s """
    cursor.execute(sql,(uf["salt"],uf["saltpassword"],uf["uid"]))
    SqlClose(conn,cursor)
    return True
    
####################################
#
#文章操作
#
####################################

def CreatArticle (ActionInfo):#创建文章
    #{"Weight": 100,"ReadArticleList":["Self"],"MaxArticleNum": 50,"ReadArticle": ["Self"]}
    Articlecolumn = ['title','uid','name','essay','type','tag','permission','group','salt','saltpassword','remark','pubtime','lastesttime']
    ArticleColumn = '('+str(Articlecolumn).replace("'","`")[1:-1]+')'
    (conn,cursor) = SqlOpen()
    #获取用户信息,鉴权
    uf = GetName (ActionInfo["uid"],cursor)
    if uf is None:
        SqlClose(conn,cursor)
        raise SqlError("CreatArticle","No Such User %s"%(ActionInfo["uid"]),ActionInfo)
    ActionInfo.update(uf)
    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)
    Per = Permission.CreateArticle(ActionInfo,ActionInfo["authorInfo"])
    if "articlepermissions" in ActionInfo:
        ArticlePer = Permission.SetArticlePermissions(ActionInfo,ActionInfo["articlepermissions"])
    else:
        ArticlePer = True
    if "articelgroup" in ActionInfo:
        ArticleGroupPer = Permission.SetArticlePermissionGroup(ActionInfo,ActionInfo["articelgroup"])
    else:
        ArticleGroupPer = True
    if Per is True and ArticlePer is True and ArticleGroupPer is True:
        try:
            #创建文章
            ArticleSql = """insert into """+TABLE["article"]+""" """+ArticleColumn+""" values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())"""
            cursor.execute(ArticleSql,(ActionInfo["title"],ActionInfo["authorInfo"]["uid"],ActionInfo["name"],ActionInfo["essay"],ActionInfo.get("type",DEFAULTARTICLETYPE),ActionInfo.get("tag",None),ActionInfo.get("articlepermissions",None),ActionInfo.get("articlegroup",None),ActionInfo.get("salt",None),ActionInfo.get("saltpassword",None),ActionInfo.get("remark",None)))
            #若上句执行错误则不会执行下句
            UserSql = """update """+TABLE["user"]+""" set `articlenum`=(`articlenum`+1) where `uid`=%s"""
            cursor.execute(UserSql,(ActionInfo["authorInfo"]["uid"]))
        except pymysql.err.IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise SqlError("CreatArticle","User:'%s' Duplicate entry Title"%ActionInfo["name"],ActionInfo)
            else:
                raise SqlError("CreatArticle",traceback.format_exc(),ActionInfo)
        finally:
            SqlClose(conn,cursor)
        return True

def EditArticle (ActionInfo):
    ARTICLEFIELD=['title','essay','type','tag','group','salt','saltpassword','remark']
    #拼接set语句
    SetUpdateColumn = ""
    SetUpdateInfo=[]
    for key in ARTICLEFIELD:
        if key in ActionInfo:
            SetUpdateColumn = SetUpdateColumn+"`"+str(key)+"`=%s,"
            SetUpdateInfo.append(ActionInfo[key])
        if "permission" in ActionInfo:
            pass
    (conn,cursor) = SqlOpen()
    #获取用户信息,鉴权
    if "uid" not in ActionInfo:#没有uid就用name获取
        ActionInfo.update(GetUid(ActionInfo['name'],cursor))
        
    ActionInfo.update(GetName(ActionInfo['uid'],cursor))
    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)
    try:
        ArticleInfo = GetArticleInfo(cursor,ActionInfo['rawtitle'],ActionInfo["authorInfo"]["uid"])
    except SqlError as e:
        SqlClose(conn,cursor)
        raise SqlError("EditArticle","No Such Article '%s' Belong to '%s'!!"%(ActionInfo["title"],ActionInfo["author"]),ActionInfo)
    
    Per = Permission.EditArticle(ActionInfo,ArticleInfo)
    if Per is True:
        try:
            SetUpdateInfo.append(ActionInfo["authorInfo"]["uid"])
            SetUpdateInfo.append(ActionInfo["rawtitle"])
            sql = """update """+TABLE["article"]+""" set """+SetUpdateColumn+"""`lastesttime`=now() where `uid`=%s AND `title`=%s"""
            num = cursor.execute(sql,SetUpdateInfo)
        except pymysql.err.IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise SqlError("EditArticle","标题重复",ActionInfo)
            else:
                raise SqlError("EditArticle",traceback.format_exc(),ActionInfo)
        finally:
            SqlClose(conn,cursor)
        return True
        
def DeleteArticleByNameTitle (ActionInfo):#必须登陆后才能删除，必须带uid
    (conn,cursor) = SqlOpen()
    ActionInfo.update(GetUid(ActionInfo['name'],cursor))
    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)
    try:
        ArticleInfo = GetArticleInfo(cursor,ActionInfo['title'],ActionInfo['authorInfo']['uid'])
    except SqlError as e:
        SqlClose(conn,cursor)
        raise SqlError("DeleteArticleByNameTitle","No Such Article '%s' Belong to '%s'!!"%(ActionInfo["title"],ActionInfo["author"]),ActionInfo)
    
    Per = Permission.DeleteArticle(ActionInfo,ArticleInfo)
    if Per is True:
        #DELETE FROM 表名称 WHERE 列名称 = 值
        ArticleSql =  """DELETE from """+TABLE["article"]+""" WHERE `uid`=%s AND `title`=%s """
        values = cursor.execute(ArticleSql,(ActionInfo["uid"],ActionInfo["title"]))
        UserSql = """update """+TABLE["user"]+""" set `articlenum`=(`articlenum`-1) where `uid`=%s"""
        cursor.execute(UserSql,(ActionInfo["uid"]))
        SqlClose(conn,cursor)
        return values
        
def GetArticle (ActionInfo):#直接获取文章信息
    Articlecolumn=('id','uid','name','title','essay','type','tag','permission','group','pubtime','lastesttime','salt','saltpassword')
    ArticleColumn = str(Articlecolumn).replace("'","`")[1:-1]
    (conn,cursor) = SqlOpen()
    ######
    #拼接索搜语句
    ######
    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)
    ActionInfo.update(GetUid(ActionInfo['name'],cursor))
    #pprint(ActionInfo)
    
    try:
        if "title" in ActionInfo:
            ArticleInfo = GetArticleInfo(cursor,ActionInfo['title'],ActionInfo["authorInfo"]["uid"])
        else:
            ArticleInfo = GetArticleInfo(cursor,ActionInfo['id'],ActionInfo["authorInfo"]["uid"])
    except SqlError as e:
        SqlClose(conn,cursor)
        raise SqlError("GetArticle","No Such Article '%s' Belong to '%s' !!"%(ActionInfo["title"],ActionInfo["author"]),ActionInfo)
    
    if ActionInfo["mode"] == "edit":
        Per = Permission.EditArticle(ActionInfo,ArticleInfo)
    else:
        Per = Permission.ReadArticle(ActionInfo,ArticleInfo)
        
    if Per is True:
        if "title" in ActionInfo:
            sql =  """select """+ArticleColumn+""" from """+TABLE["article"]+""" WHERE `name`=%s AND `title`=%s"""
            cursor.execute(sql,(ActionInfo["author"],ActionInfo["title"]))
        else:
            sql =  """select """+ArticleColumn+""" from """+TABLE["article"]+""" WHERE `name`=%s AND `id`=%s"""
            cursor.execute(sql,(ActionInfo["author"],ActionInfo["id"]))
        value = cursor.fetchone()
        SqlClose(conn,cursor)
        #若文章不存在，则在GetArticleInfo时已经开始报错
        d = dict(zip(Articlecolumn,value))
        return d

def GetArticleList (ActionInfo):#获取文章列表
    #ActionInfo应有page一项,eachpage,order 升序asc /降序desc
    Articlecolumn=['id','name','title','type','tag','saltpassword','permission','group','pubtime','lastesttime']
    ArticleColumn = str(Articlecolumn).replace("'","`")[1:-1]
    (conn,cursor) = SqlOpen()
    ######
    #拼接索搜语句
    ######
    ActionInfo["authorInfo"] = GetUid(ActionInfo['author'],cursor)
    ActionInfo.update(GetUid(ActionInfo['name'],cursor))
    #pprint(ActionInfo)
    Per = Permission.ReadArticleList(ActionInfo,ActionInfo["authorInfo"])
    if Per is True:
        if ActionInfo["order"] == "ASC":
            sql =  """select """+ArticleColumn+""" from """+TABLE["article"]+""" WHERE `uid`=%s ORDER BY `id` Limit %s,%s """
        else:
            sql =  """select """+ArticleColumn+""" from """+TABLE["article"]+""" WHERE `uid`=%s ORDER BY `id` DESC Limit %s,%s """
        cursor.execute(sql,(ActionInfo["authorInfo"]["uid"],(ActionInfo["page"]-1)*ActionInfo["eachpage"],ActionInfo["eachpage"]))
        values = cursor.fetchall()
        CountSql =  """select COUNT(*) from """+TABLE["article"]+""" WHERE `uid`=%s"""
        cursor.execute(CountSql,(ActionInfo["authorInfo"]["uid"]))
        num = cursor.fetchall()
        SqlClose(conn,cursor)
        res = {"result":[]}
        res["count"] = num
        for value in values:
            d = dict(zip(Articlecolumn,value))
            d["ifpassword"] = False if (d["saltpassword"]==None) else True
            res["result"].append(d)
        return res

def SearchArticle (ActionInfo):#简单搜索#必须保证搜索词为关键词用单个空格分开的形式
    #搜索权限设计？
    Articlecolumn=['id','name','title','essay','type','permission','group','pubtime','lastesttime']
    ArticleColumn = str(Articlecolumn).replace("'","`")[1:-1]
    ######
    #拼接索搜语句
    #登录才能使用
    #是否能全局搜索？暂定不能
    ######
    (conn,cursor) = SqlOpen()
    if "uid" not in ActionInfo:
        ActionInfo["uid"]=GetUid (ActionInfo.get("name",PUBLICUSER),cursor)["uid"]
    keyword = '%'+ActionInfo['keyword'].replace(" ","%")+'%'
    sql =  """select """+ArticleColumn+""" from """+TABLE["article"]+""" 
    WHERE ( `uid`=%s OR `uid`=%s ) AND `saltpassword` is NULL 
    AND ( `essay` LIKE %s OR  `title` LIKE %s) LIMIT 0,20"""
    cursor.execute(sql,(ActionInfo["uid"],PUBLICUSER,keyword,keyword))
    values = cursor.fetchall()
    SqlClose(conn,cursor)
    result = []
    for value in values:
        result.append(dict(zip(Articlecolumn,value)))
    return result

####################################
#
#初始化表
#
####################################
def DefineUserTable ():#取得查询所需的关键字
    (conn,cursor) = SqlOpen()
    sql =   """CREATE TABLE `"""+TABLE["user"]+"""` ( 
            `id`  int NOT NULL AUTO_INCREMENT ,
            `uid`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `name`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `mail`  varchar(50) CHARACTER SET utf8 NOT NULL  ,
            `salt`  text CHARACTER SET utf8 NOT NULL ,
            `saltpassword`  text CHARACTER SET utf8 NOT NULL ,
            `permission`  text CHARACTER SET utf8 NULL,
            `articlenum`  int DEFAULT 0 ,
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
    cursor.execute(sql)
    SqlClose(conn,cursor)
    return True
def DefineArticleTable ():#文章表
    (conn,cursor) = SqlOpen()
    sql =   """CREATE TABLE `"""+TABLE["article"]+"""` (
            `id`  bigint NOT NULL AUTO_INCREMENT ,
            `uid`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `name`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `title`  varchar(100) CHARACTER SET utf8 NOT NULL ,
            `essay`  longtext CHARACTER SET utf8 NOT NULL ,
            `type`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `tag`  text CHARACTER SET utf8 NULL ,
            `permission`  text CHARACTER SET utf8 NULL ,
            `group`  varchar(255) CHARACTER SET utf8 NULL ,
            `salt`  text CHARACTER SET utf8 NULL ,
            `saltpassword`  text CHARACTER SET utf8 NULL ,
            `remark`  text CHARACTER SET utf8 NULL ,
            `pubtime`  datetime NOT NULL ,
            `lastesttime`  datetime NOT NULL ,
            UNIQUE KEY(`uid`, `title`) ,
            INDEX (`uid`),
            INDEX (`title`),
            INDEX (`group`),
            FOREIGN KEY (`uid`) REFERENCES `"""+TABLE["user"]+"""` (`uid`),
            PRIMARY KEY (`id`)
            )"""
    cursor.execute(sql)
    SqlClose(conn,cursor)
    return True
def DefineArticleSearchTable ():#文章查询表
    (conn,cursor) = SqlOpen()
    sql =   """CREATE TABLE `"""+TABLE["search"]+"""` (
            `id`  bigint NOT NULL AUTO_INCREMENT ,
            `uid`  varchar(40) CHARACTER SET utf8 NOT NULL ,
            `b64title`  varchar(255) CHARACTER SET utf8 NOT NULL ,
            `b64essay`  longtext CHARACTER SET utf8 NOT NULL ,
            `b64tag`  text CHARACTER SET utf8 NULL ,
            `permission`  int DEFAULT 0,
            `group`  varchar(255) CHARACTER SET utf8 NULL ,
            `b64remark`  text CHARACTER SET utf8 NULL ,
            `pubtime`  datetime NOT NULL ,
            `lastesttime`  datetime NOT NULL ,
            INDEX (`uid`),
            INDEX (`group`),
            FULLTEXT (`b64title`),
            FULLTEXT (`b64essay`),
            FULLTEXT (`b64tag`),
            PRIMARY KEY (`id`)
            )
            ENGINE=MyISAM"""
    cursor.execute(sql)
    SqlClose(conn,cursor)
    return True