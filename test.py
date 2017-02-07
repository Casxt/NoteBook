try:
    import note.logger as logger
except Exception as e:
    import logger

import Note
import sqllib
import mail
from config import *
from spider import *
from sqllib import SqlError
from permission import PermissionError
from pprint import pprint
import json
#print(logger.CreateLogger())
#pprint(json.dumps(DEFAULTGROUP))
#print(logger.Record("DeBug","Test","A Test"))
#print(logger.Record("DeBug","Test","A Test"))
#print(logger.ClearLog(1))
#print(mail.Send("logger@forer.cn",MAIL_TITLE_SIGNIN,MAIL_ARTICAL_SIGNIN))