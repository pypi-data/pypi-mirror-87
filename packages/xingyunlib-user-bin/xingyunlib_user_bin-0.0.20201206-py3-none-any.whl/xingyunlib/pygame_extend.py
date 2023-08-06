import pygame,sys

def print_text(font,text,x,y,color=(255,255,255),target=None):
    imgText =font.render(text, True, color)
    if target == None:
        target = pygame.display.get_surface()
    target.blit(imgText, (x,y))

def icon(name,x,y,screen=None):
    if x>y:
        c=(x-y)//2
        aaa=0
        kfd=y
    elif y>x:
        aaa=(y-x)//2
        c=0
        kfd=x
    else:
        aaa=0
        c=0
        kfd=x
    if screen==None:
        screen=pygame.display.get_surface()
    a=pygame.image.load(name)
    a=pygame.transform.smoothscale(a, (kfd, kfd))
    k=0
    flag=True
    while flag:
        k+=1
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                flag=False
        screen.blit(a,(c,aaa))
        pygame.display.update()

class Mouse:
    def __init__(self,size,apple,type_do="rect",up_color=(255,255,255),down_color=(0,255,0)):
        self.down_color=down_color
        self.up_color=up_color
        self.size=size
        self.rect=pygame.Rect(0,0,size,size)
        self.type=type_do
        self.apple=apple
    def update(self,screen):
        self.rect.centerx,self.rect.centery=pygame.mouse.get_pos()
        down=pygame.mouse.get_pressed()[0]
        if self.type=="rect":
            if down:
                pygame.draw.rect(screen,self.down_color,self.rect,self.apple+2)
            else:
                pygame.draw.rect(screen,self.up_color,self.rect,self.apple)
        else:
            if down:
                pygame.draw.ellipse(screen,self.down_color,self.rect,self.apple+2)
            else:

                pygame.draw.ellipse(screen,self.up_color,self.rect,self.apple)
    def get_rect(self):
        self.rect.center=pygame.mouse.get_pos()
        return self.rect

class Sound:
    #初始化
    def __init__(self,file,cha=True):
        self.sound=pygame.mixer.Sound(file)
        self.channal=pygame.mixer.find_channel(cha)
    #播放
    def play(self):
        self.channal.play(self.sound)
    #停止
    def stop(self):
        self.sound.stop()

class Point(object):
    #初始化
    def __init__(self,x,y):
        self._x=x
        self._y=y
    #x
    def get_x(self):
        return self._x
    def set_x(self,x):
        self._x=x
    #y
    def get_y(self):
        return self._y
    def set_y(self,y):
        self._y=y
    #检测碰撞
    def colliderect(self,rect):
        return rect.collidepoint(self._x,self._y)
    # 放回值
    def __str__(self):
        return "{x:{:.0f}".format(self._x)+",y:{:.0f}".format(self._y)+"}"


