
# xingyunlib
[toc]

开发者：严子昱|崔轩宇

v1.2.20201004

#v1.2.xx以后全是正式版#

#hack-20201004:修复xesuser故障

版权所有，侵权必究

内置函数 导入方式：

```python
from xingyunlib import *
```
### 加密函数

```python
md=md5("111")#作用：用MD5加密"111"，返回一个字符串
s1=sha1("111")#作用：用sha1加密"111"，返回一个字符串
s256=sha256("111")#作用：用sha1加密"111"，返回一个字符串
```

### 颜色类

```python
color=colorX(颜色,传进去的颜色类型)#类型支持"rgb","hsv","hex"
#示例：
color=colorX((100,100,100),"rgb")
```

#### color.color

返回颜色

```python
z=color.color
```

#### color_to(to_color,change=False)

返回一个要转换的颜色

to_color:转换的颜色，类型支持"rgb","hsv","hex"

change：是否更改原来的颜色

```python
color=colorX((255,255,255),"rgb")#实例化rgb
color.color_to("hex",True)#更改进制为16进制
print(color.color)#打印出color.color
```



# all（一次性导入扩展！可能出现覆盖现象！）

## 使用方式

```python
from xingyunlib.all import*
#或者
import xingyunlib.all as xingyunlib
```

# print_format（print格式化扩展）

开发者：严子昱

## 导入方式

```python
from xingyunlib.print_format import*
```



### print() 

```python
print(*str,t=0,sepr=" ",end="\n") 
```


我们来逐个讲解他们的用法 

首先来看t参数： 
t=每个字停留的时间(默认为不停留) 
比如说，要每个字停留1秒，输出"nice"的代码如下： 
`print("nice",t=1)` 

然后我们来看end参数 
这个end参数其实和原来print的end参数是同样的作用 
默认是"\n"(换行符) 

最后我们看sepr参数，这个参数也是和原来print的sepr是同样的作用 
我们来看一个例子： 
`print("ni","e",sepr="c")` 
最后输出的就是“nice” 

我们来看大家这个很关心的变色简洁方式 
我们在变色具体支持这些颜色： 
红、白、绿、蓝、黄、青、紫 
用法如下（注意是两个斜杠）： 
'\\'+颜色（字的颜色变化） 
'\\l'+颜色（字的颜色变化,亮色）
'\\b'+颜色（字的背景变化） 
'\\bl'+颜色（字的背景变化,亮色） 
'\\'(去除所有的变色效果) 

### clear_os()

```python
clear_os()
```

清除屏幕上的所有文字

# xes更改（去除xeslib里面所有的print）

最新版本的xingyunlib增加了xeslib的内容

## 导入方式

```python
from xingyunlib.xes import xeslib里面的库名
```

更改：

把xeslib里面所有的print都去了

修改AIspeak.speak函数

```python
from xingyunlib.xes import AIspeak
xes.AIspeak.speak("hello python!","file.mp3")
"""
本程序作用：
将hello python！
保存到file.mp3音频文件里面，并且不播放
"""
xes.AIspeak.speak("hello python!")
"""
本程序作用：
播放hello python！这段音频
"""
```

# xesapp（获取学而思站上某个作品的数据！已修复！）

开发者：严子昱|崔轩语

## 导入方式

```python
from xingyunlib.xesapp import*
```



### xesapp(url)

```python
<xesapp>=xesapp(url)
```

构建一个运行对象
url为学而思里面的py作品网址

接下来讲这个类的方法：


##### get_hot()<u></u>

返回作品的热度

```python
print(xesapp.get_hot())
```

##### get_cover()

返回作品封面的url

```python
print(xesapp.get_cover())
```

##### load_cover(filename)

下载作品封面到filename

```python
xesapp.load_cover("")
```

##### get_view()

返回作品的观看人数

```python
print(xesapp.get_view())
```

##### get_hot()

