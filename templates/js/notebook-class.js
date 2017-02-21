
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
//虽然有createNew函数，但是考虑到这三个类全局只能有一个，故不再使用createNew函数创建

var Essay = {
//共享变量
    //内容
    text : "",
    //属性
    attribute:{
        type:"html/text",
        password:null,
        id:null,
        pubtime:"0000-00-00 00:00:00",
        lastesttime:"0000-00-00 00:00:00",
    },
    //实例列表
    instances:new Array(),
    //更改内容
    setText:function(text){
        Essay.text = text;
        Instances = Essay.instances;
        for(var i=0;i<Instances.length;i++){
            Instances[i].setEssay(Essay.text);
        }
    },
    //更改类型
    setAttribute:function(Attribute,value){
        Essay.attribute[Attribute] = value;
        Instances = Essay.instances;
        for(var i=0;i<Instances.length;i++){
            Instances[i].updateAttribute(Attribute,Essay.attribute[Attribute]);
        }
    },
//私有成员    
    createNew:function(inputid,outputid,typeid,passwordid,idid,pubtimeid,lastesttimeid){
        var essay = {
            inputId:inputid,
            outputId:outputid,
            typeId:typeid,
            passwordId:passwordid,
            idId:idid,
            pubtimeId:pubtimeid,
            lastesttimeId:lastesttimeid,
            editor:"textarea",
            wangEditor:new wangEditor(inputid.replace("#","")),
            //下面属性部分不建议从外围更改
            text : "",
            type:"html/text",
            password:null,
            id:null,
            pubtime:"0000-00-00 00:00:00",
            lastesttime:"0000-00-00 00:00:00"
        };
        Essay.instances.push(essay);
        
        //获取essay时使用此函数
        essay.get=function(){
            return essay.text;
        };
        //更新essay时使用此函数
        essay.set=function(t){
            Essay.setText(t);
        };
        //更新essay属性
        essay.setAttribute=function(Attribute,value){
            Essay.setAttribute(Attribute,value);
            if (Attribute=="type"){
                if (essay["type"] == "html"){
                    essay.changeToWangEdito();
                }else{
                    essay.changeToTextarea();
                }
            }
        };
        //格式化字符串
        essay.format=FormatEssay;
        //刷新essay显示区
        essay.show=function(e=null){
            $(essay.outputId).html(e?e:essay.format(essay.get(),essay.type));
        };
        //刷新essay输入区
        essay.updateInput=function(){
            e = essay.get();
            if (essay.editor == "textarea"){
                $(essay.inputId).val(e);
            }
            else if(essay.editor == "wangEditor"){
                essay.wangEditor.$txt.html(e);
            }
        };
        essay.cleanEssay = function(e){
            if (e){
                e = e.replace(/<script/gi, "").replace(/script>/gi, "");
                e = e.replace(/<iframe/gi, "").replace(/iframe>/gi, "");
                e = e.replace(/<link/gi, "");
                e = e.replace(/<style/gi, "").replace(/style>/gi, "");
                e = e.replace(/<frameset/gi, "").replace(/frameset>/gi, "");
                return e;
            }
            return "";
        };
        //隐藏函数供公共函数调用使用
        essay.setEssay=function(e){
            essay.text = essay.cleanEssay(e);
            essay.updateInput(essay.get());
        };
        //隐藏函数供公共函数调用使用
        essay.updateAttribute=function(Attribute,value){
            essay[Attribute] = value;
            $(essay[Attribute+"Id"]).val(value);
        };
        //隐藏函数供公共函数调用使用
        essay.getEssay=function(){
            if (essay.editor == "textarea"){
                return $(essay.inputId).val();
            }
            else if(essay.editor == "wangEditor"){
                return essay.wangEditor.$txt.html();
            }
        };
        //切换编辑器
            //切换到wangEditor
        essay.changeToWangEdito=function(){
            //同步数据
            essay.oninput();
            //更改属性
            essay.editor="wangEditor";
            //切换监听事件
            essay.wangEditor.onchange = essay.oninput;
            essay.oninput_hook = $(document).off('input',essay.inputId,function(){essay.oninput()});
            //切换gui
            OpenWangEditor(essay);
            //设置内容
            essay.updateInput();
        };
            //切换到textarea
        essay.changeToTextarea=function(){
            //同步数据
            essay.oninput();
            //更改属性
            essay.editor="textarea";
            //切换监听事件
            essay.wangEditor.onchange = function(){};
            essay.oninput_hook = $(document).on('input',essay.inputId,function(){essay.oninput()});
            //切换gui
            CloseWangEditor(essay);
            //重设wangEditor
            essay.wangEditor=new wangEditor(inputid.replace("#",""));
            //设置内容
            essay.updateInput();
        };
        //保存
        essay.saveCookie=function(){
            let path = window.location.pathname
            setCookie((path=="/")?"newessay":"essay", escape(essay.get()), 30);
            setCookie((path=="/")?"newtype":"type", escape(essay["type"]), 30);
        };
        //文章变化时执行函数
        essay.oninput = function(){
            essay.set(essay.getEssay())
            essay.show();
            essay.saveCookie();
        };
        //属性变化时执行函数
        essay.attribute_onchanget = function(){
            essay.setAttribute("type",$(essay.typeId).val());
            essay.setAttribute("password",$(essay.passwordId).val());
            essay.saveCookie();
            essay.show();
        };
        //钩子
        essay.oninput_hook = function(){};
        essay.attribute_onchange_hook = function(){};
        $(document).on('input',essay.inputId,function(){essay.oninput()});
        $(document).on('input',
        essay.typeId+','+essay.passwordId,
        function(){essay.attribute_onchanget()});
        return essay;
    }
};
//"#text-password"

