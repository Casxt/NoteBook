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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function setCookie(c_name, value, expiredays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "": ";expires=" + exdate.toGMTString()); // + ";path=/"
}
function setDefaultCookie(c_name, value, expiredays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "": ";expires=" + exdate.toGMTString()) + ";path=/ "; // 
}
function getUTCzone() {
    var d = new Date();
    utc = d.getTimezoneOffset() / 60;
    return utc;
}
//var csrftoken = getCookie('csrftoken');
//处理cookie
//初始化显示内容
$(document).ready(function() {
    AutoSetArticleKinds();//先初始化页面
    checkloginstate();
    //alert(document.cookie);
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
                //$("#header-search-buttom").hide();
                //$("#header-search").hide();
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
    //$("#header-search-buttom").show();
    //$("#header-search").show();
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
        EditArtical();
    } else if (matchpathregister.test(path)) {
        //
    } else if (matchpathlist.test(path)) {
        GetArticleList();
    } else if (matchpathsearch.test(path)) {
        //搜索
        SearchArtical();
    }  else if (matchuserpath.test(path)) {
        autogetartical();
    } else if (matchpath.test(path)) {
        autogetartical();
    } else {//匹配到不符合规则的url时？
        autoloadartical();
    }
    return 0;
}
//自动加载文章
function autoloadartical() {
    var path = window.location.pathname;
    var essay = unescape(getCookie((path=="/")?"newessay":"essay"));
    var title = unescape(getCookie((path=="/")?"newtitle":"title"));
    if (essay != 'null' && essay != "") {
        document.getElementById("text-artical").value = essay;
        document.getElementById("showartical").innerHTML = essay;
    }
    if (title != 'null' && title != "") {
        document.getElementById("text-title").value = title;
        document.getElementById("showtitle").innerHTML = title;
    }
}
//获取文章信息
$(document).on('click', '#Modal-artical-passwords-submit',
function() {
    $(this).html("Loading...");
    autogetartical(1);
});
function autogetartical() {
    var passwords = arguments[0] ? arguments[0] : 0;
    var path = window.location.pathname;
    var matchpath2 = /^\/(([\S\s]+?)\/)?(([\S\s]+?)\/)?$/g; //匹配文章
    var a = matchpath2.exec(path);
    var cookie_name = unescape(getCookie("name"));
    var isuser = true;
    a[2] = decodeURIComponent(a[2]);
    a[4] = decodeURIComponent(a[4]);
    $("#title-editer").hide();
    $("#essay-editer").hide();
    document.getElementById("showtitle").innerHTML = "Loading...";
    document.getElementById("showartical").innerHTML = "";
    if (a[2] != "undefined" && a[4] != "undefined") {
        var name_path = a[1];
        var postdata = {
            "mode":"GetArticle",
            "name": cookie_name,
            "author": a[2],
            "title": a[4],
            "password": sha256($("#Modal-artical-passwords").val()),
        };
        if (cookie_name!=a[2]){
            isuser = false;
        }
    } else if (a[2] != "undefined" && a[4] == "undefined") {
        var name_path = "";
        var postdata = {
            "mode":"GetArticle",
            "title": a[2],
            "password": sha256($("#Modal-artical-passwords").val()),
        };
    } else {
        alert("缺少关键信息");
        return 0;
    }
    if (!passwords) {
        delete(postdata["password"]);
    }
    var pas = $("#Modal-artical-passwords").val();
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/getartical/',
        data: postdata,
        dataType: 'json',
        success: function(data) {
            if (data.state == "success") {
                $("#Modal-artical-password").modal("hide");
                $("#text-title").val(data.title);
                $("#text-artical").val(data.essay);
                var title = data.title;
                var essay = data.essay;
                var href =  encodeURI(name_path) + encodeURIComponent(title);
                document.getElementById("showtitle").innerHTML = isuser?('<a " href="/e/' + href + '/">' + title + '</a>'):title;
                document.getElementById("showartical").innerHTML = FormatEssay(essay,data.type);
                document.getElementById("text-pubtime").value = data.pubtime;
                document.getElementById("text-lastesttime").value = data.lastesttime;
                document.getElementById("text-id").value = data.id;
                $("#text-type").val(data.type);
            } else if (data.state == "Need Password") {
                $("#Modal-artical-password").modal("show");
                document.getElementById("showtitle").innerHTML = data.title;
                document.getElementById("showartical").innerHTML = data.essay;
            } else {
                $("#Modal-artical-password").modal("hide");
                document.getElementById("showtitle").innerHTML = data.title;
                document.getElementById("showartical").innerHTML = data.essay;
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
        url: '/getarticallist/',
        data: postdata,
        dataType: 'json',
        success: function(data) {
            if (data.state == "success") {
                list = data.articallist;
                var count = Math.ceil(data.count/20);
                var title = "";
                var num = 0;
                for (i in list) {
                    title = list[i].title;
                    var ifpassword = list[i].ifpassword;
                    //var href =  encodeURI(name + title);encodeURI不会对/编码
                    var href =  (name?(encodeURIComponent(name)+"/"):("")) + encodeURIComponent(title);
                    html.innerHTML = html.innerHTML + '<a id="' + list[i].id + '" href="/' + href + '/" type="button" style="display:none;" class="list-group-item">\
                                                            <span class="label '+ARTICLEIDSTYLE+'">' + list[i].id + '</span><span style="padding-right: 1em;" ></span>\
                                                            '+(ifpassword?'<span class="glyphicon glyphicon-lock"></span><span style="padding-right: 1em;" ></span>':'')+'\
                                                            <strong>' + title + '</strong>\
                                                            <button value="' + title + '" type="button" class="close artical-delete" data-dismiss="alert" aria-label="Close"><span class="glyphicon glyphicon-remove"></span></button>\
                                                            <button onclick="window.location.href=' + "'/e/" + href + "/'" + '" style="padding-right: 0.5em;" type="button" class="close artical-edit" data-dismiss="alert" aria-label="Edit">\
                                                            <span class="glyphicon glyphicon-edit"></span></button></a>';
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

                //setTimeout.(jstext,num*ARTICLELISTFADEINDALY);
                if (a[4] != getCookie("name")) {
                    $(".artical-delete").hide();
                }
            } else {
                alert(data.state);
            }
            return (data);
        }
    });
}

//获取编辑文章信息 改正则时注意a的位置编号
function EditArtical() {
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
            url: '/getartical/',
            data: postdata,
            dataType: 'json',
            success: function(data) {
                if (data.state=="success"){//有该文章
                    var title = data.title;
                    var essay = data.essay;
                    edittitle = unescape(getCookie("title"))
                    editessay = unescape(getCookie("essay"))
                    if (edittitle == "null" ){
                        edittitle = title;
                    }
                    if (editessay == "null"){
                        editessay = essay;
                    }
                    $("#text-title").val(edittitle);
                    $("#text-artical").val(editessay);
                    document.getElementById("showtitle").innerHTML = title;
                    //document.getElementById("showartical").innerHTML = essay.replace(/\n/g, "<br>");
                    document.getElementById("showartical").innerHTML = FormatEssay(essay,data.type);
                    document.getElementById("text-submit").id = "text-edit-submit";
                    document.getElementById("text-edit-submit").value = title;
                    document.getElementById("text-pubtime").value = data.pubtime;
                    document.getElementById("text-lastesttime").value = data.lastesttime;
                    document.getElementById("text-id").value = data.id;
                    $("#text-type").val(data.type);
                    if (a[6] == undefined) {
                        document.getElementById("text-edit-submit").path = "/" + a[2] + a[4];
                    } else {
                        document.getElementById("text-edit-submit").path = "/" + a[2] + a[4] + a[6];
                    }
                    if (isname) {
                        document.getElementById("text-edit-submit").name = a[3];
                    }
                    return (data);
                }else{//无该文章
                    $("#title-editer").hide();
                    $("#essay-editer").hide();
                    title = "No Such Artical";
                    essay = "You Can't Edit The Artical Not Exist";
                    document.getElementById("showtitle").innerHTML = title;
                    //document.getElementById("showartical").innerHTML = essay.replace(/\n/g, "<br>");
                    document.getElementById("showartical").innerHTML = FormatEssay(word,"html/text");
                }
            }
        });
}
//搜索事件
function SearchArtical() {
    var path = window.location.pathname;
    var matchpath2 = /(^\/s(earch)?\/(([\S\s]{0,}?)\/?))$/g; //匹配文章
    var a = matchpath2.exec(path);
    var KeyWord = decodeURIComponent(a[4]);
    if (CheckSearchInput(KeyWord)){
        //
    }else{
        return false;
    }
    var html = document.getElementById("listshower");
    //var keyword = document.getElementById("header-search").value;
    var keyword = KeyWord;
    $('#search-warning').fadeIn(SEARCHWARNINGFADETIME);
    document.getElementById("search-warning").innerHTML = "Loading...";
    var res = "aa";
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
                list = data.articallist
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
                    //history.pushState({},"note", ("/search/"+encodeURIComponent(keyword)+"/"));
                    $('#search-warning').fadeOut(SEARCHWARNINGFADETIME);
                    //document.getElementById("search-warning").innerHTML = "";
                    html.innerHTML = "";
                    var cookiename = getCookie("name");
                    var num = 0;
                    for (i in list) {
                        var title = list[i].title;
                        name = list[i].name?(list[i].name):"";
                        var href =  (name?(encodeURIComponent(name)+"/"):("")) + encodeURIComponent(title);
                        html.innerHTML = html.innerHTML + '<a id="' + list[i].id + '" href="/' + href + '/" type="button" style="display:none;overflow: visible;" class="list-group-item" >\
                                                                <span class="label '+ARTICLEIDSTYLE+'">' + list[i].id + '</span><span style="padding-right: 1em;" ></span><strong>' + title + '</strong>' + (list[i].name==cookiename?('\
                                                                <button id="' + title + ' "value="' + title + '" type="button" class="close artical-delete" data-dismiss="alert" aria-label="Close"><span class="glyphicon glyphicon-remove"></span></button>\
                                                                <button onclick="window.location.href=' + "'/e/" + href + "/'" + '" style="padding-right: 0.5em;" type="button" class="close artical-edit" data-dismiss="alert" aria-label="Edit">\
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
//监控回车搜素
$(document).on('keydown', '#header-search',
//$('#header-search').keydown(
function(e) {
    if (e.keyCode == 13 && CheckSearchInput($('#header-search').val())) {
        var keyword = document.getElementById("header-search").value;
        history.pushState({},"note", ("/search/"+encodeURIComponent(keyword)+"/"));
        var res = SearchArtical();
        if (res){
            //history.back();
        }else{
            //history.back();
            }
    }
});
//按钮监控
$(document).on('click', '#header-search-buttom',
function() {
    if (CheckSearchInput($('#header-search').val())) {
        var keyword = document.getElementById("header-search").value;
        history.pushState({},"note", ("/search/"+encodeURIComponent(keyword)+"/"));
        //window.location.href = ("/search/"+encodeURIComponent(keyword)+"/");
        var res = SearchArtical();
        if (res){
            //history.back();
        }else{
            //history.back();
            }
    }
});
//检查搜索关键词
$('#header-search').on("focus",
function() {
    $('#search-warning').fadeOut(SEARCHWARNINGFADETIME);
    //document.getElementById("search-warning").innerHTML = "";
});
$('#header-search').on("change",
function() {
    CheckSearchInput($('#header-search').val());
});
//检查搜索框
function CheckSearchInput(word) {
    //var word = $('#header-search').val();
    var len = word.replace(/\s/g, "").length;
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
        //document.getElementById("search-warning").innerHTML = "";
        return true;
    }
}
//过滤关键字
//提交

//监控文章修改
$(document).on('change', '#text-artical,#attributer',
function() {
    articalshow();
});
function articalshow() //过滤文章关键字
{
    var path = window.location.pathname
    var essay = document.getElementById("text-artical").value;
    var title = document.getElementById("text-title").value;
    essay = essay.replace(/<script/g, "").replace(/script>/g, "");
    essay = essay.replace(/<iframe/g, "").replace(/iframe>/g, "");
    essay = essay.replace(/<link/g, "");
    essay = essay.replace(/<style/g, "").replace(/style>/g, "");
    essay = essay.replace(/<frameset/g, "").replace(/frameset>/g, "");
    document.getElementById("text-artical").value = essay;
    //document.getElementById("showartical").innerHTML = word.replace(/\n/g, "<br>");
    document.getElementById("showartical").innerHTML = FormatEssay(essay,$('#text-type option:selected').val());
    setCookie((path=="/")?"newessay":"essay", escape(essay), 30);
    if (essay.length >= MINESSAYLENGTH && essay.length <= MAXESSAYLENGTH && title.length >= MINTITLELENGTH && title.length <= MAXTITLELENGTH) {
        $("#text-submit,#text-edit-submit").removeAttr("disabled");
        $("#text-submit,#text-edit-submit").attr("class","btn btn-primary");
        $("#text-submit,#text-edit-submit").text("提交");
        //document.getElementById("text-submit").className = "btn btn-primary";
        //document.getElementById("text-submit").innerHTML = "提交";
        return true;
    } else {
        //$("#text-submit").attr({"disabled": "disabled"});
        //$("#text-edit-submit").attr({"disabled": "disabled"});
        return false;
    }
}
//监控标题修改
$(document).on('change', '#text-title',
function() {
    titleshow()
});
function titleshow() //过滤标题关键字
{
    var path = window.location.pathname
    var title = document.getElementById("text-title").value;
    var essay = document.getElementById("text-artical").value;
    title = title.replace(/<|>/g, "");
    title = title.replace(/\s+/g, " ");
    document.getElementById("text-title").value = title;
    document.getElementById("showtitle").innerHTML = title;
    setCookie((path=="/")?"newtitle":"title", escape(title), 30);
    if (essay.length >= MINESSAYLENGTH && essay.length <= MAXESSAYLENGTH && title.length >= MINTITLELENGTH && title.length <= MAXTITLELENGTH) {
        $("#text-submit,#text-edit-submit").removeAttr("disabled");
        $("#text-submit,#text-edit-submit").attr("class","btn btn-primary");
        $("#text-submit,#text-edit-submit").text("提交");
        //document.getElementById("text-submit").className = "btn btn-primary";
        //document.getElementById("text-submit").innerHTML = "提交";
        return true;
    } else {
        //$("#text-submit").attr({"disabled": "disabled"});
        //$("#text-edit-submit").attr({"disabled": "disabled"});
        return false;
    }
}
//监控提交修改
$(document).on('click', '#text-edit-submit',
function() { //提交文章
    var path = window.location.pathname
    var name = document.getElementById("text-edit-submit").name;
    var rawtitle = document.getElementById("text-edit-submit").value;
    var title = $("#text-title").val();
    var essay = $("#text-artical").val();
    var cookie_name = unescape(getCookie("name"));
    var postdata = {
        "mode":"SubmitEditedArticle",
        "title": title,
        "essay": essay,
        "password": $("#text-password").val(),
        "tag": $("#text-tag").val(),
        "author":name,
        "name": cookie_name,
        "rawtitle": rawtitle,
        "type":$('#text-type option:selected').val()
    };
    if ($('#text-password').attr("disabled") == "disabled") {
        delete(postdata["password"]);
    }
    if (titleshow() && articalshow()) {
        //alert(titleshow());
        $.ajax({
            beforeSend: function(request) {
                request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            type: 'POST',
            url: '/editartical/',
            data: postdata,
            dataType: 'json',
            success: function(data, status) {
                if (data.state == "success") {
                    setCookie((path=="/")?"newtitle":"title", "", 0);
                    setCookie((path=="/")?"newessay":"essay", "", 0);
                    //window.location.href = document.getElementById("text-edit-submit").path;
                    //不加括号会导致加法结合有误
                    //alert("/"+(name==""?"":name+"/")+title);
                    window.location.href = "/"+(name==""?"":name+"/")+title;
                } else {
                    document.getElementById("text-edit-submit").className = "btn btn-danger";
                    document.getElementById("text-edit-submit").innerHTML = data.state;
                }
            }
        });
    }else{
        $("#text-submit,#text-edit-submit").attr("class","btn btn-danger");
        $("#text-submit,#text-edit-submit").text("内容过少");
        //document.getElementById("text-submit").className = "btn btn-danger";
        //document.getElementById("text-submit").innerHTML = "内容过少";
    }
});
//监控提交
$(document).on('click', '#text-submit',
function() {
    var path = window.location.pathname
    var title = document.getElementById("text-title").value;
    var essay = document.getElementById("text-artical").value;
    var cookie_name = unescape(getCookie("name"));
    var postdata = {
        "mode":"SubmitArticle",
        "title": title,
        "essay": essay,
        "password": $("#text-password").val(),
        "tag": $("#text-tag").val(),
        //"author": cookie_name,
        //"name": cookie_name,
        "type":$('#text-type option:selected').val()
    };
    cookie_name=='null'?true:postdata["author"]=cookie_name;
    cookie_name=='null'?true:postdata["name"]=cookie_name;
    if ($('#text-password').attr("disabled") == "disabled") {
        delete(postdata["password"]);
    }
    if (titleshow() && articalshow()) {
    document.getElementById("text-submit").className = "btn btn-warning";
    document.getElementById("text-submit").innerHTML = "Submiting...";
    if (cookie_name == null) {
        cookie_name = "";
    } else {
        cookie_name = cookie_name + "/";
    }
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/submitartical/',
        data: postdata,
        // contentType: "application/json",//该句代码不能加，加了之后无法POST
        dataType: 'json',
        success: function(data, status) {
            if (data.state == "success") {
                setCookie((path=="/")?"newtitle":"title", "", 0);
                setCookie((path=="/")?"newessay":"essay", "", 0);
                document.getElementById("text-submit").className = "btn btn-success";
                document.getElementById("text-submit").innerHTML = "success";
                window.location.href = "/" + cookie_name + $("#text-title").val() + "/";
            } else {
                document.getElementById("text-submit").className = "btn btn-danger";
                document.getElementById("text-submit").innerHTML = data.state;
            }
        }
    });
    }else if(essay.length < MINESSAYLENGTH || title.length < MINTITLELENGTH){
        document.getElementById("text-submit").className = "btn btn-danger";
        document.getElementById("text-submit").innerHTML = "内容过少";
    }else if(essay.length > MAXESSAYLENGTH || title.length > MAXTITLELENGTH){
        document.getElementById("text-submit").className = "btn btn-danger";
        document.getElementById("text-submit").innerHTML = "内容过多";
    }
});
//监控删除
$(document).on('click', '.artical-delete',
function() { //提交文章
    var thisitem = $(this)
    var title = $(this).val();
    $(this).html('<span id="search-warning" class="label label-warning">Deleteing...</span>');
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/deleteartical/',
        data: {
            "mode":"DeleteArticle",
            "author":getCookie("name"),
            "title": title,
            "name": getCookie("name")
        },
        dataType: 'json',
        success: function(data) {
            if (data.state == "success") {
                thisitem.html('<span id="search-warning" class="label label-success">success</span>');
                thisitem.parent().hide();
                //$(("#" + title)).hide();
            } else {
                alert(data.state);
            }
        }
    });
});

