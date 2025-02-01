import pygame
import sys
import random

#Inicializar
pygame.init()

#Definir colores
BLACK = (0,0,0)
WHITE = (255,255,255)

METEOR_QUANTITY = 50

####Creación de clases#####
#Clase Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert() 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speed_x = 0 #velocidad del jugador en x

    def change_speed(self, x):
        '''modificador de la velocidad en eje X según variable x'''
        self.speed_x += x

    def update(self):
        self.rect.x += self.speed_x #movimiento en x de la nave
        #keep player within horizontal bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 900:
            self.rect.right = 900
        player.rect.y = 510 #posicion fija de la nave abajo
        
#Clase meteoro
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("meteor.png").convert() #meteor.png
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

#Clase laser

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("laser.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5

#Tamaño de pantalla
size = (900,600)

#Definir el screen
screen = pygame.display.set_mode(size)

#Creamos el reloj
clock = pygame.time.Clock()

#bandera principal
done = False

#Score
score = 0

all_sprite_list = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
laser_list = pygame.sprite.Group()

#Creamos los meteoros
for i in range(METEOR_QUANTITY):
    meteor = Meteor()
    meteor.rect.x = random.randrange(880)
    meteor.rect.y = random.randrange(450)

    #agregamos a las dos listas
    meteor_list.add(meteor)
    all_sprite_list.add(meteor)
    

#Iniciamos instancia jugador y la añadimos a la lista de todos los sprites
player = Player()
all_sprite_list.add(player)

#Cargar sonido
sound = pygame.mixer.Sound("laser5.ogg")

#Quitar el mouse
pygame.mouse.set_visible(0)

#Loop principal
while not done:
    #Detectar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_speed(-5) #velocidad a la izquierda
            if event.key == pygame.K_RIGHT:
                player.change_speed(5) #velocidad a la derecha
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            #disparo con barra espaciadora
            if event.key == pygame.K_SPACE:
                laser = Laser()
                laser.rect.x = player.rect.x  + 45 #centro en X de la nave
                laser.rect.y = player.rect.y - 20 #Punta de la nave

                #Agregamos los laseres a su lista y lista de sprites
                all_sprite_list.add(laser)
                laser_list.add(laser)
                sound.play() #reproducir sonido de laser
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.change_speed(5) #velocidad a la izquierda
            if event.key == pygame.K_RIGHT:
                player.change_speed(-5) #velocidad a la derecha

    
    all_sprite_list.update()

    #Iteramos de entre todos los laseres y detectar colisiones
    for laser in laser_list:
        meteor_hit_list = pygame.sprite.spritecollide(laser, meteor_list, True)
        #Una vez que un laser le pegue a un meteoro tiene que desaparecer
        for meteor in meteor_hit_list:
            all_sprite_list.remove(laser)
            laser_list.remove(laser)
            score += 1
            print(score)
        
        #Si el laser pasa el borde superior hay que removerlo de la pantalla
        if laser.rect.y < -10:
            all_sprite_list.remove(laser)
            laser_list.remove(laser)
  

    #Primero se coloriza la pantalla
    screen.fill(WHITE)

    #Dibujado de objetos
    all_sprite_list.draw(screen)
    
    
    #Refresca la pantalla completa
    pygame.display.flip()

    #Ticks de FPS mientras más alto, la pantalla se refrescará a tantos FPS por segundo. Normalmente se deja entre 30 y 60
    clock.tick(60)