# SQLCONFIG={'host':'',#默认127.0.0.1
        # 'user':'',
        # 'password':'',
        # 'port':3306 ,#默认即为3306
        # 'database':'',
        # 'charset':'utf8'#默认即为utf8
        # }
SQLCONFIG={'host':'5739d1cc363d7.sh.cdb.myqcloud.com',#默认127.0.0.1
        'user':'cdb_outerroot',
        'password':'753951Qwe',
        'port':4602 ,#默认即为3306
        'database':'MapleDB',
        'charset':'utf8'#默认即为utf8
        }
TABLE= {'user':'Note_user',
        'artical':'Note_artical',
        'search':'Note_search'
        }
BASE64SEARCH=False#中文分词有难度，无限期延期
PUBLICUSER='admin'
USERFIELD=('id','uid','name','mail','salt','saltpassword','right','articalnum','lgnfailedtimes','group','remark','time')
ARTICALFIELD=('id','uid','title','essay','type','tag','right','blgroup','salt','saltpassword','remark','pubtime','lastesttime')
SEARCHFIELD=('id','uid','b64title','b64essay','b64tag','right','blgroup','b64remark','pubtime','lastesttime')
#文章类型列表
ARTICALTYPELIST=['html/text','html','text','json','image','markdown',"code"]
#默认文章类型
DEFAULTARTICALTYPE=ARTICALTYPELIST[0]
#每页显示条目
EACHPAGENUM=18
#取消密码关键字
RESETARTCALPASSWORD=0
#我也忘下面这个设置是做什么的了
DEFAULTARTICALPASSWORD=0
#连续失败次数
LOGINFAILEDTIMES=3
#登陆失败惩罚时间基数(小时)
WAITETIME=0.1
#失败惩罚倍数（WAITENUM的n-3次方）
WAITENUM=2
#搜索词长度
MINSEARCHLENGTH=1
MAXSEARCHLENGTH=40
#######################
#
#邮件设置
#
#######################

#邮件发送地址
MAIL_FROM_ADDR = "maple@forer.cn"
#smtp服务器密码
MAIL_PASSWORD = 'pass'
#收件地址
MAIL_TO_ADDR = '774714620@qq.com'
#smtp服务器
MAIL_SMTP_SERVER = 'smtp.qq.com'
#邮件
#测试
MAIL_TITLE = '来自SMTP的问候……'
MAIL_ARTICAL = 'hello, send by Python...'
#注册邮件
MAIL_TITLE_SIGNIN = """NoteBook新用户验证"""
MAIL_ARTICAL_SIGNIN = """你注册了新的NoteBook账号，请点击以下网址完成注册："""
#重置密码邮件
MAIL_TITLE_RSPASSWORD = """NoteBook重置密码"""
MAIL_ARTICAL_RSPASSWORD = """您申请了重置密码，系统为您生成了新的密码：%s"""
#修改密码邮件
MAIL_TITLE_CGPASSWORD = """NoteBook修改密码"""
MAIL_ARTICAL_CGPASSWORD = """您账户的密码已经改变，若非本人操作请尽快重置密码"""


#######################
#
#错误返回
#
#######################
#权限不足
ARTICALNEEDRIGHT={
"title":"No Enough Rights",
"essay":"You Can't Edit Other User's Article",
"state":"success"
}
ARTICLETYPEERR={
"state":"Invalid Article Type"
}
