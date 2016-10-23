#/usr/bin/python3.4
import pymysql
import base64
import time
try:
    from note.config import *
except:
    from config import *
####################################
#
#用户操作
#
####################################      
def FastCreateUser (uf):#快速创建用户
    column = ('uid','name','saltpassword','mail','salt','right','time')
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

def GetUid (name,cursor,*l):#快速查询uid，right，group,可追加字段
    uf={}
    usercolumn=['uid','name','right','group']
    usercolumn.extend(l)
    SqlUserField = str(usercolumn).replace("'","`")[1:-1]
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `name`=%s """
    cursor.execute(sql,(name))
    value = cursor.fetchone()
    if value is not None:
        uf = dict(map(lambda x,y:[x,y],usercolumn,value))
    elif value is None:
        return("No Such User %s"%(name))
    else:
        return("CreatArtical Failed")
    return uf
    
def GetName (uid,cursor,*l):#快速查询uid，right，group
    uf={}
    usercolumn=['uid','name','right','group']
    usercolumn.extend(l)
    SqlUserField = str(usercolumn).replace("'","`")[1:-1]
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `uid`=%s """
    cursor.execute(sql,(uid))
    value = cursor.fetchone()
    if value is not None:
        uf = dict(map(lambda x,y:[x,y],usercolumn,value))
    elif value is None:
        return("No Such Uid %s"%(name))
    else:
        return("CreatArtical Failed")
    return uf

def GetUserInfo (af):#获取user信息
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    value = GetUid (af["name"],cursor,"mail")
    cursor.close()
    conn.commit()
    conn.close()
    return value
    
def GetLoginInfo (uf):#登录查询用
    #id,uid,name
    logincolumn=('uid','name','salt','saltpassword','lgnfailedtimes','lastfailedtime')
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
    af={}
    usercolumn=['remark','right']
    usercolumn.extend(l)
    SqlUserField = str(usercolumn).replace("'","`")[1:-1]
    sql =  """select """+SqlUserField+""" from """+TABLE["artical"]+""" WHERE `uid`=%s AND `title`=%s"""
    cursor.execute(sql,(uid,title))
    value = cursor.fetchone()
    if value is not None:
        af = dict(map(lambda x,y:[x,y],usercolumn,value))
    elif value is None:
        return("No Such Uid %s Title %s"%(uid,title))
    else:
        return("GetRemark Failed")
    return af
    
def b64(text):
    if text is None:
        return None
    bytesString = text.encode("utf-8")
    encodestr = base64.b64encode(bytesString)
    return (encodestr.decode())
    
def FastCreatArtical (af):#快速创建文章
    Articalcolumn = ('uid','title','right','essay','pubtime','lastesttime')
    ArticalColumn = str(Articalcolumn).replace("'","`")
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    #创建文章
    sql =   """insert into """+TABLE["artical"]+""" """+ArticalColumn+""" values (%s,%s,%s,%s,now(),now())"""
    cursor.execute(sql,(af.get("uid",PUBLICUSER),af["title"],af.get("right",0),af["essay"]))
    cursor.close()
    conn.commit()
    conn.close()
    return True

def CreatArtical (af):#创建文章
    Articalcolumn = ('title','uid','name','essay','type','tag','right','blgroup','salt','saltpassword','remark','pubtime','lastesttime')
    ArticalColumn = str(Articalcolumn).replace("'","`")
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    #获取用户信息,鉴权
    uf = GetName (af["uid"],cursor)
    af["name"] = uf["name"]
    if uf is not None:
        af["uid"] = uf["uid"]
        af["right"] = min(int(uf["right"]),int(af.get("right",1)))#取数字最小值做权限
        if (uf["group"] is None) or ("blgroup" not in af) or (af["blgroup"] not in value[2]):
            af["blgroup"] = None
    elif uf is None:
        return("No Such User %s"%(af["uid"]))
    else:
        return("CreatArtical Failed")
    #创建文章
    sql = """insert into """+TABLE["artical"]+""" """+ArticalColumn+""" values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())"""
    cursor.execute(sql,(af["title"],af["uid"],af["name"],af["essay"],af.get("type",DEFAULTARTICALTYPE),af.get("tag",None),af.get("right",0),af.get("blgroup",None),af.get("salt",None),af.get("saltpassword",None),af.get("remark",None)))
    cursor.close()
    conn.commit()
    conn.close()
    return True    

