from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
try:
    from note.config import *
except:
    from config import *
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def Send(MAIL_TO_ADDR=MAIL_TO_ADDR,MAIL_TITLE=MAIL_TITLE,MAIL_ARTICAL=MAIL_ARTICAL):
    msg = MIMEText(MAIL_ARTICAL, 'plain', 'utf-8')
    msg['From'] = _format_addr('<'+MAIL_FROM_ADDR+'>')
    msg['To'] = _format_addr('<'+MAIL_TO_ADDR+'>')
    msg['Subject'] = Header(MAIL_TITLE, 'utf-8').encode()
    server = smtplib.SMTP(MAIL_SMTP_SERVER, 25)
    #server.set_debuglevel(1)
    loginr = server.login(MAIL_FROM_ADDR, MAIL_PASSWORD)
    server.sendmail(MAIL_FROM_ADDR, [MAIL_TO_ADDR], msg.as_string())
    sendr = server.quit()
    return (loginr,sendr)