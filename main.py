import pygame
import random
import os
from config import *
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.scenes.maps import MapSystem
from src.scenes.menu import menu

# Inicializa pygame
pygame.init()

# Sistema de mapas
map_system = MapSystem()
map_system.carregar_backgrounds()

# Chama o menu (agora funcional)
escolha = menu(TELA, clock)

# Cria o jogador e o grupo
player = Player(100, 300)
player_group = pygame.sprite.Group(player)

# Grupo para inimigos e criar inimigos do mapa inicial
enemy_group = map_system.criar_inimigos_para_mapa(map_system.mapa_atual)

# Variáveis do jogo
vida = 100
oxigenio = 100

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

    # Movimento e animação do jogador
    teclas = pygame.key.get_pressed()
    player.update(teclas, LARGURA, ALTURA)

    # Atualizar inimigos - CORRIGIDO: passar LARGURA e ALTURA
    enemy_group.update(LARGURA, ALTURA)

    # Diminuir oxigênio
    oxigenio -= 0.010
    if oxigenio <= 0:
        print("Você ficou sem ar! Game Over.")
        rodando = False

    # Colisão com inimigos (usando sprite collision)
    colisoes = pygame.sprite.spritecollide(player, enemy_group, False)
    if colisoes and tempo_atual - ultimo_dano > INVENCIBILIDADE:
        vida -= 10
        ultimo_dano = tempo_atual
        print(f"Você foi atingido! Vida: {vida}")
        if vida <= 0:
            print("Sua vida chegou a zero! Game Over.")
            rodando = False

    # Colisão com bolhas
    for bolha in mapa_atual_data["bolhas"][:]:
        if player.rect.colliderect(bolha):
            oxigenio = min(100, oxigenio + 20)
            mapa_atual_data["bolhas"].remove(bolha)

    # Colisão com portas (troca de mapa)
    for porta in mapa_atual_data["portas"]:
        if porta["ativa"] and player.rect.colliderect(porta["rect"]):
            print(f"Entrando na porta para {porta['destination']}!")
            
            # Trocar mapa
            map_system.trocar_mapa(porta["destination"], player)
            mapa_atual_data = map_system.get_mapa_atual()
            
            # Recriar inimigos para o novo mapa
            enemy_group = map_system.criar_inimigos_para_mapa(map_system.mapa_atual)
            
            break

    # --- DESENHAR ELEMENTOS ---
    player_group.draw(TELA)  # jogador com sprite animado
    enemy_group.draw(TELA)   # inimigos com sprites animados

    # Bolhas
    for bolha in mapa_atual_data["bolhas"]:
        pygame.draw.circle(TELA, VERDE, bolha.center, bolha.width // 3)

    # Portas
    map_system.desenhar_portas(TELA)

    # Barras de status
    pygame.draw.rect(TELA, PRETO, (10, 10, 200, 20))
    pygame.draw.rect(TELA, CIANO, (10, 10, int(2 * oxigenio), 20))

    pygame.draw.rect(TELA, PRETO, (10, 40, 200, 20))
    pygame.draw.rect(TELA, VERMELHO, (10, 40, int(2 * vida), 20))

    # Nome do mapa atual
    font = pygame.font.SysFont(None, 36)
    nome_mapa = font.render(mapa_atual_data["name"], True, BRANCO)
    largura_texto = nome_mapa.get_width()
    max_largura = 200  # Largura máxima permitida para o texto

    if largura_texto > max_largura:
        # Se for muito largo, ajuste a fonte ou trunque o texto
        nome_mapa = font.render(mapa_atual_data["name"][:25] + "", True, BRANCO)
        largura_texto = nome_mapa.get_width()

    pos_x = LARGURA - largura_texto - 20  # 20px de margem
    TELA.blit(nome_mapa, (pos_x, 10))

    pygame.display.update()

print(os.getcwd())
pygame.quit()