返回作品的热度

```python
print(xesapp.get_hot())
```

##### get_like()

返回作品的点赞数

```python
print(xesapp.get_like())
```

##### get_unlike()

返回作品的点踩数

```python
print(xesapp.get_unlike())
```

##### load_file(cache = "")

默认下载作品源文件到工作目录
如果cache不为空择下载到这个文件夹

```python
xesapp.load_file()
```

##### is_like()

判断在程序运行这个作品有没有人点赞
返回一个bool值
True：点赞了
False：点踩了
None：没有点赞也没有点踩

```python
if xesapp.is_like == True:
    print("点赞了")
elif xesapp.is_like == False:
    print("点踩了")
else:
    print("什么都没点")
```

##### run_app()

运行这个作品

```python
exec(xesapp.run_app())
```


##### get_published()

获取作品第一次保存时间

```python
print(xesapp.get_published())
```

##### get_modified()

获取作品最后一次更新时间

```python
print(xesapp.get_modified())
```

##### is_hidden_code()

获取作品是否隐藏代码

```python
if xesapp.is_hidden_code():
    print("作品的代码隐藏了")
else:
    print("作品的代码没有隐藏")
```

##### get_description()

获取作品的说明

```python
print(xesapp.get_description())
```

##### get_comments()

获取作品一共有多少人评论

```python
print(xesapp.get_comments())
```

##### is_comments()

获取从这个作品初始化到现在是否有人评论

```python
if xesapp.is_comments():
    print("评论了")
else:
    print("没有评论")
```
## cmt(url)

这个是一个获取评论的api

### dta_dic

```python
#获取一个包含所有评论的列表
a=cmt("http://code.xueersi.com/home/project/detail?lang=code&pid=9785566&version=offline&form=python&langType=python")
print(a.dta_dic)
#输出
"""
（略）
"""
```

### fmt（）

```python
#返回一个字符串（评论的字符格式化）
a=cmt("http://code.xueersi.com/home/project/detail?lang=code&pid=9785566&version=offline&form=python&langType=python")
print(a.fmt())
#部分输出
"""
[2020-10-17 20:52:11]
	一维回复严子昱:快点=-=不取关就pen你

[2020-10-17 20:51:31]
	一维回复严子昱:有时关注我这个人，并不是太好的选择
	取关我吧，有事请加qq：3456198711
	微信：huiyu431249891

[2020-10-17 18:34:35]
	俊翔回复严子昱:作者是喜欢互关吗？居然关注我这样的蚂蚁，太感动了

[2020-10-15 21:56:11]
	陈奕翰回复严子昱:考虑合作嘛
	

[2020-10-10 19:29:26]
	茜幻回复严子昱:作者在吗

[2020-10-10 19:10:42]
	蒋狄璁回复严子昱:互关

.......(略)
"""

```

### sorted（by=“likes”,reverse=True）

```python
#设置排序
a=cmt("http://code.xueersi.com/home/project/detail?lang=code&pid=9785566&version=offline&form=python&langType=python")
a.sorted(by="likes",reverse=True)#reverse为 从高到低排列
print(a.fmt())

"""
[2020-10-15 21:56:11]
	陈奕翰回复严子昱:考虑合作嘛
	

[2020-10-17 20:52:11]
	一维回复严子昱:快点=-=不取关就pen你

[2020-10-17 18:34:35]
	俊翔回复严子昱:作者是喜欢互关吗？居然关注我这样的蚂蚁，太感动了

[2020-10-01 20:51:57]
	王玎珰回复严子昱:啊这
...（略）
"""


```



# **xesuser（获取学而思站上某个用户的数据！已修复！）**

<u>***注意！！***</u>

<u>***千万一定不要超高频率请求，否则会报错！！！***</u>

作者：严子昱

## 导入方式

```python
from xingyunlib.xesuser import*
```



### get_user_id("作品网址")

