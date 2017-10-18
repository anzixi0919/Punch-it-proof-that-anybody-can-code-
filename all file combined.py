import os
import sys
import pygame as pg
import random 
import math
import copy
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

# CMU 15-112 term project 'Punch It'
# Tom An(zixia)
# 9:51pm 12/6/2016
'''
Finally, after countless hours of hard work, procrastination and countless mini-panic attacks and breakdowns, here we are,
making the very finishing touches on a project that is exclusively mine for the first time. how do i feel? excited? fulfilled? 
ecsatic beyond control? or empty? perhaps all and perhaps none. thank god i am not being graded on how well i compose this passage,
if so, i'd be in serious trouble. anyway, why would i write a pretext like this? perhaps a celebration of an accomplishment. in the
past three and a half weeks, i have dedicated more than 70 hours of my time into crafting every little detail, fixing every little bug,
and thinking of innovative ways to solve the problems presented as i went along. I also learnt to take it one step at a time. I still 
remember how i pictured my project would go at the beginning: i'm gonna do it in 3-D, i'm gonna include so many features that people will
pay for it, i'm going to write up a predictive algorithm so complex that the one function itself would be a MVP....obviously, i cannot possibily
complete all of them, hence the rather frequent panic attacks and mini depressions at the early stages. but, as time goes on, i prioritized, compartmentalized
and sacrificed unnecessary features. from this, i truly learnt some thing. despite how the grade goes, i am improved.

'''
class KinectControl(object):
    '''
    The following code in this class uses the
    PyKinectV2 module developed by microsoft 
    and uses various methods and existing code 
    from the PyKinect module
    '''
    
    def __init__(self,joints):
        self.joints=joints
        self.LShoulder=self.reference3=self.joints[PyKinectV2.JointType_ShoulderLeft]
        self.RShoulder=self.reference4=self.joints[PyKinectV2.JointType_ShoulderRight]
        self.LElbow=self.joints[PyKinectV2.JointType_ElbowLeft]
        self.RElbow=self.joints[PyKinectV2.JointType_ElbowRight]
        self.LHip=self.reference1=self.joints[PyKinectV2.JointType_HipLeft]
        self.RHip=self.reference2=self.joints[PyKinectV2.JointType_HipRight] 
        self.LKnee=self.joints[PyKinectV2.JointType_KneeLeft]
        self.RKnee=self.joints[PyKinectV2.JointType_KneeRight] 
        self.LHand=self.joints[PyKinectV2.JointType_HandLeft]
        self.RHand=self.joints[PyKinectV2.JointType_HandRight]
        self.LWrist=self.joints[PyKinectV2.JointType_WristLeft]
        self.RWrist=self.joints[PyKinectV2.JointType_WristRight]
        self.LHT=self.joints[PyKinectV2.JointType_HandTipLeft]
        self.RHT=self.joints[PyKinectV2.JointType_HandTipRight] 
        self.LAnkle=self.joints[PyKinectV2.JointType_AnkleLeft]
        self.RAnkle=self.joints[PyKinectV2.JointType_AnkleRight]
        self.boolCommand={'FistClose':False,'FaceRight':True,
                 'Jump':False,'Move':False}
    
    def updateJoints(self):
        self.LShoulder=self.joints[PyKinectV2.JointType_ShoulderLeft]
        self.RShoulder=self.joints[PyKinectV2.JointType_ShoulderRight]
        self.LElbow=self.joints[PyKinectV2.JointType_ElbowLeft]
        self.RElbow=self.joints[PyKinectV2.JointType_ElbowRight]
        self.LHip=self.joints[PyKinectV2.JointType_HipLeft]
        self.RHip=self.joints[PyKinectV2.JointType_HipRight] 
        self.LKnee=self.joints[PyKinectV2.JointType_KneeLeft]
        self.RKnee=self.joints[PyKinectV2.JointType_KneeRight] 
        self.LHand=self.joints[PyKinectV2.JointType_HandLeft]
        self.RHand=self.joints[PyKinectV2.JointType_HandRight]
        self.LWrist=self.joints[PyKinectV2.JointType_WristLeft]
        self.RWrist=self.joints[PyKinectV2.JointType_WristRight]
        self.LHT=self.joints[PyKinectV2.JointType_HandTipLeft]
        self.RHT=self.joints[PyKinectV2.JointType_HandTipRight] 
        self.LAnkle=self.joints[PyKinectV2.JointType_AnkleLeft]
        self.RAnkle=self.joints[PyKinectV2.JointType_AnkleRight]
    
    def checkFistClose(self):
        x1=self.LHand.Position.x
        x2=self.LHT.Position.x
        y1=self.LHand.Position.y
        y2=self.LHT.Position.y
        z1=self.LHand.Position.z
        z2=self.LHT.Position.z
        if abs(x1-x2)<=0.05 and abs(y1-y2)<=0.05 and abs(z1-z2)<=0.05:
            return True
        return False
    
    def getAngle(self,joint1,joint2):
        x1,y1=joint1.Position.x,joint1.Position.y
        x2,y2=joint2.Position.x,joint2.Position.y
        if y2>y1:
            if x2>x1:
                try: return 180+math.atan((x2-x1)/(y1-y2))*360/(2*math.pi)
                except: return 0
            else:
                try: return -180+math.atan((x2-x1)/(y1-y2))*360/(2*math.pi)
                except: return 0
        else:
            try: return math.atan((x2-x1)/(y1-y2))*360/(2*math.pi)
            except: return 0


    def getLHandPosition(self):
        x=self.LHand.Position.x
        y=self.LHand.Position.y
        return (x,y)

    
    def getRHandPosition(self):
        x=self.RHand.Position.x
        y=self.RHand.Position.y
        return (x,y)

    def getLElbowAngle(self):
        angle=self.getAngle(self.LElbow,self.LWrist)
        return angle//1 

    def getRElbowAngle(self):
        angle=self.getAngle(self.RElbow,self.RWrist)
        return angle//1

    def getLKneeAngle(self):
        angle=self.getAngle(self.LKnee,self.LAnkle)
        return angle//1

    def getRKneeAngle(self):
        angle=self.getAngle(self.RKnee,self.RAnkle)
        return angle//1

    def getLShoulderAngle(self):
        angle=self.getAngle(self.LShoulder,self.LElbow)
        return angle//1

    def getRShoulderAngle(self):
        angle=self.getAngle(self.RShoulder,self.RElbow)
        return angle//1

    def getLHipAngle(self):
        angle=self.getAngle(self.LHip,self.LKnee)
        return angle//1

    def getRHipAngle(self):
        angle=self.getAngle(self.RHip,self.RKnee)
        return angle//1

    def jointsAngle(self):
        return [self.getRShoulderAngle(),self.getRElbowAngle(),
                self.getLShoulderAngle(),self.getLElbowAngle(),
                self.getRHipAngle(),self.getRKneeAngle(),
                self.getLHipAngle(),self.getLKneeAngle()]


    def BodyFacingRight(self):
        zl=self.LShoulder.Position.z
        zr=self.RShoulder.Position.z
        return zr>=zl 
    
    def checkJump(self):
        RShoulderY=self.RShoulder.Position.y
        LHipY=self.LHip.Position.y
        return ((LHipY-self.reference1.Position.y)+(RShoulderY-self.reference4.Position.y))>=0.25
    
    def getWeapon(self):
        x1,x2=self.LWrist.Position.x,self.RWrist.Position.x
        y1,y2=self.LWrist.Position.y,self.RWrist.Position.y
        z1,z2=self.LWrist.Position.z,self.RWrist.Position.z 
        return abs(x1-x2+y1-y2+z1-z2)<=0.05

    def move(self):
        dist1=self.LHip.Position.y-self.LKnee.Position.y
        dist2=self.RHip.Position.y-self.RKnee.Position.y
        dist3=self.LShoulder.Position.y-self.LHand.Position.y
        dist4=self.RShoulder.Position.y-self.RHand.Position.y
        if (dist1<=0.25 and dist4<=0.35) or (dist2<=0.25 and dist3<=0.35):
            return True
        else:
            return False
    
    #def updateKeys(self):

 

