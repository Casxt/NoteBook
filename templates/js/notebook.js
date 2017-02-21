var article = Article.createNew();
//处理cookie
//alert(window.location.pathname);
//系统关键search
//
////////////////
//
//常量
//
////////////////
//文章标题长度
var MINTITLELENGTH = 2
var MAXTITLELENGTH = 200
//文章正文长度
var MINESSAYLENGTH = 10
var MAXESSAYLENGTH = 50000
//搜索词长度
var MINSEARCHLENGTH = 1
var MAXSEARCHLENGTH = 40
//搜索警告动画时长
var SEARCHWARNINGFADETIME = 200
//搜索加载动画时长
var ARTICLELISTFADEINDALY = 20
var ARTICLELISTFADEINTIME = 20
//id标号颜色
var ARTICLEIDSTYLE = "label-primary"
//文章种类
var ARTIVLEKINDS = {"html/text":"Html/Text",
                    "html":"Html",
                    "markdown":"Markdown",
                    "text":"Text",
                    "json":"Json",
                    "code":"Code",
                    "test":"Test"}
var path = window.location.pathname
//当前操作模式
//编辑器预备全局变量


//var csrftoken = getCookie('csrftoken');
//处理cookie
//初始化显示内容
$(document).ready(function() {
    AutoSetArticleKinds();//先初始化页面
    checkloginstate();
    checkeurl();
});
//检查登录状态
function checkloginstate() {
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/chkls/',
        data: {
            "mode":"CheckLoginState",
            "name": getCookie("name"),
        },
        dataType: 'json',
        success: function(data) {
            if (data.loginstate == 1) {
                afterlogin(data);
            } else { //未登录即注销当前用户信息
                $("#navbar-userinfo").hide();
                $("#open-login").show();
                setDefaultCookie("name", "", 0);
                setDefaultCookie("login", 0);
                //search
                $("#search").hide();
            }

        }
    });
}
//登录成功时的动作
function afterlogin(data) {
    setDefaultCookie("name", data.name);
    setDefaultCookie("login", 1);
    $("#open-login").hide();
    $("#search").show();
    document.getElementById("menu-user").innerHTML = '<a id="navbar-userinfo" href="#" class="dropdown-toggle" data-toggle="dropdown" \
                                                    role="button" aria-haspopup="true" aria-expanded="false">\
                                                    ' + data.name + '<span class="caret"></span></a>\
                                                    <ul class="dropdown-menu">\
                                                    <li class="dropdown-header"></li>\
                                                    <li><a href="/list/' + data.name + '/">我的文章</a></li>\
                                                    <li role="separator" class="divider"></li>\
                                                    <li><a id="change-password" href="#">更改密码</a></li>\
                                                    <li><a id="open-logout" href="/">登出</a></li>\
                                                    </ul>';
}
//填写文章种类
function AutoSetArticleKinds() {
    var kinds = "";
    for (var kind in ARTIVLEKINDS) { 
        kinds = kinds + "<option value ='"+kind+"'>"+ARTIVLEKINDS[kind]+"</option>";
    } 
    document.getElementById("text-type").innerHTML = kinds;
}


