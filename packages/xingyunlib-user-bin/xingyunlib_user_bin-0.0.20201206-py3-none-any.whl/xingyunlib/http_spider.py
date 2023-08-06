def load_requests(str,between=":",line="\n"):
	rc={}
	for x in str.split(line):
		if x=="":
			continue
		y=x.split(between)
		if len(y)==1:
			continue
		elif len(y)!=2:
			y[1]="".join(y[1:])
		rc[y[0]]=y[1]
	return rc
ua_txt="""IE6.0:Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
IE7.0:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)
IE8.0:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)
IE9.0:Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)
Firefox3.5:Mozilla/5.0 (compatible; rv:1.9.1) Gecko/20090702 Firefox/3.5
Firefox3.6:Mozilla/5.0 (compatible; rv:1.9.2) Gecko/20100101 Firefox/3.6
Firefox4.0:Mozilla/5.0 (compatible; rv:2.0) Gecko/20110101 Firefox/4.0
Firefox6.0:Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0.2) Gecko/20100101 Firefox/6.0.2
Chrome11.0:Mozilla/5.0 (compatible) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.682.0 Safari/534.21
Opera11.0:Opera/9.80 (compatible; U) Presto/2.7.39 Version/11.00
Maxthon3.0:Mozilla/5.0 (compatible; U) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1
Android:Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 
iPhone:Mozilla/5.0 (iPhone; U; CPU OS 4_2_1 like Mac OS X) AppleWebKit/532.9 (KHTML, like Gecko) Version/5.0.3 Mobile/8B5097d Safari/6531.22.7
iPad:Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/4.0.2 Mobile/8C148 Safari/6533.18.5
Safari5.0:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7) AppleWebKit/534.16+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36
aa:Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
aa:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586
aa:Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
aa:Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)
aa:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)
aa:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER 
aa:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7
User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;AvantBrowser)
User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)
User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50
User-Agent:Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50
User-Agent:Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;
User-Agent:Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)
User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)
User-Agent:Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)
User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1
User-Agent:Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1
User-Agent:Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11
User-Agent:Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11
User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11
User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)
User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)
User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)"""

ua_list=[]
for _x in ua_txt.split("\n"):
	ua_list.append(":".join(_x.split(":")[1:]))
ua_list=list(set(ua_list))
def get_xes_url(url):
	import json,requests
	headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",'Content-Type': 'application/json'}
	c=requests.get(url,headers=headers)
	b = str(c.status_code)
	if b[:2] not in ["20","30"]:
		import xingyunlib.err
		xingyunlib.err.err("爬取失败！")
	else:
		return json.loads(c.text)
def spider(*args,**kwargs):
	import requests
	a=requests.get(*args,**kwargs)
	b=str(a.status_code)
	if b[:2] not in ["20","30"]:
		import xingyunlib.err
		xingyunlib.err.err(f"爬取错误，状态码：{b}")
		return
	return a

