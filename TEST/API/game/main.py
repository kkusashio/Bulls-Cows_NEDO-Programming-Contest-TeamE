import pygame
from pygame.locals import *
import os
import sys
import algo


SCREEN_RECT = Rect(0, 0, 640, 480)
CS = 32
SCREEN_NCOL = SCREEN_RECT.width//CS
SCREEN_NROW = SCREEN_RECT.height//CS
SCREEN_CENTER_X = SCREEN_RECT.width//2//CS
SCREEN_CENTER_Y = SCREEN_RECT.height//2//CS
black=(0,0,0)

def load_image(filename):
    image = pygame.image.load(filename)
    image = image.convert_alpha()
    return image

def get_image(sheet, x, y, width, height, useColorKey=False):
    image = pygame.Surface([width, height])
    image.blit(sheet, (0, 0), (x, y, width, height))
    image = image.convert()
    if useColorKey:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    #image = pygame.transform.scale(image, (32*2, 32*2))
    return image

DIR_DOWN = 0
DIR_LEFT = 1
DIR_RIGHT = 2
DIR_UP = 3
ANIM_WAIT_COUNT = 24
MOVE_VELOCITY = 4

class Player(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        sheet = load_image(filename)
        self.images = [[], [], [], []]
        for row in range(0, 4):
            for col in [0, 1, 2, 1]:
                self.images[row].append(get_image(sheet, 0 + 32 * col, 0 + 32 * row, 32, 32, True))
        self.image = self.images[DIR_DOWN][0]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_CENTER_X * CS
        self.rect.y = SCREEN_CENTER_Y * CS
        self.frame = 0
        self.anim_count = 0
        self.dir = DIR_DOWN
        self.wx, self.wy = 11, 93
        self.map = None
        self.moving = False
        self.vx, self.vy = 0, 0
        self.px, self.py = 0, 0
    def set_map(self, map_):
        self.map = map_
    def handle_keys(self):
        if self.moving:
            self.px += self.vx
            self.py += self.vy
            if self.px % CS == 0 and self.py % CS == 0:
                self.moving = False
                self.wx += self.px // CS
                self.wy += self.py // CS
                self.vx, self.vy = 0, 0
                self.px, self.py = 0, 0
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_DOWN]:
                self.dir = DIR_DOWN
                if self.map.can_move_at(self.wx, self.wy + 1):
                    self.moving = True
                    self.vy = MOVE_VELOCITY
            elif pressed_keys[K_LEFT]:
                self.dir = DIR_LEFT
                if self.map.can_move_at(self.wx - 1, self.wy):
                    self.moving = True
                    self.vx = -MOVE_VELOCITY
            elif pressed_keys[K_RIGHT]:
                self.dir = DIR_RIGHT
                if self.map.can_move_at(self.wx + 1, self.wy):
                    self.moving = True
                    self.vx = MOVE_VELOCITY
            elif pressed_keys[K_UP]:
                self.dir = DIR_UP
                if self.map.can_move_at(self.wx, self.wy - 1):
                    self.moving = True
                    self.vy = -MOVE_VELOCITY
    def update(self):
        self.handle_keys()
        self.anim_count += 1
        if self.anim_count >= ANIM_WAIT_COUNT:
            self.anim_count = 0
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
        self.image = self.images[self.dir][self.frame]