def EditArtical (af):
    ARTICALFIELD=('title','essay','type','tag','right','blgroup','salt','saltpassword','remark')
    #拼接set语句
    SetUpdateColumn = ""
    SetUpdateInfo=[]
    for key in ARTICALFIELD:
        if key in af:
            SetUpdateColumn = SetUpdateColumn+"`"+str(key)+"`=%s,"
            SetUpdateInfo.append(af[key])
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    #获取用户信息,鉴权
    if af.get("uid",None) is None:#没有uid就用name获取
        uf = GetUid(af['name'],cursor)
        af["uid"] = uf["uid"]
        af["right"] = uf["right"]
        af["group"] = uf["group"]
    SetUpdateInfo.append(af["uid"])
    SetUpdateInfo.append(af["rawtitle"])
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

def GetArtical (af):#直接获取文章信息
    Articalcolumn=('id','uid','name','title','essay','type','tag','right','blgroup','pubtime','lastesttime','salt','saltpassword')
    ArticalColumn = str(Articalcolumn).replace("'","`")[1:-1]
    ######
    #拼接索搜语句
    ######
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """select """+ArticalColumn+""" from """+TABLE["artical"]+""" WHERE `name`=%s AND  (`id`=%s OR `title`=%s)"""
    cursor.execute(sql,(af["name"],af.get("id",None),af.get("title",None)))
    value = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()
    if value is not None:
        d = dict(zip(Articalcolumn,value))
        return d
    return None

def GetArticalList (af):#获取文章列表
    #af应有page一项,eachpage
    Articalcolumn=('id','name','title','type','tag','saltpassword','right','blgroup','pubtime','lastesttime')#,'essay'
    ArticalColumn = str(Articalcolumn).replace("'","`")[1:-1]
    ######
    #拼接索搜语句
    ######
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """select """+ArticalColumn+""" from """+TABLE["artical"]+""" WHERE `uid`=%s ORDER BY `id` DESC Limit %s,%s """
    cursor.execute(sql,(af["uid"],(af["page"]-1)*af["eachpage"],af["eachpage"]))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    result = []
    for value in values:
        d = dict(zip(Articalcolumn,value))
        d["ifpassword"] = False if (d["saltpassword"]==None) else True
        result.append(d)
    print(len(values))
    return result

def CountArticalList (af):#获取用户文章数目
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """select COUNT(*) from """+TABLE["artical"]+""" WHERE `uid`=%s"""
    cursor.execute(sql,(af["uid"]))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return values
    
def SearchArtical (af):#简单搜索#必须保证搜索词为关键词用单个空格分开的形式
    Articalcolumn=('id','name','title','essay','type','right','blgroup','pubtime','lastesttime')
    ArticalColumn = str(Articalcolumn).replace("'","`")[1:-1]
    ######
    #拼接索搜语句
    #登录才能使用
    #是否能全局搜索？暂定不能
    ######
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    if "uid" not in af:
        af["uid"]=GetUid (af.get("name",PUBLICUSER),cursor)["uid"]
    keyword = '%'+af['keyword'].replace(" ","%")+'%'
    sql =  """select """+ArticalColumn+""" from """+TABLE["artical"]+""" WHERE ( `uid`=%s OR `uid`=%s ) AND 
    `saltpassword` is NULL AND ( `essay` LIKE %s OR  `title` LIKE %s) LIMIT 0,20"""
    cursor.execute(sql,(af["uid"],PUBLICUSER,keyword,keyword))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    result = []
    for value in values:
        result.append(dict(zip(Articalcolumn,value)))
    return result

def DeleteArticalByNameTitle (af):#必须登陆后才能删除，必须带uid
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    #DELETE FROM 表名称 WHERE 列名称 = 值
    sql =  """DELETE from """+TABLE["artical"]+""" WHERE `uid`=%s AND `title`=%s """
    values = cursor.execute(sql,(af["uid"],af["title"]))
    cursor.close()
    conn.commit()
    conn.close()
    return values
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
            `right`  int DEFAULT 0,
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
            `right`  int DEFAULT 0,
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
            `right`  int DEFAULT 0,
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