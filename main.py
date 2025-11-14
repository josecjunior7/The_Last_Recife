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

# Chama o menu
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

# Função para trocar mapa e recriar inimigos
def trocar_mapa_e_recriar_inimigos(novo_mapa, player, map_system):
    """Troca de mapa e recria os inimigos"""
    # Remove inimigos antigos
    for enemy in enemy_group:
        enemy.kill()
    
    # Troca o mapa
    if map_system.trocar_mapa(novo_mapa, player):
        # Recria os inimigos para o novo mapa
        novos_inimigos = map_system.criar_inimigos_para_mapa(map_system.mapa_atual)
        enemy_group.add(novos_inimigos)
        print(f"Mapas trocados para {novo_mapa}. {len(novos_inimigos)} inimigos criados.")
        return True
    return False

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
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False

    # Movimento e animação do jogador
    teclas = pygame.key.get_pressed()
    player.update(teclas, LARGURA, ALTURA)

    # Atualizar inimigos
    enemy_group.update(LARGURA, ALTURA)

    # Diminuir oxigênio
    oxigenio -= 0.05
    if oxigenio <= 0:
        print("Você ficou sem ar! Game Over.")
        rodando = False

    # Colisão com inimigos
    colisoes = pygame.sprite.spritecollide(player, enemy_group, False)
    if colisoes and tempo_atual - ultimo_dano > INVENCIBILIDADE:
        vida -= 10
        ultimo_dano = tempo_atual
        print(f"Você foi atingido! Vida: {vida}")
        
        if vida <= 0:
            print("Sua vida chegou a zero! Game Over.")
            rodando = False

    # Colisão com bolhas
    bolhas_para_remover = []
    for bolha in mapa_atual_data["bolhas"]:
        if player.rect.colliderect(bolha):
            oxigenio = min(100, oxigenio + 20)
            bolhas_para_remover.append(bolha)
            print("Bolha coletada! Oxigênio recuperado.")
    
    # Remove bolhas coletadas
    for bolha in bolhas_para_remover:
        if bolha in mapa_atual_data["bolhas"]:
            mapa_atual_data["bolhas"].remove(bolha)

    # Colisão com portas (troca de mapa)
    for porta in mapa_atual_data["portas"]:
        if porta["ativa"] and player.rect.colliderect(porta["rect"]):
            print(f"🚪 Entrando na porta para {porta['destination']}!")
            
            # Trocar mapa e recriar inimigos
            if trocar_mapa_e_recriar_inimigos(porta["destination"], player, map_system):
                mapa_atual_data = map_system.get_mapa_atual()
            
            break

    # Colisão com saída (opcional - para vencer o jogo)
    if "saida" in mapa_atual_data and player.rect.colliderect(mapa_atual_data["saida"]):
        print("Você encontrou a saída! Vitória!")
        rodando = False

    # --- DESENHAR ELEMENTOS ---
    
    # Desenhar portas primeiro (para ficarem atrás dos sprites)
    map_system.desenhar_portas(TELA)
    
    # Desenhar bolhas
    for bolha in mapa_atual_data["bolhas"]:
        pygame.draw.circle(TELA, CIANO, bolha.center, bolha.width // 3)
        # Efeito visual para bolhas
        pygame.draw.circle(TELA, BRANCO, bolha.center, bolha.width // 4)
    
    # Desenhar saída se existir
    if "saida" in mapa_atual_data:
        pygame.draw.rect(TELA, AMARELO, mapa_atual_data["saida"], 3)
        font_saida = pygame.font.SysFont(None, 24)
        texto_saida = font_saida.render("SAÍDA", True, AMARELO)
        TELA.blit(texto_saida, (mapa_atual_data["saida"].x + 10, mapa_atual_data["saida"].y + 30))
    
    # Desenhar sprites (player e inimigos)
    player_group.draw(TELA)
    enemy_group.draw(TELA)

    # --- INTERFACE DO USUÁRIO ---
    
    # Barra de oxigênio
    pygame.draw.rect(TELA, CINZA, (10, 10, 204, 24), 2)  # Borda
    pygame.draw.rect(TELA, PRETO, (12, 12, 200, 20))     # Fundo
    cor_oxigenio = CIANO if oxigenio > 30 else VERDE   # Muda cor se estiver baixo
    pygame.draw.rect(TELA, cor_oxigenio, (12, 12, int(2 * oxigenio), 20))
    
    # Texto oxigênio
    font_ui = pygame.font.SysFont(None, 20)
    texto_oxigenio = font_ui.render("Oxigênio", True, BRANCO)
    TELA.blit(texto_oxigenio, (15, 12))
    
    # Barra de vida
    pygame.draw.rect(TELA, CINZA, (10, 40, 204, 24), 2)  # Borda
    pygame.draw.rect(TELA, PRETO, (12, 42, 200, 20))     # Fundo
    cor_vida = VERDE if vida > 30 else VERMELHO          # Muda cor se estiver baixo
    pygame.draw.rect(TELA, cor_vida, (12, 42, int(2 * vida), 20))
    
    # Texto vida
    texto_vida = font_ui.render("Vida", True, BRANCO)
    TELA.blit(texto_vida, (15, 42))

    # Nome do mapa atual
    font_mapa = pygame.font.SysFont(None, 28)
    nome_mapa = font_mapa.render(mapa_atual_data["name"], True, BRANCO)
    largura_texto = nome_mapa.get_width()
    
    # Posiciona no canto superior direito
    pos_x = LARGURA - largura_texto - 20
    pygame.draw.rect(TELA, (0, 0, 0, 128), (pos_x - 10, 5, largura_texto + 20, 35))
    TELA.blit(nome_mapa, (pos_x, 15))

    # Contador de inimigos restantes
    texto_inimigos = font_ui.render(f"Inimigos: {len(enemy_group)}", True, BRANCO)
    TELA.blit(texto_inimigos, (LARGURA - 120, 50))

    # Instruções
    texto_instrucoes = font_ui.render("WASD: Mover | ESC: Sair", True, BRANCO)
    TELA.blit(texto_instrucoes, (LARGURA - 200, ALTURA - 30))

    pygame.display.update()

pygame.quit()