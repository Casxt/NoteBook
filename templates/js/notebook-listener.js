
//��ȡ������Ϣ
$(document).on('click', '#Modal-artical-passwords-submit',
function() {
    $(this).html("Loading...");
    autogetartical(1);
});
//��ػس�����
$(document).on('keydown', '#header-search',
//$('#header-search').keydown(
function(Key) {
    if (Key.keyCode == 13 && CheckSearchInput($('#header-search').val())) {
        var keyword = document.getElementById("header-search").value;
        history.pushState({},
        "note", ("/search/" + encodeURIComponent(keyword) + "/"));
        var res = SearchArtical();
        if (res) {
            //history.back();
        } else {
            //history.back();
        }
    }
});
//������ť���
$(document).on('click', '#header-search-buttom',
function() {
    if (CheckSearchInput($('#header-search').val())) {
        var keyword = document.getElementById("header-search").value;
        history.pushState({},
        "note", ("/search/" + encodeURIComponent(keyword) + "/"));
        var res = SearchArtical();
        if (res) {
            //history.back();
        } else {
            //history.back();
        }
    }
});
//��������ؼ���
$('#header-search').on("focus",
function() {
    $('#search-warning').fadeOut(SEARCHWARNINGFADETIME);
    //document.getElementById("search-warning").innerHTML = "";
});
$('#header-search').on("change",
function() {
    CheckSearchInput($('#header-search').val());
});

