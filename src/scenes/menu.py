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
    # Carregar background para seleção de personagem
    try:
        background_selecao = pygame.image.load("assets/images/backgrounds.png").convert()
        background_selecao = pygame.transform.scale(background_selecao, (LARGURA, ALTURA))
        print("✅ Background de seleção carregado com sucesso!")
    except:
        # Fallback: fundo azul escuro se a imagem não existir
        background_selecao = pygame.Surface((LARGURA, ALTURA))
        background_selecao.fill((0, 0, 50))
        print("⚠️ Background de seleção não encontrado. Usando fallback.")

    # Carregar imagem do texto "ESCOLHA O SEU PERSONAGEM"
    try:
        img_texto_escolha = pygame.image.load("assets/images/textchoise.png").convert_alpha()
        # Redimensionar mantendo proporção
        largura_original, altura_original = img_texto_escolha.get_size()
        nova_largura = int(largura_original * 0.4)
        nova_altura = int(altura_original * 0.4)
        img_texto_escolha = pygame.transform.scale(img_texto_escolha, (nova_largura, nova_altura))
        print("✅ Texto de escolha carregado com sucesso!")
    except:
        img_texto_escolha = None
        print("⚠️ Texto de escolha não encontrado. Usando texto renderizado.")

    # Carregar imagens dos personagens
    try:
        img_masculino = pygame.image.load("assets/images/escolha/aelyon.png").convert_alpha()
        img_masculino = pygame.transform.scale(img_masculino, (150, 300))
        print("✅ Personagem masculino carregado com sucesso!")
    except:
        # Fallback: criar retângulo azul
        img_masculino = pygame.Surface((200, 300))
        img_masculino.fill((30, 144, 255))
        pygame.draw.rect(img_masculino, (110, 130, 180), (50, 50, 100, 200))
        pygame.draw.circle(img_masculino, (100, 149, 237), (100, 80), 30)
        print("⚠️ Personagem masculino não encontrado. Usando fallback.")

    try:
        img_feminino = pygame.image.load("assets/images/escolha/thalic.png").convert_alpha()
        img_feminino = pygame.transform.scale(img_feminino, (200, 300))
        print("✅ Personagem feminino carregado com sucesso!")
    except:
        # Fallback: criar retângulo rosa
        img_feminino = pygame.Surface((200, 300))
        img_feminino.fill((255, 182, 193))
        pygame.draw.rect(img_feminino, (219, 112, 147), (50, 50, 100, 200))
        pygame.draw.circle(img_feminino, (199, 21, 133), (100, 80), 30)
        print("⚠️ Personagem feminino não encontrado. Usando fallback.")

    # --- CARREGAR IMAGENS DOS NOMES DOS PERSONAGENS ---
    try:
        img_nome_masculino = pygame.image.load("assets/images/aelyonname.png").convert_alpha()
        # Redimensionar se necessário
        largura_nome, altura_nome = img_nome_masculino.get_size()
        if largura_nome > 200:
            escala_nome = 0.2
            img_nome_masculino = pygame.transform.scale(
                img_nome_masculino, 
                (int(largura_nome * escala_nome), int(altura_nome * escala_nome))
            )
        print("✅ Nome 'AELYON' carregado com sucesso!")
    except:
        img_nome_masculino = None
        print("⚠️ Imagem do nome 'AELYON' não encontrada. Usando texto renderizado.")

    try:
        img_nome_feminino = pygame.image.load("assets/images/thalicname.png").convert_alpha()
        # Redimensionar se necessário
        largura_nome, altura_nome = img_nome_feminino.get_size()
        if largura_nome > 200:
            escala_nome = 0.2
            img_nome_feminino = pygame.transform.scale(
                img_nome_feminino, 
                (int(largura_nome * escala_nome), int(altura_nome * escala_nome))
            )
        print("✅ Nome 'THALIC' carregado com sucesso!")
    except:
        img_nome_feminino = None
        print("⚠️ Imagem do nome 'THALIC' não encontrada. Usando texto renderizado.")

    # Posições dos elementos
    pos_masculino = (LARGURA // 4 - 100, ALTURA // 2 - 90)   # Ajustado para centralizar melhor
    pos_feminino = (3 * LARGURA // 4 - 100, ALTURA // 2 - 90)

    # --- POSIÇÕES DOS NOMES (LADO A LADO ACIMA DOS PERSONAGENS) ---
    # Nomes posicionados acima e centralizados com os personagens
    pos_nome_masculino = (LARGURA // 4.5, ALTURA // 2 - 150)
    pos_nome_feminino = (3 * LARGURA // 4, ALTURA // 2 - 100)

    # Textos de fallback
    font_titulo = pygame.font.SysFont(None, 48)
    font_opcoes = pygame.font.SysFont(None, 36)
    font_instrucoes = pygame.font.SysFont(None, 28)
    
    titulo_fallback = font_titulo.render("ESCOLHA O SEU PERSONAGEM", True, BRANCO)
    texto_masculino_fallback = font_opcoes.render("AELYON", True, BRANCO)
    texto_feminino_fallback = font_opcoes.render("THALIC", True, BRANCO)

    rodando = True
    while rodando:
        # Desenhar background
        tela.blit(background_selecao, (0, 0))

        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return None

        # --- LÓGICA DO MOUSE ---
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        # --- DEFINIR RECTS ---
        rect_masculino = pygame.Rect(pos_masculino[0], pos_masculino[1], 150, 300)
        rect_feminino = pygame.Rect(pos_feminino[0], pos_feminino[1], 200, 300)

        # --- DESENHAR ELEMENTOS ---
        
        # Texto "ESCOLHA O SEU PERSONAGEM"
        if img_texto_escolha:
            texto_rect = img_texto_escolha.get_rect(center=(LARGURA // 2, 120))
            tela.blit(img_texto_escolha, texto_rect)
        else:
            tela.blit(titulo_fallback, (LARGURA // 2 - titulo_fallback.get_width() // 2, 100))

        # --- DESENHAR NOMES DOS PERSONAGENS ---
        # Nomes centralizados acima dos personagens
        if img_nome_masculino:
            nome_masculino_rect = img_nome_masculino.get_rect(center=pos_nome_masculino)
            tela.blit(img_nome_masculino, nome_masculino_rect)
        else:
            texto_masculino_rect = texto_masculino_fallback.get_rect(center=pos_nome_masculino)
            tela.blit(texto_masculino_fallback, texto_masculino_rect)

        if img_nome_feminino:
            nome_feminino_rect = img_nome_feminino.get_rect(center=pos_nome_feminino)
            tela.blit(img_nome_feminino, nome_feminino_rect)
        else:
            texto_feminino_rect = texto_feminino_fallback.get_rect(center=pos_nome_feminino)
            tela.blit(texto_feminino_fallback, texto_feminino_rect)

        # Personagens com borda de seleção
        cor_borda_masculino = VERDE if rect_masculino.collidepoint(mouse) else BRANCO
        cor_borda_feminino = VERDE if rect_feminino.collidepoint(mouse) else BRANCO
        
        # Desenhar bordas
        pygame.draw.rect(tela, cor_borda_masculino, rect_masculino, 4)
        pygame.draw.rect(tela, cor_borda_feminino, rect_feminino, 4)
        
        # Desenhar personagens
        tela.blit(img_masculino, pos_masculino)
        tela.blit(img_feminino, pos_feminino)

        # Instruções na parte inferior
        texto_instrucao = font_instrucoes.render("Clique em um personagem para selecionar", True, BRANCO)
        tela.blit(texto_instrucao, (LARGURA // 2 - texto_instrucao.get_width() // 2, ALTURA - 80))
        
        texto_voltar = font_instrucoes.render("ESC: Voltar ao menu", True, CINZA)
        tela.blit(texto_voltar, (LARGURA // 2 - texto_voltar.get_width() // 2, ALTURA - 40))

        # --- CLIQUES ---
        if rect_masculino.collidepoint(mouse) and clique[0]:
            print("🎮 Personagem AELYON selecionado!")
            return "masculino"

        if rect_feminino.collidepoint(mouse) and clique[0]:
            print("🎮 Personagem THALIC selecionado!")
            return "feminino"

        pygame.display.flip()
        clock.tick(FPS)