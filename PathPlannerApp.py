import pygame, os, sys
from pygame.locals import *
from time import sleep
import math
import neat
import tkinter as tk
from tkinter import filedialog
import pickle

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Auto Route Planner")
screen = pygame.display.set_mode((1450,850),0,32)
screen.fill('white')
font = pygame.font.Font('freesansbold.ttf',18)

class Button:
    def __init__(self,text,x_pos,y_pos,x_text,y_text,width,height,enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_text = x_text
        self.y_text = y_text
        self.width = width
        self.height = height
        self.enabled = enabled
        self.draw()

    def draw(self):
        button_text = font.render(self.text, True,'black')
        button_rect =pygame.rect.Rect((self.x_pos,self.y_pos)
                                      ,(self.width,self.height))
        if self.check_click():
            pygame.draw.rect(screen,(100,100,100,255),button_rect,0,7)
        elif self.enabled==False:
            pygame.draw.rect(screen,(100,100,100,255),button_rect,0,7)
        else:
            pygame.draw.rect(screen,'light gray',button_rect,0,7)   
        pygame.draw.rect(screen,'black',button_rect,2,5)
        screen.blit(button_text,(self.x_pos+self.x_text,
                                 self.y_pos+self.y_text))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos,self.y_pos),
                                       (self.width,self.height))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        else:
            False