```python
   user_id=get_user_id("作品网址")
   #本作品最重要的函数，这个获取作品网址的作者的user_id
```

### get__fans(user_id) 

```python
   fans_info=get_fans(user_id) 
   #这个user_id从上面拿
   #获取这个人粉丝的大部分信息，返回一个列表
   #每项是一个字典：
      fans_info[x]["realname"]#:获取第x项他的名字
      fans_info[x]["avatar_path"]#:获取第x项他头像的url
      fans_info[x]["fans"]#:获取第x项他的粉丝数量
      fans_info[x]["follows"]#:获取第x项他的关注数量
```

### get_follows(user_id) 

```python
   follows_info=get_follows(user_id) 
   #大体和get_fans一样
   #获取这个人粉丝的大部分信息，返回一个列表
   #每项是一个字典：
      follows_info[x]["realname"]#:获取第x项他的名字
      follows_info[x]["avatar_path"]#:获取第x项他头像的url
      follows_info[x]["fans"]#:获取第x项他的粉丝数量
      follows_info[x]["follows"]#:获取第x项他的关注数量
```

### get_info(user_id) 

```python
   user_info=get_info(user_id) 
   #获取这个人的大部分信息，返回一个字典
   user_info["name"]#:返回这个人的名字
   user_info["slogan"]#:返回这个人的口号(名字下面那段)
   user_info["fans"]#:返回这个人的粉丝数量
   user_info["follows"]#:返回这个人的关注数量
   user_info["icon"]#:返回这个人的头像url
```

### user(user_id)

```python
   user=user(user_id)#这个其实大部分都是前面的内容，不过前面的加载比较慢，这个适用需要数据比较多的程序
   user.works#：获取发布的作品总数
   #user.work_info#：获取发布的作品的信息，返回一个列表，列表的每项都是字典
   user.work_num#：获取一共有多少个作品（曾经发过的也算）

   user.fans#：获取粉丝总数
   #user.fans_info#：获取粉丝信息（和get_fans返回一样的信息）

   user.follows#：获取关注总数
   #user.follows_info#：获取关注信息（和get_follows返回一样的信息）
   user.like_num#：获取点赞总数
   user.view_num#：获取浏览总数
   user.favorites#：获取收藏总数
    
```

# xesapi

## 导入方式

```python
from xingyunlib.xesapi import* 
```

## get_api(url)

返回url这个api上的数据

示例->http://code.xueersi.com/api/index/works/modules

```python
print(get_api("http://code.xueersi.com/api/index/works/modules"))
"""
==输出==
{'stat': 1, 'status': 1, 'msg': '操作成功', 'data': [{'title': '可多推荐', 'simple_title': '推荐', 'lines': 2, 'projects': [{'id': 11584188, 'name': '圆圈战争', 'category': 1, 'type': 'normal', 'user_id': 9686613, 'thumbnail': 'https://rescode.xesimg.com/hufu-code/common/mit/32f6766530dc287c1c8ab00c634e352b.png', 'published': 1, 'published_at': '2020-11-18 19:42:53', 'modified_at': '2020-11-18 19:42:53', 'likes': 4, 'views': 333, 'comments': 0, 'version': '3.0', 'source': 'xes_live', 'deleted_at': None, 'original_id': 2, 'created_at': '2020-11-17 20:46:43', 'updated_at': '2020-11-20 21:25:02', 'weight': 1, 'adapter': '', 'hidden_code': 2, 'source_code_views': 3, 'removed': 0, 'first_frame': 'https://rescode.xesimg.com/hufu-code/common/mit/32f6766530dc287c1c8ab00c634e352b.png', 'unlikes': 5, 'project_id': 11584188, 'works_id': 11584188, 'lang': 'scratch', 'popular_score': 12.13, 'username': '冯嘉睿', 'user_avatar': 'https://oot.xesimg.com/user/h/cc1e41a2dc511b8108a05b8f0dc8cf69.jpg', 'project_type': 'scratch', 'topic_id': 'CS_11584188'}, {'id': 11027485, 'name': '井字棋小游戏(双人)', 'category': 1, 'type': 'normal', 'user_id': 7818569, 'thumbnail': 
...(略)
"""
```

