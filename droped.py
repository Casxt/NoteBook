def GetUserInfo (uf):#��ѯ�û���Ϣ#�����ں�̨�������ݣ�
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

def UserInfoForArtical (uf):#��ѯ��������������Ϣ
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

def GetArticalInfo (af):#Ĭ�����еĹؼ��ʶ�����ģ������#�߼�����,�ֶ�����ͨ���
    SqlARTICALFIELD = str(ARTICALFIELD).replace("'","`")[1:-1]
    ######
    #ƴ���������
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