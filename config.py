import pygame

# Configurações da tela
LARGURA, ALTURA = 1200, 720
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("O Último Recife")
FPS = 60
clock = pygame.time.Clock()

# Grid
TILE_SIZE = 60

# Cores (RGB)
AZUL = (0, 100, 200)
BRANCO = (255, 255, 255)
VERMELHO = (200, 50, 50)
VERDE = (50, 200, 50)
