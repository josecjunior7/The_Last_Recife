import pygame
import random

# Jogador
player = pygame.Rect(100, 300, 40, 40)
velocidade = 5
oxigenio = 100

# Bolhas ( ar/oxigênio )
bolhas = [pygame.Rect(random.randint(100, 700), random.randint(50, 550), 20, 20) for _ in range(5)]