#test function for kinect class
def kinectDemo():
    kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body)
    while True:
        if kinect.has_new_body_frame():
            #print(1)
            bodies=kinect.get_last_body_frame()

            if bodies is not None:
                #print(2)
                for i in range(0,kinect.max_body_count):
                    body=bodies.bodies[i]
                    if not body.is_tracked:
                        continue 
                    joints=body.joints

                    control=KinectControl(joints)
                   
                    print(control.getLShoulderAngle())
                    #print(control.checkFistClose())
                    #print(control.move())
                    #print(control.checkJump())




"""
all pygame module methods and techniques are learnt with the help of 
the official pygame documentation at http://www.pygame.org/docs/ 

"""
#minimal physics simulation for all falling sprites
class Physics(object):
    def __init__(self):
        self.vx=self.vy=0
        self.grav=0.9
        self.fall=False 
        
    def physicsUpdate(self):
        if self.fall:
            self.vy+=self.grav
        #else:
         #   self.vy=0

#basic framework, skeleton and drawing schemes for the enemy and player subclasses
class Human(pg.sprite.Sprite):
    HEROIMG=pg.image.load('breastplate.png')
    #retrieved from http://opengameart.org/sites/default/files/breastplate.png
    ENEMYIMG=pg.image.load('shirt.png') 
    #retrieved from http://opengameart.org/sites/default/files/shirt_1.png


    #part of this class is inspired from moving_platforms.py from 
    #https://github.com/Mekire/pygame-samples/blob/master/platforming/moving_platforms.py
    #by Mekire to accomodate my game


    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.cloth=Human.HEROIMG if isinstance(self,Player) else Human.ENEMYIMG
        self.cloth=pg.transform.scale(self.cloth,(30,45))
        self.type='person'
        self.thighlength=0.194
        self.calflength=0.194
        self.uarmlength=0.186
        self.larmlength=0.146
        self.handlength=0.07
        self.hipwidth=0.19
        self.shoulderwidth=0.22
        self.lowerhip=0.055
        self.upperhip=0.055
        self.torsolength=0.233
        self.hipwidth=0.14
        self.speed=8
        self.jumpPower=-20
        self.health=150
        self.isDying=False
        self.isAlive=True
        self.obstacleDown=False
        self.onMoving=False
        self.dieSplash=False
        self.walls=None
        self.fireTime=0
        self.dieTime=0
        self.conversion=2*math.pi/360
        self.jointsAngle=[0,0,0,0,0,0,0,0]
        self.LHandPos=(0,0)
        self.RHandPos=(0,0)
        self.LFootPos=(0,0)
        self.RFootPos=(0,0)
        self.LFist=Projectile(self.LHandPos)
        self.RFist=Projectile(self.RHandPos)
        self.LFoot=Projectile(self.LFootPos)
        self.RFoot=Projectile(self.RFootPos)
        self.Fists=pg.sprite.Group([self.LFist,self.RFist,self.LFoot,self.RFoot])

    def checkCollision(self,offset,obstacles):#modified from moving_platform example(refer to the beginning of class)
        self.rect.move_ip(offset[0],offset[1])
        collide=pg.sprite.spritecollideany(self,obstacles)
        self.rect.move_ip(-offset[0],-offset[1])
        return collide 

    def updatePos(self,obstacles):
        self.checkFall()
        if self.vy!=0:
            self.move((0,self.vy),1,obstacles)
        if self.vx!=0: 
            self.move((self.vx,0),0,obstacles)
        
    def checkFall(self):
        if not self.obstacleDown:
            self.fall=True
        else: 
            self.fall=False

    #pre-update for better accuracy
    def update0(self,obstacles):
        obstacles=obstacles.copy()
        obstacles.remove(self)
        self.obstacleDown=self.obstacleBelow(obstacles)

    def obstacleBelow(self,obstacles):
        self.rect.move_ip((0,1))
        collide=pg.sprite.spritecollide(self,obstacles,False)
        self.rect.move_ip((0,-1))
        return collide 
    
    def checkOnMoving(self,obstacles):#modified from moving_platform example(refer to the beginning of class)
        if not self.fall:
            nowMoving=self.onMoving
            anyMoving,anyNonMoving=[],[]
            for collide in self.obstacleDown:
                if collide.type=='Moving':
                    self.onMoving=collide
                    anyMoving.append(collide)
                else:
                    anyNonMoving.append(collide)
                if anyMoving==[]:
                    self.onMoving=False
                elif anyNonMoving in anymoving or nowMoving in anyMoving:
                    self.onMoving=nowMoving
               
    def move(self,offset,index,obstacles):
        self.rect.move_ip(offset[0],offset[1])
        while pg.sprite.spritecollideany(self,obstacles):
            self.rect[index]+=(1 if offset[index]<0 else -1)
        
    def jump(self):
        if not self.fall: #and not self.checkCollision((0,-1),obstacles):
            self.vy=self.jumpPower
            self.fall=True

    #changes joints angles for animation
    def changePos(self,idealAngles,speed):
        counter=0
        for i in range(8):
            
            if abs(self.jointsAngle[i]-idealAngles[i])<=6: counter+=1
            elif (self.jointsAngle[i]-idealAngles[i])>5: self.jointsAngle[i]-=speed
            else: self.jointsAngle[i]+=speed
        return counter==8

    #if health is below 0, this function starts dying animation
    def checkDying(self):
        #dieAngles=[-self.orientation*i for i in [90,90,90,90,90,90,90,90]]
        if self.isDying:
            time=pg.time.get_ticks()
            if self.dieSplash==False:
                blocks=[BodyBlocks((a+self.rect.x,b+self.rect.y)) for a in range(0,60,20) for b in range(0,90,30)]
                self.bodyblocks.add(blocks)
                self.dieSplash=True
            
            self.isAlive=False  
            if time-self.dieTime>=2000:
                self.kill()
                self.isDying=False
    
     #creates bullet instances each time this is called
    def fireBullet(self,pos,angle,color=pg.Color('black'),power=2):
        if Projectile.count<=300:
            time=pg.time.get_ticks()
            if time-self.fireTime>=500:
                bullets=Bullet(pos,angle,color)
                if self.bullets==None:
                    self.bullets=pg.sprite.Group(bullets)
                else:
                    self.bullets.add(bullets)
                self.fireTime=time        

    def drawTorso(self,l):
        x,y=self.cx,self.cy
        pt1=(x-l*(self.shoulderwidth/2),y-l*(self.upperhip+self.torsolength))
        pt2=(x+l*(self.shoulderwidth/2),y-l*(self.upperhip+self.torsolength))
        pt3=(x,y-l*self.upperhip)
        pg.draw.polygon(self.torso,pg.Color('green'),[pt1,pt2,pt3])

    def drawHip(self,l):
        x,y=self.cx,self.cy
        pt1=(x-l*(self.hipwidth/2),y+self.lowerhip*l)
        pt2=(x+l*(self.hipwidth/2),y+self.lowerhip*l)
        pt3=(x,y-l*self.upperhip)
        pg.draw.polygon(self.torso,pg.Color('green'),[pt1,pt2,pt3])

    def drawArm(self,location,l,angle1=0,angle2=0):
        x,y=self.cx,self.cy
        dl1,dl2=0.077*l,0.11*l 
        offangle=(10*2*math.pi/360)
        pt1=location
        pt2=(location[0]+math.sin(angle1-offangle)*dl1,location[1]+math.cos(angle1-offangle)*dl1)
        pt3=(location[0]+math.sin(angle1)*self.uarmlength*l,location[1]+math.cos(angle1)*self.uarmlength*l)
        pt4=(location[0]+math.sin(angle1+offangle)*dl1,location[1]+math.cos(angle1+offangle)*dl1)
        pt5=(pt3[0]+math.sin(angle1-offangle)*dl2,pt3[1]+math.cos(angle2-offangle)*dl2)
        pt6=(pt3[0]+math.sin(angle2)*self.larmlength*l,pt3[1]+math.cos(angle2)*self.larmlength*l)
        pt7=(pt3[0]+math.sin(angle1+offangle)*dl2,pt3[1]+math.cos(angle2+offangle)*dl2)
        #print(pt1)
        pg.draw.polygon(self.torso,pg.Color('red'),[pt1,pt2,pt3,pt4,pt1])
        pg.draw.polygon(self.torso,pg.Color('red'),[pt3,pt5,pt6,pt7,pt3])
        return (pt6[0]+self.rect.centerx-25,pt6[1]+self.rect.centery-45)

    def drawLeg(self,location,l,angle1=0,angle2=0):
        x,y=self.cx,self.cy
        dl1=0.0833*l 
        dl2=0.1277*l
        offangle=(15*2*math.pi/360)
        pt1=location
        pt2=(location[0]+math.sin(angle1-offangle)*dl1,location[1]+(math.cos(angle1-offangle)*dl1))
        pt3=(location[0]+math.sin(angle1)*self.thighlength*l,location[1]+math.cos(angle1)*self.thighlength*l)
        pt4=(location[0]+math.sin(angle1+offangle)*dl1,location[1]+(math.cos(angle1+offangle)*dl1))
        pt5=(pt3[0]+math.sin(angle2-offangle)*dl2,pt3[1]+math.cos(angle2-offangle)*dl2)
        pt6=(pt3[0]+math.sin(angle2)*self.calflength*l,pt3[1]+math.cos(angle2)*self.calflength*l)
        pt7=(pt3[0]+math.sin(angle2+offangle)*dl2,pt3[1]+math.cos(angle2+offangle)*dl2)
        pg.draw.polygon(self.torso,pg.Color('red'),[pt1,pt2,pt3,pt4,pt1])
        pg.draw.polygon(self.torso,pg.Color('red'),[pt3,pt5,pt6,pt7,pt3])
        return (pt6[0]+self.rect.centerx-25,pt6[1]+self.rect.centery-45)

    def drawHuman(self):
        #print(self.LHandPos)
        (x,y)=self.rectDimension
        larmPos=(self.cx-y*(self.shoulderwidth/2),self.cy-y*(self.upperhip+self.torsolength))
        rarmPos=(self.cx+y*(self.shoulderwidth/2),self.cy-y*(self.upperhip+self.torsolength))
        llegPos=(self.cx-y*(self.hipwidth/2),self.cy+y*self.lowerhip)
        rlegPos=(self.cx+y*(self.hipwidth/2),self.cy+y*self.lowerhip)
        a1,a2=self.jointsAngle[0],self.jointsAngle[1]
        a3,a4=self.jointsAngle[2],self.jointsAngle[3]
        a5,a6=self.jointsAngle[6],self.jointsAngle[7]
        a7,a8=self.jointsAngle[4],self.jointsAngle[5]
        self.RHandPos=self.drawArm(rarmPos,y,a1*self.conversion,a2*self.conversion)
        self.drawTorso(y)
        self.drawHip(y)
        self.LHandPos=self.drawArm(larmPos,y,a3*self.conversion,a4*self.conversion)
        self.LFootPos=self.drawLeg(llegPos,y,a5*self.conversion,a6*self.conversion)
        self.RFootPos=self.drawLeg(rlegPos,y,a7*self.conversion,a8*self.conversion)
        
        
        
       

    
    
