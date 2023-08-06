# 输入文本框(带按钮，按enter也可以运行)
"""
创建(就当button控件用)：
a=inpu_box(tk,函数名,**按钮的配置)

打包：
a.pack(**pack的配置)

配置：
a.config_entry(**文本框的配置)
a.config_button(**按钮的配置)
其实你基本可以当做Entry来用，除了初始化语句还有配置以外基本都是一样的
"""
import tkinter as tk

class inpt_box:
	def __init__(self, *w, command, **arg):
		import tkinter as tk
		self.Frame = tk.Frame(*w)
		self.cmd = command
		self.Entry = tk.Entry(self.Frame, bd=3)
		self.Button = tk.Button(self.Frame, command=self.cmd, **arg)

	def config_entry(self, **arg):
		self.Entry.configure(**arg)

	def config_button(self, **arg):
		self.button.configure(**arg)

	def get(self):
		return self.Entry.get()

	def insert(self, *w):
		self.Entry.insert(*w)

	def delete(self, *w):
		self.Entry.delete(*w)

	def _kao(self, *event):
		self.cmd()

	def pack(self, **arg):
		self.Entry.pack(fill="x", side="left", expand=True)
		self.Button.pack(fill="x", side="left")
		self.Entry.bind("<Return>", self._kao)
		self.Frame.pack(**arg)


# --end--

# 覆盖tk的Text控件
from tkinter.scrolledtext import ScrolledText as Text


# --end---
class Imgbutton:
	def __init__(self, root, width=100, img="", text="", command="", **arg):
		import tkinter as tk
		import PIL.Image
		import PIL.ImageTk
		self.img = PIL.ImageTk.PhotoImage(
			PIL.Image.open(img).resize(
				(width, width),
				PIL.Image.ANTIALIAS
			)
		)
		self.command = command
		self.Frame = tk.Frame(root)
		self.Label = tk.Label(self.Frame, text=text, image=self.img, compound="top", **arg)
		self.Label.bind("<Button-1>", self.command)
		self.Label.pack(fill="both", expand=True)

	# def command(self,*event):
	#     self.com()
	def configure(self, **arg):
		self.Label.configure(**arg)

	def pack(self, *K):
		self.Frame.pack(*K)

class ListBX:
	def __init__(self,root,*w,**arg):
		import tkinter as tk
		self.Frame = tk.Frame(root)
		# self.cmd = command
		self.get = tk.Scrollbar(self.Frame)
		self.ListBox = tk.ListBox(self.Frame, *w,yscrollcommand=self.get.set,**arg)
		self.get.config(command=self.ListBox.yview)
		self.ListBox.pack(side=tk.LEFT, fill=tk.BOTH,expand=True)
		self.get.pack(side=tk.RIGHT,fill=tk.X)
	def config(self,**kwargs):
		self.ListBox.config(**kwargs)
	def run(self,text:"str"):
		exec("self.ListBox."+text)
	def pack(self,*w,**kwargs):
		self.Frame.pack(*w,**kwargs)
class Show_text(tk.Text):
	def __init__(self,*w,**kwargs):
		super().__init__(*w,**kwargs)
		self.configure(exportselection=0,state=tk.DISABLED,relief=tk.RAISED)
	def finsert(self,*w,**kwargs):
		self.configure(exportselection=0, state=tk.NORMAL)
		self.insert(*w,**kwargs)
		self.configure(exportselection=0, state=tk.DISABLED)



def center(root):
	# root=tk.Tk()
	root.update()

	sw = root.winfo_screenwidth()

	sh = root.winfo_screenheight()

	ww = root.winfo_width()

	wh = root.winfo_height()

	x = (sw - ww) / 2

	y = (sh - wh) / 2

	root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

def jitter(root,times=3):
	# root = tk.Tk()
	import time


	root.update()
	root.focus_get()
	root.attributes('-topmost', True)
	time.sleep(0.1)
	ww = root.winfo_width()
	wh = root.winfo_height()
	wx = root.winfo_x()
	wy = root.winfo_x()
	for x in range(times):
		for y in (1, 2, 3, 4):
			root.update()
			if y == 1: wx += 10
			if y == 2: wy += 10
			if y == 3: wx -= 10
			if y == 4: wy -= 10
			root.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
			time.sleep(0.05)
	root.attributes('-topmost', False)
	return True
