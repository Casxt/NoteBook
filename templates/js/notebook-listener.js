
//获取文章信息
$(document).on('click', '#Modal-article-passwords-submit',
function() {
    $(this).html("Loading...");
    autogetarticle(1);
});
//监控回车搜素
$(document).on('keydown', '#header-search',
//$('#header-search').keydown(
function(Key) {
    if (Key.keyCode == 13 && CheckSearchInput($('#header-search').val())) {
        var keyword = document.getElementById("header-search").value;
        history.pushState({},
        "note", ("/search/" + encodeURIComponent(keyword) + "/"));
        var res = SearchArticle();
        if (res) {
            //history.back();
        } else {
            //history.back();
        }
    }
});
//搜索按钮监控
$(document).on('click', '#header-search-buttom',
function() {
    if (CheckSearchInput($('#header-search').val())) {
        var keyword = document.getElementById("header-search").value;
        history.pushState({},
        "note", ("/search/" + encodeURIComponent(keyword) + "/"));
        var res = SearchArticle();
        if (res) {
            //history.back();
        } else {
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

//监控提交修改
$(document).on('click', '#text-edit-submit',
function() { //提交文章
    document.getElementById("text-edit-submit").className = "btn btn-warning";
    document.getElementById("text-edit-submit").innerHTML = "submitting...";
    var path = window.location.pathname
    var name = document.getElementById("text-edit-submit").name;
    var rawtitle = document.getElementById("text-edit-submit").value;
    var title = $("#text-title").val();
    var essay = $("#text-article").val();
    var cookie_name = unescape(getCookie("name"));
    var postdata = {
        "mode": "SubmitEditedArticle",
        "title": title,
        "essay": essay,
        "password": $("#text-password").val(),
        "tag": $("#text-tag").val(),
        "author": name,
        "name": cookie_name,
        "rawtitle": rawtitle,
        "type": $('#text-type option:selected').val()
    };
    if(!postdata["name"]){
        delete postdata["name"];
    }
    if(!postdata["author"]){
        delete postdata["author"];
    }
    if($('#text-password').attr("disabled") == "disabled") {
        delete(postdata["password"]);
    }
    if (CheckArticle()) {
        $.ajax({
            beforeSend: function(request) {
                request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            type: 'POST',
            url: '/editarticle/',
            data: postdata,
            dataType: 'json',
            success: function(data, status) {
                if (data.state == "success") {
                    setCookie((path == "/") ? "newtitle": "title", "", 0);
                    setCookie((path == "/") ? "newessay": "essay", "", 0);
                    document.getElementById("text-edit-submit").className = "btn btn-success";
                    document.getElementById("text-edit-submit").innerHTML = data.state;
                    window.location.href = "/" + (name == "" ? "": name + "/") + title;
                } else {
                    document.getElementById("text-edit-submit").className = "btn btn-danger";
                    document.getElementById("text-edit-submit").innerHTML = data.state;
                }
            }
        });
    } 
});
//监控提交
$(document).on('click', '#text-submit',
function() {
    var path = window.location.pathname
    var title = document.getElementById("text-title").value;
    var essay = document.getElementById("text-article").value;
    var cookie_name = unescape(getCookie("name"));
    var postdata = {
        "mode": "SubmitArticle",
        "title": title,
        "essay": essay,
        "password": $("#text-password").val(),
        "tag": $("#text-tag").val(),
        "type": $('#text-type option:selected').val()
    };
    cookie_name == 'null' ? true: postdata["author"] = cookie_name;
    cookie_name == 'null' ? true: postdata["name"] = cookie_name;
    if ($('#text-password').attr("disabled") == "disabled") {
        delete(postdata["password"]);
    }
    if (CheckArticle()) {
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
            url: '/submitarticle/',
            data: postdata,
            // contentType: "application/json",//该句代码不能加，加了之后无法POST
            dataType: 'json',
            success: function(data, status) {
                if (data.state == "success") {
                    setCookie((path == "/") ? "newtitle": "title", "", 0);
                    setCookie((path == "/") ? "newessay": "essay", "", 0);
                    setCookie((path == "/") ? "newtype": "type", "", 0);
                    document.getElementById("text-submit").className = "btn btn-success";
                    document.getElementById("text-submit").innerHTML = data.state;
                    window.location.href = "/" + cookie_name + $("#text-title").val() + "/";
                } else {
                    document.getElementById("text-submit").className = "btn btn-danger";
                    document.getElementById("text-submit").innerHTML = data.state;
                }
            }
        });
    }
});

//监控跳转
$(document).on('click', '.article-list-item',
function() { //提交文章
    var href = $(this).attr('href');
    if (href && href!="" && href!="undefined"){
        window.location.href = href;
    }    
});

//监控编辑按钮
$(document).on('click', '.article-edit',
function() { //提交文章
    var href = $(this).parent().parent().attr("href");
    //清空herf防止跳转
   $(this).parent().parent().attr("href","");
    window.location.href = '/e'+href;
});

//监控删除
$(document).on('click', '.article-delete',
function() { //提交文章
    var thisitem = $(this);
    //清空herf防止跳转
    $(this).parent().parent().attr("href","");
    var title = $(this).parent().children("strong").text();
    
    $(this).html('<span class="label label-warning">deling...</span>');
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/deletearticle/',
        data: {
            "mode": "DeleteArticle",
            "author": getCookie("name"),
            "title": title,
            "name": getCookie("name")
        },
        dataType: 'json',
        success: function(data) {
            if (data.state == "success") {
                thisitem.html('<span id="search-warning" class="label label-success">success</span>');
                thisitem.parent().parent().hide();
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
            "mode": "Login",
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
    $("#attributer").slideToggle("slow"); //slideToggle实现切换
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
$(document).on('click', '#open-login',
function() {
    //window.open("/login");
});
$(document).on('click', '#open-logout',
function() {
    logout();
});

//监控注册按钮
$(document).on('click', '#Signup-bottom',
function() {
    $("#Modal-Login").modal('hide');
    $("#Modal-Register").modal({
        remote: "/register",
        show: true
    });
});
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
                "mode": "Register",
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
                "mode": "ChangePassword",
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
                    window.location.href = "/";
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
                "mode": "ResetPassword",
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
                    window.location.href = "/";
                }
            }
        });
    }
});