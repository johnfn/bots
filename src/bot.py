#TODO: separate drawing from moving

import random
import pygame
import operator
from pygame.locals import *

UP, LEFT, RIGHT, DOWN = 0,1,2,3
FALSE, TRUE = 0, 1
allBots = []


pygame.init()


window = pygame.display.set_mode((500,500))
pygame.display.set_caption("bots!")

screen = pygame.display.get_surface()



def isNum(x):
    stripped=""
    try:
        stripped = str(int(x))
        return True
    except: 
        return False

def removeNewline(str):
    return str.replace('\n', '')

def draw_rect(x, y, w, c=(255,0,0)):
    gfx = pygame.Surface([15,15])
    gfx.fill((255,0,0))
    
    rect = gfx.get_rect()
    rect.x = x
    rect.y = y

    gfx = pygame.Surface([w,w])
    gfx.fill(c)
    
    screen.blit(gfx, rect)


class bul:
    def __init__(self, x, y, dir):
        self.x=x
        self.y=y
        self.dir=dir

    def update(self):
        draw_rect(self.x, self.y, 2, (255,255,255))
        if (self.dir==UP): self.y -= 1
        if (self.dir==LEFT): self.x -=1
        if (self.dir==RIGHT):self.x +=1
        if (self.dir==DOWN):self.y +=1



class bot:
    def __init__(self, x, y, code):
        self.health = 100
        self.buls = []
        self.cooldown = 0
        self.cooldownMin = 25

        self.x=x
        self.y=y
        self.w=15

        self.vars = {}
        
        self.keywords = ["rand", "pass"]
        
        self.specialVars = ["x", "y", "ex", "ey"]

        self.evaluate( "(progn (set x 0) (set y 0) (set ex 100) (set ey 100))")

        code = removeNewline(code) #TODO: This doesn't work at all
        self.code = code


    def shoot(self, dir):
        b = bul(self.x+self.w/2, self.y+self.w/2, dir)
        self.buls.append(b)



    def split(self, str):
        while str.find("  ") != -1: str.replace("  ", " ")
        if (str[0] != '('): return [str]
        
        str = str[1:-1]
        str = " " + str + " "
    
        depth = [0]*len(str)
        parens = 0
        for i, letter in enumerate(str):
            if letter == '(': parens += 1
            if letter == ')': parens -= 1
        
            if letter==" " and parens==0:
                depth[i] = 0
            else:
                depth[i] = parens+1

        res = [""]
        for index, i in enumerate(depth):
            if i == 0:
                res.append("")
            else:
                res[-1]+= str[index]
        return res[1:-1]

    
    def evaluate(self,expression):
        parts = self.split(expression)
        
        if len(parts) == 1:
            if isNum(parts[0]):
                return int(parts[0])
            else:
                if parts[0] in self.keywords:
                    if parts[0] == "rand": return random.random()
                    if parts[0] == "pass": return 0
                return self.vars[parts[0]][1] 

        
        function = parts[0]

        if function == "+": return reduce(operator.add,[self.evaluate(x) for x in parts[1:]])
        if function == "-": return reduce(operator.sub,[self.evaluate(x) for x in parts[1:]])
        if function == "*": return reduce(operator.mul,[self.evaluate(x) for x in parts[1:]])
        if function == "/": return reduce(operator.div,[self.evaluate(x) for x in parts[1:]])


        #conditionals

        if function == "=":
            if self.evaluate(parts[1]) == self.evaluate(parts[2]):
                return TRUE
            return FALSE

        if function == ">":
            if self.evaluate(parts[1]) > self.evaluate(parts[2]):
                return TRUE
            return FALSE
        if function == "<":
            if self.evaluate(parts[1]) <  self.evaluate(parts[2]):
                return TRUE
            return FALSE


        #variables

        if function == "set": 
            print "Setting", parts[1], "to", self.evaluate(parts[2])
            self.vars[parts[1]] = [parts[2], self.evaluate(parts[2])]
            return 0

        #awkward

        if function == "progn": 
            for x in parts[1:-1]: 
                self.evaluate(x)
            return self.evaluate(parts[-1])
        
        if function == "print":
            print " ".join([str(self.evaluate(x)) for x in parts[1:]])
            return 0
        
        if function == "shoot":
            if self.cooldown > self.cooldownMin:
                dir = self.evaluate(parts[1]) % 4
                self.shoot(dir)
                self.cooldown = 0
                return TRUE
            return FALSE

        if function == "if":
            if self.evaluate(parts[1]):
                return self.evaluate(parts[2])
            else:
                return self.evaluate(parts[3])


        raise NameError("Unknown function: " + function)
        return 5

    """Moves the bot 1 time unit forward, but does not draw it."""
    def update(self):
        self.cooldown += 1
        self.evaluate(self.code)
        
        for v in self.specialVars:
            if v.upper() == "X": self.x = self.evaluate(self.vars["x"][0])
            if v.upper() == "Y": self.y = self.evaluate(self.vars["y"][0])



    """Draws the bot in it's current position."""
    def draw(self):
        draw_rect(self.x, self.y, self.w)

        for b in self.buls: 
            b.update()
            if b.x > 500 or b.x < 0 or b.y > 500 or b.y < 0: self.buls.remove(b)



b = bot( 20, 20, "(if (< x ex) (set x (+ x 1)) (shoot 2))")

b.update()

def runGame():
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == QUIT:
                play = False
            if event.type == KEYDOWN:
                b.shoot(RIGHT)

        pygame.time.wait(1)
        screen.fill((0,0,0))
    
        b.update()
        b.draw()

        pygame.display.flip()



runGame()

