import pygame
from moviepy.editor import VideoFileClip
from pygame.locals import *
import random
import threading
import time


# Definir algunas constantes
WIDTH = 852
HEIGHT = 480
BALL_SIZE = 20
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 80
PADDLE_SPEED = 5
BALL_SPEED = 2

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Crear ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Cargar sonidos
sonido_golpe = pygame.mixer.Sound("golpe.wav")
sonido_punto = pygame.mixer.Sound("win.wav")

# Crear la bola
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED

    def update(self):
        # Mover la bola
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Comprobar colisiones con los bordes
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x

        # Comprobar colisiones con las paletas
        if pygame.sprite.spritecollide(self, paddles, False):
            self.speed_x = -self.speed_x
            sonido_golpe.play()

        # Comprobar si alguien ha anotado un punto
        if self.rect.right >= WIDTH:
            jugador1.score += 1
            self.reset()
            sonido_punto.play()
        elif self.rect.left <= 0:
            jugador2.score += 1
            self.reset()
            sonido_punto.play()
  

    def reset(self):
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED

# Crear las paletas
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0

    def update(self):
        # Mover la paleta
        self.rect.y += self.speed

        # Comprobar colisiones con los bordes
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Crear los jugadores
class Player:
    def __init__(self, x, y):
        self.score = 0
        self.paddle = Paddle(x, y)
        
    def move_up(self):
        self.paddle.speed = -PADDLE_SPEED
        
    def move_down(self):
        self.paddle.speed = PADDLE_SPEED
        
    def stop_move(self):
        self.paddle.speed = 0

jugador1 = Player(50, HEIGHT / 2)
jugador2 = Player(WIDTH-50, HEIGHT/2)
       
paddles = pygame.sprite.Group(jugador1.paddle, jugador2.paddle)
ball = Ball(WIDTH/2, HEIGHT/2)
sprites = pygame.sprite.Group(paddles, ball)
       
def mostrar_puntaje():
    font = pygame.font.Font(None, 50)
    puntaje1 = font.render(str(jugador1.score), True, WHITE)
    puntaje2 = font.render(str(jugador2.score), True, WHITE)
    screen.blit(puntaje1, (WIDTH/4, 50))
    screen.blit(puntaje2, (WIDTH-WIDTH/4, 50))
    


def mostrar_menu():

	# Carga el archivo de video
	clip = VideoFileClip('fondo6.mp4')

	clip.preview()
	# Reproduce el video en una ventana	
	# Cierra la ventana de video cuando el video ha terminado de reproducirse
	clip.close()
		
	jugar()
	



'''
	ancho = 1280
	largo = 720
	
	imagen = pygame.image.load("fondo3.gif")
	ventana = pygame.display.set_mode((ancho, largo))
	
	font = pygame.font.SysFont(None, 48)
	text = font.render('Presione espacio para jugar', True, (WHITE))
	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				elif event.key == K_SPACE:
					jugar()
		
		ventana.blit(imagen, (0, 0))
		ventana.blit(text, (ancho/2 - text.get_width()/2, largo/2 - text.get_height()/2))
		pygame.display.flip()
		  
'''



def jugar():
    # Bucle principal del juego
    while True:
        # Eventos de pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_w:
                    jugador1.move_up()
                elif event.key == pygame.K_s:
                    jugador1.move_down()
                elif event.key == pygame.K_UP:
                    jugador2.move_up()
                elif event.key == pygame.K_DOWN:
                    jugador2.move_down()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    jugador1.stop_move()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    jugador2.stop_move()

        # Actualizar objetos
        sprites.update()

        # Dibujar objetos en pantalla
        screen.fill(BLACK)
        mostrar_puntaje()
        sprites.draw(screen)

        # Actualizar pantalla
        pygame.display.flip()

mostrar_menu()
