//////////////////////
//
//�������ܺ���
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
//��ʾ��ʽ������
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
    essay = essay.replace(/\  /g,"&nbsp;&nbsp;"); //��2�ո�Ϊ��λ�滻
    //����ȫ����ʽ���ǵøĻ�ȥ
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
    //����������ɫ 
    document.body.style.backgroundColor="#292929";
    document.body.style.color = "#f8f8f2";
    //���±���ɫ #f8f8f2 color
    document.getElementById('showartical').setAttribute("style", "background:#23241f;"); 
}

//////////////////////
//
//�༭��
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
//չʾ����
//
/////////////////////
function CheckArticle() //�����ύ��ť״̬
{
    let essay = article.getEssay();
    let title = article.getTitle();
    if (essay.length >= MINESSAYLENGTH && essay.length <= MAXESSAYLENGTH && title.length >= MINTITLELENGTH && title.length <= MAXTITLELENGTH) {
        $("#text-submit,#text-edit-submit").removeAttr("disabled");
        $("#text-submit,#text-edit-submit").attr("class","btn btn-primary");
        $("#text-submit,#text-edit-submit").text("�ύ");
        return true;
    } else if (essay.length < MINESSAYLENGTH || title.length < MINTITLELENGTH) {
        $("#text-submit,#text-edit-submit").attr('disabled', 'disabled');
        $("#text-submit,#text-edit-submit").attr("class", "btn btn-danger");
        $("#text-submit,#text-edit-submit").text("���ݹ���");
        return false;
    } else if (essay.length > MAXESSAYLENGTH || title.length > MAXTITLELENGTH) {
        $("#text-submit,#text-edit-submit").attr('disabled', 'disabled');
        $("#text-submit,#text-edit-submit").attr("class", "btn btn-danger");
        $("#text-submit,#text-edit-submit").text("���ݹ���");
        return false;
    }
}