//监控登录按钮
$(document).on('click', "#open-login",
function() {
    $("#Modal-Login").modal("show");
});
$(document).on('click', "#login-bottom",
function() { //提交登录
    document.getElementById("login-bottom").className = "btn btn-warning";
    document.getElementById("login-bottom").innerHTML = "Checking...";
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/login/',
        data: {
            "mode":"Login",
            "name": $("#login-name").val(),
            "password": sha256($("#login-password").val())
        },
        dataType: 'json',
        success: function(data) { //登陆成功
            if (data.state != "success") {
                document.getElementById("login-bottom").className = "btn btn-danger";
                document.getElementById("login-bottom").innerHTML = data.state;
            } else if (data.state == "success") {
                setDefaultCookie("login", 1);
                setDefaultCookie("name", data.name);
                document.getElementById("login-bottom").className = "btn btn-success";
                document.getElementById("login-bottom").innerHTML = "Success";
                $('#Modal-Login').modal('hide');
                afterlogin(data);
            }
        }
    });
});
//监控详细信息按钮
$(document).on('click', '#text-info-show',
function() //详细信息
{
    $("#attributer").slideToggle("slow");//slideToggle实现切换
});
$(document).on('click', '#text-shower-show',
function() //展示框
{
    $("#shower").slideToggle("slow");
});
$(document).on('click', '#text-password-on',
function() //启用密码
{
    $(this).html("禁用");
    $(this).attr('id', 'text-password-off');
    $("#text-password").removeAttr('disabled');
});
$(document).on('click', '#text-password-off',
function() //禁用密码
{
    $(this).html("启用");
    $(this).attr('id', 'text-password-on');
    $("#text-password").attr('disabled', 'disabled');
});
//监控打开登录退出页
//提交登录
$(document).on('click', '#open-login',
function() {
    //window.open("/login");
});
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
$(document).on('click', '#open-logout',
function() {
    logout();
});