## get_page(page,lang="",tag="",type="popular")

page：页码

lang：语言

tag：标签

type：爬取页面类型（默认为popular）

```python
print(get_page(1,"cpp"))
'''
==输出==
{'page': '1', 'per_page': '35', 'total': 7000, 'data': [{'id': 10443775, 'name': '教你如何黑电脑', 'category': 1, 'type': 'normal', 'user_id': 8730932, 'thumbnail': 'https://livefile.xesimg.com/programme/assets/b33adba6678f5e477f65d0f36d5581eb.jpg', 'la
...(略)
'''
```

## page_all_tags

这个是一个常量(就是上面那个tag可以取得量)

```python
print(page_all_tags)
"""
==输出==
{'all_tags': ['游戏', '动画', '故事', '模拟', '艺术', '教程', '算法', '海龟', '沙盒专区', '其他'], 'tips': '1、为什么要给作品打分类标签？n为你的作品选择分类，更有利于其他小朋友精准的找到你的作品，这样，你的作品被别人看到的机率会更大哦。n一定要准确的选择分类，不要随便选择不或者不选呦！nn2、如何为自己的作品选择分类？n要想准确的选择分类，首先要先知道每个分类代表什么意思，一起来了解一下吧！n游戏：射击，冒险，跑酷，换装等等这些都算作游戏。n动画：用编程实现动画效果的作品。n故事：用编程表达一个奇妙的故事，比如写小说。n模拟：视频软件模拟器，音乐软件模拟器，浏览器模拟器，甚至做个模拟的系统。n艺术：美术，音乐等等类型的作品都可以。n教程：如果你是大牛，就快做作品教别人和你一样优秀吧！n算法：算法是解决一个问题的方法，C++用户请看这里。n海龟：海龟画图是python语言中专门用户画图的方法呦！n沙盒专区：MC？mini？为什么不自己创作一个类似的作品呢？n其他：如果没想好自己作品的分类，就选这个吧。'}
"""
```

# pygame_extend（pygame扩展）

导入方式：

```python
from xingyunlib.pygame_extend import *
```

(这样顺便导入pygame和sys欸嘿嘿)

！没写完教程等需求多了在说把！

# tkinter_extend（tkinter扩展）

## 导入方式

```python
from xingyunlib.tkinter_extend import*
```

作者：严子昱

##   inpu_box

(class)

```python
#创建(就当button控件用)：
a=inpu_box(tk,函数名,**按钮的配置)

#打包：
a.pack(**pack的配置)

#配置：
a.config_entry(**文本框的配置)
a.config_button(**按钮的配置)
#其实你基本可以当做Entry来用，除了初始化语句还有配置以外基本都是一样的
#（剩下的教程还没写完）
```

## jitter()

作用：抖动窗口（需要在窗口加载完毕后使用，否则可能会出现鬼畜）

```python
from tkinter import *
root = Tk()
a = Text(root)
a.pack(fill=BOTH)

jitter(root)
root.mainloop()
```

## center()

作用：将窗口居中

```python
from tkinter import *
root = Tk()
a = Text(root)
a.pack(fill=BOTH)

jitter(root)
root.mainloop()
```

# dsfAdmin（自动安装第三方库）

开发者|严子昱

(暂时只支持windows)

## 导入方式

```python
from xingyunlib.dsfAdmin import*
```



### get_pakages()

作用：获取已安装每个包的版本

```python
for x in range(len(get_pakages())):
    print("库"+x[0].center(19," "),"版本"+x[1].center(10," "))
    
```

### find_pakages(pakages,ver=None)