#main class for the player, is a subclass of human and physics              
class Player(Physics,Human):
    def __init__(self,location,kinect,health=100):
        Physics.__init__(self)
        Human.__init__(self)
        #pg.sprite.Sprite.__init__(self)
        self.kinect=kinect
        self.rectDimension=(50,90)
        self.cx,self.cy=25,45
        self.torso=pg.Surface(self.rectDimension).convert_alpha()
        self.torso.fill((0,0,0,0))
        self.rect=self.torso.get_rect(topleft=location)
        self.speed=8
        self.weaponTimer=0
        self.jumpPower=-15
        self.bullets=None
        self.bodyblocks=None
        self.orientation=1
        
        self.level=1
        self.health=health
    
    #checks if game pause condition is met
    def checkPause(self):
        if self.kinect!=None:
            return abs(self.kinect.RWrist.Position.x)>=1.1
    
    #read and collect data from the kinect sensor
    #and carry out those commands            
    def checkCommand(self):
        #print(1)
        self.vx=0
        #print(self.kinect==None)
        if self.kinect!=None and self.isAlive and not self.isDying:
            if self.kinect.BodyFacingRight() and self.kinect.move():
                self.vx+=self.speed
            if not self.kinect.BodyFacingRight() and self.kinect.move():
                self.vx-=self.speed
            if self.kinect.checkJump() and not self.kinect.move(): self.jump()
            if self.kinect.checkFistClose() and self.kinect.getWeapon(): 
                if self.kinect.BodyFacingRight():
                    self.fireBullet((self.RFist.rect.centerx+5,self.RFist.rect.centery),90,7)
                    self.fireBullet((self.RFist.rect.centerx+5,self.RFist.rect.centery),90,7)
                    #print(0)
                else:
                    self.fireBullet((self.LFist.rect.centerx-5,self.LFist.rect.centery),-90,7)
                    self.fireBullet((self.RFist.rect.centerx+5,self.RFist.rect.centery),-90,7)
            #if not self.haveStick and self.kinect.getWeapon():
            #    self.getStick()
            #if self.haveStick and self.kinect.getWeapon():
            #    self.removeStick()

    


    def draw(self,surface):
        if self.isAlive:
            pg.draw.circle(self.torso,pg.Color('blue'),(25,10),7)
            self.torso.blit(self.cloth,(10,15))
            surface.blit(self.torso,self.rect)
            self.Fists.draw(surface)
            #if self.stickPts!=None:
             #   pg.draw.aaline(surface,(0,0,0),self.stickPts[0],self.stickPts[1])
            if self.bullets!= None:
                self.bullets.draw(surface)
            if self.bodyblocks!=None:
                self.bodyblocks.draw(surface)

        

    def update(self,obstacles):
        #self.fireBullet(self.LHandPos,-90)
        obstacles1=obstacles.copy()
        obstacles1.remove(self)
        #update blocks for bleeding effects
        if self.bodyblocks!= None:
               for block in self.bodyblocks:
                   block.update(self.walls)
        if self.isAlive:
            if self.health<=0:
                self.isDying=True 
            if self.kinect!= None and self.health>0:
                self.jointsAngle=self.kinect.jointsAngle()
                if self.kinect.BodyFacingRight(): self.orientation=1
                if not self.kinect.BodyFacingRight: self.orientation=-1
            self.checkCommand()
            if self.bullets!= None:
                for bullet in self.bullets:
                    bullet.update(obstacles1) 
            self.health+=0.05 if self.health<100 else 0
            self.LFist.update(self.LHandPos,obstacles1)
            self.RFist.update(self.RHandPos,obstacles1)
            self.LFoot.update(self.LFootPos,obstacles1)
            self.RFoot.update(self.RFootPos,obstacles1)
            #if self.stickPts!=None:
            #    self.stick1.update(self.stickPts[0],obstacles1)
            #    self.stick2.update(self.stickPts[1],obstacles1)
            #self.checkDying()
            #self.torso.fi
            self.checkDying()
            self.checkOnMoving(obstacles1)
            self.updatePos(obstacles1)
            self.physicsUpdate()
            self.torso.fill((0,0,0,0))
            self.drawHuman()
        #if not self.isAlive: 
            #self.torso.fill((0,0,0,0))
            #self.mode='start'

