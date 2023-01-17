# $ Student Number : 121409592
# $ Name: Jakc Feighery

# My High Score : 665

import sys, pygame
from random import randint
from pygame.locals import *
from pygame import mixer 

class SpaceInvaders:
    '''
    Space Invaders Game Class 
        - init - sets up variables before game is ran
        - rungame - while True game is being run
    '''
    def __init__(self):
        ''' nitialising variables for Space Invader Class '''
        # init pygame
        pygame.init()       
        pygame.font.init()
        self._clock = pygame.time.Clock()
        self._my_font = pygame.font.SysFont('arial', 17)    # font for score 
        self._end_font = pygame.font.SysFont('arial', 30)
        # init screen
        self._size = self._width, self._height = 520, 740   # dimensions for screen window 
        self._bg = Background('BG.png', [0,0])   # making of bagkround class with file location and where the image starts 
        self._screen = pygame.display.set_mode((self._size)) 
        # init player
        self._playermodel = PlayerState(self._width/2 - 30, self._height - 60, self._width, 5, "spaceship.png")     ## player model , x, y start at bottom of screen and half way accross, iamge file aswell
        # init bullets
        self._bulletmodel = BulletState(15, 15, 0, 1000, 5 ,"bullet.png")
        self._enemybulletmodel = BulletState(15, 15, 0, 1000, -5 ,"bullet.png")
        #init enemies 
        self._enemiemodel = EnemyState(30, 30 , -2,"invader_1.png")   
        # init score 
        self._score = 0 # score starts at 0
        # sounds 
        self._shoot_sound = mixer.Sound("shoot.wav")
        self._enemy_shoot_sound = mixer.Sound("enemyshoot.wav")
        self._collision_sound = mixer.Sound("explosion.wav")

    def rungame(self):
        ''' While True , Space Invader Game is being run '''
          #background music 
        mixer.music.load("bg_music.mp3")
        mixer.music.play(-1, fade_ms=2000)
        while True:
            # pygame time 
            self._clock.tick(60)
            self._current_time = pygame.time.get_ticks()

            for event in pygame.event.get():            
                if event.type == pygame.QUIT: 
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:     # if left is presses or held
                self._playermodel.handleMoveLeft()  # handle left movement 
            if keys[pygame.K_RIGHT]:       # if right is presses or held 
                self._playermodel.handleMoveRight() # handle right movement 
            if keys[pygame.K_SPACE] and self._current_time >= self._bulletmodel._next_bullet_time :       # if player presses or holds SPACE and it has been 1 second since last shot fired 
                self._bulletmodel._next_bullet_time = self._current_time + self._bulletmodel._bullet_delay
                self._bulletmodel._bulletlist.append([self._playermodel.getXPos() + 10, self._playermodel.getYPos() - 50])   # append bullet with x and y relative to current position of player
                self._shoot_sound.play(fade_ms=200)
                # add enemiw bullet
                randenemie = randint(0, len(self._enemiemodel._enemylist) - 5)      # a random enemie in current list
                chance = randint(1,3)   # random cahnce 
                if chance == 2:
                    self._enemybulletmodel._bulletlist.append([self._enemiemodel._enemylist[randenemie][0] + 15, self._enemiemodel._enemylist[randenemie][1] + 40])     # add to bullet enmie model list
                    self._enemy_shoot_sound.play()  # sound
            # TEXT 
            self._text_surface = self._my_font.render('Score : ' + str(self._score), True, (223, 255, 0))   # creating surface 
            # screen backround - first before bullets, player, enemies and text ; layering
            self._screen.fill([230,230,250])    # if image dosen't load backup colour will be a purple 
            self._screen.blit(self._bg._image, self._bg._rect)  # fill screen with BG image
            # BULLETS
            self._bulletmodel.drawbullets(self._screen) # passing this instance of screen to draw to. Drawing and Deleting silmintaneously
            self._enemybulletmodel.drawbullets(self._screen) # passing this instance of screen to draw to. Drawing and Deleting silmintaneously

            # ENEMIES
            self._enemiemodel.drawenemies(self._screen, self._current_time) # passing this instance of screen to draw to. Drawing and Deleting silmintaneously

            # COLLISIONS 
            # collision check (Player bullets - enemies) and score if collision
            if self._bulletmodel.collision1(self._enemiemodel._enemylist):
                self._collision_sound.play()
                self._score += 5
            # collision check (Enemie Bullets - player) end if collision
            if self._enemybulletmodel.collision2(self._playermodel):
                self._collision_sound.play()
                SpaceInvaders.endgame(self)
            # collision between (Player and Enemie) end if collision
            if self._playermodel.enemycollision(self._enemiemodel._enemylist):
                SpaceInvaders.endgame(self)

            #Fills and blits
            self._screen.blit(self._playermodel._playerview, (self._playermodel.getXPos(), self._playermodel.getYPos())) # blit player 
            self._screen.blit(self._text_surface, (12,3))  # blit text score 
            pygame.display.set_caption("Space Invaders - Jack Feighery")    # caption for pygame Window 

            # flip/update
            pygame.display.flip()


    def endgame(self):
        ''' when git by bullet or Invader Game ends displaying score  '''
        mixer.music.stop()
        while True:
            for event in pygame.event.get():            
                    if event.type == pygame.QUIT: 
                        sys.exit()
            self._screen.fill([230,230,250])    # if image dosen't load backup colour will be a purple 
            self._screen.blit(self._bg._image, self._bg._rect)  # fill screen with BG image
            self._text_surface_end = self._end_font.render('GAME OVER !                 Score : ' + str(self._score), True, (223, 255, 0))   # creating surface 
            self._screen.blit(self._text_surface_end, (50,50))
        
            pygame.display.flip()


