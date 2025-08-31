import pygame
import random


# Inimigos (peixes)
inimigos = [pygame.Rect(random.randint(200, 700), random.randint(50, 550), 50, 30) for _ in range(3)]