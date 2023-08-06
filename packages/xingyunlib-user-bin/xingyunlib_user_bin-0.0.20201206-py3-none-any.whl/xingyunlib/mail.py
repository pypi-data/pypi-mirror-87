import zmail
"""
content-type: 邮件内容的类型
subject: 邮件主题
to：收件人
from：寄件人
date: 年-月-日 时间 时区
boundary: 如果邮件为multiple parts，你可以得到其分界线
content: 邮件的文本内容（仅在text/plain时可以被解析）
contents: 邮件的body,里面包含着由分界线分割的每一个段落
attachments: None 或者 [['附件名称;编码方式','附件的二进制内容']...]
id: 在邮箱中的id
"""
# 你的邮件内容
def send(to,title,text):
	mail_content = {
		'subject': title,  # 随便填写
		'content_html': f"<pre>{text}</pre>", # Absolute path will be  # 随便填写
	}

	# 使用你的邮件账户名和密码登录服务器
	try:
		server = zmail.server('3450982589@qq.com', 'jdairgsskrhzcjbf')


		server.send_mail(to, mail_content)
	except:
		raise Exception("发太多次邮件啦！！！")
	# 发送邮件

# send("2292068915@qq.com","py发送","hhc")
