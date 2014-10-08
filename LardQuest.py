""" Donovan Powers Term Project: Lard Quest, a Knights Tale
Player helath currently very high for debugging purposes

TODO:
cluster bomb
seeking bullets
add boss fight music


*Multiplyaer????!!!???

"""
import sys
import pygame
from pygame.locals import *
from random import *
import math

class Main(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((780, 600))
        pygame.display.set_caption("Lard Quest")
        #create sprite group for all player projectiles
        self.heroBulletsGroup = pygame.sprite.RenderPlain()
        self.powerUps = pygame.sprite.RenderPlain()
        self.mapVars = MapVars(self.heroBulletsGroup, self.powerUps)
        self.stage = Stage()
        self.arrow = pygame.image.load('arrow.png').convert_alpha()
        #make inital call to set up mapVars
        self.stage.update(self.mapVars)
        self.player = Portly()
        self.hearts = Hearts()
        self.stock = Stock()
        self.playThanks = True
        #draw background
        #self.screen.blit(self.stage.tile, (0,0))
        
        self.playerGroup = pygame.sprite.RenderPlain(self.player,
                                                     self.hearts,
                                                     self.stock)
        
        #load and play music on loop
        pygame.mixer.music.load('music.ogg')
        pygame.mixer.music.play(-1)
        #after calling all starting instances, start main loop
        self.main()

        
    def main(self):
        #Main Loop
        clock = pygame.time.Clock()
        #60 frames a second
        while 1:
            clock.tick(60)

            #while paused only display paused screen and look for unpause input
            if self.mapVars.paused == True:
                self.stage.paused()
                self.screen.blit(self.stage.tile, (0, 0))
                for event in pygame.event.get():
                     if (event.type == KEYDOWN) and event.key == K_p:
                            self.mapVars.paused = False
            #While unpaused run main loop
            #this code handles death
            elif self.stage.dead == True:
                self.stage.death()
                self.screen.blit(self.stage.tile, (0, 0))
                pygame.display.update()
                pygame.time.wait(5000)
                self.player.respawn(self.stage)

                
            elif self.stage.gameover == True:
                self.stage.gameOver()
                self.screen.blit(self.stage.tile, (0, 0))
                for event in pygame.event.get():
                    if (event.type == KEYDOWN) and event.key == K_RETURN:
                        self.__init__()


            elif self.mapVars.win == True:
                self.stage.youWin()
                self.screen.blit(self.stage.tile, (0, 0))
                if self.playThanks == True:
                    pygame.mixer.music.load('thanks.ogg')
                    pygame.mixer.music.play(1)
                    self.playThanks = False
                for event in pygame.event.get():
                    if (event.type == KEYDOWN) and event.key == K_RETURN:
                        self.__init__()
                
                
                

            #This code runs the main menu
            elif self.mapVars.paused == False and self.stage.mainScreen != None:
                for event in pygame.event.get():
                    if (event.type == KEYDOWN) and event.key == K_UP:
                        self.stage.mainScreen = "start"
                    elif event.type == KEYDOWN and event.key == K_DOWN:
                        self.stage.mainScreen = "instructions"
                    elif event.type == KEYDOWN and event.key == K_RETURN:
                        if self.stage.mainScreen == "instructions":
                            self.stage.mainScreen = "help"
                        elif self.stage.mainScreen == "help":
                            self.stage.mainScreen = "start"
                        elif self.stage.mainScreen == "start":
                            self.stage.tile = pygame.image.load('opening.png')
                            self.screen.blit(self.stage.tile, (0,0))
                            pygame.display.update()
                            pygame.display.flip()
                            pygame.time.wait(5000)
                            self.mapVars.stage = 0
                            self.stage.mainScreen = None
                #Draw Everything
                self.stage.update(self.mapVars)
                self.screen.blit(self.stage.tile, (0, 0))
                
                            
                    
                
            elif self.mapVars.paused == False and self.stage.mainScreen == None:
                #Handle Input Events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit ()
                    self.player.move(event)
                    if event.type == MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        bullet = HeroBullet(self.player, mouse)
                        self.heroBulletsGroup.add(bullet)
                    if (event.type == KEYDOWN) and event.key == K_p:
                        self.mapVars.paused = True
                            
                 #update everything
                self.player.update(self.mapVars,
                                   self.stage, self.hearts, self.stock,
                                   self.mapVars.enemyBullets, self.heroBulletsGroup,
                                   self.powerUps)
                self.heroBulletsGroup.update()
                self.mapVars.enemies.update(self.heroBulletsGroup, self.player,
                                            self.powerUps)
                self.mapVars.enemyBullets.update(self.player)
                self.stage.update(self.mapVars)
                self.powerUps.update(self.player, self.mapVars.enemies)
                #Draw Everything
                
                self.screen.blit(self.stage.tile, (0, 0))
                self.powerUps.draw(self.screen)
                #if level clear, flag player forward
                if self.mapVars.canAdvance == True:
                    self.screen.blit(self.arrow, (360, 20))
                self.playerGroup.draw(self.screen)
                self.heroBulletsGroup.draw(self.screen)
                self.mapVars.enemyBullets.draw(self.screen)
                self.mapVars.enemies.draw(self.screen)
            pygame.display.update()
            pygame.display.flip()


class MapVars(object):

    def __init__(self, heroBulletsGroup, powerups):
        #this class holds all semi global stage vars
        self.stage = -1
        self.wave = 0
        self.enemies = pygame.sprite.RenderPlain()
        self.enemyBullets = pygame.sprite.RenderPlain()
        self.newStage(heroBulletsGroup, powerups)
        self.canAdvance = False
        self.paused = False
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.win = False
        self.songpos = 0 #this variable stores where the background music left
        #off

    def stage0(self):
        #spawns waves of enemies
        #each time a wave is killed counter is advanced and next wave is spawned
        if self.wave == 0:
            enemy = BasicEnemy((50,100))
            enemy1 = BasicEnemy((200,100))
            enemy2 = BasicEnemy((250,100))
            enemy3 = BasicEnemy((400,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3)
        elif self.wave == 1:
            enemy = BasicEnemy((20,100))
            enemy1 = BasicEnemy((40,100))
            enemy2 = BasicEnemy((60,100))
            enemy3 = BasicEnemy((80,100))
            enemy4 = BasicEnemy((self.area.right - 20,100))
            enemy5 = BasicEnemy((self.area.right - 40,100))
            enemy6 = BasicEnemy((self.area.right - 60,100))
            enemy7 = BasicEnemy((self.area.right - 80,100))
            enemy8 = BasicEnemy((self.area.right/2,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3, enemy4, enemy5,
                             enemy6, enemy7, enemy8)
        elif self.wave == 2:
            enemy = BasicEnemy((20,100))
            enemy1 = BasicEnemy((40,100))
            enemy2 = BasicEnemy((60,100))
            enemy3 = BasicEnemy((80,100))
            enemy4 = BasicEnemy((self.area.right - 20,100))
            enemy5 = BasicEnemy((self.area.right - 40,100))
            enemy6 = BasicEnemy((self.area.right - 60,100))
            enemy7 = BasicEnemy((self.area.right - 80,100))
            enemy8 = BasicEnemy((self.area.right/2,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3, enemy4, enemy5,
                             enemy6, enemy7, enemy8)
        elif self.wave == 3:
            enemy = BasicEnemy((20,100))
            enemy1 = BasicEnemy((20,130))
            enemy2 = BasicEnemy((20,160))
            enemy3 = BasicEnemy((20,190))
            enemy4 = BasicEnemy((self.area.right - 20,100))
            enemy5 = BasicEnemy((self.area.right - 20,130))
            enemy6 = BasicEnemy((self.area.right - 20,160))
            enemy7 = BasicEnemy((self.area.right - 20,190))
            enemy8 = BasicEnemy((self.area.right - 20, 220))
            self.enemies.add(enemy, enemy1, enemy2, enemy3, enemy4, enemy5,
                             enemy6, enemy7, enemy8)
        elif self.wave == 4:
            enemy = BasicEnemy((20,100))
            enemy1 = BasicEnemy((40,100))
            enemy2 = BasicEnemy((60,100))
            enemy3 = BasicEnemy((80,100))
            enemy4 = BasicEnemy((self.area.right - 20,100))
            enemy5 = BasicEnemy((self.area.right - 40,100))
            enemy6 = BasicEnemy((self.area.right - 60,100))
            enemy7 = BasicEnemy((self.area.right - 80,100))
            enemy8 = BasicEnemy((self.area.right/2,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3, enemy4, enemy5,
                             enemy6, enemy7, enemy8)
        elif self.wave == 5:
            enemy = Ghost((80,100), self)
            enemy1 = Ghost((200,100), self)
            enemy2 = Ghost((320,100), self)
            enemy3 = Ghost((440,100), self)
            enemy4 = Ghost((self.area.right - 80,100), self)
            enemy5 = Ghost((self.area.right - 200,100), self)
            enemy6 = Ghost((self.area.right - 320,100), self)
            enemy7 = Ghost((self.area.right - 440,100), self)
            enemy8 = BasicEnemy((self.area.right/2,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3, enemy4, enemy5,
                             enemy6, enemy7, enemy8)
            #after all waves are clear it loads the next stage
        if self.wave >= 6:
            self.fanFare()
            self.canAdvance = True
            
    def stage1(self):
        if self.wave == 0:
            enemy = BasicEnemy((50,100))
            enemy1 = BasicEnemy((200,100))
            enemy2 = BasicEnemy((250,100))
            enemy3 = BasicEnemy((400,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3)
        elif self.wave == 1:
            enemy = MultiTurret((300,200), self)
            enemy4 = MultiTurret((600,200), self)
            enemy1 = BasicEnemy((200,400))
            enemy2 = BasicEnemy((100,200))
            enemy3 = BasicEnemy((200,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3, enemy4)
        elif self.wave >= 2:
            self.fanFare()
            self.canAdvance = True
            
    def stage2(self):
        if self.wave == 0:
            enemy = MultiTurret((self.area.right -200, self.area.bottom/2), self)
            enemy1 = MultiTurret((200, self.area.bottom/2), self)
            enemy2 = BasicEnemy((250,100))
            enemy3 = BasicEnemy((400,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3)
        elif self.wave == 1:
            enemy = Ghost((80,100), self)
            enemy1 = Ghost((200,100), self)
            enemy2 = Ghost((320,100), self)
            enemy3 = Ghost((440,100), self)
            enemy4 = Ghost((self.area.right - 80,100), self)
            enemy5 = Ghost((self.area.right - 200,100), self)
            enemy6 = Ghost((self.area.right - 320,100), self)
            enemy7 = Ghost((self.area.right - 440,100), self)
            enemy8 = BasicEnemy((self.area.right/2,100))
            enemy9 = BasicEnemy((20,100))
            enemy10 = BasicEnemy((40,100))
            enemy11 = BasicEnemy((60,100))
            enemy12 = BasicEnemy((80,100))
            enemy13 = BasicEnemy((self.area.right - 20,100))
            enemy14 = BasicEnemy((self.area.right - 40,100))
            enemy15 = BasicEnemy((self.area.right - 60,100))
            enemy16 = BasicEnemy((self.area.right - 80,100))
            enemy17 = BasicEnemy((self.area.right/2,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3, enemy4, enemy5,
                             enemy6, enemy7, enemy8, enemy9, enemy10, enemy11,
                             enemy12, enemy13, enemy14, enemy15, enemy16,
                             enemy17)
        elif self.wave == 2:
            enemy = SeekingTurret((80,100), self)
            enemy1 = SeekingTurret((200,100), self)
            enemy2 = SeekingTurret((320,100), self)
            enemy3 = SeekingTurret((440,100), self)
            enemy4 = SeekingTurret((self.area.right - 80,100), self)
            enemy5 = SeekingTurret((self.area.right - 200,100), self)
            enemy6 = SeekingTurret((self.area.right - 320,100), self)
            enemy7 = SeekingTurret((self.area.right - 440,100), self)
            enemy8 = BasicEnemy((self.area.right/2,100))
            enemy9 = BasicEnemy((20,100))
            enemy10 = BasicEnemy((40,100))
            enemy11 = BasicEnemy((60,100))
            enemy12 = BasicEnemy((80,100))
            enemy13 = BasicEnemy((self.area.right - 20,100))
            enemy14 = BasicEnemy((self.area.right - 40,100))
            enemy15 = BasicEnemy((self.area.right - 60,100))
            enemy16 = BasicEnemy((self.area.right - 80,100))
            enemy17 = BasicEnemy((self.area.right/2,100))
            enemy18 = BasicEnemy((20,100))
            enemy19 = BasicEnemy((40,100))
            enemy20 = BasicEnemy((60,100))
            enemy21 = BasicEnemy((80,100))
            enemy22 = BasicEnemy((self.area.right - 20,100))
            enemy23 = BasicEnemy((self.area.right - 40,100))
            enemy24 = BasicEnemy((self.area.right - 60,100))
            enemy25 = BasicEnemy((self.area.right - 80,100))
            enemy26 = BasicEnemy((self.area.right/2,100))
            self.enemies.add(enemy, enemy1, enemy2, enemy3, enemy4, enemy5,
                             enemy6, enemy7, enemy8, enemy9, enemy10, enemy11,
                             enemy12, enemy13, enemy14, enemy15, enemy16,
                             enemy17, enemy18, enemy19, enemy20, enemy21,
                             enemy22, enemy23, enemy24, enemy25, enemy26)
        elif self.wave >=3:
            self.fanFare()
            self.canAdvance = True
    def stage3(self):
        if self.wave == 0:
            enemy1 = MultiTurret((self.area.right-100,100), self)
            enemy2 = SeekingTurret((self.area.right/2,100), self)
            enemy3 = SeekingTurret((self.area.right/2,350), self)
            enemy4 = MultiTurret((150, 250), self)    
            self.enemies.add(enemy1, enemy2, enemy3, enemy4)
        elif self.wave >= 1:
            self.fanFare()
            self.canAdvance = True
        

    def stage4(self):
        if self.wave == 0:
            enemy = Archon((self.area.right/2, 100), self, 1)
            enemy1 = SeekingTurret((self.area.right-100,200),self)
            enemy2 = SeekingTurret((self.area.left+ 100,200), self)
            self.enemies.add(enemy, enemy1, enemy2)
        elif self.wave == 1:
            enemy = Archon((self.area.right/2, 100), self, 2)
            enemy1 = SeekingTurret((self.area.right-100,200),self)
            enemy2 = SeekingTurret((self.area.left+ 100,200), self)
            self.enemies.add(enemy, enemy1, enemy2)
        elif self.wave == 2:
            enemy = Archon((self.area.right/2, 100), self, 3)
            enemy1 = SeekingTurret((self.area.right-100,200),self)
            enemy2 = SeekingTurret((self.area.left+ 200,200), self)
            enemy3 = SeekingTurret((self.area.right-200,200),self)
            enemy4 = SeekingTurret((self.area.left+ 100,200), self)
            self.enemies.add(enemy, enemy1, enemy2, enemy3, enemy4)
        elif self.wave == 3:
            self.fanFare()
            self.canAdvance = True

    def fanFare(self):
        #stop music, play music to show level is over
        pygame.mixer.music.load('fanFare.ogg')
        pygame.mixer.music.play(1)

    def newStage(self, heroBulletsGroup, powerups):
        #given stage number calls a stage init that sets enemy spawns
        self.stage += 1
        pygame.mixer.music.load('music.ogg')
        pygame.mixer.music.play(-1)
        #remove all old bullets
        for bullet in heroBulletsGroup:
            bullet.kill()
        #remove all old powerups
        for powerup in powerups:
            powerup.kill()
        self.canAdvance = False
        self.wave = 0
        if self.stage == 0:
            self.stage0()
        if self.stage == 1:
            self.stage1()
        if self.stage == 2:
            self.stage2()
        if self.stage == 3:
            self.stage3()
        if self.stage == 4:
            self.stage4()
        

class Stage(pygame.sprite.Sprite):
    #this class swap out the image for each screen and its background,
    #creating the illusion that the player is moving
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.mainScreen = "start"
        self.gameover = False
        self.dead = False
        
    #Called by main if gameover
        #displayes gamve over screen
    def gameOver(self):
        self.tile = pygame.image.load('gameover.png').convert()
        


    #called by main if dead
        #displays dead screen for 3 seconds then respawns
    def death(self):
        self.tile = pygame.image.load('dead.png').convert()
        



        
    def update(self, mapVars):
        #based on stage number load correct background
        #on each stage, check if wave is over and spawn new waves
        #yeah I know its over 20 lines, but its really just data
        if self.mainScreen != None:
            self.callMainScreen()
        elif mapVars.stage == 0:
            self.tile = pygame.image.load('screen0.png').convert_alpha()
            if mapVars.wave == 0 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage0()
            elif mapVars.wave == 1 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage0()
            elif mapVars.wave == 2 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage0()
            elif mapVars.wave == 3 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage0()
            elif mapVars.wave == 4 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage0()
            elif mapVars.wave == 5 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage0()
        elif mapVars.stage == 1:
            self.tile = pygame.image.load('screen1.png').convert_alpha()
            if mapVars.wave == 0 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage1()
            elif mapVars.wave == 1 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage1()
        elif mapVars.stage == 2:
            self.tile = pygame.image.load('screen2.png').convert_alpha()
            if mapVars.wave == 0 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage2()
            elif mapVars.wave == 1 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage2()
            elif mapVars.wave == 2 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage2()
        elif mapVars.stage == 3:
            self.tile = pygame.image.load('screen3.png').convert_alpha()
            if mapVars.wave == 0 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage3()
            elif mapVars.wave == 1 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage3()
        elif mapVars.stage == 4:
            self.tile = pygame.image.load('screen4.png').convert_alpha()
            if mapVars.wave == 0 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage4()
            elif mapVars.wave == 1 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage4()
            elif mapVars.wave == 2 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage4()
            elif mapVars.wave == 3 and len(mapVars.enemies) == 0:
                mapVars.wave += 1
                mapVars.stage4()
        elif mapVars.stage == 5:
            mapVars.win = True

    def youWin(self):
        self.tile = pygame.image.load('youWin.png').convert()
            
            

    def callMainScreen(self):
        #load correct main screen depending on key input
        if self.mainScreen == "start":
            self.tile = pygame.image.load('main_start.png').convert()
        if self.mainScreen == "instructions":
            self.tile = pygame.image.load('main_instructions.png').convert()
        if self.mainScreen == "help":
            self.tile = pygame.image.load('main_help.png').convert()
        
        

    #when game is paused swtich to pause screen
    def paused(self):
        self.tile = pygame.image.load('pause.png').convert_alpha()

class Portly(pygame.sprite.Sprite):
    #this handles the main player, Portly
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.portly = pygame.image.load('portlyN.png').convert_alpha()
        self.image = pygame.image.load('portlyN.png').convert_alpha()
        #load knight sprite and get collision box
        self.rect = self.portly.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.pos = (self.area.right/2,
                    self.area.bottom - (self.rect.height/2))
        self.rect.center = self.pos
        self.up = self.down = self.left = self.right = False
        self.health = 100
        self.lives = 3
        self.direction = "N"
        
        
        
    def move(self, event):
        self.oldrect = self.rect
        keyReleased = False
        #for key press, moves in that direction until key released
        if event.type == KEYDOWN and event.key == K_UP:
            self.up = True
        elif event.type == KEYUP and event.key == K_UP:
            self.up = False
        elif event.type == KEYDOWN and event.key == K_DOWN:
            self.down = True
        elif event.type == KEYUP and event.key == K_DOWN:
            self.down = False
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            self.right = True
        elif event.type == KEYUP and event.key == K_RIGHT:
            self.right = False
        elif event.type == KEYDOWN and event.key == K_LEFT:
            self.left = True
        elif event.type == KEYUP and event.key == K_LEFT:
            self.left = False
            
    def update(self, mapVar, stage, hearts, stock, enemyBullets, heroBullets, powerups):
        self.posx = self.rect.center[0]
        self.posy = self.rect.center[1]
        self.oldrect = self.rect
        if self.up == True:
            self.rect = self.rect.move((0, -3))
        if self.down == True:
            self.rect = self.rect.move((0,+3))
        if self.right == True:
            self.rect = self.rect.move((3,0))
        if self.left == True:
            self.rect = self.rect.move((-3,0))
        if self.rect.top < self.area.top and mapVar.canAdvance == True:
            #If stage is cleared, when you walk to top of stage advance screen
            mapVar.newStage(heroBullets, powerups)
            self.rect.center = self.pos
        #Keep in bounds of screen 
        #get the direction the player is moving
        elif (self.rect.left < self.area.left or
           self.rect.right > self.area.right or self.rect.top < self.area.top
            or self.rect.bottom > self.area.bottom):
                self.rect = self.oldrect
        self.getDirection()
        self.updateLife(stage, hearts, stock, enemyBullets)
        self.changeDirection()

    def changeDirection(self):
        #animate sprite based on direction moving
        if self.direction == "N":
            self.image = pygame.image.load('portlyN.png').convert_alpha()
        elif self.direction == "NE":
            self.image = pygame.image.load('portlyNE.png').convert_alpha()
        elif self.direction == "NW":
            self.image = pygame.image.load('portlyNW.png').convert_alpha()
        elif self.direction == "W":
            self.image = pygame.image.load('portlyW.png').convert_alpha()
        elif self.direction == "E":
            self.image = pygame.image.load('portlyE.png').convert_alpha()
        elif self.direction == "S":
            self.image = pygame.image.load('portlyS.png').convert_alpha()
        elif self.direction == "SE":
            self.image = pygame.image.load('portlySE.png').convert_alpha()
        elif self.direction == "SW":
            self.image = pygame.image.load('portlySW.png').convert_alpha()

    def getDirection(self):
        #Based on key presses determine direction
        if self.up == True and self.left == True:
            self.direction = "NW"
        elif self.up == True and self.right == True:
            self.direction = "NE"
        elif self.up == True and (self.left == False and self.right == False):
            self.direction = "N"
        elif self.left == True and (self.down == False and self.up == False):
            self.direction = "W"
        elif self.right == True and (self.down == False and self.up == False):
            self.direction = "E"
        elif self.down == True and self.right == True:
            self.direction = "SE"
        elif self.down == True and self.left == True:
            self.direction = "SW"
        elif self.down == True and (self.left == False and self.right == False):
            self.direction = "S"

    def updateLife(self, stage, hearts, stock, enemyBullets):
        #if dead, display death and reduce life
        #if no lives left gameover
        # display correct number of lives and the health bar
        if self.health <= 0:
            for bullet in enemyBullets:
                bullet.kill()
            if self.lives <= 0:
                stage.gameover = True
                stage.gameOver()
            stage.dead = True
            stage.death()
        elif self.health > 80:
            hearts.image = pygame.image.load('5hearts.png').convert_alpha()
        elif self.health <= 80 and self.health > 60:
            hearts.image = pygame.image.load('4hearts.png').convert_alpha()
        elif self.health <= 60 and self.health > 40:
            hearts.image = pygame.image.load('3hearts.png').convert_alpha()
        elif self.health <= 40 and self.health > 20:
            hearts.image = pygame.image.load('2hearts.png').convert_alpha()
        elif self.health <= 20 and self.health > 0:
            hearts.image = pygame.image.load('1hearts.png').convert_alpha()
        if self.lives == 3:
            stock.image = pygame.image.load('3stock.png').convert_alpha()
        elif self.lives == 2:
            stock.image = pygame.image.load('2stock.png').convert_alpha()
        elif self.lives == 1:
            stock.image = pygame.image.load('1stock.png').convert_alpha()
        elif self.lives == 0:
            stock.image = pygame.image.load('0stock.png').convert_alpha()
            
            
            
    def respawn(self, stage):
        stage.dead = False
        self.portly = pygame.image.load('portlyN.png').convert_alpha()
        self.image = pygame.image.load('portlyN.png').convert_alpha()
        #load knight sprite and get collision box
        self.rect = self.portly.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.pos = (self.area.right/2,
                    self.area.bottom - (self.rect.height/2))
        self.rect.center = self.pos
        self.up = self.down = self.left = self.right = False
        self.health = 100
        self.lives -= 1

class Hearts(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.hearts = pygame.image.load('5hearts.png').convert_alpha()
        self.image = pygame.image.load('5hearts.png').convert_alpha()
        self.rect = self.hearts.get_rect()
        self.rect.center = (self.area.right/2,
                                       self.area.bottom - (self.rect.height/2))

class Stock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.stock = pygame.image.load('3stock.png').convert_alpha()
        self.image = pygame.image.load('3stock.png').convert_alpha()
        self.rect = self.stock.get_rect()
        self.rect.center = (self.area.right/4,
                                   self.area.bottom - (self.rect.height/2))
class EnemyBullet(pygame.sprite.Sprite):

    def __init__(self, direction, pos):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.bullet = pygame.image.load('blade.png').convert_alpha()
        self.image = pygame.image.load('blade.png').convert_alpha()
        #load bullet sprite and get collision box
        self.rect = self.bullet.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.direction = direction

    def update(self, player):
        self.rect = self.rect.move((self.direction))
        if (self.rect.right < self.area.left or
           self.rect.left > self.area.right or self.rect.bottom < self.area.top
            or self.rect.top > self.area.bottom):
            self.kill()
        #if hit player, remove and do damage
        elif self.rect.colliderect(player.rect):
            self.kill()
            player.health -= 20
        
    

class HeroBullet(pygame.sprite.Sprite):

    def __init__(self, player, mouse):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.bullet = pygame.image.load('blade.png').convert_alpha()
        self.image = pygame.image.load('blade.png').convert_alpha()
        #load bullet sprite and get collision box
        self.rect = self.bullet.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.pos = player.rect.center
        self.rect.center = self.pos
        self.speed = 7
        self.direction = (0,5)
        self.mousex = mouse[0]
        self.mousey = mouse [1]
        self.getVector(player)
        #self.getDirection(player)
        
    def getVector(self, player):
        #allows multidirection shooting, creating vector for shot
        xdiff = self.mousex - self.pos[0]
        ydiff = self.mousey - self.pos[1]
        self.angle = math.atan2(ydiff, xdiff)
        self.xVector = self.speed*math.cos(self.angle)
        self.yVector = self.speed*math.sin(self.angle)


##  This code used allow for 8 directional shooting, but is no longer needed
##  Keeping around incase I need this some where else
##    def getDirection(self, player):
##        direction = (0,-5)
##        if player.direction == "N":
##            direction = (0,-5)
##        elif player.direction == "NE":
##            direction = (5,-5)
##        elif player.direction == "NW":
##            direction = (-5,-5)
##        elif player.direction == "E":
##            direction = (5, 0)
##        elif player.direction == "W":
##            direction = (-5,0)
##        elif player.direction == "S":
##            direction = (0,5)
##        elif player.direction == "SE":
##            direction = (5,5)
##        elif player.direction == "SW":
##            direction = (-5, 5)
##        self.direction = direction

        
    def update(self):
        #Move bullet along vector from mouse to sprite
        self.rect = self.rect.move((self.xVector, self.yVector))
        if (self.rect.right < self.area.left or
           self.rect.left > self.area.right or self.rect.bottom < self.area.top
            or self.rect.top > self.area.bottom):
            self.kill()
        

            
        
class BasicEnemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.enemy = pygame.image.load('enemy.png').convert_alpha()
        self.image = pygame.image.load('enemy.png').convert_alpha()
        #load enemy sprite and get collision box
        self.rect = self.enemy.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.dirx = 0
        self.diry = 0
        #randomly determine if enemy is carrying a powerup
        self.willDropPickup = randint(0, 100)
        if self.willDropPickup <= 10: 
            self.willDropPickup = True

    def update(self, heroBullets, player, powerUps):
        #get position of self
        self.posx = self.rect.center[0]
        self.posy = self.rect.center[1]
        #set direction based on player
        if self.posx < player.posx:
            self.dirx = +1
        elif self.posx > player.posx:
            self.dirx = -1
        elif self.posx == player.posx:
            self.dirx = 0
        if self.posy < player.posy:
            self.diry = +1
        elif self.posy > player.posy:
            self.diry = -1
        elif self.posy == player.posy:
            self.diry = 0
        #Move the enemies
        self.rect = self.rect.move((self.dirx, self.diry))
        #at each move see if enemy is hit with bullet
        for bullet in heroBullets:
            if self.rect.colliderect(bullet.rect):
                #if enemy is holding powerup, create powerup
                if self.willDropPickup == True:
                    pickup = Powerup(self.rect.center)
                    powerUps.add(pickup)
                self.kill()
                bullet.kill()
        if self.rect.colliderect(player.rect):
            #if enemy is holding powerup, create powerup
            if self.willDropPickup == True:
                pickup = Powerup(self.rect.center)
                powerUps.add(pickup)
            self.kill()
            player.health -= 20

 
class Powerup(pygame.sprite.Sprite):

    
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.powerup = pygame.image.load('medkit.png').convert_alpha()
        self.image = pygame.image.load('medkit.png').convert_alpha()
        self.pos = position
        self.rect = self.powerup.get_rect()
        self.powerupList = ['medkit', 'bomb', 'medkit', 'medkit']
        self.getPowerup()
        #load enemy sprite and get collision box
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = self.pos

    def getPowerup(self):
        #randomly select a power up from power ups list
        self.powerup = choice(self.powerupList)
        if self.powerup == 'medkit':
            self.image = pygame.image.load('medkit.png')
        elif self.powerup == 'bomb':
            self.image = pygame.image.load('bomb.png')
        

    def update(self, player, enemies):
        #if powerup picked up, activate power
        if self.rect.colliderect(player.rect):
            if self.powerup == 'medkit':
                self.medkit(player)
                self.kill()
            elif self.powerup == 'bomb':
                self.bomb(enemies)
                self.kill()
        
    def medkit(self, player):
        #heal player 
        if player.health < 100:
            player.health += 20

    def bomb(self, enemies):
        #nuke all enemies
        for enemy in enemies:
            enemy.kill()
        

class Ghost(pygame.sprite.Sprite):
    
        def __init__(self, pos, mapVars):
            pygame.sprite.Sprite.__init__(self) #call Sprite intializer
            self.ghost = pygame.image.load('ghost.png').convert_alpha()
            self.image = pygame.image.load('ghost.png').convert_alpha()
            #load enemy sprite and get collision box
            self.rect = self.ghost.get_rect()
            screen = pygame.display.get_surface()
            self.area = screen.get_rect()
            self.mapVars = mapVars
            self.pos = pos
            self.countTillShot = 0
            self.rect.center = self.pos

        def update(self, heroBullets, player, powerups):
            self.countTillShot += 1
            if self.countTillShot % 70 == 0:
                bullet = EnemyBullet((0,5), self.pos)
                self.mapVars.enemyBullets.add(bullet)
            for bullet in heroBullets:
                if self.rect.colliderect(bullet.rect):
                    self.kill()
                    bullet.kill()
            if self.rect.colliderect(player.rect):
                self.kill()
                player.health -= 20
class MultiTurret(pygame.sprite.Sprite):
    #A stationary turret that rotates and shoot in 8 directions
    
    def __init__(self, pos, mapVars):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.turret = pygame.image.load('turret1.png').convert_alpha()
        self.image = pygame.image.load('turret1.png').convert_alpha()
        #load enemy sprite and get collision box
        self.rect = self.turret.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.mapVars = mapVars
        self.pos = pos
        self.countTillShot = 0
        self.rect.center = self.pos
        self.phase = 0
        self.health = 200

    def update(self, heroBullets, player, powerups):
        #at every shot rorate 45 degrees
        #after full rotation start at first point
        self.countTillShot += 1
        if self.countTillShot % 60 == 0:
            self.phase += 1
            if self.phase == 8:
                self.phase = 0
            if self.phase == 0:
                self.image = pygame.image.load('turret1.png').convert_alpha()
                bullet = EnemyBullet((0,5), self.pos)
                self.mapVars.enemyBullets.add(bullet)
            elif self.phase == 1:
                self.image = pygame.image.load('turret2.png').convert_alpha()
                bullet = EnemyBullet((5,5), self.pos)
                self.mapVars.enemyBullets.add(bullet)
            elif self.phase == 2:
                self.image = pygame.image.load('turret3.png').convert_alpha()
                bullet = EnemyBullet((5,0), self.pos)
                self.mapVars.enemyBullets.add(bullet)
            elif self.phase == 3:
                self.image = pygame.image.load('turret4.png').convert_alpha()
                bullet = EnemyBullet((5,-5), self.pos)
                self.mapVars.enemyBullets.add(bullet)
            elif self.phase == 4:
                self.image = pygame.image.load('turret5.png').convert_alpha()
                bullet = EnemyBullet((0,-5), self.pos)
                self.mapVars.enemyBullets.add(bullet)
            elif self.phase == 5:
                self.image = pygame.image.load('turret6.png').convert_alpha()
                bullet = EnemyBullet((-5,-5), self.pos)
                self.mapVars.enemyBullets.add(bullet)
            elif self.phase == 6:
                self.image = pygame.image.load('turret7.png').convert_alpha()
                bullet = EnemyBullet((-5,0), self.pos)
                self.mapVars.enemyBullets.add(bullet)
            elif self.phase == 7:
                self.image = pygame.image.load('turret8.png').convert_alpha()
                bullet = EnemyBullet((-5,5), self.pos)
                self.mapVars.enemyBullets.add(bullet)
        #add bullet to group and do colide detection
        for bullet in heroBullets:
            if self.rect.colliderect(bullet.rect):
                self.health -= 20
                bullet.kill()
            if self.health <= 0:
                self.kill()
        if self.rect.colliderect(player.rect):
            player.health -= 20
            self.kill()

class SeekingTurret(pygame.sprite.Sprite):
    #A stationary turret that shoots seeking bullets
    
    def __init__(self, pos, mapVars):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.turret = pygame.image.load('seeking.png').convert_alpha()
        self.image = pygame.image.load('seeking.png').convert_alpha()
        #load enemy sprite and get collision box
        self.rect = self.turret.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.mapVars = mapVars
        self.pos = pos
        self.countTillShot = 0
        self.rect.center = self.pos
        self.health = 100

    def update(self, heroBullets, player, powerups):
        self.countTillShot += 1
        if self.countTillShot % 60 == 0:
            bullet = SeekingBullet(self.pos, player)
            self.mapVars.enemyBullets.add(bullet)
        #add bullet to group and do colide detection
        for bullet in heroBullets:
            if self.rect.colliderect(bullet.rect):
                self.health -= 20
                bullet.kill()
            if self.health <= 0:
                self.kill()
        
class SeekingBullet(pygame.sprite.Sprite):
    #creates a bullet that shoots at the position the player was in when
    #the bullet spawned

    def __init__(self, startingPos, player):
        pygame.sprite.Sprite.__init__(self)
        self.bullet = pygame.image.load('blade.png').convert_alpha()
        self.image = pygame.image.load('blade.png').convert_alpha()
        #load bullet sprite and get collision box
        self.rect = self.bullet.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.pos = startingPos
        self.rect.center = self.pos
        self.speed = 5
        self.getVector(player)

    def update(self, player):
        self.rect = self.rect.move((self.xVector, self.yVector))
        if (self.rect.right < self.area.left or
           self.rect.left > self.area.right or self.rect.bottom < self.area.top
            or self.rect.top > self.area.bottom):
            self.kill()
        #if hit player, remove and do damage
        elif self.rect.colliderect(player.rect):
            self.kill()
            player.health -= 20

    def getVector(self, player):
        #allows multidirection shooting, creating vector for shot
        self.playerx,self.playery = player.rect.center[0], player.rect.center[1]
        xdiff = self.playerx - self.pos[0]
        ydiff = self.playery - self.pos[1]
        self.angle = math.atan2(ydiff, xdiff)
        self.xVector = self.speed*math.cos(self.angle)
        self.yVector = self.speed*math.sin(self.angle)
        
            
class Archon(pygame.sprite.Sprite):
    #First boss enemy
    def __init__(self, pos, mapVars, stage):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.archon = pygame.image.load('archon.png').convert_alpha()
        self.image = pygame.image.load('archon.png').convert_alpha()
        #load enemy sprite and get collision box
        self.rect = self.archon.get_rect()
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.mapVars = mapVars
        self.pos = pos
        self.countTillShot = 0
        self.rect.center = self.pos
        self.health = 700
        self.direction = (5,0)
        self.stage = stage
        


    def update(self, heroBullets, player, powerups):
        self.countTillShot += 1
        #moves left to right straffing
        if self.stage == 1:
            self.rect = self.rect.move((self.direction))
        #onces wounded move faster
        elif self.stage == 2:
            self.rect = self.rect.move((self.direction))
            self.rect = self.rect.move((self.direction))
        elif self.stage == 3 and self.countTillShot%50 == 0:
            self.oldrect = self.rect
            #Random movement across board to simulate teleporting
            randx = randint(50, self.area.right-50)
            randy = randint(50, self.area.right-50)
            self.rect.center = (randx, randy)
            #if it teleported on top of player dont move
            if self.rect.colliderect(player.rect):
                self.rect = self.oldrect
                
        if (self.rect.left < self.area.left):
            self.direction = (5,0)
        elif self.rect.right > self.area.right:
            self.direction = (-5,0)
        #once very wounded, teleport
        if self.countTillShot % 50 == 0:
            bullet = EnemyBullet((0,5), self.rect.center)
            bullet1 = EnemyBullet((5,0), self.rect.center)
            bullet2 = EnemyBullet((0,-5), self.rect.center)
            bullet3 = EnemyBullet((5,5), self.rect.center)
            bullet4 = EnemyBullet((-5,5), self.rect.center)
            bullet5 = EnemyBullet((5,-5), self.rect.center)
            bullet6 = EnemyBullet((-5,-5), self.rect.center)
            bullet7 = EnemyBullet((-5,0), self.rect.center)
            self.mapVars.enemyBullets.add(bullet, bullet1, bullet2, bullet3,
                                          bullet4, bullet5, bullet6, bullet7)
        for bullet in heroBullets:
            if self.rect.colliderect(bullet.rect):
                self.health -= 20
                bullet.kill()
        if self.rect.colliderect(player.rect):
            player.health -= 1
        if self.health <= 0:
            self.kill()



Main()