作用：获取时否安装pakage这个库，ver代表版本，默认不进行版本监测

```python
if find_pakages("xingyunlib"):
    print("你有安装xingyunlib库！")
else:
    print("你没有安装xingyunlib库！")
```

### upgrade_pakages(pakage)

作用：更新pakage这个库

```python
upgrade_pakages(“xingyunlib”)
```

### install_pakages(pakage)

作用：安装这个库,常和find_pakages一起用

```python
if not find_pakages("alsolib"):
	install_pakages("alsolib")
#注意这个，这个非常重要的,可以在没安装第三方库的时候自动下载库
```

### dump_pip_list(filename)

作用：将库的list保存到这个文件里面

### load_pip_list(filename)

作用：将这个文件里面的库导出到正在使用的编译器

```python
dump_pip_list("pip_pakages")
#同目录会出现一个‘pip_pakages.pip’文件
# |把这个文件移到另一台电脑
# v
load_pip_list("pip_pakages")
#然后这个程序就会自动安装在第一台电脑上所有的第三方库了
```



# image（pillow及wordcloud扩展）

开发者|严子昱

## 导入方式

```python
from xingyunlib.image import*
```

## resize(filename,XY)

作用：将filename这个文件变成XY大的文件

```python
resive("img1.png",(100,100))
#将img1.png变成100x100的缩略图
```

## cloud(text,font_path,savafile=None,image=None,background_color="white",color=True)
（这个函数要安装numpy和wordcloud库）

作用：text为列表，font_path为字体文件的位置

savafile为保存的文件名，image为模板图片的名字

background_color为背景颜色 color为是否根据模板图片的颜色上色（在有模板的情况下）

```python
import os
text="ahuidgayugwuydgatywefuwfdytafayuofdwtyfauyfatyfautfatyfatyufduyoawfgtydfeutoaftyaf".split("a")
cloud(text,"(你的字体文件)","all.png")
os.startfile("all.png")
```

## add_text(img, text, **args)

这个**args包括以下内容

```python
font=（”字体文件.ttf”，字号）
XY=（x坐标，y坐标）#这个坐标以图片左上角为0，0（原点）
fillColor=颜色（建议使用16进制颜色）
show_img=True#设置是否在修改完成后显示图片，默认为False
change_img="newimgname.png"#设置输出的图片文件名
add_text("原图.png","广告",font=font,XY=XY,fillColor=fillColor,show_img=show_img,change_img=change_img)
```

# user（自定义用户类）

开发者|严子昱

## 导入方式

```python
from xingyunlib.user import *
```

初始化：

## user_login(filename=None)

filename:之前的保存数据的文件名，如果没有保存过请不要写filename

```python
user=user_login()
#导入之前的数据
user=user_login("<数据文件名称>")
```

注册：

#### user.registered(name,key,flag=True,filename=None)

name:注册的名字

key:密码

