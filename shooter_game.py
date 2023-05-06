#Создай собственный Шутер!
from random import *
from pygame import *
win_height = 500
win_width = 700
window = display.set_mode((win_width,win_height))
display.set_caption("Стрелялки")
galaxy  = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
finish = False
game = True
font.init()
font2 = font.Font(None,36)
score = 0
stop = 3
goal = 10


    
class GameSprite(sprite.Sprite):
    def __init__(self,images,x,y,sizex,sizey,speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(images),(sizex,sizey))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def recet(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<win_width-80:
            self.rect.x+=self.speed
    def fire(self):
        pyla = Puly("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
        pgrops.add(pyla)
lost = 0
class enemy(GameSprite):
    def update(self):
        self.rect.y+= self.speed
        global lost 
        if self.rect.y>win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost+=1

class Puly(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

pgrops = sprite.Group()

ship = player("rocket.png",5,win_height-100,80,100,10)
monsters = sprite.Group()
for i in range (1,9):
    vrag = enemy("ufo.png",randint(80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(vrag)

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if not finish:
        window.blit(galaxy,(0,0))

        text = font2.render("Счет:" + str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропущено:" + str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        

        
        ship.update()
        ship.recet()
        monsters.update()
        monsters.draw(window)
        pgrops.update()
        pgrops.draw(window)
        collide = sprite.groupcollide(monsters,pgrops,True,True)
        for c in collide:
            score +=1
            monstr =enemy("ufo.png",randint(80,win_width-80),-40,80,50,randint(1,5)) 
            monsters.add(monstr)
        if sprite.spritecollide(ship,monsters,False) or lost>= stop:
            finish = True
        if score >= goal:
            finish = True
      
    else:
        finish = False
        score = 0
        lost = 0
        for b in pgrops:
            b.kill()
        for m in monsters:
            m.kill()


        time.delay(3000)
        for i in range(1, 6):
            monstr =enemy("ufo.png",randint(80,win_width-80),-40,80,50,randint(1,5)) 
            monsters.add(monstr)

    display.update()
    time.delay(60)

