def GetUserInfo (uf):#查询用户信息#仅用于后台传输数据！
    #id,uid,name
    SqlUserField = str(USERFIELD).replace("'","`")[1:-1]
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `id`=%s  OR `uid`=%s OR `name` LIKE %s"""
    print(sql)
    cursor.execute(sql,(uf.get("id",""),uf.get("uid",""),uf.get("name","")))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    list=[]
    for value in values:
        list.append(dict(map(lambda x,y:[x,y],USERFIELD,value)))
    return list

def UserInfoForArticle (uf):#查询创建文章所需信息
    #id,uid,name
    usercolumn=('uid','name','right')
    SqlUserField = str(column).replace("'","`")[1:-1]
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """select """+SqlUserField+""" from """+TABLE["user"]+""" WHERE `name`=%s """
    cursor.execute(sql,(uf["name"]))
    value = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()
    if value is None:
        return None
    d = dict(map(lambda x,y:[x,y],logincolumn,value))
    return d
    
def TestGetArticleInfo():
    #'title','bluser','essay','right','blgroup'
    uf={'uid':"admin",
        }
    list = sqllib.GetArticleInfo (uf)
    return list

def GetArticleInfo (af):#默认所有的关键词都进行模糊搜索#高级搜索,手动输入通配符
    SqlARTICLEFIELD = str(ARTICLEFIELD).replace("'","`")[1:-1]
    ######
    #拼接索搜语句
    a = ""
    for key in af:
        s ="`"+key+"` LIKE '"+af[key]+"' OR "
        a = a+s
    Search = a[0:-4]
    ######
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """select """+SqlARTICLEFIELD+""" from """+TABLE["article"]+""" WHERE """+Search
    print(sql)
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    list=[]
    for value in values:
        list.append(dict(map(lambda x,y:[x,y],ARTICLEFIELD,value)))
    return list   

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


def GetRemark (uid,title,cursor,*l):#快速查询remark 等
    ActionInfo={}
    usercolumn=['remark','permission']
    usercolumn.extend(l)
    SqlUserField = str(usercolumn).replace("'","`")[1:-1]
    sql =  """select """+SqlUserField+""" from """+TABLE["article"]+""" WHERE `uid`=%s AND `title`=%s"""
    cursor.execute(sql,(uid,title))
    value = cursor.fetchone()
    if value is not None:
        ActionInfo = dict(map(lambda x,y:[x,y],usercolumn,value))
    else:
        raise SqlError("GetRemark","No Such Uid %s Title %s"%(uid,title))
    return ActionInfo

def FastCreatArticle (ActionInfo):#快速创建文章
    Articlecolumn = ('uid','title','permission','essay','pubtime','lastesttime')
    ArticleColumn = str(Articlecolumn).replace("'","`")
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    #创建文章
    ArticleSql = """insert into """+TABLE["article"]+""" """+ArticleColumn+""" values (%s,%s,%s,%s,now(),now())"""
    cursor.execute(ArticleSql,(ActionInfo.get("uid",PUBLICUSER),ActionInfo["title"],ActionInfo.get("permission",0),ActionInfo["essay"]))
    UserSql = """update """+TABLE["user"]+""" set `articlenum`=(`articlenum`+1) where `uid`=%s"""
    cursor.execute(UserSql,(ActionInfo.get("uid",PUBLICUSER)))
    cursor.close()
    conn.commit()
    conn.close()
    return True
    
def b64(text):
    if text is None:
        return None
    bytesString = text.encode("utf-8")
    encodestr = base64.b64encode(bytesString)
    return (encodestr.decode())    
    
def CountArticleList (ActionInfo):#获取用户文章数目#废弃
    conn = pymysql.connect(**SQLCONFIG)
    cursor = conn.cursor()
    sql =  """select COUNT(*) from """+TABLE["article"]+""" WHERE `uid`=%s"""
    cursor.execute(sql,(ActionInfo["uid"]))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return values