//检查链接
function checkeurl() {
    var path = window.location.pathname;
    var matchpath = /^\/([\S\s]+?)\/$/g; //^\/([\S|\s]+?)\/$
    var matchuserpath = /^\/([\S\s]+?)\/([\S\s]+?)\/$/g; //^\/用户名\/文章名\/$
    var matchpathlogin = /^\/login\/([\S]{0,})$/g; //匹配login/...
    var matchpathlogout = /^\/logout\/([\S]{0,})$/g; //匹配logout/...
    var matchpathedit = /^\/e(dit)?\/([\S]{0,})$/g; //匹配edit/...
    var matchpathregister = /^\/register\/([\S]{0,})$/g; //匹配register/...
    var matchpathlist = /^\/l(ist)?\/([\S]{0,})$/g; //匹配list/...
    var matchpathsearch = /^\/s(earch)?\/([\S\s]{0,})$/g; //匹配list/...
    if (matchpathlogin.test(path)) {
        //
    } else if (matchpathlogout.test(path)) {
        //
    } else if (matchpathedit.test(path)) {
        EditArticle();

    } else if (matchpathregister.test(path)) {
        //
    } else if (matchpathlist.test(path)) {
        var html = document.getElementById("listshower");
        var pagehtml = document.getElementById("list-page");
        var cookie_name = unescape(getCookie("name"));
        html.innerHTML = "";
        pagehtml.innerHTML = "";
        $("#title-editer").hide();
        $("#essay-editer").hide();
        $("#shower").hide();
        GetArticleList();
    } else if (matchpathsearch.test(path)) {
        //搜索
        SearchArticle();
    }  else if (matchuserpath.test(path)) {
        autogetarticle();
    } else if (matchpath.test(path)) {
        autogetarticle();
    } else {//匹配到不符合规则的url时？
        autoloadarticle();
    }
    return 0;
}
//自动加载文章
function autoloadarticle() {
    let path = window.location.pathname;
    let essay = unescape(getCookie((path=="/")?"newessay":"essay"));
    let title = unescape(getCookie((path=="/")?"newtitle":"title"));
    let type = unescape(getCookie((path=="/")?"newtype":"type"));
    if (type != 'null' && type != "") {
        article.setAttribute("type",type);
    }
    if (essay != 'null' && essay != "") {
        article.setEssay(essay);
    }
    if (title != 'null' && title != "") {
        article.setTitle(title);
    }
    article.show();
    article.updateInput();
}

function autogetarticle() {
    let passwords = arguments[0] ? arguments[0] : 0;
    let path = window.location.pathname;
    let matchpath2 = /^\/(([\S\s]+?)\/)?(([\S\s]+?)\/)?$/g; //匹配文章
    let a = matchpath2.exec(path);
    let cookie_name = unescape(getCookie("name"));
    let isuser = true;
    a[2] = decodeURIComponent(a[2]);
    a[4] = decodeURIComponent(a[4]);
    $("#title-editer").hide();
    $("#essay-editer").hide();
    document.getElementById("showtitle").innerHTML = "Loading...";
    document.getElementById("showarticle").innerHTML = "";
    if (a[2] != "undefined" && a[4] != "undefined") {
        var name_path = a[1];
        var postdata = {
            "mode":"GetArticle",
            "name": cookie_name,
            "author": a[2],
            "title": a[4],
            "password": sha256($("#Modal-article-passwords").val()),
        };
        if (cookie_name!=a[2]){
            isuser = false;
        }
    } else if (a[2] != "undefined" && a[4] == "undefined") {
        var name_path = "";
        var postdata = {
            "mode":"GetArticle",
            "title": a[2],
            "password": sha256($("#Modal-article-passwords").val()),
        };
    } else {
        alert("缺少关键信息");
        return 0;
    }
    if (!passwords) {
        delete(postdata["password"]);
    }
    var pas = $("#Modal-article-passwords").val();
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/getarticle/',
        data: postdata,
        dataType: 'json',
        success: function(data) {
            if (data.state == "success") {
                $("#Modal-article-password").modal("hide");
                article.setAttribute("pubtime",data.pubtime);
                article.setAttribute("id",data.id);
                article.setAttribute("lastesttime",data.lastesttime);
                article.setAttribute("type",data.type);
                article.setTitle(data.title);
                article.setEssay(data.essay);
                let title = article.title.cleanTitle(data.title);
                let essay = article.essay.cleanEssay(data.essay);
                let href =  encodeURI(name_path) + encodeURIComponent(title);
                console.log(data.type);
                article.show(isuser?('<a " href="/e/' + href + '/">' + title + '</a>'):title,
                            article.essay.format(essay,data.type));
                //article.setTitle(edittitle);
                //article.setEssay(editessay);
                //article.show();
                //article.updateInput();
            } else if (data.state == "Need Password") {
                $("#Modal-article-password").modal("show");
                document.getElementById("showtitle").innerHTML = data.title;
                document.getElementById("showarticle").innerHTML = data.essay;
            } else {
                $("#Modal-article-password").modal("hide");
                document.getElementById("showtitle").innerHTML = data.title;
                document.getElementById("showarticle").innerHTML = data.essay;
            }
            return (data);
        }
    });
}

