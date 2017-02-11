import traceback
import json
from pprint import pprint
#traceback.format_exc()
try:
    from note.config import *
    import note.sqllib as sqllib
    from note.sqllib import SqlError
    from note.permission import PermissionError
except Exception as e:
    import sqllib
    from config import *
    from sqllib import SqlError
    from permission import PermissionError

# def CreateLogger():
    # LoggerInfo={
    # "uid":LoggerId,
    # "name":LoggerName,
    # "mail":LoggerMail,
    # "group":"Logger",
    # "password":LoggerPass
    # }
    # (massage,state)=Note.CreateUser(LoggerInfo)
    # return (massage,state)

def Record(Level,Summary,Detial,Addition=0):
    import datetime
    count = Addition
    Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Add = (" "+str(Addition)) if Addition else ""
    Title = "[LOG][%s%s][%s]%s"%(Level,Add,Time,Summary)
    ArticleInfo={
        "title":Title,
        "name":LoggerName,
        "author":LoggerName,
        "uid":LoggerId,
        }
    if LogLevel[Level] >= RecordLevel:
        try:
            ArticleInfo["essay"] = json.dumps(Detial)
            ArticleInfo["type"] = "json"
        except TypeError as e:
            ArticleInfo["essay"] = str(Detial)
            ArticleInfo["type"] = "html/text"
            
        #考虑专用函数
        try:
            res = sqllib.CreatArtical(ArticleInfo)
        except PermissionError as e:
            if "You Can't Create More Article" in e.err:
                ClearLog(LoggerDeleteNum)
                Record(Level,Summary,Detial)
        except SqlError as e:
            if "Duplicate entry" in e.err:
                Record(Level,Summary,Detial,count+1)
    if LogLevel[Level] >= PrintDetialLevel:
        print(Title)
        pprint(Detial)
    elif LogLevel[Level] >= PrintLevel:
        print(Title)
        
def ClearLog(Num):
    ArticleListInfo={
    "name":LoggerName,
    "author":LoggerName,
    "uid":LoggerId,
    "order":"ASC",
    "page":1,
    "eachpage":Num
    }
    results = sqllib.GetArticalList(ArticleListInfo)["result"]
    #考虑批量删除函数
    for result in results:
        DeleteInfo = {
        "title":result["title"],
        "name":LoggerName,
        "author":LoggerName,
        "uid":LoggerId
        }
        sqllib.DeleteArticalByNameTitle(DeleteInfo)
    return (results)