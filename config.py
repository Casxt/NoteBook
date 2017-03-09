SQLCONFIG={'host':'',#默认127.0.0.1
        'user':'',
        'password':'',
        'port':3306 ,#默认即为3306
        'database':'',
        'charset':'utf8'#默认即为utf8
        }
TABLE= {'user':'Note_user',
        'article':'Note_article',
        'search':'Note_search'
        }
BASE64SEARCH=False#中文分词有难度，无限期延期
PUBLICUSER='admin'
USERFIELD=('id','uid','name','mail','salt','saltpassword','permission','articlenum','lgnfailedtimes','group','remark','time')
ARTICLEFIELD=('id','uid','title','essay','type','tag','permission','blgroup','salt','saltpassword','remark','pubtime','lastesttime')
SEARCHFIELD=('id','uid','b64title','b64essay','b64tag','permission','blgroup','b64remark','pubtime','lastesttime')
#文章类型列表
ARTICLETYPELIST=('html/text','html','text','json','image','markdown',"code")
#默认文章类型
DEFAULTARTICLETYPE=ARTICLETYPELIST[0]
#每页显示条目
EACHPAGENUM=18
MAX_EACHPAGE_NUM=100
MIN_EACHPAGE_NUM=1
#取消密码关键字
RESETARTCALPASSWORD=0
#我也忘下面这个设置是做什么的了
DEFAULTARTICLEPASSWORD=0
#连续失败次数
LOGINFAILEDTIMES=3
#登陆失败惩罚时间基数(小时)
WAITETIME=0.1
#失败惩罚倍数（WAITENUM的n-3次方）
WAITENUM=2
#搜索词长度
MINSEARCHLENGTH=1
MAXSEARCHLENGTH=40
#标题长度
MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 2
#文章长度
MAX_ESSAY_LENGTH = 15000
MIN_ESSAY_LENGTH = 2
#api模式
MODE_LIST=("edit","CheckLoginState","GetArticle",
"GetArticleList","SearchArticle","SubmitEditedArticle",
"SubmitArticle","DeleteArticle","Login","Logout","Register",
"ChangePassword","ResetPassword","CheckLoginState",)
#######################
#
#邮件设置
#
#######################

#邮件发送地址
MAIL_FROM_ADDR = "maple@forer.cn"
#smtp服务器密码
MAIL_PASSWORD = ''
#收件地址
MAIL_TO_ADDR = '774714620@qq.com'
#smtp服务器
MAIL_SMTP_SERVER = 'smtp.qq.com'
#邮件
#测试
MAIL_TITLE = '来自SMTP的问候……'
MAIL_ARTICLE = 'hello, send by Python...'
#注册邮件
MAIL_TITLE_SIGNIN = """NoteBook新用户验证"""
MAIL_ARTICLE_SIGNIN = """你注册了新的NoteBook账号，请点击以下网址完成注册："""
#重置密码邮件
MAIL_TITLE_RSPASSWORD = """NoteBook重置密码"""
MAIL_ARTICLE_RSPASSWORD = """您申请了重置密码，系统为您生成了新的密码：%s"""
#修改密码邮件
MAIL_TITLE_CGPASSWORD = """NoteBook修改密码"""
MAIL_ARTICLE_CGPASSWORD = """您账户的密码已经改变，若非本人操作请尽快重置密码"""


#######################
#
#错误返回
#
#######################
#权限不足
ARTICLENEEDpermission={
"title":"No Enough permissions",
"essay":"You Can't Edit Other User's Article",
"state":"success"
}
ARTICLETYPEERR={
"state":"Invalid Article Type"
}


#######################
#
#权限组
#
#######################
try:
    from note.group import *
except:
    from group import *
    
#######################
#
#日志
#
#######################
LoggerName = "Logger"
LoggerId = "Logger"
LoggerPass = "Logger"
LoggerMail = "Logger@forer.cn"
LoggerDeleteNum = 1
LogLevel = {
"CRITICAL":50,
"ERROR":40,
"WARNING":30,
"INFO":20,
"DEBUG":10,
"NOTSET":0
}
RecordLevel = LogLevel["ERROR"]
PrintLevel = LogLevel["INFO"]
PrintDetialLevel = LogLevel["WARNING"]