//////////////////////
//
//基础功能函数
//
/////////////////////
function isPhone() {
    var flag = false;
    var userAgentInfo = navigator.userAgent;
    var Agents = ["Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod"];
    for (var i = 0; i < Agents.length; i++) {
        if (userAgentInfo.indexOf(Agents[i]) > 0) {
            flag = true;
            break;
        }
    }
    return flag;
}
//////////////////////
//
//显示格式化函数
//
/////////////////////
function FormatEssay(essay,type) {
    //document.getElementById('showarticle').setAttribute("style", ""); 
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
    document.getElementById('showarticle').style.background="#FFFFFF"; 
    $("#header-search").css('background-color','');
    $("#header-search").css('border','');
    $("#header-search").css('color','');
    
    $("#header-search-buttom").css('background-color','');
    $("#header-search-buttom").css('border','');
    $("#header-search-buttom").css('color','');
    
    $("#shower-panel").css('background-color','');
    $("#shower-panel").css('border','');
    $("#shower-panel").css('color','');
    
    $("#shower-panel-heading").css('background-color','');
    $("#shower-panel-heading").css('border','');
    $("#shower-panel-heading").css('color','');
    //document.getElementById('showarticle').setAttribute("style", "background:#FFFFFF;"); 
    //document.getElementById('header-search').setAttribute("style", "");
    //document.getElementById('header-search-buttom').setAttribute("style", "");
    //document.getElementById('shower-panel').setAttribute("style", "");
    //document.getElementById('shower-panel-heading').setAttribute("style", "");
}
function SetPageStyleBlack(){
    //navbar-inverse panel-title #75715e
    //$("#shower-panel").attr("class", "panel panel-primary");
    $("#navbar").attr("class", "navbar navbar-inverse navbar-fixed-top ");
    document.getElementById('showarticle').setAttribute("style", ""); 
    
    $("#header-search").css('background-color','#696969');
    $("#header-search").css('border','#292929');
    $("#header-search").css('color','#ffffff');
    
    $("#header-search-buttom").css('background-color','#696969');
    $("#header-search-buttom").css('border','#696969');
    $("#header-search-buttom").css('color','#ffffff');
    
    $("#shower-panel").css('background-color','#696969');
    $("#shower-panel").css('border','#696969');
    $("#shower-panel").css('color','#ffffff');
    
    $("#shower-panel-heading").css('background-color','#696969');
    $("#shower-panel-heading").css('border','#696969');
    $("#shower-panel-heading").css('color','#ffffff');
    
    //document.getElementById('header-search').setAttribute("style", "background-color:#696969;border:#292929;color:#ffffff;");
    //document.getElementById('header-search-buttom').setAttribute("style", "background-color:#696969;border:#696969;color:#ffffff;"); 
    //document.getElementById('shower-panel').setAttribute("style", "background-color:#696969;border:#696969;color:#ffffff;");
    //document.getElementById('shower-panel-heading').setAttribute("style", "background-color:#696969;border:#696969;color:#ffffff;"); 
    //设置字体颜色 
    document.body.style.backgroundColor="#292929";
    document.body.style.color = "#f8f8f2";
    //文章背景色 #f8f8f2 color
    document.getElementById('showarticle').style.background="#23241f"; 
}

//////////////////////
//
//编辑器
//
/////////////////////
function ConfigWangEditor(editor){
    editor.config.menus = $.map(wangEditor.config.menus, function(item, key) {
        if (item === 'fullscreen'||
            item === 'emotion') {
            return null;
        }
        return item;
    });
if (isPhone()){
        editor.config.menus = [
        'bold',
        'underline',
        'italic',
        'eraser',
        'head',
        'unorderlist',
        'orderlist',
        'alignleft',
        'aligncenter'
     ];
    }

}
function OpenWangEditor(essay){
    editor = essay.wangEditor;
    ConfigWangEditor(editor);
    editor.create();
}
function CloseWangEditor(essay){
    $(".wangEditor-container").remove();
    $(essay.inputId).show();
}
//////////////////////
//
//展示框函数
//
/////////////////////
function CheckArticle() //设置提交按钮状态
{
    var essay = article.getEssay();
    var title = article.getTitle();
    if (essay.length >= MINESSAYLENGTH && essay.length <= MAXESSAYLENGTH && title.length >= MINTITLELENGTH && title.length <= MAXTITLELENGTH) {
        $("#text-submit,#text-edit-submit").removeAttr("disabled");
        $("#text-submit,#text-edit-submit").attr("class","btn btn-primary");
        $("#text-submit,#text-edit-submit").text("提交");
        return true;
    } else if (essay.length < MINESSAYLENGTH || title.length < MINTITLELENGTH) {
        $("#text-submit,#text-edit-submit").attr('disabled', 'disabled');
        $("#text-submit,#text-edit-submit").attr("class", "btn btn-danger");
        $("#text-submit,#text-edit-submit").text("内容过少");
        return false;
    } else if (essay.length > MAXESSAYLENGTH || title.length > MAXTITLELENGTH) {
        $("#text-submit,#text-edit-submit").attr('disabled', 'disabled');
        $("#text-submit,#text-edit-submit").attr("class", "btn btn-danger");
        $("#text-submit,#text-edit-submit").text("内容过多");
        return false;
    }
}

