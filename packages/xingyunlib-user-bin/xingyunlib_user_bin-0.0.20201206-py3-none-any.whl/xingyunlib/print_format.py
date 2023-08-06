"""
   前景色            背景色            颜色
   --------------------------------------------
     30                40              黑色
     31                41              红色
     32                42              绿色
     33                43              黃色
     34                44              蓝色
     35                45              紫色
     36                46              青色
     37                47              白色
     90                100             亮黑
     91                101             亮红
     92                102             亮绿
     93                103             亮黃
     94                104             亮蓝
     95                105             亮紫
     96                106             亮青
     97                107             亮白
     
   显示方式         清除代码           意义
   --------------------------------------------
      0                --              终端默认设置
      4                24              使用下划线
      7                27              反白显示
      8                28              不可见
    
    
    光标设置 格式:\\033[数字+字母,数字、字母如下所示
    
    字母              数字             意义
   --------------------------------------------
     A                 x               光标上移x行
     B                 x               光标下移x行
     C                 x               光标左移x列
     D                 x               光标右移x列
     H                 y,x             光标设置为(x,y)(注意顺序)
     K                 无              清除从光标到行尾的内容
     s                 无              保存光标位置
     u                 无              回复光标位置
     l                 ?25             隐藏光标
     h                 ?25             显示光标
     J                 2               清屏(但不会恢复光标)
"""

#从这里复制(这个pygame和python都能用)
def replace(strname,*w):
    for x in w:
        strname=strname.replace(x[0],x[1])
    return strname

def print(*w,t=None,end="\n",sepr=" "):
    #严子昱出品，版本V4.1.0
    #V5.0.0没有改这里哈
    import sys
    import time
    str_all=""
    
    for x in w:
        
        if w.index(x)==len(w)-1:
            str_all+=str(x)
        else:
            str_all+=str(x)+sepr
    str_all=replace(str_all,("\\黑","\033[30m"),
                ("\\红","\033[31m"),
                ("\\绿","\033[32m"),
                ("\\黄","\033[33m"),
                ("\\蓝","\033[34m"),
                ("\\紫","\033[35m"),
                ("\\青","\033[36m"),
                ("\\白","\033[37m" ),
                ("\\l红", "\033[91m"),
                ("\\l绿", "\033[92m"),
                ("\\l黄", "\033[93m"),
                ("\\l蓝", "\033[94m"),
                ("\\l紫", "\033[95m"),
                ("\\l青", "\033[96m"),
                ("\\l白", "\033[97m"),
                ("\\bl红","\033[101m"),
                ("\\bl绿","\033[102m"),
                ("\\bl黄","\033[103m"),
                ("\\bl蓝","\033[104m"),
                ("\\bl紫","\033[105m"),
                ("\\bl青","\033[106m"),
                ("\\bl白","\033[107m"),
                ("\\bl黑","\033[100m"),
                ("\\b红", "\033[41m"),
                ("\\b绿", "\033[42m"),
                ("\\b黄", "\033[43m"),
                ("\\b蓝", "\033[44m"),
                ("\\b紫", "\033[45m"),
                ("\\b青", "\033[46m"),
                ("\\b白", "\033[47m"),
                ("\\b黑", "\033[40m"),
                ("\\","\033[0m"))
    if t==None:
        sys.stdout.write(str_all)
        sys.stdout.flush()
    else:
        for y in str_all:
            sys.stdout.write(y)
            sys.stdout.flush()
            #print(z,end="")
            time.sleep(t)
    sys.stdout.write(end)
def print_lines(*w,t=0.05,line_end="\n",sepr="",line_t=0.1):
    import sys
    import time
    for x in w:
        if w.index(x)==len(w)-1:
            print(str(x),t=t,end=line_end)
        else:
            print(str(x),t=t,end=line_end)
            sys.stdout.write(sepr)
            time.sleep(line_t)
#复制到这里
#
# #只有pygame能用的
# def show_img(url,prin="正在显示文件（没看见的去任务栏找）",inpu=" 看/运行 完点【ENTER】键："):
#     print(prin)
#     import os
#     os.system(url)
#     input(inpu)
#     #严子昱出品，版本V5.0.0

def clear_os():
    import sys
    sys.stdout.write("\033[2J\033[00H")
# print("nice")