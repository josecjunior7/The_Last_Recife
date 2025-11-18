# config.py
import pygame

# Configurações da tela
LARGURA = 1280
ALTURA = 720
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("O Último Recife")
FPS = 60
clock = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
CIANO = (0, 255, 255)
MARROM = (139, 69, 19)
DOURADO = (255, 215, 0)
CINZA = (128, 128, 128)

ENERGIA_ESCURA = (75, 0, 130)  # Roxo escuro