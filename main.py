# main.py (seu código atualizado)
import pygame
import random
import os
from config import *
from src.entities.player import *
from src.entities.enemy import *
from src.scenes.maps import MapSystem
from src.scenes.menu import menu


# Inicializa pygame
pygame.init()

# Sistema de mapas
map_system = MapSystem()
map_system.carregar_backgrounds()

# Menu inicial
escolha = menu(TELA, clock)

# Variáveis do jogador
player = pygame.Rect(100, 300, 40, 60)  # Posição inicial será ajustada pelo mapa
vida = 100
oxigenio = 100
velocidade = 5

# Invencibilidade
INVENCIBILIDADE = 1000
ultimo_dano = 0

# Loop principal
rodando = True
while rodando:
    clock.tick(FPS)
    
    # Usa o background do mapa atual
    background = map_system.get_background_atual()
    if background:
        TELA.blit(background, (0, 0))
    else:
        TELA.fill(PRETO)
    
    tempo_atual = pygame.time.get_ticks()
    mapa_atual_data = map_system.get_mapa_atual()

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and player.left > 0:
        player.x -= velocidade
    if teclas[pygame.K_RIGHT] and player.right < LARGURA:
        player.x += velocidade
    if teclas[pygame.K_UP] and player.top > 0:
        player.y -= velocidade
    if teclas[pygame.K_DOWN] and player.bottom < ALTURA:
        player.y += velocidade

    # Diminuir oxigênio
    oxigenio -= 0.05
    if oxigenio <= 0:
        print("Você ficou sem ar! Game Over.")
        rodando = False

    # Movimentar inimigos
    for inimigo in mapa_atual_data["inimigos"]:
        inimigo.x += random.choice([-2, 2])
        if inimigo.left < 0:
            inimigo.left = 0
        if inimigo.right > LARGURA:
            inimigo.right = LARGURA

    # Colisão com inimigos
    for inimigo in mapa_atual_data["inimigos"]:
        if player.colliderect(inimigo):
            if tempo_atual - ultimo_dano > INVENCIBILIDADE:
                vida -= 10
                ultimo_dano = tempo_atual
                print(f"Você foi atingido! Vida: {vida}")
                if vida <= 0:
                    print("Sua vida chegou a zero! Game Over.")
                    rodando = False

    # Colisão com bolhas
    for bolha in mapa_atual_data["bolhas"][:]:
        if player.colliderect(bolha):
            oxigenio = min(100, oxigenio + 20)
            mapa_atual_data["bolhas"].remove(bolha)

    # Colisão com portas (troca de mapa)
    for porta in mapa_atual_data["portas"]:
        if porta["ativa"] and player.colliderect(porta["rect"]):
            print(f"Entrando na porta para {porta['destination']}!")
            map_system.trocar_mapa(porta["destination"], player)
            # Recarrega os dados do novo mapa
            mapa_atual_data = map_system.get_mapa_atual()
            break  # Sai do loop após trocar de mapa

    # Colisão com saída (vitória)
    #if player.colliderect(mapa_atual_data["saida"]):
        #print("Parabéns! Você passou de fase.")
        #rodando = False

    # --- Desenhar elementos ---
    pygame.draw.rect(TELA, BRANCO, player)  # Jogador
    
    # Inimigos
    for inimigo in mapa_atual_data["inimigos"]:
        pygame.draw.rect(TELA, VERMELHO, inimigo)
    
    # Bolhas
    for bolha in mapa_atual_data["bolhas"]:
        pygame.draw.circle(TELA, VERDE, bolha.center, bolha.width//2)
    
    # Saída
    #pygame.draw.rect(TELA, AMARELO, mapa_atual_data["saida"])
    
    # Portas (agora desenhadas pelo sistema de mapas)
    map_system.desenhar_portas(TELA)

    # Barra de oxigênio
    pygame.draw.rect(TELA, PRETO, (10, 10, 200, 20))
    pygame.draw.rect(TELA, CIANO, (10, 10, int(2 * oxigenio), 20))

    # Barra de vida
    pygame.draw.rect(TELA, PRETO, (10, 40, 200, 20))
    pygame.draw.rect(TELA, VERMELHO, (10, 40, int(2 * vida), 20))

    # Nome do mapa atual
    font = pygame.font.SysFont(None, 36)
    nome_mapa = font.render(mapa_atual_data["name"], True, BRANCO)
    TELA.blit(nome_mapa, (LARGURA - 200, 10))

    pygame.display.update()

print(os.getcwd())


pygame.quit()