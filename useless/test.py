import sqllib
import Note
import hashlib
import base64
import re
###########################
#  
#NOTE检查
#  
###########################
def TestCheckUser():
    shapassword = hashlib.sha256()
    shapassword.update(("admin").encode('utf-8'))
    #print(shapassword.hexdigest())
    return(Note.CheckUser({'name':"admin@ad-min.cn",'password':shapassword.hexdigest()}))

def TestCheckUserName():
    return(Note.CheckUserName("admin"))

def TestNoteCreateUser():
    uf={
        'name':'testuser',
        'password':"testuser",
        'mail':'tst@ad-min.cn',
        }
    r = Note.CreateUser (uf)
    return r
###########################
#  
#sqllib检查
#  
###########################
def TestFastCreateUser():
    password = hashlib.sha256()
    shapassword = hashlib.sha256()
    shapassword.update(("admin").encode('utf-8'))
    password.update((shapassword.hexdigest()+"salt").encode('utf-8'))
    uf={'uid':'admin',
        'name':'admin',
        'saltpassword':password.hexdigest(),
        'mail':'admin@ad-min.cn',
        'salt':'salt'
        }
    sqllib.FastCreateUser (uf)
    return 1
    
def TestSqllibCreateUser():
    password = hashlib.sha256()
    shapassword = hashlib.sha256()
    shapassword.update(("test").encode('utf-8'))
    password.update((shapassword.hexdigest()+"salt").encode('utf-8'))
    uf={'uid':'test',
        'name':'test',
        'saltpassword':password.hexdigest(),
        'mail':'test@ad-min.cn',
        'salt':'salt'
        }
    sqllib.CreateUser (uf)
    return 1    
    
def TestCreatArtical():
    #'bluser','title','right','essay'
    uf={'name':'admin',
        'title':'TestCreatArtical',
        'essay':'FirstTestCreatArtical',
        'right':0,
        }
    sqllib.CreatArtical (uf)
    uf={'name':'admin',
    'title':'sadwdwdzvw',
    'essay':'dfeddhnrgvfewv4',
    'right':0,
    "blgroup":None,
    "password":"123456",
    "remark":"4242"
    }
    sqllib.CreatArtical (uf)
    return 1
    
    
def TestFastCreatArtical():
    #'bluser','title','right','essay'
    uf={'name':'admin',
    'title':'的说法是否为',
    'essay':'暗粉色哥哥说是，单色哥哥为各位',
    }
    sqllib.FastCreatArtical (uf)
    uf={'name':'admin',
        'title':'FirstCreatArtical',
        'essay':'FirstTestCreatArtical',
        }
    sqllib.FastCreatArtical (uf)
    uf={'name':'admin',
    'title':'sadfww',
    'essay':'dfgrhcbrrbfbsasxcw',
    }
    sqllib.FastCreatArtical (uf)
    return 1
def TestGetUserInfo():
    #`uid`=%s OR `name`=%s
    uf={'id':1,
        'uid':'2',
        'name':"%a%"
        }
    list = sqllib.GetUserInfo (uf)
    return list

def TestGetLoginInfo():
    #'title','bluser','essay','right','blgroup'
    uf={
        'name':"admin"
        }
    list = sqllib.GetLoginInfo (uf)
    return list      
def TestSearchArtical():
    uf={'keyword':"a"
    }
    list = sqllib.SearchArtical (uf)
    return list

def TestEditArtical():
    uf={'rawtitle':"sadfw",
        'title':"qwe",
        'name':"admin",
        'right':1,
        'essay':'df',
        
    }
    list = sqllib.EditArtical (uf)
    return list
###########################
#  
#临时测试
#  
###########################
def b64(text):
    if text is None:
        return None
    bytesString = text.encode("utf-8")
    encodestr = base64.b64encode(bytesString)
    return (encodestr.decode())
def TestBase64():
    copyright = 'Copyright (c) 大师傅的说法是 %……&808r32*(&(.，。、'
    bytesString = copyright.encode("utf-8")
    encodestr = base64.b64encode(bytesString)
    print(encodestr)
    print(encodestr.decode())
    af={'keyword':"说法是 是，单色"
    }
    a = list(map(lambda x:b64(x),af['keyword'].split(" ")))
    print(a)
    return "tguy"
    
def TestBase64():
    copyright = 'Copyright (c) 大师傅的说法是 %……&808r32*(&(.，。、'
    bytesString = copyright.encode("utf-8")
    encodestr = base64.b64encode(bytesString)
    print(encodestr)
    print(encodestr.decode())
    af={'keyword':"说法是 是，单色"
    }
    a = list(map(lambda x:b64(x),af['keyword'].split(" ")))
    print(a)
    return "tguy"

def TestTrue():
    copyright = 'Copyright (c) 大师傅的说法是 %……&808r32*(&(.，。、'
    if(copyright):
        print (True)
    else:
        print (False)
    if(copyright is True):
        print (True)
    else:
        print (False)
    copyright = 0
    if(copyright):
        print (True)
    else:
        print (False)
    return "False"
def TestPassword (Password):#检查密码是否合法
    s = r'[0-9a-zA-Z@.\-\_\#\$\^\&\*]{0,29}'
    if re.match(s, Password):
        return True
    else:
        return False   
print(TestNoteCreateUser ())
# try:
    # TestFastCreatArtical()
    # print("TestFastCreatArtical")
# except Exception as e:
    # if "Duplicate entry" in str(e):
        # print("title aready exist")