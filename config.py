SQLCONFIG={'host':'host',#默认127.0.0.1
        'user':'user',
        'password':'password',
        'port':3306 ,#默认即为3306
        'database':'database',
        'charset':'utf8'#默认即为utf8
        }
TABLE= {'user':'Note_user',
        'artical':'Note_artical',
        'search':'Note_search'
        }
BASE64SEARCH=False#中文分词有难度，无限期延期，请勿更改此项。
PUBLICUSER='admin'
USERFIELD=('id','uid','name','mail','salt','saltpassword','right','prikey','pubkey','articalnum','lgnfailedtimes','group','remark','time')
ARTICALFIELD=('id','uid','title','essay','tag','right','blgroup','salt','saltpassword','pubkey','prikey','remark','pubtime','lastesttime')
SEARCHFIELD=('id','uid','b64title','b64essay','b64tag','right','blgroup','b64remark','pubtime','lastesttime')
DEFAULTARTICALPASSWORD=0
#连续失败次数
LOGINFAILEDTIMES=3
#初始等待时间(小时)
WAITETIME=0.1
#失败惩罚倍数（WAITENUM的n-3次方）
WAITENUM=2
#邮件发送地址
MAIL_FROM_ADDR = ""
#smtp服务器密码
MAIL_PASSWORD = ''
#收件地址
MAIL_TO_ADDR = ''
#smtp服务器
MAIL_SMTP_SERVER = ''
#注册邮件内容
MAIL_ARTICAL = 'hello, send by Python...'
MAIL_ARTICAL_SIGNIN = """你注册了新的NoteBook账号，请点击以下网址完成注册："""
#注册邮件标题
MAIL_TITLE = '来自SMTP的问候……'
MAIL_TITLE_SIGNIN = """NoteBook新用户验证"""