class Map:
    def __init__(self, screen, filename, player):
        self.ncol = 0
        self.nrow = 0
        self.screen = screen
        self.player = player
        self.defaultPaletteIdx = 0
        self.defaultIdx = 0
        self.mapDataBottom = []
        self.mapDataTop = []
        self.mapchipDatas = []
        self.loadMap(filename)
    def loadMap(self, mapFileName):
        # load map file
        mapchipDefFiles = []
        with open(mapFileName, "r") as fi:
            num_def_file = int(fi.readline())
            for i in range(num_def_file):
                def_f = fi.readline().strip()
                mapchipDefFiles.append(def_f)
            self.defaultPaletteIdx, self.defaultIdx = [int(tok) for tok in fi.readline().split(",")]
            self.ncol, self.nrow = [int(tok) for tok in fi.readline().split(",")]
            def readMapData(mapData):
                for row in range(self.nrow):
                    colDatas = [tuple(int(tok2) for tok2 in tok.split(":")) for tok in fi.readline().split(",")]
                    for col, colData in enumerate(colDatas):
                        mapData[row][col] = colData
            # bottom
            line = fi.readline()
            if not line.startswith("Bottom"):
                print("Format Error!")
            self.mapDataBottom = [[(self.defaultPaletteIdx, self.defaultIdx) for col in range(self.ncol)] for row in range(self.nrow)]
            readMapData(self.mapDataBottom)
            # top
            line = fi.readline()
            if not line.startswith("Top"):
                print("Format Error!")
            self.mapDataTop = [[(self.defaultPaletteIdx, self.defaultIdx) for col in range(self.ncol)] for row in range(self.nrow)]
            readMapData(self.mapDataTop)
        # load mapchip definition file
        self.mapchipDatas = []
        for mapchipDefFile in mapchipDefFiles:
            with open(mapchipDefFile, "r") as fi:
                png_f = fi.readline().strip()
                data = MapchipData()
                data.mapchipFile = png_f
                self.mapchipDatas.append(data)
                data.sheet = load_image(os.path.join("data", png_f))
                data.ncol, data.nrow = [int(tok) for tok in fi.readline().split(",")]
                for row in range(data.nrow):
                    for col in range(data.ncol):
                        idx, movable = [int(tok) for tok in fi.readline().split(",")]
                        data.mapchipData[idx] = movable
    def to_xy(self, data, idx):
        return (idx % data.ncol, idx // data.ncol)
    def drawImage(self, paletteIdx, idx, sx, sy, px, py):
        data = self.mapchipDatas[paletteIdx]
        x, y = self.to_xy(data, idx)
        self.screen.blit(data.sheet, (sx * CS + px, sy * CS + py), (x * CS, y * CS, CS, CS))
    def draw(self):
        px = -self.player.px
        py = -self.player.py
        screen_wx = self.player.wx - SCREEN_CENTER_X
        screen_wy = self.player.wy - SCREEN_CENTER_Y
        for sy in range(-1, SCREEN_NROW+1):
            for sx in range(-1, SCREEN_NCOL+1):
                wx = screen_wx + sx
                wy = screen_wy + sy
                if not (0 <= wx < self.ncol) or not (0 <= wy < self.nrow):
                    self.drawImage(self.defaultPaletteIdx, self.defaultIdx, sx, sy, px, py)
                else:
                    paletteIdx, idx = self.mapDataBottom[wy][wx]
                    self.drawImage(paletteIdx, idx, sx, sy, px, py)
                    paletteIdx, idx = self.mapDataTop[wy][wx]
                    self.drawImage(paletteIdx, idx, sx, sy, px, py)
    def can_move_at(self, wx, wy):
        if not (0 <= wx < self.ncol) or not (0 <= wy < self.nrow):
            return False
        paletteIdx, idx = self.mapDataTop[wy][wx]
        data = self.mapchipDatas[paletteIdx]
        movable = data.mapchipData[idx]
        if movable:
            return True
        else:
            return False

class MapchipData:
    def __init__(self):
        self.sheet = None
        self.mapchipFile = ""
        self.ncol = 0
        self.nrow = 0
        self.mapchipData = {}
        self.startRow = 0

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale),int(height*scale)))
        #self.image = pygame.transform.scale(image,(45,45))
        #self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked = False
    def draw(self):
        action = False
        #get mouse pos
        pos = pygame.mouse.get_pos()
        #check mouseover
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #0 left click
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action