flag设置为True:如果已经导入数据则返回False(如果已经注册过了就不让你注册)否则返回True(注册成功）

flag设置为False：都可以注册

filename：保存数据文件的名称

```python
type=user.registered(input("请输入你的名字："),input("请输入你的密码："),flag=True,filename="data")
if type==True:
    print("注册成功！")
else:
    print("注册失败！")
```

#### user.login(name,key)

name:注册时的名称

key:密码

返回一个bool值，为True或False

True：验证密码正确 False：验证失败

```python
type=user.login(input("请输入你的名字："),input("请输入你的密码："))
if type==True:
    print("注册成功！")
else:
    print("注册失败！")
```

#### user.load(filename)

导入保存的数据，filename为文件名

```python
b=user_login()
b.load("你保存的文件名")
```

# mail

## 导入方式

```python
from xingyunlib import mail
```

用法：

## mail.send(to,title,txt)

```python
mail.send("3161399620@qq.com","hello python","hello world!")
```

to:发送给的邮箱

title:标题

txt:发送的文本

# err（自定义抛出错误）

## 导入方式

```python
from xingyunlib import err
```

当你有一些程序想在特定的情况终止怎么办？

试试下面的程序

## err(txt)

```python
from xingyunlib import err
a=input("请输入1：")
if a!="1":#如果非1
    err.err("你没有输入1。。。")
else:
    ...
    #程序自然退出
```

# http_spider（爬虫）

## 导入方式

```python
from xingyunlib import http_spider
```

## load_requests(str,between,line)

默认值：between=":" ; line="\n"

between：分隔符

line：换行符

这个概念有点难理解，具体看下面示例，能不能听懂由天命

```python
from xingyunlib import http_spider
header=http_spider.load_requests("""Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.116 Safari/537.36""",": ","\n")#那段字符串是从浏览器复制出来的
print(header)
"""
----------
输出：
{'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.116 Safari/537.36'}
"""

```

主要作用是自动分析从浏览器复制出来的headers

## spider(*args,**kwargs)

这个函数就明显很水，完全是凑数用的，不过对于一些新手来说还是有点用的

其实就是requests的变体，增加了一个判断是否状态码是否10x，40x，50x的功能而已

```python
from xingyunlib import http_spider
print(http_spider.spider("http://code.xueersi.com/api/compilers/6?id=6").text)
#略去输出结果
```

## ua_list

话不多说，上代码

```python
from xingyunlib import http_spider
print(http_spider.ua_list)
"""
输出：
['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)', 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)', 'Mozilla/5.0 (compatible; rv:1.9.1) Gecko/20090702 Firefox/3.5', 'Mozilla/5.0 (compatible; rv:1.9.2) Gecko/20100101 Firefox/3.6', 'Mozilla/5.0 (compatible; rv:2.0) Gecko/20110101 Firefox/4.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0.2) Gecko/20100101 Firefox/6.0.2', 'Mozilla/5.0 (compatible) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.682.0 Safari/534.21', 'Opera/9.80 (compatible; U) Presto/2.7.39 Version/11.00', 'Mozilla/5.0 (compatible; U) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1', 'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 ', 'Mozilla/5.0 (iPhone; U; CPU OS 4_2_1 like Mac OS X) AppleWebKit/532.9 (KHTML, like Gecko) Version/5.0.3 Mobile/8B5097d Safari/6531.22.7', 'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/4.0.2 Mobile/8C148 Safari/6533.18.5', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7) AppleWebKit/534.16+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4']
"""
```

这是一个列表，里面有很多笔者搜集的ua，（截至2020-9-19）收录了15个ua，足够你用了

## get_xes_url(url)

爬取一个xes的页面

```python
from xingyunlib import http_spider
print(http_spider.get_xes_url("http://code.xueersi.com/api/compilers/6?id=6"))
#略去输出结果
```

# data（保存数据）

数据类方法

2020-10-1

作者：严子昱

## 导入方式

```python
from xingyunlib import data
```

## Data

初始化方法：

```python
dta=data.Data(filename,find=False)
"""
filename:文件名，若没有则创建
find:搜索模式，若没有filename则报错
"""
```

输入数据：

### change_data(data)

```python
dta=data.Data(filename,find=False)
#略
"""
data参数支持的数据:
list,bool,tutle,str,set,dict,int,float
"""
dta.change_data("加油！")
```

### eval_data()

把从文件中保存的数据转换成可执行内容

```python
"""fruit.txt内容：
["apple","orange"]
"""
dta=data.Data("fruit.txt",find=False)
dta.eval_data()
for x in dta.data:
    print(f"fruit:{x}")
"""
输出结果：
fruit:apple
fruit:orange
"""


```

### save()

保存结果到文件中

```python
dta=data.Data("great",find=False)
dta.change_data(["hhc","hhv"])
dta.save()
"""great内容:
["hhc","hhv"]"""
```