#main class for damage-doing sprites
class Projectile(pg.sprite.Sprite):
    count=0
    def __init__(self,location,color=pg.Color('black')):
        pg.sprite.Sprite.__init__(self)
        self.rect=pg.Rect(location[0],location[1],5,5)
        self.image=pg.Surface((5,5)).convert()
        self.image.fill(color)
        self.prev=0
        self.power=1
        Projectile.count+=1
        self.inContact=False
    
    #updates position 
    def update(self,location,obstacles):
        (self.rect.centerx,self.rect.centery)=location
        self.power=abs(self.rect.centerx-self.prev)
        self.prev=self.rect.centerx
        self.checkContact(obstacles)
        
    def checkContact(self,obstacles):
        if pg.sprite.spritecollideany(self,obstacles) and not self.inContact:
            target=pg.sprite.spritecollide(self,obstacles,False)[0]
            #does damage when in contact
            target.health-=self.power*2
            if isinstance(target,Human) and target.bodyblocks!=None:
                target.bodyblocks.add(BodyBlocks((self.rect.centerx,self.rect.centery)))
            elif isinstance(target,Human): target.bodyblocks=pg.sprite.Group(BodyBlocks((self.rect.centerx,self.rect.centery)))
            self.inContact=True
        if self.inContact and not pg.sprite.spritecollideany(self,obstacles):
            self.inContact=False  
            

class Bullet(Projectile,Physics):
    def __init__(self,location,angle,color=pg.Color('black'),power=2):
        Projectile.__init__(self,location,color)
        Physics.__init__(self)
        self.grav=0.15
        self.fall=True
        #unchangable, high initial speed
        self.vx=24*math.sin(angle*2*math.pi/360)
        self.vy=24*math.cos(angle*2*math.pi/360)
        self.power=power

    def move(self,offset,obstacles):
        self.rect.move_ip(offset[0],offset[1])
        if pg.sprite.spritecollideany(self,obstacles):
            self.checkContact(obstacles)
            self.kill()
            Projectile.count-=1

    def update(self,obstacles):
     #   Projectile.update(self)#,obstacles):
        self.physicsUpdate()
        self.move((self.vx,self.vy),obstacles)
        self.image=pg.Surface(self.rect.size).convert()
       

 #small blocks that simulates bleeding effects
class BodyBlocks(Projectile,Physics):
    def __init__(self,location):
        Projectile.__init__(self,location,pg.Color('red'))
        Physics.__init__(self)
        self.rect.width,self.rect.height=2,2
        self.grav=0.01*random.randint(6,12)
        self.fall=True
        self.fallClock=0

    def move(self,offset,obstacles):
        self.rect.move_ip(offset[0],offset[1])
        if pg.sprite.spritecollideany(self,obstacles):
            if pg.time.get_ticks()-self.fallClock>=7000:
                self.kill()
            
            

    def update(self,obstacles):
        self.physicsUpdate()
        self.move((0.1,self.vy),obstacles)
       

         