function GetArticleList() { //获取文章列表
    var path = window.location.pathname;
    var matchpath2 = /(^\/l(ist)?\/((\D[\S\s]+?)\/)?)((\d+?)\/)?$/g; //匹配文章
    var a = matchpath2.exec(path);
    var pagepath = a[1];
    var page=a[6]?a[6]:1;
    var name = a[4]?a[4]:"";//a[3]name带"/"，空时为undefined
    a[4] = decodeURI(a[4]);//a[4]name不带"/"
    //alert(a[5]);
    var html = document.getElementById("listshower");
    var pagehtml = document.getElementById("list-page");
    var cookie_name = unescape(getCookie("name"));
    html.innerHTML = "";
    pagehtml.innerHTML = "";
    $("#title-editer").hide();
    $("#essay-editer").hide();
    $("#shower").hide();
    if (!a[3]) {
        postdata = {
            'mode':'GetArticleList',
            'name': cookie_name,
            "page":page,
            'order':'DESC'
        }
        //name = ""
    } else {
        postdata = {
            'mode':'GetArticleList',
            'name': cookie_name,
            'author':a[4],
            "page":page,
            'order':'DESC'
        }
    }
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/getarticlelist/',
        data: postdata,
        dataType: 'json',
        success: function(data) {
            if (data.state == "success") {
                list = data.articlelist;
                var count = Math.ceil(data.count/20);
                var title = "";
                var num = 0;
                for (i in list) {
                    title = list[i].title;
                    var ifpassword = list[i].ifpassword;
                    //var href =  encodeURI(name + title);encodeURI不会对/编码
                    var href =  (name?(encodeURIComponent(name)+"/"):("")) + encodeURIComponent(title);//href="/' + href + '/"
/*onclick="window.location.href=' + "'/e/" + href + "/'" + '" */
                    html.innerHTML = html.innerHTML + '<li id="' + list[i].id + '" href="/' + href + '/" type="button" onclick="return true" style="display:none;" class="list-group-item article-list-item">\
                                                            <h5 style="margin:0.08em;" ><span class="label '+ARTICLEIDSTYLE+'">' + list[i].id + '</span><span style="padding-right: 1em;" ></span>\
                                                            '+(ifpassword?'<span class="glyphicon glyphicon-lock"></span><span style="padding-right: 1em;" ></span>':'')+'\
                                                            <strong>' + title + '</strong>\
                                                            <button value="' + title + '" type="button" class="close article-delete"><span class="glyphicon glyphicon-remove"></span></button>\
                                                            <button  style="padding-right: 0.5em;" type="button" class="close article-edit"><span class="glyphicon glyphicon-edit"></span></button>\
                                                            </h5></li>';
                    num++;
                }
                for (i=1;i<=count;i++) {
                    if (i==page){
                        var id = ("pagenum"+i);
                        pagehtml.innerHTML = pagehtml.innerHTML + '<li id="'+id+'" style="display:none;overflow: visible;" class="active"><a>'+i+'</a></li>';
                        list.push({"id":id});
                        num++;
                    }else{
                        var id = ("pagenum"+i);
                        pagehtml.innerHTML = pagehtml.innerHTML + '<li id="'+id+'" style="display:none;overflow: visible;"><a href="'+pagepath+i+'">'+i+'</a></li>';
                        list.push({"id":id});
                        num++;
                    }
                }
                ArticleListFadeIn(list,0,num);
                if (a[4] != getCookie("name")) {
                    $(".article-delete").hide();
                }
            } else {
                alert(data.state);
            }
            return (data);
        }
    });
}