var Title = {
//共享变量
    //内容
    text : "",
    //实例列表
    instances:new Array(),
    //更改内容
    setText:function(text){
        Title.text = text;
        Instances = Title.instances;
        for(var i=0;i<Instances.length;i++){
            Instances[i].setTitle(text);
        }
    },

//私有成员    
    createNew:function(inputid,outputid){
        var title = {
            inputId:inputid,
            outputId:outputid,
            //下面一行属性部分不建议从外围更改
            text : ""
        };
        Title.instances.push(title);
        
        //获取title时使用此函数
        title.get=function(){
            return title.text;
        };
        //更新title时使用此函数
        title.set=function(t){
            Title.setText(t);
        };
        //刷新title显示区时使用此函数
        title.show=function(t=null){
            $(title.outputId).html(t?t:title.get());
        };
        //刷新title输入区
        title.updateInput=function(){
            $(title.inputId).val(title.cleanTitle(title.get()));
        };
        title.cleanTitle = function(t){
            t = t.replace(/<|>/g, "");
            t = t.replace(/^\s+/g, "");
            t = t.replace(/\s/g, " ");
            return t;
        };
        //保存
        title.saveCookie=function(){
            let path = window.location.pathname
            setCookie((path=="/")?"newtitle":"title", escape(title.get()), 30);
        };
        //隐藏函数供公共函数调用使用
        title.setTitle=function(t){
            t = title.cleanTitle(t);
            title.text = t;
            title.updateInput();
        };
        //隐藏函数供公共函数调用使用
        title.getTitle=function(){
            return $(title.inputId).val();
        };
        title.oninput = function(){
            title.set(title.getTitle())
            title.show();
            title.saveCookie();
        };
        
        title.oninput_hook = $(document).on('input',title.inputId,function(){title.oninput()});
        
        return title;
    }
};


var Article = {
    createNew:function(){
        var article = {
            title:Title.createNew("#text-title","#showtitle"),
            essay:Essay.createNew("#text-article","#showarticle","#text-type","#text-password","#text-id","#text-pubtime","#text-lastesttime")
        };
        article.show=function(t=null,e=null){
            article.title.show(t);
            article.essay.show(e);
        };
        article.updateInput=function(){
            article.title.updateInput();
            article.essay.updateInput();
        };
        article.setTitle=function(t){
            article.title.set(t);
        };
        article.setEssay=function(e){
            article.essay.set(e);
        };
        article.setAttribute=function(Attribute,value){
            article.essay.setAttribute(Attribute,value);
        };
        article.getTitle=function(){
            return article.title.get();
        };
        article.getEssay=function(){
            return article.essay.get();
        };
        article.getAttribute=function(Attribute){
            return article.essay[Attribute];
        };
        article.changeToWangEdito=function(){
            article.essay.changeToWangEdito();
        };
        article.changeToTextarea=function(){
            article.essay.changeToTextarea();
        };
        article.loadArticle=function(){
        };
        return article;
    }
}
