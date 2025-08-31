import pygame
from config import TILE_SIZE

def carregar_fase(mapa):
    """
    Recebe um mapa (lista de strings) e retorna
    um dicionário com os objetos da fase.
    """
    objetos = {
        "paredes": [],
        "inimigos": [],
        "bolhas": [],
        "saida": None,
        "player": None
    }

    for y, linha in enumerate(mapa):
        for x, celula in enumerate(linha):
            px, py = x * TILE_SIZE, y * TILE_SIZE

            if celula == "1":  # Parede
                parede = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
                objetos["paredes"].append(parede)

            elif celula == "2":  # Inimigo
                inimigo = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
                objetos["inimigos"].append(inimigo)

            elif celula == "3":  # Bolha
                bolha = pygame.Rect(px + 20, py + 20, 20, 20)
                objetos["bolhas"].append(bolha)

            elif celula == "4":  # Posição inicial do jogador
                objetos["player"] = pygame.Rect(px, py, 40, 40)

            elif celula == "5":  # Saída
                objetos["saida"] = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)

    return objetos
