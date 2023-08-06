# import cv2
from random import  random
from os import startfile
from xingyunlib.code import md5
cache=[]

def send_name():return md5(md5(__name__)+str(random()))

def show_cv(image):
	z = send_name() + ".png"
	cv2.imwrite(z,image)
	startfile(z)
	cache.append(z)

def show_html(echats):
	z = send_name() + ".html"
	echats.render(z)
	startfile(z)
	cache.append(z)
def show_plt(plt):
	z = send_name() + ".png"
	plt.savefig(z)
	startfile(z)
	cache.append(z)



