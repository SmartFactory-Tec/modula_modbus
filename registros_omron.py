import pygame
import random
from pyModbusTCP.client import ModbusClient
import numpy as np
import time


    
pygame.init()
screen_x= 500
screen_y = 800
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
myhost = "192.168.0.15"
myport = 12345
c = ModbusClient(host=myhost,port=myport)

class Missions:
    #1:MissionStatus 0-Charge, 1-Move, 2-Free
    #2: #Goalx
    #3: #Goaly
    #4: Battery
    #5: RobotStatus 0-Charging, 1:Moving, 2:Free,3-Success,4-Failure
    #6: Distance
    #7: Locationx robot
    #8: Locationy robot
    #9: Goalxpi robot
    #10: Goalypi robot
    #11: Locationxpi robot
    #12: Locationypi robot
    def __init__(self):
        self.inforobot=[0,10,0,0,0,0,0,0,0,0,0,0]
        self.missions = [[[584,176],[11412,10106]],[[355,175],[10212,10078]],[[528,405],[11206,10717]]]
    def change_mission(self,index):
        if index==4:
            self.inforobot[0]=29
        elif index==5:
            self.inforobot[0]=10
        elif index==10:
            self.inforobot[0]=60

        else:
            self.inforobot[0]=1
            mymission = self.missions[index]
            #Goal Robot x,y
            self.inforobot[1] = mymission[1][0]
            self.inforobot[2] = mymission[1][1]
            #PI /Locationx,y
            self.inforobot[8] = mymission[0][0]
            self.inforobot[9] = screen_y - mymission[0][1]



class Button:
    def __init__(self, text,  pos, font,index):
        self.x, self.y = pos
        self.size=(120,50)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.title = text
        self.font = pygame.font.SysFont("Arial", font)
        self.color = 'black'
        self.oldcolor='black'
        self.index=index
        self.mymission=Missions()
        self.index == 10
        self.send_info()
    def show(self):
        self.surface = pygame.Surface(self.size)
        self.text = self.font.render(self.title, 1, pygame.Color("White"))
        while self.oldcolor == self.color:
            self.color = random.choice(['black','blue','green','orange','red'])
        self.surface.fill(self.color)
        self.oldcolor = self.color
        self.surface.blit(self.text, (0, 0))
        screen.blit(self.surface, (self.x, self.y))
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    """
                    if self.index == 4:

                        self.mymission.change_mission(0)
                        self.send_info()
                        bits = c.read_holding_registers(0, 12)
                        while bits[0] == 1:
                            bits = c.read_holding_registers(0, 12)
                        self.send_info()

                        self.mymission.change_mission(1)
                        self.send_info()
                        while bits[0] == 1:
                            bits = c.read_holding_registers(0, 12)
                        self.send_info()

                        self.mymission.change_mission(2)
                        self.send_info()
                        while bits[0] == 1:
                            bits = c.read_holding_registers(0, 12)
                        self.send_info()
                            
                        


                    else:
                        self.show()
                        self.mymission.change_mission(self.index)
                        self.send_info()
                    """
                    self.show()
                    self.mymission.change_mission(self.index)
                    self.send_info()


    def send_info(self):
        if c.open():
            #Read Battery / RobotStatus /Distance (Modbus)
            bits = c.read_holding_registers(0, 12)
            self.mymission.inforobot[3]=bits[3]
            self.mymission.inforobot[4] = bits[4]
            self.mymission.inforobot[5] = bits[5] 
            print(bits)
            #Map coordinate location to pi
            theta = np.radians(13)
            offsetx=7.9115512
            offsety=2.50132282
            rheight=11.29203556
            rwidth=17.69995916
            c1, s = np.cos(theta), np.sin(theta)
            R = np.array(((c1, -s), (s, c1)))
            #Convert bit +-
            self.mymission.inforobot[10]=int(mapping(bits[6]+offsetx,screen_x,rwidth))
            self.mymission.inforobot[11]=int(mapping(bits[7]+offsety,screen_y,rheight))
            #Update registers self.mymissionStatus,Goalx,Goaly
            c.write_multiple_registers(0,[self.mymission.inforobot[0],self.mymission.inforobot[1],self.mymission.inforobot[2]])
            print("Si")
            time.sleep(1)
        else:
            print("unable to connect to "+myhost+":"+str(myport))

def mapping(x,game,ros):
    return (x*game)/ros
def mainloop():
    pygame.display.set_caption('SmartFactory Demo')
    Icon = pygame.image.load('non.jpg')
    font1 = pygame.font.SysFont('chalkduster.ttf', 36)
    screen.blit(pygame.image.load("fondo.jpg").convert(), (10 ,10))
    img1 = font1.render('SmartFactory Demo', True, 'red')
    screen.blit(img1, (130, 50))
    pygame.display.set_icon(Icon)
    button1.show()
    button2.show()
    button3.show()
    button4.show()
    button5.show()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event)
            button2.click(event)
            button3.click(event)
            button4.click(event)
            button5.click(event)

            #c.write_multiple_registers(8,[mission.inforobot[8],mission.inforobot[9],mission.inforobot[10],mission.inforobot[11]])
        clock.tick(30)
        pygame.display.update()
 


 
button1 = Button(
    "Home",
    (screen_x/2-50, 100),
    font=30,
    index=0)
 
button2 = Button(
    "Pick",
    (screen_x/2-50, 200),
    font=30,
    index=1)
 
button3 = Button(
    "Place",
    (screen_x/2-50, 300),
    font=30,
    index= 2)

button4 = Button(
    "paro",
    (screen_x/2-50, 400),
    font=30,
    index= 5)

button5 = Button(
    "Process",
    (screen_x/2-50, 600),
    font=30,
    index= 4)
 
mainloop()