class Text:     
    def __init__(self,text,x_pos,y_pos,
                 font,text_col,enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font= font
        self.text_col = text_col
        self.enabled = enabled
        self.draw()

    def draw(self):
        text_disp = font.render(self.text,True,
                                self.text_col)
        screen.blit(text_disp,
                    (self.x_pos,self.y_pos))

class Point:
    def __init__(self, x_pos,
                y_pos,x_target,
                y_target,color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_move = 0
        self.y_move = 0
        self.x_limit = [5,1445]
        self.y_limit = [5,845]
        self.center = [x_pos + 5, y_pos + 5]
        self.isAlive = True
        self.x_target = x_target
        self.y_target = y_target
        self.x_tick = 0
        self.y_tick = 0
        self.color = color 

    def update(self,x_pos,y_pos):
        if self.isAlive:
            self.x_pos = x_pos + self.x_tick
            self.y_pos = y_pos + self.y_tick
            self.center = [x_pos + self.x_tick+ 5, 
                           y_pos + self.y_tick+ 5]
        else:
            pass
        self.draw()

    def draw(self):
        self.survive()
        if self.x_pos>230 and self.y_pos>10:
            pointRect = pygame.rect.Rect((self.x_pos + self.x_move, 
                                          self.y_pos + self.y_move), 
                                          (10, 10))
            pygame.draw.rect(screen, self.color, pointRect, 0, 4)
            pointRect = pygame.rect.Rect((self.x_pos + self.x_move,
                                           self.y_pos + self.y_move), 
                                           (10, 10))
            pygame.draw.rect(screen, (2,2,2,255), pointRect, 1, 4)
        
    def radarData(self):
        distance = 1
        
        angles = [0, 45, 90, 135, 180, 225, 270, 315]
        distance_list = [1, 1, 1, 1, 1, 1, 1, 1]
        pointCenter = [self.center[0],self.center[1]]

        for i in range(8):
            checkRadar = True
            while checkRadar:
                distance_list[i] += 1
                if distance_list[i] > 300:
                    checkRadar = False
                x_end = int(self.center[0] + 
                            (distance_list[i] * 
                             math.sin(math.radians(angles[i]))))
                y_end = int(self.center[1] + 
                            (distance_list[i] * 
                             math.cos(math.radians(angles[i]))))
                if x_end>self.x_limit[1] or x_end <self.x_limit[0] or y_end >self.y_limit[1] or y_end <self.y_limit[0]:
                    pass
                else:
                    if screen.get_at((x_end, y_end)) == (0, 0, 0, 255) or screen.get_at((x_end, y_end)) == (190, 190, 190, 255) :
                        x_end = self.center[0]
                        y_end = self.center[1]
                        checkRadar = False
                """
                pygame.draw.line(screen, 'red', (self.center[0], self.center[1]), (x_end, y_end), 1)   #DRAW RADAR LINES 
                pointRect = pygame.rect.Rect((self.x_pos + self.x_move, self.y_pos + self.y_move), (10, 10))
                pygame.draw.rect(screen, self.color, pointRect, 0, 4)
                pointRect = pygame.rect.Rect((self.x_pos + self.x_move, self.y_pos + self.y_move), (10, 10))
                pygame.draw.rect(screen, (2,2,2,255), pointRect, 1, 4)
                """
        return distance_list

    def checkCollusion(self, distance):
        stateCollusion = False
        if any(d < distance for d in self.radarData()):
            stateCollusion = True
        else:
            stateCollusion = False
        return stateCollusion
    
    def move(self, direction):
        if direction == 0:
            pass
        if direction == 1:
            self.y_tick = -8
        elif direction == 3:
            self.y_tick=  +8 
        elif direction == 2:
            self.x_tick = +8
        elif direction == 4:
            self.x_tick = -8

    def survive(self):
        if self.checkCollusion(9) or self.x_pos>1430 or self.x_pos<230 or self.y_pos>850 or self.y_pos<10:
            self.isAlive = False
        else:
            self.isAlive = True
    
    def dataOutput(self):
        data = self.radarData()
        dataAdd = int(calcDist(self.center[0],self.center[1],self.x_target,self.y_target))
        data.append(dataAdd)
        data.append(self.x_pos)
        data.append(self.y_pos)
        data.append(self.x_target)
        data.append(self.y_target)
        #print(data)
        return data
    
    def distToTarget(self):
        distance = self.radarData()
        return distance[8]

def calcDist(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def chooseMap():
    root = tk.Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename()
    return file_path

destCounter = 0
run_main = True
genbtnState = False  
gen_swState = False
choose_destState = False
destBtnState = True
dispPathState = False
engGenClicked = False
generalInfo = 0
total_generations = 2000

dest1 = [0,0]
dest2 = [0,0]

x_move = 0
y_move = 0 

population_size = 20
generation = 0
genEnd = True

def run_generations(genomes,config):
    pygame.draw.rect(screen,(190, 190, 190, 255),pygame.rect.Rect((0,0),(1450,800)),0,0)  
    pygame.draw.rect(screen,'white',pygame.rect.Rect((230,10),(1200,800)),0,0)    
    mapBlack = pygame.image.load(mapPath)
    text_fileState = Text(f'Map {mapPath} ',40,133,font,'black',True)
    pygame.draw.rect(screen,'black',pygame.rect.Rect((230,10),(1200,800)),1,0)  
    screen.blit(mapBlack,(230,10))

    dispPathState = False
    btn_generate.draw()
    btn_options.draw()
    btn_browse.draw()
    btn_chooseDest.draw()
    btn_dispPath = Button("Display Path",15,480,47,13,200,50,dispPathState)
    
    point1.draw()
    point2.draw()
        
    print(engGenClicked)
    nets = []
    points = []
    ge =[]

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)
        points.append(Point(dest1[0],dest1[1],dest2[0],dest2[1],'blue'))

    point_list = []
    
    x_listAll = []
    y_listAll = []
    x_listBest = []
    y_listBest = []

    print("RUN GENERATIONS LOOP")

    global generation
    generation += 1
    main_tick = 0
    time = 50
    
    best_index = 0

    choose_path = 0

    while True :
        main_tick +=1

        if generation < 7:
            time = 10
        if generation >= 7 and generation < 20:
            time = 50
        if generation >= 20: 
            time = 200

        point1.draw()
        point2.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

          
        x_list = []
        y_list = []

        for n in range(population_size):
            x_list.append(points[n].x_pos)
            y_list.append(points[n].y_pos)
        x_listAll.append(x_list)
        y_listAll.append(y_list)
    
        if best_index !=0:
            if choose_path == 0:
                for n in range(len(x_listAll)):
                    x_listBest.append(x_listAll[n][best_index])
                    y_listBest.append(y_listAll[n][best_index])
                choose_path = 1

        for index, point in enumerate(points):
            output = nets[index].activate(point.dataOutput())
            i = output.index(max(output))
            #print(output[0],output[1])
            if output[0] > 0:
                point.move(2)
            if output[0] < 0:
                point.move(4)
            if output[1] > 0:
                point.move(3)
            if output[1] < 0:
                point.move(1)
            
            point.move(output)
            point.update(point.x_pos,point.y_pos)
        
            distanceToTarget= point.dataOutput()[8]
            if distanceToTarget<20:
                    succeeded_points +=1
                    best_index = index
                    #print(point_list[best_index])
                    
        remain_points = 0
        succeeded_points = 0
        point_fitness = []
        for i, point in enumerate(points):
            if point.isAlive:
                remain_points +=1
                distanceToTarget= point.dataOutput()[8]
                genomes[i][1].fitness =100-(math.sqrt(distanceToTarget))
                if point.x_pos == point1.x_pos and point.y_pos == point1.y_pos:  
                    genomes[i][1].fitness -=500
                #if point.checkCollusion(30):
                #    genomes[i][1].fitness -=50
                point_fitness.append(genomes[i][1])
                if  distanceToTarget < 20:
                    #genomes[i][1].fitness +=1000
                    dispPathState = True
                    genEnd = False
                    path_points = [x_listBest,y_listBest]
                    file = open("targetCoordinates.py","w")
                    file.write("path_points = " + str(path_points))
                    file.close()
                    print('data Writed')
                #print(math.sqrt(distanceToTarget))
                print(genomes[i][1].fitness)
                    
        for point in points:
            point.draw()
           
        pygame.draw.rect(screen,(190, 190, 190, 255),pygame.rect.Rect((0,290),(230,180)),0,0)
        pygame.draw.rect(screen,'black',pygame.rect.Rect((15,330),(200,140)),2,3)
        text_title =Text('NEAT Information',45,300,font,'black',True)
        text_generationNumber =Text(f'Generation {generation}',60,340,font,'black',True)
        text_liveNumber =Text(f'{remain_points} Points Alive',55,370,font,'black',True)      
        text_deadNumber =Text(f'{population_size-remain_points} Points Died',53,400,font,'black',True)
        text_passedTime =Text(f'{main_tick} time passed',55,430,font,'black',True)
        
        if remain_points == 0 or main_tick > time:
            pygame.draw.rect(screen,'white',pygame.rect.Rect((230,10),(1200,800)),0,0) 
            pygame.draw.rect(screen,'black',pygame.rect.Rect((230,10),(1200,800)),1,0)  
            screen.blit(mapBlack,(230,10))
            point2.draw()
            break
        if generalInfo == 2:
            pygame.draw.rect(screen,(190, 190, 190, 255),pygame.rect.Rect((400,810),(1000,50)),0,0)
            text_generalInfo2 =Text('Wait For the Generation, Press "Display Path" Button When Path Found',500,817,font,'black',True)
        point1.draw()
        point2.draw()
        
        
        pygame.display.update()
        clock.tick(90)

    

"""  

"""

screen.fill('gray')
pygame.draw.rect(screen,'white',pygame.rect.Rect((230,10),(1200,800)),0,0)    


mapPath = 'Map 1.png'  
path_points = []
if __name__ == "__main__": 

    while True:
        mapBlack = pygame.image.load(mapPath)
        pygame.draw.rect(screen,'black',pygame.rect.Rect((230,10),(1200,800)),1,0)  
        screen.blit(mapBlack,(230,10))
        
        btn_generate= Button("Generate",15,10,55,13,200,50,genbtnState)
        btn_options= Button("Options",15,70,60,13,200,50,True)
        btn_browse = Button("Browse File",15,170,45,13,200,50,True)
        btn_chooseDest = Button("Choose Destinations",15,230,15,13,200,50,destBtnState)
        btn_dispPath = Button("Display Path",15,480,47,13,200,50,dispPathState)

        pygame.draw.rect(screen,(190, 190, 190, 255),pygame.rect.Rect((0,290),(230,180)),0,0)
        pygame.draw.rect(screen,'black',pygame.rect.Rect((15,330),(200,140)),2,3)
        text_title =Text('NEAT Information',45,300,font,'black',True)
        text_generationNumber =Text(f'Generation {generation}',60,340,font,'black',True)
        text_liveNumber =Text(f'{0} Points Alive',55,370,font,'black',True)      
        text_deadNumber =Text(f'{population_size-0} Points Died',53,400,font,'black',True)
        text_passedTime =Text(f'{0} time passed',55,430,font,'black',True)
        pygame.draw.rect(screen,(190, 190, 190, 255),pygame.rect.Rect((0,125),(230,40)),0,0)
        text_fileState = Text(f'Map {mapPath} ',40,133,font,'black',True)
        
        mouse_pos = pygame.mouse.get_pos()
        
        #print(screen.get_at(mouse_pos))

        for event in pygame.event.get():
            if event.type == QUIT:
                run_main = False
                pygame.quit()
                sys.exit()
            if btn_chooseDest.check_click():
                choose_destState = True
                destBtnState = False 
                generalInfo = 1
            if btn_generate.check_click():
                genbtnState = False
                gen_swState = True

    

        if btn_dispPath.check_click():
            import targetCoordinates
            path = targetCoordinates.path_points 
            
            for index in range(len(path[0])):
                print("X COORDİNATE: ",path[0][index],"Y COORDİNATE: ",path[1][index])
                points = Point(path[0][index],path[1][index],0,0,'green')
                points.draw()

            
        
        if btn_browse.check_click():
            mapPath = chooseMap()

        if mouse_pos[0]>230 and mouse_pos[0]<1430 and mouse_pos[1]>10 and mouse_pos[1]<810 and choose_destState:
            if pygame.mouse.get_pressed()[0]:                       
                generalInfo = 1
                destCounter +=1
                if destCounter ==1:
                    dest1=[mouse_pos[0]-5,mouse_pos[1]-5]
                    print()        
                if destCounter==2:
                    dest2=[mouse_pos[0]-5,mouse_pos[1]-5]
                    genbtnState = True
                sleep(0.1)
                if destCounter == 2:
                    point2 = Point(dest2[0],dest2[1],dest1[0],dest1[1],'green')
                    point1 = Point(dest1[0],dest1[1],dest2[0],dest2[1],'green')
                    point1.update(dest1[0],dest1[1])
                    point2.update(dest2[0],dest2[1])
                    point1.draw()
                    point2.draw()
                    print(point1.x_pos,"  ",point1.y_pos)
                    destBtnState = False
                    choose_destState= False
        
        pygame.draw.rect(screen,(190, 190, 190, 255),pygame.rect.Rect((400,810),(1000,50)),0,0)
        if generalInfo == 0:
            text_generalInfo1 =Text('Choose Two Point to Generate Path,Press "Choose Destination" Button',500,817,font,'black',True) 
        if generalInfo == 1:
            text_generalInfo1 =Text('Mark Starting Point, Then Target Point And Press "Generate" Button',500,817,font,'black',True) 
        if generalInfo == 3: 
            text_generalInfo1 =Text('Path Founded, Click "Display Path" Button To Display or Save it With "Save" Button or Regenerate Again',450,817,font,'black',True)
        pygame.display.update()
        clock.tick(90)
        
        if genEnd:
            config_path = "./config-feedforward.txt"
            config = neat.config.Config(neat.DefaultGenome,
                                        neat.DefaultReproduction,
                                        neat.DefaultSpeciesSet, 
                                        neat.DefaultStagnation, 
                                        config_path)
            p = neat.Population(config)
            p.add_reporter(neat.StdOutReporter(True))
            stats = neat.StatisticsReporter()
            p.add_reporter(stats)
            
            if gen_swState:
                destBtnState = False
                generalInfo = 2
                pygame.draw.rect(screen,(190, 190, 190, 255),pygame.rect.Rect((400,810),(1000,50)),0,0)

                with open('population.pkl', 'rb') as f:
                    p = pickle.load(f)
                best_genome = p.run(run_generations,total_generations)
                print(best_genome)
                with open('population.pkl', 'wb') as f:
                    pickle.dump(p, f)
                with open('winner_genome_new.pkl', 'wb') as f:
                    pickle.dump(best_genome, f)
                gen_swState = False
                generalInfo = 3
                destBtnState = True
                dispPathState = True  