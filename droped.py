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

def UserInfoForArtical (uf):#查询创建文章所需信息
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
    
def TestGetArticalInfo():
    #'title','bluser','essay','right','blgroup'
    uf={'uid':"admin",
        }
    list = sqllib.GetArticalInfo (uf)
    return list

def GetArticalInfo (af):#默认所有的关键词都进行模糊搜索#高级搜索,手动输入通配符
    SqlARTICALFIELD = str(ARTICALFIELD).replace("'","`")[1:-1]
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
    sql =  """select """+SqlARTICALFIELD+""" from """+TABLE["artical"]+""" WHERE """+Search
    print(sql)
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    list=[]
    for value in values:
        list.append(dict(map(lambda x,y:[x,y],ARTICALFIELD,value)))
    return list    