//获取编辑文章信息 改正则时注意a的位置编号
function EditArticle() {
    var path = window.location.pathname;
    var matchpath2 = /^\/e(dit)?\/(([\S\s]+?)\/)?(([\S\s]+?)\/)?(([\S\s]+?)\/)?$/g; //匹配文章
    var a = matchpath2.exec(path);
    var cookie_name = unescape(getCookie("name"));
    a[3] = decodeURIComponent(a[3]);
    a[5] = decodeURIComponent(a[5]);
    var isname = 0
        if (a[3] != "undefined" && a[5] != "undefined") {
            postdata = {
                "mode": "edit",
                "name": cookie_name,
                "author": a[3],
                "title": a[5]
            }
            isname = 1
        } else if (a[3] != "undefined" && a[5] == "undefined") {
            postdata = {
                "mode": "edit",
                "title": a[3]
            }
        }
        $.ajax({
            beforeSend: function(request) {
                request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            type: 'POST',
            url: '/getarticle/',
            data: postdata,
            dataType: 'json',
            success: function(data) {
                if (data.state=="success"){//有该文章
                    let title = data.title;
                    let essay = data.essay;
                    let edittitle = unescape(getCookie("title"))
                    let editessay = unescape(getCookie("essay"))
                    if (!edittitle || edittitle == "null" ){
                        
                        edittitle = title;
                    }
                    if (!edittitle || editessay == "null" || editessay == ""){
                        
                        editessay = essay;
                    }
                    document.getElementById("text-submit").id = "text-edit-submit";
                    document.getElementById("text-edit-submit").value = title;
                    article.setAttribute("pubtime",data.pubtime);
                    article.setAttribute("id",data.id);
                    article.setAttribute("lastesttime",data.lastesttime);
                    article.setAttribute("type",data.type);
                    article.setTitle(edittitle);
                    article.setEssay(editessay);
                    article.updateInput();
                    article.show();
                    if (a[6] == undefined) {
                        document.getElementById("text-edit-submit").path = "/" + a[2] + a[4];
                    } else {
                        document.getElementById("text-edit-submit").path = "/" + a[2] + a[4] + a[6];
                    }
                    if (isname) {
                        document.getElementById("text-edit-submit").name = a[3];
                    }
                    return (data);
                }
            }
        });
}
//搜索事件
function SearchArticle() {
    let path = window.location.pathname;
    let matchpath2 = /(^\/s(earch)?\/(([\S\s]{0,}?)\/?))$/g; //匹配文章
    let a = matchpath2.exec(path);
    let KeyWord = decodeURIComponent(a[4]);
    if (CheckSearchInput(KeyWord)){
        //
    }else{
        return false;
    }
    let html = document.getElementById("listshower");
    let keyword = KeyWord;
    $('#search-warning').fadeIn(SEARCHWARNINGFADETIME);
    document.getElementById("search-warning").innerHTML = "Loading...";
    let res = "aa";
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/search/',
        data: {
            'mode':"SearchArticle",
            'keyword': keyword,
            'name': getCookie("name")
        },
        dataType: 'json',
        success: function(data) {
            if (data.state == "success") {
                list = data.articlelist
                //var title = "";
                if (list.length < 1) {
                    $('#search-warning').fadeIn(SEARCHWARNINGFADETIME);
                    document.getElementById("search-warning").innerHTML = "没有找到";
                    res = false;
                    history.back();
                } else {
                    SetPageStyleWhite();
                    $("#title-editer").hide();
                    $("#essay-editer").hide();
                    $("#shower").hide();
                    $("#list-page").hide();
                    $('#search-warning').fadeOut(SEARCHWARNINGFADETIME);
                    html.innerHTML = "";
                    var cookiename = getCookie("name");
                    var num = 0;
                    for (i in list) {
                        var title = list[i].title;
                        name = list[i].name?(list[i].name):"";
                        var href =  (name?(encodeURIComponent(name)+"/"):("")) + encodeURIComponent(title);
                        html.innerHTML = html.innerHTML + '<a id="' + list[i].id + '" href="/' + href + '/" type="button" style="display:none;overflow: visible;" class="list-group-item" >\
                                                                <span class="label '+ARTICLEIDSTYLE+'">' + list[i].id + '</span><span style="padding-right: 1em;" ></span><strong>' + title + '</strong>' + (list[i].name==cookiename?('\
                                                                <button id="' + title + ' "value="' + title + '" type="button" class="close article-delete" data-dismiss="alert" aria-label="Close"><span class="glyphicon glyphicon-remove"></span></button>\
                                                                <button onclick="window.location.href=' + "'/e/" + href + "/'" + '" style="padding-right: 0.5em;" type="button" class="close article-edit" data-dismiss="alert" aria-label="Edit">\
                                                                <span class="glyphicon glyphicon-edit"></span></button>'):('<button class="close" style="font-size: 1em;" type="button" >'+(list[i].name?list[i].name:'Public Aritcal')+'</button>'))+'</a>';
                        num++;
                   }
                   ArticleListFadeIn(list,0,num);
                   res = true;
                }
            }else{
                document.getElementById("search-warning").innerHTML = data.state;
                res = false;
                history.back();
            }
        }
    });
    return res;
}
//列表加载动画
function ArticleListFadeIn(list,i,num){
    if (i<num){
        var jstext = "$('#"+list[i].id+"').fadeIn("+ARTICLELISTFADEINTIME+")"
        window.setTimeout(jstext,i*ARTICLELISTFADEINDALY);
        i = i+1;
        ArticleListFadeIn(list,i,num)
    }
    return 0;
}