class gamestate():
    def __init__(self):
        self.state='intro'

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'
        #screen.blit(menu_image,(0,0))
        screen.blit(background,(0,0))
        myFont = pygame.font.SysFont("Times New Roman", 32)
        myFont2 = pygame.font.SysFont("Times New Roman", 16)
        title = myFont.render("HIT AND BULL RPG",1, black)
        instructions = myFont2.render("CLICK TO PLAY", 1, black)
        screen.blit(title, (200, 150))
        screen.blit(instructions, (250, 300))
        #screen.blit(ready_text,(screen_width/2,screen_height))
        pygame.display.flip()
    
    #methodに入れておく
    def main_game(self):
        #for event in pygame.event.get():
        #   if event.type == pygame.QUIT:
        #        pygame.quit()
        #screen.blit(background,(0,0))
        screen.fill((0, 255, 0))
        fieldMap.draw()
        group.update()
        group.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    self.state = 'HB_game'
        #pygame.display.flip()

    def HB_game(self):
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        myFont = pygame.font.SysFont("Times New Roman", 32)
        screen.blit(game_bg,(0,0))
        input_number_display = myFont.render(' '.join(input_number[:5]),1, black)
        screen.blit(input_number_display, (100, 150))
        if clear_button.draw():
            input_number.clear()
        if enter_button.draw():
            algo.main()
            input_number.clear()
        if button_1.draw():
            input_number.append("1")
        if button_2.draw():
            input_number.append("2")
        if button_3.draw():
            input_number.append("3")
        if button_4.draw():
            input_number.append("4")
        if button_5.draw():
            input_number.append("5")
        if button_6.draw():
            input_number.append("6")
        if button_7.draw():
            input_number.append("7")
        if button_8.draw():
            input_number.append("8")
        if button_9.draw():
            input_number.append("9")
        if button_0.draw():
            input_number.append("0")
        if button_a.draw():
            input_number.append("a")
        if button_b.draw():
            input_number.append("b")
        if button_c.draw():
            input_number.append("c")
        if button_d.draw():
            input_number.append("d")
        if button_e.draw():
            input_number.append("e")
        if button_f.draw():
            input_number.append("f")
        
        #screen.blit(menu_image,(0,0))
        #screen.blit(background,(0,0))
        pygame.display.flip()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'HB_game':
            self.HB_game()

#general setup
pygame.init()
clock = pygame.time.Clock()
game_state=gamestate()#class→オブジェクト

#game screen
#screen_width = 1920
#screen_height = 1080
#screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Sprites")
pygame.mouse.set_visible(True)

screen = pygame.display.set_mode(SCREEN_RECT.size)
pygame.display.set_caption("Short Tale Story")
player = Player(os.path.join("data", "pipo-charachip021.png"))
group = pygame.sprite.RenderUpdates()
group.add(player)
fieldMap = Map(screen, "field.map", player)
player.set_map(fieldMap)
clock = pygame.time.Clock()

#image loading
ready_text = pygame.image.load("ready.png")
menu_image = pygame.image.load("menu_image.png")
background = pygame.image.load("background.png")
game_bg=pygame.image.load("white.png")
clear = pygame.image.load("button.png")
enter = pygame.image.load("button.png")
button1 = pygame.image.load("button/button1.jpg").convert_alpha()
button2 = pygame.image.load("button/button2.jpg").convert_alpha()
button3 = pygame.image.load("button/button3.jpg").convert_alpha()
button4 = pygame.image.load("button/button4.jpg").convert_alpha()
button5 = pygame.image.load("button/button5.jpg").convert_alpha()
button6 = pygame.image.load("button/button6.jpg").convert_alpha()
button7 = pygame.image.load("button/button7.jpg").convert_alpha()
button8 = pygame.image.load("button/button8.jpg").convert_alpha()
button9 = pygame.image.load("button/button9.jpg").convert_alpha()
button0 = pygame.image.load("button/button0.jpg").convert_alpha()
buttona = pygame.image.load("button/buttona.jpg").convert_alpha()
buttonb = pygame.image.load("button/buttonb.jpg").convert_alpha()
buttonc = pygame.image.load("button/buttonc.jpg").convert_alpha()
buttond = pygame.image.load("button/buttond.jpg").convert_alpha()
buttone = pygame.image.load("button/buttone.jpg").convert_alpha()
buttonf = pygame.image.load("button/buttonf.jpg").convert_alpha()

clear_button = Button(50,400, clear, 0.35)
enter_button = Button(200, 400, enter, 0.35)
button_1= Button(50, 200, button1,0.35)
button_2= Button(100, 200, button2,0.35)
button_3= Button(150,200, button3,0.35)
button_4= Button(200,200, button4,0.35)
button_5= Button(50,250, button5,0.35)
button_6= Button(100,250, button6,0.35)
button_7= Button(150,250, button7,0.35)
button_8= Button(200,250, button8,0.35)
button_9= Button(50,300, button9,0.35)
button_0= Button(100,300, button0,0.35)
button_a= Button(150,300, buttona,0.35)
button_b= Button(200,300, buttonb,0.35)
button_c= Button(50,350, buttonc,0.35)
button_d= Button(100,350, buttond,0.35)
button_e= Button(150,350, buttone,0.35)
button_f= Button(200,350, buttonf,0.35)

input_number=[]
#if __name__ == '__main__':
#    main()

while True:
    game_state.state_manager()
    clock.tick(60)