from pprint import pprint
try:
    from note.config import *
except:
    from config import *
def ReadArticleList(User,Article):
    if "Self" in User["permissions"]["ReadArticleList"]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"]["ReadArticleList"]:
        if Article["uid"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"]["ReadArticleList"]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"]["ReadArticleList"]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"]["ReadArticleList"]:
        return True
    return "Don't Have Permission to Read Other's ArticleList"
    
def ReadArticle(User,Article):
    if "Self" in User["permissions"]["ReadArticle"]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"]["ReadArticle"]:
        if Article["uid"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"]["ReadArticle"]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"]["ReadArticle"]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"]["ReadArticle"]:
        return True
    return "Don't Have Permission to Read Other's Article"
    
def CreateArticle(User,Article):
    if User["permissions"]["MaxArticleNum"] <= Article["articalnum"]:
        return "You Can't Create More Article"
    if "Self" in User["permissions"]["CreateArticle"]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"]["CreateArticle"]:
        if Article["uid"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"]["CreateArticle"]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"]["CreateArticle"]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"]["CreateArticle"]:
        return True
    return "Don't Have Permission to Create Other's Article"
    
    
def EditArticle(User,Article):
    if "Self" in User["permissions"]["EditArticle"]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"]["EditArticle"]:
        if Article["uid"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"]["EditArticle"]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"]["EditArticle"]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"]["EditArticle"]:
        return True
    return "Don't Have Permission to Edit Other's Article"
    
def DeleteArticle(User,Article):
    if "Self" in User["permissions"]["DeleteArticle"]:
        if User["uid"] == Article["uid"]:
            return True
    if "PublicUser" in User["permissions"]["DeleteArticle"]:
        if Article["uid"] == PUBLICUSER:
            return True
    if "SameGroup" in User["permissions"]["DeleteArticle"]:
        if User["permissions"]["Weight"] == Article["permissions"]["Weight"]:
            return True
    if "LowerGroup" in User["permissions"]["DeleteArticle"]:
        if User["permissions"]["Weight"] > Article["permissions"]["Weight"]:
            return True
    if "All" in User["permissions"]["DeleteArticle"]:
        return True
    return "Don't Have Permission to Delete Other's Article"
