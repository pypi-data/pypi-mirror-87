"""
开发者：严子昱|崔轩宇

v1.2.20201004

#v1.2.xx以后全是正式版#

#hack-20201004:修复xesuser故障

版权所有，侵权必究

内置函数 导入方式：

```python
from xingyunlib import *
```
### 加密函数s

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

"""
def help_xesapp():
	_ver = "2.2.0"
	_mit = "正式版"
	_logo = """
	\   / ┌──   ╭───
	 \ /　Ｅ──  │
	　Ｘ   └──  Ｓ──╮
	 / \  Ａ-Ｐ-Ｐ  │
	/   \       ───╯
	"""

	_pr = """Ver """ + _ver + """ :""" + _mit + """
	""" + _logo
	_help_str = """
		   <xesapp>
	 改-变-xes-作-品-格-局
	开发者：严子昱|崔轩语
	星光版权所有，转载请注明出处
	本库方法命名都是使用下划线命名法


	说明：
	    help()
	        获取帮助
	    help_english()
	        获取英文帮助
	    update()
	        查看更新
	    <xesapp>=xesapp(url)
	        构建一个运行对象
	        url为学而思里面的py作品网址
	    方法：
	    	|---2.0.0---|
		    <xesapp>.get_hot()
		        作用：返回作品的热度\n
		    <xesapp>.get_cover()
		    	作用：返回作品封面的url\n
		    <xesapp>.load_cover(filename)
		    	作用：下载作品封面到filename\n
		    <xesapp>.get_view()
		    	作用：返回作品的观看人数\n
		    <xesapp>.get_code()
		    	作用：返回作品的代码\n
		    <xesapp>.get_hot()
		    	作用：返回作品的热度\n
		    <xesapp>.get_like()
		    	作用：返回作品的点赞数\n
		    <xesapp>.get_unlike()
		    	作用：返回作品的点踩数\n
		    <xesapp>.load_file(cache = "")
		    	作用：默认下载作品源文件到工作目录
		    	如果cache不为空择下载到这个文件夹\n
		    <xesapp>.is_like()
		    	作用：判断在程序运行这个作品有没有人点赞
		    	返回一个bool值，为True，False或None
		    	True：点赞了
		    	False：点踩了
		    	None：没有点赞也没有点踩\n
		    exec(<xesapp>.run_app())
	            作用：运行这个作品(注意要exec里面的内容)
	        |----2.2.0---|
	        <xesapp>.get_published()
	        	作用：获取作品第一次保存时间\n
	        <xesapp>.get_modified()
	        	作用：获取作品最后一次更新时间\n
	        <xesapp>.is_hidden_code()
	        	作用：获取作品是否隐藏代码\n
	        <xesapp>.get_description()
	        	作用：获取作品的说明
			<xesapp>.get_comments()
				作用：获取作品一共有多少人评论
			<xesapp>.is_comments()
				作用：获取从<xesapp>初始化到现在是否有人评论

	---------end----------
	更多方法后续推进中，欢迎大家加入星光工作室
	副室长QQ：2292068915"""

	print(_pr)
	print(_help_str)
def help_xesuser():
	_help_str = """
	<xesuser>
	改-变-xes-作-品-格-局
	开发者：严子昱
	星光版权所有，转载请注明出处
	本库方法命名都是使用下划线命名法
	
	· user_id=get_user_id("作品网址")
		本作品最重要的函数，这个获取作品网址的作者的user_id
	
	· fans_info=get_fans(user_id) #这个user_id从上面拿
		获取这个人粉丝的大部分信息，返回一个列表
		每项是一个字典：
			fans_info[x]["realname"]:获取第x项他的名字
			fans_info[x]["avatar_path"]:获取第x项他头像的url
			fans_info[x]["fans"]:获取第x项他的粉丝数量
			fans_info[x]["follows"]:获取第x项他的关注数量
	
	· follows_info=get_follows(user_id) #大体和get_fans一样
		获取这个人粉丝的大部分信息，返回一个列表
		每项是一个字典：
			follows_info[x]["realname"]:获取第x项他的名字
			follows_info[x]["avatar_path"]:获取第x项他头像的url
			follows_info[x]["fans"]:获取第x项他的粉丝数量
			follows_info[x]["follows"]:获取第x项他的关注数量
	
	· follows_info=get_follows(user_id) #大体和get_fans一样
		获取这个人粉丝的大部分信息，返回一个列表
		每项是一个字典：
			follows_info[x]["realname"]:获取第x项他的名字
			follows_info[x]["avatar_path"]:获取第x项他头像的url
			follows_info[x]["fans"]:获取第x项他的粉丝数量
			follows_info[x]["follows"]:获取第x项他的关注数量
	
	· user_info=get_info(user_id) 
		获取这个人的大部分信息，返回一个字典
		user_info["name"]:返回这个人的名字
		user_info["slogan"]:返回这个人的口号(名字下面那段)
		user_info["fans"]:返回这个人的粉丝数量
		user_info["follows"]:返回这个人的关注数量
		user_info["icon"]:返回这个人的头像url
	
	· <user>=user(user_id)#这个其实大部分都是前面的内容，不过前面的加载比较慢，这个适用需要数据比较多的程序
		<user>.works：获取发布的作品总数
		<user>.work_info：获取发布的作品的信息，返回一个列表，列表的每项都是字典
		<user>.work_num：获取一共有多少个作品（曾经发过的也算）
		
		<user>.fans：获取粉丝总数
		<user>.fans_info：获取粉丝信息（和get_fans返回一样的信息）
		
		<user>.follows：获取关注总数
		<user>.follows_info：获取关注信息（和get_follows返回一样的信息）
		
		<user>.like_num：获取点赞总数
		<user>.view_num：获取浏览总数
		<user>.favorites：获取收藏总数
		
	"""

	print(_help_str)
def help_tkinter_extend():
	print("""
inpu_box：
	创建(就当button控件用)：
	a=inpu_box(tk,函数名,**按钮的配置)
	
	打包：
	a.pack(**pack的配置)
	
	配置：
	a.config_entry(**文本框的配置)
	a.config_button(**按钮的配置)
	其实你基本可以当做Entry来用，除了初始化语句还有配置以外基本都是一样的

""")







