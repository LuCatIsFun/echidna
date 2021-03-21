# Echidna - 基于django的博客

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Echidna是一个基于`Python3.7`和`Django3`的博客系统

![首页](example/index.jpg "首页")
![文章](example/article.jpg "文章")


## 特点
* 好玩的登录方式（使用终端登录）
* 支持黑夜模式
* 流畅的动效与交互体验
* 愉悦的书写体验
    * 图片支持粘贴
    * 图片支持拖拽缩放大小
    * 支持复制粘贴Word，excel
    * 代码高亮（两种高亮风格黑夜模式与白天模式自动切换）
    * 自动保存草稿
    * 文章支持设置标签，分组，支持设置密码
* 引入disqus评论

## 目录结构
<pre>
    ├── README.md                   # 说明文件
    ├── apps                        # 子项目目录
    │   ├── README.md                   - # 项目规范说明文件
    │   ├── article                     - # 文章模块
    │   └── user                        - # 用户模块
    ├── echidna                     # 项目主目录
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py             # 主配置文件
    │   ├── urls.py                 # 请求URL主入口
    │   └── wsgi.py
    ├── db.sqlite3                  # 自带数据库（仅开发环境）
    ├── env                         # 不同环境的配置文件
    │   ├── README.md                   - # 配置文件使用说明
    │   └── env                         - # 环境配置文件
    ├── logs                        # 日志
    │   └── uwsgi.log                   - # 运行日志
    ├── manage.py
    ├── reload                      # (uwsgi) 监听该文件变动重启服务
    ├── requirements.txt            # 项目依赖
    ├── static                      # 静态资源文件
    │   ├── css
    │   ├── image
    │   └── js
    └── uwsgi.ini                   # uwsgi配置文件
</pre> 
    
## 开发中
新的页面：
* 我的项目
* 关于我

新的功能：
* 文章检索功能
* 文章目录

## 目录

- [特点](#特点)
- [开发中](#开发中)
- [安装](#安装)
- [使用](#使用)
- [作者](#作者)
- [贡献](#贡献)
- [许可证](#许可证)

## 安装

* 安装包依赖
  * 进到工程目录 命令行执行: <code>pip3 install -r requirements.txt</code>
* 首次初始化数据库:
  * 进到工程目录 命令行执行: <code>python3 manage migrate</code>
* 启动
  * 开发环境
    * 进到工程目录 命令行执行: <code>python3 manage runserver 127.0.0.1:8000</code>
    * 创建管理员用户 命令行执行: <code>python3 manage.py createsuperuser</code>
  * uwsgi
    * 项目目录下执行 <code>uwsgi --ini uwsgi.ini</code>

## 访问项目

* 访问项目
  * 浏览器打开：http://127.0.0.1:8000

## 常见问题

1. `No module named "Crypto"`
```shell script
# 因Python crypto库遗留问题所致，详情参考下方链接
pip uninstall crypto pycryptodome
pip install pycryptodome
```
参考文档：[解释Crypto模块怎么就这么"皮"](https://www.cnblogs.com/fawaikuangtu123/p/9761943.html)


## 相关资料

* 安装Python运行环境
  * https://www.python.org/downloads
* 安装Python包管理工具pip
  * https://www.runoob.com/w3cnote/python-pip-install-usage.html
* 安装Django Web框架
  * https://www.djangoproject.com/download
* 安装开发工具Pycharm
  * https://www.jetbrains.com/pycharm/download/#section=windows



## 作者

[@liyao2598330](https://github.com/liyao2598330)

## 贡献

你可以新开一个[issue](https://github.com/liyao2598330/echidna/issues/new) 或提交PR来参与


## 许可证

[MIT](LICENSE) © liyao2598330
