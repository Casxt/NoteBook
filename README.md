# NoteBook<br>
2016.7.22更新分页<br>
2016。8.5支持多文档<br>
一个在线笔记记录网站<br>
后台通过django接受数据，前台通过js实现交互<br>
没有使用django的页面渲染<br>
填好config以后运行setup.py可以直接创建数据库<br>
表名在配置文件中可改，列名不可以改<br>
公用账户是admin，密码admin。暂不支持更改，日后会支持<br>
功能包括：<br>
* 用户注册（非注册用户也可快速记录笔记）
* 邮件提醒
* 文章密码
* 搜索功能（简易的搜索）
* 支持html标签效果
* 支持markdown标签效果
* 用户权限系统(有计划)<br><br><br>
进度
* 文章增删改 已完成
* 文章密码及其他信息增删改 已完成
* 用户注册 已完成
* 用户登录及多次失败锁定 已完成
* 确认邮件 已完成
* 修改密码 已完成
* 分页系统 已完成
* markdown 已完成
* 权限系统 计划中
* 网页交互界面 与系统开发同步<br><br><br>
有些地方的防恶意注入还没做，还有防xss也不完善。<br>
示例：note.forer.cn<br>
