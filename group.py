import math
Inf = math.inf
#Self
#PublicUser
#SameGroup
#LowerGroup
#All
USER_PERMISSIONS=("Weight","DispitePass","ReadArticle","ReadArticleList","CreateArticle","DeleteArticle","EditArticle","SearchArticle","MaxArticleNum")
####################################
#
#Ĭ���û���
#
#################################### 
DEFAULTGROUP={
"Weight":10,
"ReadArticle":("Self","LowerGroup"),
"ReadArticleList":("Self","PublicUser"),
"CreateArticle":("Self"),
"DeleteArticle":("Self"),
"EditArticle":("Self"),
"SearchArticle":("Self"),
"MaxArticleNum":100
}
####################################
#
#�߼��û���(�̳���DEFAULTGROUP)
#
#################################### 
VIPGROUP = dict(DEFAULTGROUP)
VIPGROUP.update({
"Weight":10,
"ReadArticle":("LowerGroup"),
"MaxArticleNum":1000
})
####################################
#
#����Ա�û���(�̳���VIPGROUP)
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
####################################
#
#ȫȨ���û���(ADMINGROUP)
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


USER_GROUP={"Default":DEFAULTGROUP,"Vip":VIPGROUP,"Admin":ADMINGROUP,"Manage":MANAGEGROUP}