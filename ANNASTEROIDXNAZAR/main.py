from pygame import *
from random import *

mixer.pre_init(44100, -16, 1, 512)
w, h = 700, 500

window = display.set_mode((w, h))
display.set_caption("Asteroids")

#class Enemy(GameSprite):
#
#    def update(self):
#        self.rect.y += self.speed
#        global lost
#        global hearts
#
#        if self.rect.y > h:
#            
#            hearts.pop(0)
#            self.rect.y = 0
#            self.rect.x = randint(0, w-50)
#            lost = lost + 1









game = True
finish = False
clock = time.Clock()
score = 0
background = transform.scale(image.load("love.jpg"), (w, h))
class GameSprite(sprite.Sprite):
    def __init__(self, pImage, pX, pY, sizeX, sizeY, pSpeed):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = pX
        self.rect.y = pY
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.image, (self.rect.x, self.rect.y))
bullets = sprite.Group()
class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if  keys[K_a]:
            self.rect.x -= self.speed

        if  keys[K_d]:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("heart.png", self.rect.centerx, self.rect.top, 15, 30, 15 )
        bullets.add(bullet)


ship = Player("Nazar5.png", 10, h-100, 100, 95, 4)

lost = 0
class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        global hearts

        if self.rect.y > h:
            
            hearts.pop(0)
            self.rect.y = 0
            self.rect.x = randint(0, w-50)
            lost = lost + 1

asteroids = sprite.Group()


for i in range(2):
    pics = ["Anna2.png", "Anna3.png"]
    asteroid = Enemy(choice(pics), randint(0, w-50), -40, 50, 50, randint(1, 5))
    asteroids.add(asteroid)



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
            


mixer.init()
mixer.music.load("Aga.mp3")
mixer.music.play()

fire_sound = mixer.Sound("Chmok.ogg")
fire_sound.set_volume(0.1)

font.init()

mainfont = font.Font(None, 40)

from time import time as timer
reload_time = False
num_fire = 0

i = 0

hearts = []
lives = 10
hX = 300
for i in range(lives):
    heart = GameSprite("love.png", hX, 10, 40, 37, 0)
    hearts.append(heart)
    hX += 40

restart = GameSprite("restart_nophone.png", 225, 100, 260, 240, 0 )

start = GameSprite("start (1).png", 180, 120, 350, 240, 0)

game_text = mainfont.render("Любовні пригоди ", True, (117, 41, 80))

exit = GameSprite("exit.png", 5, 5, 60, 60, 0)
finish = True

while game:
    
    for e in event.get():        
        if e.type == QUIT:
            game = False
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and reload_time == False:

                    ship.fire()
                    fire_sound.play()
                    num_fire += 1

                if num_fire >= 5 and reload_time == False:
                    reload_time = True
                    reload_start = timer()
                    

            if e.key == K_r:
                for a in asteroids:
                    a.rect.y = 190
                    a.rect.x = randint(0, w-100)
                finish, score, lost = 0, 0, 0
                lives = 10
                hX = 300
                for i in range(lives):
                    heart = GameSprite("love.png", hX, 10, 40, 37, 0)
                    hearts.append(heart)
                    hX += 40

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = e.pos
                if restart.rect.collidepoint(x,y) and finish:
                    for a in asteroids:
                        a.rect.y = -100
                        a.rect.x = randint(0, w-100)
                    finish, score, lost = 0, 0, 0
                    hearts = []
                    lives = 10
                    hx = 300
                    for i in range(lives):
                        heart = GameSprite("love.png", hX, 10, 40, 37, 0)
                        hearts.append(heart)
                        hX += 40
                if start.rect.collidepoint(x,y):

                    finish = False
           
                if exit.rect.collidepoint(x,y):
                    game = False

                    hX = 300
                    num_fire = 0
                    Reload_time = False



    if finish:
        window.blit(background, (0, 0))
        start.draw()
        exit.draw()
        window.blit(game_text, (230, 100))
         

    if not finish:
        window.blit(background, (0,0))
        for heart in hearts:
            heart.draw()
        score_text = mainfont.render("Killed: "+str(score), True, (117, 41, 80))
        lost_text = mainfont.render("Missed: "+str(lost), True, (117, 41, 80))
        window.blit(score_text, (5, 10))
        window.blit(lost_text, (5, 50))       
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)


        if reload_time:
            reload_end = timer()
            if reload_end - reload_start < 3:
                        reload = mainfont.render("Realoding", True, (117, 41, 80))
                        window.blit(reload, (5, 85))   
 
            else:
                num_fire = 0
                reload_time = False  
        if sprite.spritecollide(ship, asteroids, False):
            try:
                hearts.pop(0)
            except:
                pass
            
        collides = sprite.groupcollide(bullets, asteroids, True, True)
        for c in collides:
            score += 1
            pics = ["Anna2.png", "Anna3.png"]
            asteroids.add(Enemy("Anna2.png", randint(0, w-50), -40, 50, 50, randint (1, 2)))
            asteroid = Enemy(choice(pics), randint(0, w-50), -40, 50, 50, randint(1, 2))
            asteroids.add(asteroid)

        if len(hearts) <= 0:
            
            lose_text = mainfont.render("YOU LOSE", True, (117, 41, 80))
            
            window.blit(lose_text, (270, 200))
            finish = True
        
        
    

            
           


        ship.draw()
        ship.update()
    display.update()
    clock.tick(75)   