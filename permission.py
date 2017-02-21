from pprint import pprint
try:
    from note.config import *
except:
    from config import *
    
####################################
#
#异常
#
####################################  
class PermissionError(Exception):
    def __init__(self,FunctionName,Massage, ActionInfo=None):  
        self.info = ActionInfo
        self.function = FunctionName
        self.err = Massage
        Exception.__init__(self)

####################################
#
#鉴权函数
#
####################################      
def ReadArticleList(User,Article):
    PermissionName = "ReadArticleList"
    if "Self" in User["permissions"][PermissionName]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"][PermissionName]:
        if Article["name"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"]["ReadArticleList"]:
        return True
    if Article["name"] in User["permissions"][PermissionName]:
        return True
    raise PermissionError("ReadArticleList","User:'%s' Don't Have Permission to Read Other's ArticleList"%User["name"],[User,Article])
    
def ReadArticle(User,Article):
    PermissionName = "ReadArticle"
    if "Self" in User["permissions"][PermissionName]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"][PermissionName]:
        if Article["name"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"][PermissionName]:
        return True
    if Article["name"] in User["permissions"][PermissionName]:
        return True
    raise PermissionError("ReadArticle","User:'%s' Don't Have Permission to Read Other's Article"%User["name"],[User,Article])
    
def CreateArticle(User,Article):
    PermissionName = "CreateArticle"
    if User["permissions"]["MaxArticleNum"] <= Article["articlenum"]:
        raise PermissionError("CreateArticle","You Can't Create More Article",[User,Article]) 
    if "Self" in User["permissions"][PermissionName]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"][PermissionName]:
        if Article["name"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"][PermissionName]:
        return True
    if Article["name"] in User["permissions"][PermissionName]:
        return True
    raise PermissionError("CreateArticle","User:'%s' Don't Have Permission to Create Other's Article"%User["name"],[User,Article]) 
    
def EditArticle(User,Article):
    PermissionName = "EditArticle"
    if "Self" in User["permissions"][PermissionName]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"][PermissionName]:
        if Article["name"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"][PermissionName]:
        return True
    if Article["name"] in User["permissions"][PermissionName]:
        return True
    raise PermissionError("EditArticle","User:'%s' Don't Have Permission to Edit Other's Article"%User["name"],[User,Article])
    
def DeleteArticle(User,Article):
    PermissionName = "DeleteArticle"
    if "Self" in User["permissions"][PermissionName]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"][PermissionName]:
        if Article["name"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"][PermissionName]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"][PermissionName]:
        return True
    if Article["name"] in User["permissions"][PermissionName]:
        return True
    raise PermissionError("DeleteArticle","User:'%s' Don't Have Permission to Delete Other's Article"%User["name"],[User,Article])