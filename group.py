import math
Inf = math.inf
#Self
#PublicUser
#SameGroup
#LowerGroup
#All
USER_PERMISSIONS=("Weight","DispitePass","ReadArticle","ReadArticleList","CreateArticle","DeleteArticle","EditArticle","SearchArticle","MaxArticleNum")
ARTICLE_PERMISSIONS=("Weight")
DEFAULT_GROUP = "Default"
DEFAULT_ARTICLE_GROUP = "DefaultArticleGroup"
####################################
#
#默认用户组
#
#################################### 
DEFAULTGROUP={
"Weight":10,
"ReadArticle":("Self","LowerGroup","SameGroup"),
"ReadArticleList":("Self","PublicUser"),
"CreateArticle":("Self"),
"DeleteArticle":("Self"),
"EditArticle":("Self","PublicUser"),
"SearchArticle":("Self","PublicUser"),
"MaxArticleNum":100
}
DEFAULTARTICLEGROUP={
"Weight":10
}
####################################
#
#高级用户组(继承自DEFAULTGROUP)
#
#################################### 
VIPGROUP = dict(DEFAULTGROUP)
VIPGROUP.update({
"Weight":20,
"ReadArticle":("LowerGroup"),
"MaxArticleNum":1000
})
VIPARTICLEGROUP= dict(DEFAULTARTICLEGROUP)
VIPARTICLEGROUP.update({
"Weight":20
})
####################################
#
#管理员用户组(继承自VIPGROUP)
#
#################################### 
ADMINGROUP = dict(VIPGROUP)
ADMINGROUP.update({
"Weight":100,
"ReadArticle":("LowerGroup"),
"ReadArticleList":("LowerGroup"),
"CreateArticle":("LowerGroup"),
"DeleteArticle":("LowerGroup"),
"EditArticle":("LowerGroup"),
"SearchArticle":("LowerGroup"),
"MaxArticleNum":9999999,
})
ADMINARTICLEGROUP = dict(VIPARTICLEGROUP)
ADMINARTICLEGROUP.update({
"Weight":100
})
####################################
#
#全权限用户组(ADMINGROUP)
#
#################################### 
MANAGEGROUP = dict(VIPGROUP)
MANAGEGROUP.update({
"Weight":Inf,
"DispitePass":("All"),
"ReadArticle":("All"),
"ReadArticleList":("All"),
"CreateArticle":("All"),
"DeleteArticle":("All"),
"EditArticle":("All"),
"SearchArticle":("All"),
"MaxArticleNum":Inf,
})
MANAGEARTICLEGROUP = dict(ADMINARTICLEGROUP)
MANAGEARTICLEGROUP.update({
"Weight":Inf
})
####################################
#
#日志用户组(ADMINGROUP)
#
#################################### 
LOGGERGROUP = dict(DEFAULTGROUP)
LOGGERGROUP.update({
"Weight":ADMINGROUP["Weight"],
"DispitePass":("Self"),
"ReadArticle":("Self"),
"ReadArticleList":("Self"),
"CreateArticle":("Self"),
"DeleteArticle":("Self"),
"EditArticle":("Self"),
"SearchArticle":("Self"),
"MaxArticleNum":50,
})
LOGGERARTICLEGROUP = dict(DEFAULTARTICLEGROUP)
LOGGERARTICLEGROUP.update({
"Weight":ADMINARTICLEGROUP["Weight"]
})
#Keep this line on the buttom
USER_GROUP={"Default":DEFAULTGROUP,"Vip":VIPGROUP,"Admin":ADMINGROUP,"Manage":MANAGEGROUP,"Logger":LOGGERGROUP}
ARTICLE_GROUP={"DefaultArticleGroup":DEFAULTARTICLEGROUP,"VipArticleGroup":VIPARTICLEGROUP,"AdminArticleGroup":ADMINARTICLEGROUP,"ManageArticleGroup":MANAGEARTICLEGROUP,"LoggerArticleGroup":LOGGERARTICLEGROUP}