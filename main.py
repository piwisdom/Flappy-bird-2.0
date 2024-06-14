from pygame import * 
from random import randint

# superclass 
class Main(): 
        def __init__(self, file, x, y, speed): 
                self.speed = speed 
                self.image = transform.scale(image.load(file), (50, 50))
                self.rect = self.image.get_rect()
                self.rect.x = x 
                self.rect.y = y 
        
        def update(self): 
                screen.blit(self.image, (self.rect.x, self.rect.y))
                

# player
class Miner(Main): 
        def __init__(self, file, x, y, speed):
                super().__init__(file, x, y, speed)
                self.angle = 0 
                
        def update(self): 
                rotated_img = transform.rotate(self.image, self.angle)
                screen.blit(rotated_img, (self.rect.x, self.rect.y))
                self.angle += self.speed
                self.angle = min(0, self.angle)
                
        def controls(self):
                keys = key.get_pressed()
                if keys[K_SPACE] and self.rect.y > 0: 
                        self.rect.y -= self.speed * 2 
                        self.angle = 15
                else: 
                        self.rect.y += self.speed
                        self.angle = min(-15, self.angle + self.speed)

# pipe class
class Pipe: 
        def __init__(self, x, y, speed): 
                self.speed = speed
                self.width = 65
                self.height = randint(100, 300)
                self.top_rect = Rect(x, y, self.width, self.height)
                self.bottom_rect = Rect(x, y + self.height + 200, self.width, HEIGHT - self.height - 100)
        
        def update(self): 
                global score
                self.top_rect.x -= self.speed
                self.bottom_rect.x -= self.speed
                if self.top_rect.right < 0:
                        score += 1
                        self.reset()
        
        def draw_pipe(self): 
                draw.rect(screen, white, self.top_rect)
                draw.rect(screen, white, self.bottom_rect)
        
        def  reset(self): 
                self.height = randint(100, 300)
                self.top_rect = Rect(WIDTH, 0, self.width, self.height)
                self.bottom_rect = Rect(WIDTH,  self.height + 200, self.width, HEIGHT - self.height - 100)
        
font.init()

WIDTH = 450
HEIGHT =  600
white = (255, 255, 255)
score = 0 
score_font = font.Font(None, 45)
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Flappy Bird 2.0")
clock = time.Clock()
#
background = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))

miner = Miner("miner.png", 100, 300, 10)

pipes  = [Pipe(WIDTH + i *200 , 0,  5) for i in range(2)]

run  = True 
while run: 
        for e in event.get(): 
                if e.type == QUIT:
                        quit() 
                        run = False
        
        screen.blit(background, (0, 0))
        miner.update()
        miner.controls()
        
        for pipe in pipes: 
                pipe.update()
                pipe.draw_pipe()
                if miner.rect.colliderect(pipe.top_rect) or miner.rect.colliderect(pipe.bottom_rect):
                        print("Game Over!")
                        run  = False 
                
                if pipes[0].top_rect.right < 0: 
                        pipes.pop(0)
                        pipes.append(Pipe(WIDTH, 0, 5))
                        score += 1 
                
                if miner.rect.y > HEIGHT: 
                        run  = False
                        
                score_text = score_font.render("Score:"+str(score), True, white)
                screen.blit(score_text, (10, 10))
        
        display.update() 
        clock.tick(20)