class PlayerState:
    ''' Class to Represent current state of Player '''
    def __init__(self, xpos, ypos, maxxpos, change, imagefile):
        self._xPos = xpos
        self._yPos = ypos
        self._maxXPos = maxxpos
        self._playerchange = change
        self._playerview = pygame.image.load(imagefile)     # space ship player image load

    def getXPos(self):
        '''returns current X coordinate of Player'''
        return self._xPos
    
    def getYPos(self):
        '''returns current Y coordinate of Player'''
        return self._yPos
    
    def handleMoveLeft(self):
        '''Changes X cooridiante of player Left in relatuion to player change speed '''
        if self._xPos + self._playerchange  > 5 :
            self._xPos -= self._playerchange
    def handleMoveRight(self):
        '''Changes X cooridiante of player Right in relatuion to player change speed '''
        if self._xPos - self._playerchange < self._maxXPos - 65:
            self._xPos += self._playerchange

    def enemycollision(self, enemylist):
        ''' collision detection between enmie and player '''
        for e in enemylist: 
            if self.getYPos() > e[1] and self.getYPos() < e[1] + 30:
                if (self.getXPos() > e[0]) and (self.getXPos() < e[0] + 30) or (self.getXPos() + 60 > e[0]) and (self.getXPos() + 60 < e[0] + 30):
                    return True


