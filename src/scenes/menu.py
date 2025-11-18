import pygame
import sys
from config import *

pygame.init()

# --- CARREGAR IMAGEM DE FUNDO ---
background = pygame.image.load("assets/images/Background.png").convert()
background = pygame.transform.scale(background, (LARGURA, ALTURA))

# --- CARREGAR IMAGENS DOS BOTÕES ---
img_novo_jogo = pygame.image.load("assets/images/NewGame.png").convert_alpha()
img_sair = pygame.image.load("assets/images/Out.png").convert_alpha()

# --- ESCALAS INDIVIDUAIS ---
escala_novo = 0.25   # escala do botão "Novo Jogo"
escala_sair = 0.15   # escala do botão "Sair"

# --- REDIMENSIONAMENTO COM ESCALAS INDIVIDUAIS ---
largura_novo, altura_novo = img_novo_jogo.get_size()
img_novo_jogo = pygame.transform.scale(
    img_novo_jogo,
    (int(largura_novo * escala_novo), int(altura_novo * escala_novo))
)

largura_sair, altura_sair = img_sair.get_size()
img_sair = pygame.transform.scale(
    img_sair,
    (int(largura_sair * escala_sair), int(altura_sair * escala_sair))
)

# --- POSIÇÕES INDIVIDUAIS DOS BOTÕES ---
pos_novo_jogo = (500, 360)  # (x, y)
pos_sair = (550, 535)       # (x, y)

# --- FUNÇÃO DO MENU PRINCIPAL ---
def menu(tela, clock):
    rodando = True
    while rodando:
        tela.blit(background, (0, 0))

        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- LÓGICA DO MOUSE ---
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        # --- DEFINIR RECTS NAS POSIÇÕES ESPECÍFICAS ---
        jogar_rect = img_novo_jogo.get_rect(topleft=pos_novo_jogo)
        sair_rect = img_sair.get_rect(topleft=pos_sair)

        # --- DESENHA BOTÕES ---
        tela.blit(img_novo_jogo, jogar_rect)
        tela.blit(img_sair, sair_rect)

        # --- CLIQUES ---
        if jogar_rect.collidepoint(mouse) and clique[0]:
            return "selecao_personagem"  # Agora vai para seleção de personagem

        if sair_rect.collidepoint(mouse) and clique[0]:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

# --- FUNÇÃO DE SELEÇÃO DE PERSONAGEM ---
def selecao_personagem(tela, clock):
    # Carregar imagens dos personagens (você precisará criar essas imagens)
    try:
        img_masculino = pygame.image.load("assets/images/personagem_masculino.png").convert_alpha()
        img_feminino = pygame.image.load("assets/images/personagem_feminino.png").convert_alpha()
    except:
        # Fallback: criar retângulos coloridos se as imagens não existirem
        img_masculino = pygame.Surface((200, 300))
        img_masculino.fill(AZUL)
        img_feminino = pygame.Surface((200, 300))
        img_feminino.fill(ROSA)

    # Redimensionar imagens
    img_masculino = pygame.transform.scale(img_masculino, (200, 300))
    img_feminino = pygame.transform.scale(img_feminino, (200, 300))

    # Posições dos personagens
    pos_masculino = (LARGURA // 4 - 100, ALTURA // 2 - 150)
    pos_feminino = (3 * LARGURA // 4 - 100, ALTURA // 2 - 150)

    # Textos
    font_titulo = pygame.font.SysFont(None, 48)
    font_opcoes = pygame.font.SysFont(None, 36)
    
    titulo = font_titulo.render("SELECIONE SEU PERSONAGEM", True, BRANCO)
    texto_masculino = font_opcoes.render("MASCULINO", True, BRANCO)
    texto_feminino = font_opcoes.render("FEMININO", True, BRANCO)

    rodando = True
    while rodando:
        tela.fill((0, 0, 50))  # Fundo azul escuro

        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return None  # Volta ao menu principal

        # --- LÓGICA DO MOUSE ---
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        # --- DEFINIR RECTS ---
        rect_masculino = pygame.Rect(pos_masculino[0], pos_masculino[1], 200, 300)
        rect_feminino = pygame.Rect(pos_feminino[0], pos_feminino[1], 200, 300)

        # --- DESENHAR ELEMENTOS ---
        # Título
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

        # Personagens com borda de seleção
        cor_borda_masculino = VERDE if rect_masculino.collidepoint(mouse) else BRANCO
        cor_borda_feminino = VERDE if rect_feminino.collidepoint(mouse) else BRANCO
        
        pygame.draw.rect(tela, cor_borda_masculino, rect_masculino, 3)
        pygame.draw.rect(tela, cor_borda_feminino, rect_feminino, 3)
        
        tela.blit(img_masculino, pos_masculino)
        tela.blit(img_feminino, pos_feminino)

        # Textos abaixo dos personagens
        tela.blit(texto_masculino, (pos_masculino[0] + 60, pos_masculino[1] + 320))
        tela.blit(texto_feminino, (pos_feminino[0] + 60, pos_feminino[1] + 320))

        # Instrução
        texto_instrucao = font_opcoes.render("Clique em um personagem para selecionar", True, BRANCO)
        tela.blit(texto_instrucao, (LARGURA // 2 - texto_instrucao.get_width() // 2, ALTURA - 100))

        # --- CLIQUES ---
        if rect_masculino.collidepoint(mouse) and clique[0]:
            return "masculino"

        if rect_feminino.collidepoint(mouse) and clique[0]:
            return "feminino"

        pygame.display.flip()
        clock.tick(FPS)