class Enemy(Physics,Human):
    count=0
    def __init__(self,location,speed):
        Physics.__init__(self)
        Human.__init__(self)
        #pg.sprite.Sprite.__init__(self)
        Enemy.count+=1
        self.speed=speed
        self.rectDimension=(50,90)
        self.cx,self.cy=25,45
        self.playerPos=(0,0)
        self.torso=pg.Surface(self.rectDimension).convert_alpha()
        self.torso.fill((0,0,0,165))
        self.rect=self.torso.get_rect(topleft=location)
        self.routeUpdateTime=0
        self.JRO=1
        self.health=75
        self.conversion=2*math.pi/360
        self.punchCount=4
        self.kickCount=3
        self.weapon='fist'
        self.orientation=1 
        self.bullets=None
        self.bodyblocks=None
        self.inCombo=False
        self.bugFixerTimer=2000
        self.moveTimer=0
        self.command=[]
        self.commandIndex=0
        self.enemyPosList=[]
     
    #enemy AI algorithm helper move function    
    def doMove(self):
        #print(self.commandIndex)
        if self.command!=[] and self.command!=None:
            #time=pg.time.get_ticks()
            if self.Move(self.command[self.commandIndex]):# or time-self.bugFixerTimer>=400:
                #self.bugFixerTimer=time
                self.commandIndex+=1

        

    #regular move function
    def MOve(self,speed):
        angles=self.jointsAngle
        IA1=[a*self.orientation for a in [45,135,-45,0,-20,-60,90,0]]
        IA2=[a*self.orientation for a in [-45,0,45,135,60,0,-20,-90]]
        if self.weapon!='fist':
            #angles[0]=90*self.orientation
            #angles[1]=90*self.orientation
            IA1=[self.orientation*90,self.orientation*90]+IA1[2:]
            IA2=[self.orientation*90,self.orientation*90]+IA2[2:]
        if self.kickCount==3 and self.punchCount==4:
            self.vx=self.orientation*speed
            if self.JRO==1:
                effAngles=IA1
                if self.changePos(effAngles,15):
                    self.JRO=-1
                    #for i in range(8):
                     #   angles[i]+=self.orientation*IA1[i]/7.5
                #elif angles[2]*self.orientation>0:
                 #   for i in range(8):
                  #      angles[i]-=self.orientation*IA2[i]/7.5
            elif self.JRO==-1:
                effAngles=IA2
                if self.changePos(effAngles,15):
                    self.JRO=1
                       
    
    def checkBarrier(self):
        sx,sy=(self.rect.centerx-20)//50,self.rect.centery//50
        px,py=(self.playerPos[0]-20)//50,self.playerPos[1]//50
        for i in range(min(sy,py),max(sy,py)):
            for j in range(min(sx,px),max(sx,px)):
                if self.world[i][j]!=0:# or (j,i) in self.enemyPosList:
                    return False 
        return True

    #AI move function that takes in coordinate 
    #command generated by backtracking algorithm
    def Move(self,coord1):
        time=pg.time.get_ticks()
        (x,y)=((self.rect.centerx-45)//50,self.rect.centery//50)
        if self.rect.centerx<=70:x=0
        (fx,fy)=coord1
        coord=(fx-x,fy-y)
        angles=self.jointsAngle
        IA1=[coord[0]*i for i in [45,135,-45,0,-20,-60,90,0]]
        IA2=[coord[0]*i for i in [-45,0,45,135,60,0,-20,-90]]
        self.vx=self.speed*coord[0]
        if self.weapon!='fist':
            angles[0]=90*self.orientation
            angles[1]=90*self.orientation
        
        if abs(fx*50+45-self.rect.centerx)<=10 and abs(fy*50+5-self.rect.centery)<=10:
            self.rect.centerx=fx*50+45
            self.moveTimer=time
            return True
        if coord[0]!=0:
            if coord[1]>=0:
                if self.JRO==1:
                    effAngles=IA1
                    if self.changePos(effAngles,15):
                        self.JRO=-1
                       
                elif self.JRO==-1:
                    effAngles=IA2
                    if self.changePos(effAngles,15):
                        self.JRO=1
            elif coord[1]<0:
                self.jump()
            
        if coord[0]==0:
           
            if coord[1]<0:
               
                self.jump()
            elif coord[1]>0:
                self.vy=self.vy
        if coord==(0,0): 
            self.moveTimer=time
            return True
        
    #change joints to animate jumping           
    def checkJump(self):
        if self.fall:
            if self.vy<0:
                jumpAngles=[-25,90,-15,100,15,-15,80,-80]
            elif self.vy>=0:
                jumpAngles=[0,0,0,0,0,0,0,0]
            self.changePos(jumpAngles,20)

    #start punching animation sequence
    def doPunch(self):
        if self.punchCount==4 and self.kickCount==3:
            self.punchCount=0
    
    #start kicking animation sequence
    def doKick(self):
      
        if self.kickCount==3 and self.punchCount==4:
            self.kickCount=0
    #animate punch when activated      
    def checkPunch(self):
        #print(1)
        restAngle=[self.orientation*i for i in[0,130,0,130,0,0,0,0]]
        punchAngle1=[self.orientation*i for i in[90,90,0,130,0,0,0,0]]
        punchAngle2=[self.orientation*i for i in[0,130,90,90,0,0,0,0]]
        if self.vx==0 and self.kickCount==3:
            if self.punchCount==0:
                if self.changePos(restAngle,15):
  
                    self.punchCount=1
            elif self.punchCount==1:
                if self.changePos(punchAngle1,15):
                    self.punchCount=2
            elif self.punchCount==2:
                if self.changePos(punchAngle2,15):
                    self.punchCount=3
            elif self.punchCount==3:
                if self.changePos([0,0,0,0,0,0,0,0,0],15):
                    self.punchCount=4
    #animate kick when activated
    def checkKick(self):
        if self.orientation>0:
            angle1=[self.orientation*i for i in[0,70,-15,20,50,-20,10,0]]
            angle2=[self.orientation*i for i in[20,90,-15,-15,100,100,0,0]]
        elif self.orientation<0:
            angle1=[self.orientation*i for i in[0,70,-15,20,10,0,50,-20]]
            angle2=[self.orientation*i for i in[20,90,-15,-15,0,0,100,100]]
        rest=[0,0,0,0,0,0,0,0]
        if not self.fall and self.vx==0 and self.punchCount==4:
            if self.kickCount==0:
                if self.changePos(angle1,15):
                    self.kickCount=1
            elif self.kickCount==1:
                if self.changePos(angle2,15):
                    self.kickCount=2
            elif self.kickCount==2:
                if self.changePos(rest,15):
                    self.kickCount=3
    
    
   

    #main AI algoritm using backtracing recursion to produce route to 
    #player avoiding all obstacles
    def enemyAI(self,spos,coord):
        
        
        command=[(spos)]
        visited=[]
        try:
            xorientation,yorientation=(coord[0]-spos[0])//abs(coord[0]-spos[0]),(coord[1]-spos[1])//abs(coord[1]-spos[1])
        except:
            xorientation,yorientation=1,1
        def isLegal(board,pos):
            if not(0<=pos[1]<len(board) and 0<=pos[0]<len(board[0])):
                return False
    
    
            if board[pos[1]][pos[0]]==0 and board[pos[1]-1][pos[0]]==0:
                return True
        def getCommand(board,spos,tpos):
            nonlocal xorientation
            nonlocal yorientation
            x,y=xorientation,yorientation
            dirs=[(x,0),(-x,0),
                   (0,y), (0,-y)]
            if spos==tpos:
                return command
            else:
                for dir in dirs:
                    newPos=(spos[0]+dir[0],spos[1]+dir[1])
                    if isLegal(board,newPos) and (newPos not in visited):
                        visited.append(newPos)
                        command.append(newPos)
                    
                        solution=getCommand(board,newPos,tpos)                     
                                        
                        if solution!=[]:
                            return solution
                        command.remove(newPos)
                return []
        self.command=getCommand(self.world,((self.rect.x-20)//50,self.rect.centery//50),((self.playerPos[0]-20)//50,self.playerPos[1]//50))
        print(self.command)


    #main enemy AI sequence; determines when to use higher or lower level AI
    def sequence(self):
        
        dist=self.playerPos[0]-self.rect.centerx
        angle=10#(math.asin((0.08*dist/144)))*360/(2*math.pi)#(0.08*dist/144)))
        time=pg.time.get_ticks()
        realDist=abs(dist)
        if abs(self.rect.centery-self.playerPos[1])>=60 and not self.checkBarrier():
            try:
                self.orientation=-self.command[commandIndex][0]+(self.rect.centerx-20)//50
            except:
                self.orientation=1
            self.doMove()
            if time-self.routeUpdateTime>=5000:
                self.routeUpdateTime=time
                self.moveTimer=time
                #higher level AI
                self.enemyAI(((self.rect.centerx-20)//50,self.rect.centery//50),((self.playerPos[0]-20)//50,self.playerPos[1]//50))
              
                self.commandIndex=1
                
        if self.checkBarrier():
            try:
                self.orientation=dist/abs(dist)
            except:
                self.orientation=1
            #lower level AI
            self.closeCombat(angle,realDist)

        
            
        
   
    #lower level enemy AI,
    #activated when in close proximity with the player
    def closeCombat(self,angle,dist):
       
       if dist<=55 and abs(self.rect.centery-self.playerPos[1])<45:
           self.doCombo()
       else:
           self.updateActions()
           self.MOve(self.speed)
          
           if self.weapon=='gun': 
               self.fireBullet(self.LHandPos,(90+angle)*self.orientation) 
                
    #attack combinations
    def doCombo(self):
        if True:
            num=random.random()
           
            if self.health>=30:
                pt1=0.5
                pt2=0.75
            elif self.health<30:
                pt1=0.2
                pt2=0.3
            if num<=pt1:
                self.doPunch()
            if pt1<num<=pt2:
                self.doKick()
            if pt2<num<=1:
                self.doPunch()
                self.vx=random.randint(-3,3)
           
         
    
    def draw(self,surface):
        if self.bodyblocks!=None:
            self.bodyblocks.draw(surface)
        if self.isAlive:
            pg.draw.circle(self.torso,pg.Color('red'),(25,10),7)
            self.torso.blit(self.cloth,(10,15))
            surface.blit(self.torso,self.rect)
            if self.bullets!= None:
                self.bullets.draw(surface)
        
            self.Fists.draw(surface)
            
            
    
    def updateActions(self):
        if self.vx!=0:
            self.kickCount=3
            self.punchCount=4

    def update(self,obstacles,player,people):#,world,coord):
        obstacles1=obstacles.copy()
        obstacles1.remove(self)
        self.checkDying()
        #self.vx=0
        if Enemy.count>=3: self.weapon='gun'
        elif Enemy.count<3: self.weapon='fist'
        #print(self.health)
        if self.bodyblocks!= None:
            for block in self.bodyblocks:
                block.update(self.walls)
        if not self.isAlive: 
            self.torso.fill(pg.Color('pink'))
        if self.isAlive:
            if self.health<=0:
                self.isDying=True 
                self.dieTime=pg.time.get_ticks()
            if self.bullets!= None:
                obstacle=obstacles1.copy()
                obstacle.remove(people)
                obstacle.add(player)
                for bullet in self.bullets:
                    bullet.update(obstacle)
            self.sequence()
            self.updateActions()
            self.torso.fill((0,0,0,0))
            self.LFist.update(self.LHandPos,obstacles1)
            self.RFist.update(self.RHandPos,obstacles1)
            self.LFoot.update(self.LFootPos,obstacles1)
            self.RFoot.update(self.RFootPos,obstacles1)
            self.checkKick()
            self.checkPunch()
            self.checkJump()
            self.physicsUpdate()
            self.updatePos(obstacles1)
            self.drawHuman()
            self.vx=0

class Obstacle(pg.sprite.Sprite):
    def __init__(self,rect,color,image=None,interval=50):
        pg.sprite.Sprite.__init__(self)
        self.rect=pg.Rect(rect)
        self.image=pg.Surface(self.rect.size).convert_alpha()
        self.image.fill(color)
        self.health=10000
        self.mode=None
        self.type='stationary'
        if image!=None:
            for a in range(0,rect[2],interval):
                self.image.blit(image,(a,0))

class MovingObstacles(Obstacle):
    
    #part of this class is inspired from moving_platforms.py from 
    #https://github.com/Mekire/pygame-samples/blob/master/platforming/moving_platforms.py
    #by Mekire to accomodate my game

    def __init__(self,rect,color,axis,length,speed=2,delay=300):
        Obstacle.__init__(self,rect,color)
        self.axis=axis
        self.dist=length
        self.start=self.rect[self.axis]
        self.end=self.rect[self.axis]+self.dist
        self.speed=speed
        self.delay=delay
        self.mode='Moving'
        self.time=0
        self.move=True

    def update(self,people,obstacles):#modified from moving_platform example(refer to the beginning of class)
        obstacles=obstacles.copy()
        obstacles.remove(self)
        now=pg.time.get_ticks()
        if self.move:
            speed=self.speed
            if self.rect[self.axis]+speed<=self.start or self.rect[self.axis]+speed>=self.end:
                speed=self.start-self.rect[self.axis] if self.rect[self.axis]+speed<=self.start else self.end-self.rect[self.axis]
                self.move=False
                self.time=now
                self.speed=self.speed*-1
            self.rect[self.axis]+=speed
        elif now-self.time>self.delay:
            self.move=True

    def movePeople(self,now,people,obstacles,speed):#modified from moving_platform example(refer to the beginning of class)
        for person in people:
            if person.onMoving!=False and self in person.onMoving or pg.sprite.collide_rect(self,person):
                axis=self.axis
                offset=(speed,0) if self.axis==0 else (0,speed)
                person.move(offset,axis,obstacles)
                if pg.sprite.collide_rect(self,person):
                    if self.speed>0:
                        self.rect[axis]=person.rect[axis]-self.rect.size[axis]
                    else:
                        self.rect[axis]=person.rect[axis]+person.rect.size[axis]
                    self.move=False
                    self.time=now
                    self.speed=self.speed*-1


class GameControl(object):
    
    def __init__(self,kinect,level=0):
        self.screen=pg.display.get_surface()
        self.screenRect=self.screen.get_rect()
        self.kinect=kinect 
        self.player=Player((20,10),self.kinect)
        self.enemy=None
        self.curView=self.screen.get_rect()
        self.level=pg.Surface((2040,720)).convert_alpha()
        self.board=[[0]*40 for i in range(14)]
        #all maps are stored here in a 14*40 3d list, 1 represents the presence of obstacles
        #list is also used in higher level enemy AI to work out optimal route
        self.worlds=[[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0],
                    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                    [0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1],
                    [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1],
                    [0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,1,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                    [1,0,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0],
                    [0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0],
                    [1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
                   [[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]]]
        self.world=self.worlds[level]     
        self.tile=pg.image.load('dirtBlock.png') #retrieved from http://opengameart.org/content/32x32-blocks-and-more
        self.tile=pg.transform.scale(self.tile,(50,50))
        self.light=pg.image.load('parallax-forest-lights.png') #retrieved from http://opengameart.org/content/forest-background
        self.lightCoord=[(200,150),(400,50),(500,290),(450,70),(800,100),(1000,40),(1400,90),(1700,40)]
        self.tree=pg.image.load('Tree - Pine 04.png')#retrieved from http://opengameart.org/content/pine-tree-pack
        self.treeCoord=[(200,490),(400,490),(700,490),(1000,490),(1500,490)]
        self.levelRect=self.level.get_rect()
        self.keys=None
        self.obstacles1=pg.sprite.Group(self.makeObs())
        self.nonPerson=self.obstacles1.copy()
        self.player.walls=self.nonPerson
        self.playerCoord=(0,0)
        self.obstacles=pg.sprite.Group(self.obstacles1,self.player)
        self.people=pg.sprite.Group(self.player)
        self.boardUpdate=0
        self.enemyClock=0
        self.enemySpawnSpaceList=self.getPlaces()
        self.enemyPosList=[]
        self.mode='game'
        Enemy.count=0
        self.enemyKiled=0
       

    #randomly generates a list of places to spawn enemies
    def getPlaces(self):
        list=[]
        for i in range(1,13):
            for j in range(1,39):
                if (self.world[i][j]==0 and 
                    self.world[i+1][j]==0):
                    if not ((j,a) for a in [i-1,i+1]) in list:
                        list.append((j,i))
        return list

    #function that spawns enemies
    def addEnemy(self):
        time=pg.time.get_ticks()
        if time-self.enemyClock>=2500:
            coord1=self.enemySpawnSpaceList[random.randint(0,len(self.enemySpawnSpaceList)-1)]
            coord=(coord1[0]*50+20,coord1[1]*50)
            enemy=Enemy(coord,8)
            enemy.walls=self.nonPerson
            enemy.world=self.world
            self.obstacles.add(enemy)
            self.people.add(enemy)
            if self.enemy==None:
                self.enemy=pg.sprite.Group(enemy)
            else:
                self.enemy.add(enemy)
            self.enemyClock=time


    #functions that creates obstacle classes based on the 2-d list
    def makeObs(self):
        obsCoord=[]
        for y in range(14):
            prev=0
            length=0
            for x in range(40):
                if self.world[y][x]==1 and x==39:
                    length+=1
                    obsCoord.append((x+1-length,y,length))
                elif self.world[y][x]==1:
                    length+=1
                    prev=1
                elif self.world[y][x]!=1 and prev==1:
                    obsCoord.append((x-length,y,length))
                    length=0
                    prev=0
                
        
        blocks=[]
        for coord in obsCoord:
            (x,y,l)=coord
            blocks.append(Obstacle((20+x*50,y*50,50*l,50),(random.randint(0,155),random.randint(0,155),random.randint(0,155)),self.tile) )
        walls = [Obstacle((0,700,2040,20),(100,100,100)),
                 Obstacle((0,0,20,720),(100,100,100)),
                 Obstacle((2020,0,20,720),(100,100,100))]
        #movingBlocks=[MovingObstacles((380,500,50,20),(100,200,0),0,30,1,1600)]
        #print(obsCoord)
        return blocks+walls#+movingBlocks
        
    #keeps the screen centered at player
    def updateView(self):
        self.curView.center=self.player.rect.center
        self.curView.clamp_ip(self.levelRect)
        
    def eventLoop(self):
        pass

    def update(self,keys):
        if self.player.checkPause(): self.mode='start'
        if not self.player.isAlive:
            self.mode='start'
        self.enemyKiled=Enemy.count-len(self.enemy) if self.enemy!=None else 0
        if self.enemy!=None:
           
            for enemy in self.enemy:
             
                enemy.enemyPosList=self.enemyPosList
                enemy.playerPos=(self.player.rect.centerx,self.player.rect.centery)
                enemy.update0(self.obstacles)
                enemy.update(self.obstacles,self.player,self.people)
     
        if self.enemy==None: self.addEnemy()
        if self.enemy!=None and len(self.enemy)<2:
            self.addEnemy()
        self.keys=keys
        self.player.kinect=self.kinect
        self.player.update0(self.obstacles1)
        self.player.update(self.obstacles)
        
        #self.obstacles1.update(self.people,self.obstacles)
        self.updateView()
       
       

           
    def draw(self):
        self.level.fill((200,200,200))
        for a in self.lightCoord:
            self.level.blit(self.light,a)
        for b in self.treeCoord:
            self.level.blit(self.tree,b)
        self.obstacles1.draw(self.level)
        self.player.draw(self.level)
        #self.screen.blit(self.level,(0,0),self.curView)
        self.obstacles1.draw(self.level)
        self.player.draw(self.level)
     
        if self.enemy!= None:
            #self.enemy.draw(self.level)
            for enemy in self.enemy:
                enemy.draw(self.level)
        self.screen.blit(self.level,(0,0),self.curView)
        pg.draw.rect(self.screen,(0,0,0),(300,30,250,20))
        pg.draw.rect(self.screen,(255,0,0),(300,30,self.player.health*2.5,20))
        drawText(self.screen,'enemy killed: %d'%(self.enemyKiled),(0,0,0),(300,55,200,40),pg.font.SysFont('monospace',12,True))
        




#this class is the start menu of this game, it is responsible for
#displaying instructions, customizing player, displaying and starting 
#different levels and starting the game

class StartControl(object):
    BACKGROUND=pg.image.load('Full-background.png')
    #retrieved from http://opengameart.org/content/cozy-endless-game-background
    def __init__(self,a):
        self.instructions='''In the Game, control the player with your body movements, punch and kick the enemy to reduce enemy health. Player can jump by jumping, move by walk in place, fire bullets by putting two hands together. The objective is to survive as long as possible. To customize player, click customize, you can adjust the strength, health and speed of the player. Move left hand to move cursor, close fist to click. While in game, to pause, just walk away.'''   
        self.iconImg=pg.image.load('rock.png')
        #retrieved from http://opengameart.org/content/32x32-blocks-and-more
        self.iconImg=pg.transform.scale(self.iconImg,(100,100))
        self.cursorImg=pg.image.load('3.png') 
        #retrieved from http://opengameart.org/content/cursor
        self.cursorImg=pg.transform.scale(self.cursorImg,(30,30))
        self.helpImg=pg.image.load('help.png')
        #retrieved from http://www.freeiconspng.com/free-images/help-icon-17014
        self.helpImg=pg.transform.scale(self.helpImg,(150,100))
        self.image=pg.transform.scale(StartControl.BACKGROUND,(1000,700))
        self.screen=pg.display.get_surface()
        self.screenRect=self.screen.get_rect()
        self.level=pg.Surface((1000,700)).convert_alpha()
        self.levelRect=self.level.get_rect()
        self.Game=Obstacle((250,200,500,100),(100,100,100,0),self.iconImg,100)
        self.Game.mode=('game',0)
        self.font=pg.font.SysFont('monospace',70,True)
        self.gameText=self.font.render('PLAY GAME',1,(255,0,0))
        self.LevelSelect=Obstacle((250,350,500,100),(100,100,100,0),self.iconImg,100)
        self.LevelSelect.mode=('start')
        self.levelsText=self.font.render('VIEW LEVELS',1,(255,0,0))
        self.customize=Obstacle((250,500,500,100),(100,100,100,0),self.iconImg,100)
        self.customize.mode=('start')
        self.helpText=self.font.render('CUSTOMIZE',1,(255,0,0))
        self.insTextFont=pg.font.SysFont('monospace',20,True)
        self.instructionText=self.insTextFont.render(self.instructions,1,(0,0,0))
        self.Help=Obstacle((50,50,150,100),(0,0,0,0),self.helpImg,150)
        self.Help.mode=('start')
        self.Cursor=Obstacle((50,50,30,30),(0,0,0,0),self.cursorImg,30)
        self.cursor=pg.sprite.Group(self.Cursor)
        self.helpGroup=pg.sprite.Group(self.Help)
        self.group=pg.sprite.Group([self.Game,self.LevelSelect,self.customize,self.Help])
        self.keys=None
        self.kinect=a
        self.mode=('start')
        self.displayHelp=False
        self.isLevelSelect=False
        self.inCustomize=False
        self.level1=self.font.render('LEVEL ONE',1,(255,0,0))
        self.level2=self.font.render('LEVEL TWO',1,(255,0,0))
        self.level3=self.font.render('LEVEL THREE',1,(255,0,0))
        self.level4=self.font.render('LEVEL FOUR',1,(255,0,0))
        self.title=self.font.render('PUNCH IT!',1,(0,0,0))
        self.health=4
        self.strength=4
        self.speed=4
        self.timer=0
        self.demoPlayer=pg.image.load('demoPlayer.png')#retrieved from http://opengameart.org/content/agent-b

   
    def eventLoop(self):
        (x,y)=(self.Cursor.rect.centerx,self.Cursor.rect.centery)
        if self.keys!= None and not self.isLevelSelect and not self.inCustomize:
            if pg.sprite.spritecollideany(self.Cursor,self.group) and self.keys['FistClose']:
                select=pg.sprite.spritecollide(self.Cursor,self.group,False)
                self.mode=select[0].mode
                if select[0] is self.Help and self.displayHelp==False:
                   
                    self.displayHelp=True
                elif select[0] is self.Help and self.displayHelp==True:
                    self.displayHelp=False
                if select[0] is self.LevelSelect:
                    self.isLevelSelect=True
                if select[0] is self.customize:
                    self.inCustomize=True
        elif self.keys!=None and self.isLevelSelect:
            if self.keys['FistClose'] and 300<=x<=700 and 100<=y<=200:
                self.mode=('game',0)
            elif self.keys['FistClose'] and 300<=x<=700 and 250<=y<=350:
                self.mode=('game',1)
            elif self.keys['FistClose'] and 300<=x<=700 and 400<=y<=500:
                self.mode=('game',2)
            elif self.keys['FistClose'] and 300<=x<=700 and 550<=y<=650:
                self.mode=('game',3)
        elif self.keys!= None and self.inCustomize:
            
            if self.keys['FistClose']:
                if 700<=x<=750 and 150<=y<=200:
                    self.health-=0.5 if self.health>0 else 0
                if 800<=x<=850 and 150<=y<=200:
                    self.health+=0.5 if self.health<10 else 0
                if 700<=x<=750 and 250<=y<=300:
                    self.speed-=0.5 if self.speed>0 else 0
                if 800<=x<=850 and 250<=y<=300:
                    self.speed+=0.5 if self.speed<10 else 0
                if 700<=x<=750 and 350<=y<=400:
                    self.strength-=0.5 if self.strength>0 else 0
                if 800<=x<=850 and 350<=y<=400:
                    self.strength+=0.5 if self.strength<10 else 0
                if 0<=x<=100 and 0<=y<=100:
                    self.inCustomize=False
       
    
    def update(self,location,keys):
        location=((location[0]+0.2)*1000,(0.2-location[1])*1000)
        (self.Cursor.rect.centerx,self.Cursor.rect.centery)=location
        self.keys=keys

    def draw(self):

        self.level.fill(pg.Color('red'))
        self.level.blit(self.image,(0,0))
       
        if self.displayHelp==True:
            drawText(self.level,self.instructions,(0,0,0),(100,300,800,300),self.insTextFont)
            self.helpGroup.draw(self.level)
        elif self.isLevelSelect:
            self.level.blit(self.level1,(300,100))
            self.level.blit(self.level2,(300,250))
            self.level.blit(self.level3,(300,400))
            self.level.blit(self.level4,(300,600))
        elif self.inCustomize:
            for rect in [(700,150,50,50),(800,150,50,50),(700,250,50,50),(800,250,50,50),(700,350,50,50),(800,350,50,50)]:
                drawText(self.level,'less'if rect[0]==700 else'more',(0,0,0),rect,self.insTextFont)
            drawText(self.level,'HEALTH',(0,0,0),(500,150,80,50),self.insTextFont)
            drawText(self.level,'SPEED',(0,0,0),(500,250,80,50),self.insTextFont)
            drawText(self.level,'STRENGTH',(0,0,0),(500,350,100,50),self.insTextFont)
            pg.draw.rect(self.level,(255,0,0),(500,120,self.health*10,20))
            pg.draw.rect(self.level,(255,0,0),(500,220,self.speed*10,20))
            pg.draw.rect(self.level,(255,0,0),(500,320,self.strength*10,20))
            self.level.blit(self.demoPlayer,(100,100))
        else:# not self.displayHelp and not self.isLevelSelect and not self.inCustomize:
            self.group.draw(self.level)
            self.level.blit(self.gameText,(290,230))
            self.level.blit(self.levelsText,(280,380))
            self.level.blit(self.helpText,(270,530))
            self.level.blit(self.title,(290,110))

        self.cursor.draw(self.level)
        self.screen.blit(self.level,(0,0))





#the dispatcher class that cuts between start menu and game interface,
#also updates the data for the currently running mode
#
class TotalControl(object):
    #kinect=None
    
    def __init__(self):
        self.joints=None 
        self.kinect=None
        self.startScreen=StartControl(self.kinect)
        self.game=None
      
        
        self.mode='start'
        self.done=False 
        self.keys={'FistClose':False,'FaceRight':False,
                 'Jump':False,'Move':False,
                 'jointsAngle':[0,0,0,0,0,0,0,0]}
        self.startKinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body)
        self.clock=pg.time.Clock()
        
    def eventLoop(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.done=True 
        if self.mode=='start':
            self.startScreen.eventLoop()
        elif self.mode=='game':
            self.game.eventLoop()
        elif self.mode=='customize':
            self.customize.eventLoop()
       
            
    def update(self):
        self.kinectUpdate()
        location=(50,200)
        if self.kinect==None and self.joints!= None:
            self.kinect=KinectControl(self.joints)
        if self.kinect!= None and self.joints!= None:
            self.kinect.joints=self.joints
            self.kinect.updateJoints()
            if self.game!=None:
                self.game.kinect=self.kinect
            #print(self.keys['FistClose'])
            self.keys['Jump']= self.kinect.checkJump()
            self.keys['FistClose']=self.kinect.checkFistClose()
            self.keys['Move']=   self.kinect.move()
            self.keys['FaceRight']=self.kinect.BodyFacingRight()
            self.keys['jointsAngle']=self.kinect.jointsAngle()
            location=self.kinect.getLHandPosition()
            
        #self.keys=pg.key.get_pressed
        if self.mode=='start':
            self.startScreen.update(location,self.keys)
            if self.startScreen.mode[0]=='game':
                if self.game==None:
                    self.game=GameControl(self.kinect,self.startScreen.mode[1])
                    self.game.player.speed=10+self.startScreen.speed
                    self.game.player.jumpPower=-17-self.startScreen.strength//2
                    self.game.player.health=75+self.startScreen.health*6
                    self.mode='game'
                elif self.game!=None:
                    self.mode='game'
                self.startScreen.__init__(self.kinect)
                

        if self.mode=='game':
            self.game.update(self.keys)
            if self.game.player.health<=0:
                self.mode='start'
                self.game=None
            elif self.game.mode=='start':
                self.mode='start'

            #self.updateInstances(self.game.mode)
       
       
    
   
           
    def draw(self):
        if self.mode=='start':
            self.startScreen.draw()
        elif self.mode=='game':
            self.game.draw()
       
    
    def kinectUpdate(self):
        if self.startKinect.has_new_body_frame():
            bodies=self.startKinect.get_last_body_frame()
            if bodies is not None:
                for i in range(0,self.startKinect.max_body_count):
                    body=bodies.bodies[i]
                    if not body.is_tracked:
                        continue 
                    self.joints=body.joints
                    
    
    def mainLoop(self):
        while not self.done:

            self.eventLoop()
            self.draw()
            self.update()
            pg.display.flip()
            self.clock.tick(100)


#the following helper function is copied from http://www.pygame.org/wiki/TextWrap


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pg.Rect(rect)
    y = rect.top
    lineSpacing = -2
 
    # get the height of the font
    fontHeight = font.size("Tg")[1]
 
    while text:
        i = 1
 
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
 
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
 
        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
 
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
 
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
 
        # remove the text we just blitted
        text = text[i:]
 
    #return text


def runFn():  
    if __name__=='__main__':
        os.environ['SDL_VIDEO_CENTERED']='1'
        pg.init()
        pg.display.set_mode((1000,700))
        runIt=TotalControl()
        runIt.mainLoop()
        pg.quit()
        sys.exit()

runFn()
#kinectDemo()