class Background(pygame.sprite.Sprite):     # BAckground as I wanted an image of stars not just a solid colour
    ''' Class for Sprite Background '''
    def __init__(self, imagefile, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self._image = pygame.image.load(imagefile)
        self._rect = self._image.get_rect()
        self._rect.left , self._rect.top = location

        
class BulletState(pygame.sprite.Sprite):
    '''' Class for State of Bullets '''
    def __init__(self, width, height, next_bullet_time, bullet_delay, bulletspeed, imagefile ):
        self._width = width
        self._height = height
        self._size = width, height
        self._bulletlist = []
        self._bulletspeed = bulletspeed
        self._next_bullet_time = next_bullet_time
        self._bullet_delay = bullet_delay
        self._bulletview = pygame.image.load(imagefile)  # laod bullet image for bullet

    def drawbullets(self, screen):
        ''' Drawring bullets to given screen, they go vertivally up screen, are delted if they reach top of screen '''
        for b in self._bulletlist:
            screen.blit(self._bulletview, ( *b, self._height, self._width))     # draw bullet with bullet iamge, and bullet rect               
            b[1] -= self._bulletspeed    # make bullet go up screen 5 pixels 

        for b in self._bulletlist[:]:   # checking lsit while iterating 
            if b[1] < 0:        # if y == 0 delete
                self._bulletlist.remove(b)

    def collision1(self, enemielist):
        ''' collision detection between Player bullets and current enemies  '''
        for b in self._bulletlist:
            for e in enemielist: 
                if b[1] > e[1] and b[1] < e[1] + 30:
                    if (b[0] > e[0]) and (b[0] < e[0] + 30) or (b[0] + 30 > e[0]) and (b[0] + 30 < e[0] + 30):
                        enemielist.remove(e)
                        self._bulletlist.remove(b)
                        return True
                    
    def collision2(self, player):
        ''' collision detection between enemy bullets and player '''
        for b in self._bulletlist:
                if b[1] > player.getYPos() and b[1] < player.getYPos() + 60:
                    if (b[0] > player.getXPos()) and (b[0] < player.getXPos() + 60) or (b[0] + 60 > player.getXPos()) and (b[0] + 30 < player.getXPos() + 60):
                        self._bulletlist.remove(b)
                        return True
                        
                        

class EnemyState(pygame.sprite.Sprite):
    '''Class for State of Enemiers'''
    def __init__(self, width, height , speed, imagefile):
        self._widht = width
        self._height = height
        self._size = width, height
        self._enemylist = []
        self._enemyspeed = speed
        self._enemyview = pygame.image.load(imagefile)
        self._movedelay = 1500      # enemies move every second adn half 1500
        self._nextmovetime = 3000   # 3 seconds before enemies commence movemenent 
        self._directionchagne = 1   # direction dosetn chage at start, -1 to change 
        # initalise starting enemies 32 for my game 
        self._x , self._y, self._x1, self._y1= 20,20,0,0   
        for _ in range(48): # 48 enemies to start with 
            if _ % 12 == 0 and _ != 0:      # check if its time for a new row 
                self._x1 = 0    # reset the x coord 
                self._y1 += 35  # add anotother row
            self._enemylist.append([self._x + self._x1, self._y + self._y1])    # add to enemylist x adn y coord + difference from starting enemie 
            self._x1 += 40
            
    
    def drawenemies(self, screen, currenttime):
        ''' Drawing enemies to given screen, they go left when hitting screen they go down height they right.... repeat '''
        for e in self._enemylist:    
            screen.blit(self._enemyview, ( *e, self._height, self._widht))

        if currenttime >= self._nextmovetime:   # if delay has passed move all enemies to the right or left 
            self._nextmovetime = currenttime + self._movedelay  # creating next movetime 
            for e in self._enemylist[:]:        # for each enemie 
                e[0] += self._enemyspeed * self._directionchagne # change x coord by enemy speed and ranint for little variation

        for e in self._enemylist[:]:        # to check if they have hit walls 
            if e[0] <= 5:   #  if near left windiw wall 
                EnemyState.moveenemiesdown(self, "left")    # call to move down fucntion with parameter "left"
            if e[0] >= 485: # if near right window wall 
                EnemyState.moveenemiesdown(self, "right")   # call to move down fucntion with parameter "right"

        
    def moveenemiesdown(self, wall):
        ''' To move all enemies down the height of one enemie if they have hit they walls  '''
        for e in self._enemylist:
            e[1] += 30  # go down height of an enime
            if wall == "left":
                self._directionchagne = -1
                e[0] += 4
            if wall == "right":
                self._directionchagne = 1
                e[0] -= 4
        EnemyState.increaseSpeed(self)
        EnemyState.addenemies(self)  

    def increaseSpeed(self):
        ''' Increase speed of enemies '''
        self._movedelay = self._movedelay*0.9
    
    def addenemies(self):
        self._x , self._y, self._x1, self._y1 = 20,10,0,0
        for _ in range(12): # add 12 enemies 
            self._enemylist.append([self._x + self._x1, self._y + self._y1])    # add to enemylist x adn y coord + difference from starting enemie 
            self._x1 += 40

       

if __name__ == "__main__":
    mygame = SpaceInvaders()
    mygame.rungame()