//����ύ�޸�
$(document).on('click', '#text-edit-submit',
function() { //�ύ����
    document.getElementById("text-edit-submit").className = "btn btn-warning";
    document.getElementById("text-edit-submit").innerHTML = "submitting...";
    var path = window.location.pathname
    var name = document.getElementById("text-edit-submit").name;
    var rawtitle = document.getElementById("text-edit-submit").value;
    var title = $("#text-title").val();
    var essay = $("#text-artical").val();
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
            url: '/editartical/',
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
//����ύ
$(document).on('click', '#text-submit',
function() {
    var path = window.location.pathname
    var title = document.getElementById("text-title").value;
    var essay = document.getElementById("text-artical").value;
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
            url: '/submitartical/',
            data: postdata,
            // contentType: "application/json",//�þ���벻�ܼӣ�����֮���޷�POST
            dataType: 'json',
            success: function(data, status) {
                if (data.state == "success") {
                    setCookie((path == "/") ? "newtitle": "title", "", 0);
                    setCookie((path == "/") ? "newessay": "essay", "", 0);
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
//���ɾ��
$(document).on('click', '.artical-delete',
function() { //�ύ����
    var thisitem = $(this);
    var title = $(this).val();
    $(this).html('<span id="search-warning" class="label label-warning">Deleteing...</span>');
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        type: 'POST',
        url: '/deleteartical/',
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
                thisitem.parent().hide();
                //$(("#" + title)).hide();
            } else {
                alert(data.state);
            }
        }
    });
});

//��ص�¼��ť
$(document).on('click', "#open-login",
function() {
    $("#Modal-Login").modal("show");
});
$(document).on('click', "#login-bottom",
function() { //�ύ��¼
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
        success: function(data) { //��½�ɹ�
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
//�����ϸ��Ϣ��ť
$(document).on('click', '#text-info-show',
function() //��ϸ��Ϣ
{
    $("#attributer").slideToggle("slow"); //slideToggleʵ���л�
});
$(document).on('click', '#text-shower-show',
function() //չʾ��
{
    $("#shower").slideToggle("slow");
});
$(document).on('click', '#text-password-on',
function() //��������
{
    $(this).html("����");
    $(this).attr('id', 'text-password-off');
    $("#text-password").removeAttr('disabled');
});
$(document).on('click', '#text-password-off',
function() //��������
{
    $(this).html("����");
    $(this).attr('id', 'text-password-on');
    $("#text-password").attr('disabled', 'disabled');
});
//��ش򿪵�¼�˳�ҳ
$(document).on('click', '#open-login',
function() {
    //window.open("/login");
});
$(document).on('click', '#open-logout',
function() {
    logout();
});

//���ע�ᰴť
$(document).on('click', '#Signup-bottom',
function() {
    $("#Modal-Login").modal('hide');
    $("#Modal-Register").modal({
        remote: "/register",
        show: true
    });
});
//����ύע��
$(document).on('click', '#register-Signup',
function() //�ύע��
{
    var name = $("#register-name").val();
    var mail = $("#register-mail").val();
    var password1 = $("#register-password").val();
    var password2 = $("#register-confirm-password").val();
    var istrue = true;
    if (!CheckRegisterName(name)) {
        document.getElementById("register-name-warning").innerHTML = "�û�������";
        return false;
    }
    if (!CheckRegisterMail(mail)) {
        document.getElementById("register-mail-warning").innerHTML = "��������";
        return false;
    }
    if (!CheckRegisterPassword(password1)) {
        document.getElementById("register-password-warning").innerHTML = "��������";
        istrue = false;
    }
    if (!CheckRegisterPassword(password2)) {
        document.getElementById("register-confirm-password-warning").innerHTML = "��������";
        istrue = false;
    }
    if (password1 != password2) {
        document.getElementById("register-confirm-password-warning").innerHTML = "2���������벻ͬ";
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

//���ע�����޸�
$(document).on('focus', '#register-name', //�������
function() {
    document.getElementById("register-name-warning").innerHTML = "";
});

$(document).on('blur', '#register-name', //�������
function() {
    var name = $("#register-name").val();
    if (!CheckRegisterName(name)) {
        document.getElementById("register-name-warning").innerHTML = "�����Ƿ��ַ�";
    }
    if (name.length < 5) {
        document.getElementById("register-name-warning").innerHTML = "����5λ";
    }
});

$(document).on('focus', '#register-mail', //�������
function() {
    document.getElementById("register-mail-warning").innerHTML = "";
});

$(document).on('blur', '#register-mail', //�������
function() {
    var mail = $("#register-mail").val();
    if (!CheckRegisterMail(mail)) {
        document.getElementById("register-mail-warning").innerHTML = "��ʽ����";
    }
});
$(document).on('focus', '#register-password', //�������1
function() {
    document.getElementById("register-password-warning").innerHTML = "";
});

$(document).on('blur', '#register-password', //�������1
function() {
    var password1 = $("#register-password").val();
    if (!CheckRegisterPassword(password1)) {
        document.getElementById("register-password-warning").innerHTML = "�����Ƿ��ַ�";
    }
    if (password1.length < 6) {
        document.getElementById("register-password-warning").innerHTML = "����6λ";
    }
});
$(document).on('focus', '#register-confirm-password', //�������2
function() {
    document.getElementById("register-confirm-password-warning").innerHTML = "";
});

$(document).on('blur', '#register-confirm-password', //�������2
function() {
    var password1 = $("#register-password").val();
    var password2 = $("#register-confirm-password").val();
    if (!CheckRegisterPassword(password2)) {
        document.getElementById("register-confirm-password-warning").innerHTML = "�����Ƿ��ַ�";
    }
    if (password2.length < 6) {
        document.getElementById("register-confirm-password-warning").innerHTML = "����6λ";
    }
    if (password1 != password2) {
        document.getElementById("register-confirm-password-warning").innerHTML = "2���������벻ͬ";
    }
});

//=====================
//����������
//=====================
//����޸����밴ť
$(document).on('click', "#change-password",
function() {
    $("#change-user-password").modal("show");
});
//�������1
$(document).on('focus', '#change-newpassword',
function() {
    document.getElementById("change-password-warning").innerHTML = "";
});
//�������1
$(document).on('blur', '#change-newpassword',
function() {
    var password1 = $("#change-newpassword").val();
    if (!CheckRegisterPassword(password1)) {
        document.getElementById("change-password-warning").innerHTML = "�����Ƿ��ַ�";
    }
    if (password1.length < 6) {
        document.getElementById("change-password-warning").innerHTML = "����6λ";
    }
});
//�������2
$(document).on('focus', '#change-confirm-newpassword',
function() {
    document.getElementById("change-confirm-password-warning").innerHTML = "";
});
//�������2
$(document).on('blur', '#change-confirm-newpassword',
function() {
    var password1 = $("#change-newpassword").val();
    var password2 = $("#change-confirm-newpassword").val();
    if (!CheckRegisterPassword(password2)) {
        document.getElementById("change-confirm-password-warning").innerHTML = "�����Ƿ��ַ�";
    }
    if (password2.length < 6) {
        document.getElementById("change-confirm-password-warning").innerHTML = "����6λ";
    }
    if (password1 != password2) {
        document.getElementById("change-confirm-password-warning").innerHTML = "2���������벻ͬ";
    }
});
$(document).on('click', "#change-password-submit",
function() {
    var oldpassword = $("#change-oldpassword").val();
    var password1 = $("#change-newpassword").val();
    var password2 = $("#change-confirm-newpassword").val();
    var istrue = true;
    if (!CheckRegisterPassword(oldpassword)) {
        document.getElementById("change-oldpassword-warning").innerHTML = "��������";
        istrue = false;
    }
    if (!CheckRegisterPassword(password1)) {
        document.getElementById("change-password-warning").innerHTML = "��������";
        istrue = false;
    }
    if (!CheckRegisterPassword(password2)) {
        document.getElementById("change-confirm-password-warning").innerHTML = "��������";
        istrue = false;
    }
    if (password1 != password2) {
        document.getElementById("change-confirm-password-warning").innerHTML = "2���������벻ͬ";
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
//��������
//=====================
//����������밴ť
$(document).on('click', "#reset-open",
function() {
    $("#Modal-Login").modal("hide");
    $("#reset-password").modal("show");
});
//�ύ��������
$(document).on('click', "#reset-submit",
function() {
    var name = $("#reset-name").val();
    var mail = $("#reset-mail").val();
    var istrue = true;
    if (!CheckRegisterName(name)) {
        document.getElementById("reset-name-warning").innerHTML = "�û�������";
        istrue = false;
    }
    if (!CheckRegisterMail(mail)) {
        document.getElementById("reset-mail-warning").innerHTML = "��������";
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