//检查搜索框
function CheckSearchInput(word) {
    let len = word.replace(/\s/g, "").length;
    if (len < MINSEARCHLENGTH) {
        $('#search-warning').fadeIn(SEARCHWARNINGFADETIME);
        document.getElementById("search-warning").innerHTML = "至少"+MINSEARCHLENGTH+"个字";
        return false;
    } else if (word.length >= MAXSEARCHLENGTH) {
        $('#search-warning').fadeIn(SEARCHWARNINGFADETIME);
        document.getElementById("search-warning").innerHTML = "至多"+MAXSEARCHLENGTH+"个字";
        return false;
    } else {
        $('#search-warning').fadeOut(SEARCHWARNINGFADETIME);
        return true;
    }
}
//过滤关键字
//提交



//提交登出
function logout() {
    $.ajax({
        type: 'GET',
        url: '/logout/',
        data: {
            "mode":"Logout",
            "name": getCookie("name")
        },
        dataType: 'json',
        success: function(data) {
            if (data.info != "success") {
                //失败？
            } else if (data.info == "success") { //成功退出
                $("#navbar-userinfo").hide();
                $("#open-login").show();
                setDefaultCookie("login", 0, 0);
                setDefaultCookie("name", "", 0);
                window.location.href = window.location.pathname;
            }
        }
    });
}


//检查注册字符
function CheckRegisterName(name) {
    let matchname = /^[a-zA-Z][0-9a-zA-Z@.\-]{4,29}$/g;
    if (matchname.test(name)) {
        return true;
    }
    return false;
}
function CheckRegisterMail(mail) {
    let matchemail = /^[0-9a-zA-Z][0-9a-zA-Z\-]{0,}@[0-9a-zA-Z\.\-]+?\.[a-zA-Z\.]+[a-zA-Z]$/g;
    if (matchemail.test(mail)) {
        return true;
    }
    return false;
}
function CheckRegisterPassword(passwords) {
    let matchepassword = /^[0-9a-zA-Z@.\-\_\#\$\^\&\*]{6,128}$/g;
    if (matchepassword.test(passwords)) {
        return true;
    }
    return false;
}

//document.body.style.backgroundImage="url(http://www.iteye.com/upload/logo/user/37073/648c9ed4-f54b-3f4a-ac54-905f5a483307.gif?1236833802)"; //改变背景图片  