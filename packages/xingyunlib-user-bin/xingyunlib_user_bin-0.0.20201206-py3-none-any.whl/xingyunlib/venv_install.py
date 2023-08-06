import os
def cre():
	a=input("文件夹名称:")
	global filename, global_filename
	filename=a
	global_filename=os.getcwd()+"\\"+a
	with open("venv.txt","w") as f:
		f.write(f"{filename}|{global_filename}|{filename}"+"\\scripts\\python.exe ")
	cmd="python -m venv "+global_filename
	os.system(cmd)
	...
def cre_cmd():
	txt="""import os
with open("venv.txt","r") as f:
	filename,global_filename,py=f.read().split("|")
os.system(filename+r"\\scripts\\activate")
while True:
	
	cmd=input(f"{global_filename}:\\nvenv{{{filename}}}>python ")
	if cmd=="exit":
		import sys;sys.exit()
	cmd=py+cmd
	try:
		os.system(cmd)
	except:
		pass
	
	"""
	with open("cmd.py","w") as f:
		f.write(txt)
def setup():
	cre()
	cre_cmd()
if __name__ == '__main__':
    setup()