//检查注册字符
function CheckRegisterName(name) {
    var matchname = /^[a-zA-Z][0-9a-zA-Z@.\-]{4,29}$/g;
    if (matchname.test(name)) {
        return true;
    }
    return false;
}
function CheckRegisterMail(mail) {
    var matchemail = /^[0-9a-zA-Z][0-9a-zA-Z\-]{0,}@[0-9a-zA-Z\.\-]+?\.[a-zA-Z\.]+[a-zA-Z]$/g;
    if (matchemail.test(mail)) {
        return true;
    }
    return false;
}
function CheckRegisterPassword(passwords) {
    var matchepassword = /^[0-9a-zA-Z@.\-\_\#\$\^\&\*]{6,128}$/g;
    if (matchepassword.test(passwords)) {
        return true;
    }
    return false;
}

//监控提交注册
$(document).on('click', '#register-Signup',
function() //提交注册
{
    var name = $("#register-name").val();
    var mail = $("#register-mail").val();
    var password1 = $("#register-password").val();
    var password2 = $("#register-confirm-password").val();
    var istrue = true;
    if (!CheckRegisterName(name)) {
        document.getElementById("register-name-warning").innerHTML = "用户名有误";
        return false;
    }
    if (!CheckRegisterMail(mail)) {
        document.getElementById("register-mail-warning").innerHTML = "邮箱有误";
        return false;
    }
    if (!CheckRegisterPassword(password1)) {
        document.getElementById("register-password-warning").innerHTML = "密码有误";
        istrue = false;
    }
    if (!CheckRegisterPassword(password2)) {
        document.getElementById("register-confirm-password-warning").innerHTML = "密码有误";
        istrue = false;
    }
    if (password1 != password2) {
        document.getElementById("register-confirm-password-warning").innerHTML = "2次输入密码不同";
        istrue = false;
    }
    if (istrue) {
        document.getElementById("register-Signup").className = "btn btn-warning";
        document.getElementById("register-Signup").innerHTML = "Loading...";
        $.ajax({
            beforeSend: function(request) {
                request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            type: 'POST',
            url: '/register/',
            data: {
                "mode":"Register",
                "name": name,
                "mail": mail,
                "password": password1
            },
            dataType: 'json',
            success: function(data) {
                if (data.state == "success") {
                    document.getElementById("register-Signup").className = "btn btn-success";
                    document.getElementById("register-Signup").innerHTML = "success";
                    window.location.href = "/";
                } else {
                    document.getElementById("register-Signup").className = "btn btn-danger";
                    document.getElementById("register-Signup").innerHTML = data.state;
                }
            }
        });
    }
});

//监控注册栏修改
$(document).on('focus', '#register-name', //检查姓名
function() {
    document.getElementById("register-name-warning").innerHTML = "";
});

$(document).on('blur', '#register-name', //检查姓名
function() {
    var name = $("#register-name").val();
    if (!CheckRegisterName(name)) {
        document.getElementById("register-name-warning").innerHTML = "包含非法字符";
    }
    if (name.length < 5) {
        document.getElementById("register-name-warning").innerHTML = "至少5位";
    }
});

$(document).on('focus', '#register-mail', //检查邮箱
function() {
    document.getElementById("register-mail-warning").innerHTML = "";
});

$(document).on('blur', '#register-mail', //检查邮箱
function() {
    var mail = $("#register-mail").val();
    if (!CheckRegisterMail(mail)) {
        document.getElementById("register-mail-warning").innerHTML = "格式错误";
    }
});
$(document).on('focus', '#register-password', //检查密码1
function() {
    document.getElementById("register-password-warning").innerHTML = "";
});

$(document).on('blur', '#register-password', //检查密码1
function() {
    var password1 = $("#register-password").val();
    if (!CheckRegisterPassword(password1)) {
        document.getElementById("register-password-warning").innerHTML = "包含非法字符";
    }
    if (password1.length < 6) {
        document.getElementById("register-password-warning").innerHTML = "至少6位";
    }
});
$(document).on('focus', '#register-confirm-password', //检查密码2
function() {
    document.getElementById("register-confirm-password-warning").innerHTML = "";
});

$(document).on('blur', '#register-confirm-password', //检查密码2
function() {
    var password1 = $("#register-password").val();
    var password2 = $("#register-confirm-password").val();
    if (!CheckRegisterPassword(password2)) {
        document.getElementById("register-confirm-password-warning").innerHTML = "包含非法字符";
    }
    if (password2.length < 6) {
        document.getElementById("register-confirm-password-warning").innerHTML = "至少6位";
    }
    if (password1 != password2) {
        document.getElementById("register-confirm-password-warning").innerHTML = "2次输入密码不同";
    }
});
//=====================
//更改密码检查
//=====================
//监控修改密码按钮
$(document).on('click', "#change-password",
function() {
    $("#change-user-password").modal("show");
});
//检查密码1
$(document).on('focus', '#change-newpassword',
function() {
    document.getElementById("change-password-warning").innerHTML = "";
});
//检查密码1
$(document).on('blur', '#change-newpassword',
function() {
    var password1 = $("#change-newpassword").val();
    if (!CheckRegisterPassword(password1)) {
        document.getElementById("change-password-warning").innerHTML = "包含非法字符";
    }
    if (password1.length < 6) {
        document.getElementById("change-password-warning").innerHTML = "至少6位";
    }
});
//检查密码2
$(document).on('focus', '#change-confirm-newpassword',
function() {
    document.getElementById("change-confirm-password-warning").innerHTML = "";
});
//检查密码2
$(document).on('blur', '#change-confirm-newpassword',
function() {
    var password1 = $("#change-newpassword").val();
    var password2 = $("#change-confirm-newpassword").val();
    if (!CheckRegisterPassword(password2)) {
        document.getElementById("change-confirm-password-warning").innerHTML = "包含非法字符";
    }
    if (password2.length < 6) {
        document.getElementById("change-confirm-password-warning").innerHTML = "至少6位";
    }
    if (password1 != password2) {
        document.getElementById("change-confirm-password-warning").innerHTML = "2次输入密码不同";
    }
});
$(document).on('click', "#change-password-submit",
function() {
    var oldpassword = $("#change-oldpassword").val();
    var password1 = $("#change-newpassword").val();
    var password2 = $("#change-confirm-newpassword").val();
    var istrue = true;
    if (!CheckRegisterPassword(oldpassword)) {
        document.getElementById("change-oldpassword-warning").innerHTML = "密码有误";
        istrue = false;
    }
    if (!CheckRegisterPassword(password1)) {
        document.getElementById("change-password-warning").innerHTML = "密码有误";
        istrue = false;
    }
    if (!CheckRegisterPassword(password2)) {
        document.getElementById("change-confirm-password-warning").innerHTML = "密码有误";
        istrue = false;
    }
    if (password1 != password2) {
        document.getElementById("change-confirm-password-warning").innerHTML = "2次输入密码不同";
        istrue = false;
    }
    if (istrue) {
        document.getElementById("change-password-submit").className = "btn btn-warning";
        document.getElementById("change-password-submit").innerHTML = "Changing...";
        $.ajax({
            beforeSend: function(request) {
                request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            type: 'POST',
            url: '/changepassword/',
            data: {
                "mode":"ChangePassword",
                "name": getCookie("name"),
                "password": sha256($("#change-oldpassword").val()),
                "newpassword": $("#change-confirm-newpassword").val()
            },
            dataType: 'json',
            success: function(data) {
                if (data.state != "success") {
                    document.getElementById("change-password-submit").className = "btn btn-danger";
                    document.getElementById("change-password-submit").innerHTML = data.state;
                } else if (data.state == "success") {
                    document.getElementById("change-password-submit").className = "btn btn-success";
                    document.getElementById("change-password-submit").innerHTML = "Success";
                }
            }
        });
    }
});
//=====================
//重置密码
//=====================
//监控重置密码按钮
$(document).on('click', "#reset-open",
function() {
    $("#Modal-Login").modal("hide");
    $("#reset-password").modal("show");
});
//提交重置密码
$(document).on('click', "#reset-submit",
function() {
    var name = $("#reset-name").val();
    var mail = $("#reset-mail").val();
    var istrue = true;
    if (!CheckRegisterName(name)) {
        document.getElementById("reset-name-warning").innerHTML = "用户名有误";
        istrue = false;
    }
    if (!CheckRegisterMail(mail)) {
        document.getElementById("reset-mail-warning").innerHTML = "邮箱有误";
        istrue = false;
    }
    if (istrue) {
        document.getElementById("reset-submit").className = "btn btn-warning";
        document.getElementById("reset-submit").innerHTML = "Reseting...";
        $.ajax({
            beforeSend: function(request) {
                request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            type: 'POST',
            url: '/resetpassword/',
            data: {
                "mode":"ResetPassword",
                "name": $("#reset-name").val(),
                "mail": $("#reset-mail").val()
            },
            dataType: 'json',
            success: function(data) {
                if (data.state != "success") {
                    document.getElementById("reset-submit").className = "btn btn-danger";
                    document.getElementById("reset-submit").innerHTML = data.state;
                } else if (data.state == "success") {
                    document.getElementById("reset-submit").className = "btn btn-success";
                    document.getElementById("reset-submit").innerHTML = "Success";
                }
            }
        });
    }
});



//////////////////////
//
//显示格式化函数
//
/////////////////////
function FormatEssay(essay,type) {
    //document.getElementById('showartical').setAttribute("style", ""); 
    SetPageStyleWhite();
    if (type=='html/text'){
        essay = FormatHtmlText(essay);
    }else if(type=='html'){
        essay = FormatHtml(essay);
    }else if(type=='text'){
        essay = FormatText(essay);
    }else if(type=='code'){
        essay = FormatCode(essay);
    }else if(type=='markdown'){
        try{
            essay = FormatMarkdown(essay);
          }catch(err){
            essay = err;
          }
    }else if(type=='json'){
        try{
            essay = FormatJson(essay);
          }catch(err){
            essay = err;
          }
    }else{
        essay = FormatHtmlText(essay);
    }
    return essay;
}

function FormatHtmlText(essay) {
    essay = essay.replace(/\n/g, "<br>");
    essay = essay.replace(/\ /g,"&nbsp;"); 
    return essay;
}

function FormatHtml(essay) {
    return essay;
}

function FormatText(essay) {
    essay = essay.replace(/\&/g,"&gt;");  
    essay = essay.replace(/</g,"&#60;");  
    essay = essay.replace(/>/g,"&#62;");  
    essay = essay.replace(/\ /g,"&nbsp;");  
    essay = essay.replace(/\'/g,"'");  
    essay = essay.replace(/\"/g,"&quot;");  
    //essay = essay.replace(/\n/g," <br>"); 
    return essay;
}

function FormatJson(essay) {
    essay = JSON.parse(essay);
    essay = JSON.stringify(essay, null, 4);
    essay = essay.replace(/\n/g, "<br>");
    essay = essay.replace(/\ /g,"&nbsp;"); 
    return essay;
}

function FormatMarkdown(essay) {
    var md = window.markdownit();
    essay = md.render(essay);
    return essay;
}

function FormatCode(essay) {
    var conf = {
    tabReplace: '    ',
    useBR:true
    }
    hljs.configure(conf)
    var py = hljs.highlightAuto(essay);
    essay = py.value;
    essay = hljs.fixMarkup(essay);
    essay = essay.replace(/\  /g,"&nbsp;&nbsp;"); //以2空格为单位替换
    //更改全局样式，记得改回去
    SetPageStyleBlack();
    return essay;
}
function SetPageStyleWhite(){
    $("#shower-panel").attr("class", "panel panel-default");
    $("#navbar").attr("class", "navbar navbar-default navbar-fixed-top");
    document.body.style.backgroundColor="#FFFFFF";
    document.body.style.color = "#000000";
    document.getElementById('showartical').setAttribute("style", "background:#FFFFFF;"); 
    document.getElementById('header-search').setAttribute("style", "");
    document.getElementById('header-search-buttom').setAttribute("style", "");
    document.getElementById('shower-panel').setAttribute("style", "");
    document.getElementById('shower-panel-heading').setAttribute("style", "");
}
function SetPageStyleBlack(){
    //navbar-inverse panel-title #75715e
    //$("#shower-panel").attr("class", "panel panel-primary");
    $("#navbar").attr("class", "navbar navbar-inverse navbar-fixed-top ");
    document.getElementById('showartical').setAttribute("style", ""); 
    document.getElementById('header-search').setAttribute("style", "background-color:#696969;border:#292929;color:#ffffff;");
    document.getElementById('header-search-buttom').setAttribute("style", "background-color:#696969;border:#696969;color:#ffffff;"); 
    document.getElementById('shower-panel').setAttribute("style", "background-color:#696969;border:#696969;color:#ffffff;");
    document.getElementById('shower-panel-heading').setAttribute("style", "background-color:#696969;border:#696969;color:#ffffff;"); 
    //设置字体颜色 
    document.body.style.backgroundColor="#292929";
    document.body.style.color = "#f8f8f2";
    //文章背景色 #f8f8f2 color
    document.getElementById('showartical').setAttribute("style", "background:#23241f;"); 
}
//document.body.style.backgroundImage="url(http://www.iteye.com/upload/logo/user/37073/648c9ed4-f54b-3f4a-ac54-905f5a483307.gif?1236833802)"; //改变背景图片  