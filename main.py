import pygame
import random
import os
import math
import sys
from config import *
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.scenes.maps import MapSystem
from src.scenes.menu import menu, selecao_personagem

# --- SISTEMA DE TRANSIÇÃO ENTRE FASES ---
TEXTOS_FASES = {
    1: "VELHO RECIFE: Nas águas antigas do recife submerso, criaturas esquecidas aguardam sua chegada. Colete energias escuras e enfrente os perigos das profundezas.",
    2: "CAVERNA SUBMERSA: Entre passagens secretas e corredores escuros, a caverna esconde segredos ancestrais. Cuidado com as criaturas que habitam estas águas traiçoeiras.",
    3: "RECIFE DE CORAL: Beleza e perigo se misturam neste jardim subaquático. Os corais brilham com energia, mas escondem inimigos à espreita.",
    4: "JARDIM SUBMARINO: Uma floresta submersa de vida marinha e mistérios. As plantas dançam nas correntes, mas não se deixe distrair pelos perigos ocultos.",
    5: "SALA DE MÁQUINAS: SUBMERSA Máquinas antigas ainda funcionam nas profundezas, criando campos de energia perigosos. Navigue com cautela entre os mecanismos ativos.",
    6: "SALA DO REI: O trono submerso aguarda. Aqui, o destino dos oceanos será decidido. Enfrente os guardiões finais e restaure o equilíbrio das águas."
}

# --- CARREGAR SPRITES ---
def carregar_sprites():
    """Carrega os sprites das portas, bolhas e energias"""
    sprites = {}
    
    try:
        # Sprite da porta fechada
        sprites['porta_fechada'] = pygame.image.load("assets/images/miniwhirlpool.png").convert_alpha()
        sprites['porta_fechada'] = pygame.transform.scale(sprites['porta_fechada'], (80, 100))
    except:
        print("⚠️ Sprite da porta fechada não encontrado. Usando fallback.")
        sprites['porta_fechada'] = pygame.Surface((80, 100))
        sprites['porta_fechada'].fill(VERMELHO)
        pygame.draw.rect(sprites['porta_fechada'], CINZA, (10, 10, 60, 80))
    
    try:
        # Sprite da porta aberta
        sprites['porta_aberta'] = pygame.image.load("assets/images/whirlpool.png").convert_alpha()
        sprites['porta_aberta'] = pygame.transform.scale(sprites['porta_aberta'], (80, 100))
    except:
        print("⚠️ Sprite da porta aberta não encontrado. Usando fallback.")
        sprites['porta_aberta'] = pygame.Surface((80, 100))
        sprites['porta_aberta'].fill(VERDE)
        pygame.draw.rect(sprites['porta_aberta'], CIANO, (20, 10, 40, 80))
    
    try:
        # Sprite da bolha
        sprites['bolha'] = pygame.image.load("assets/images/bolhas.png").convert_alpha()
        sprites['bolha'] = pygame.transform.scale(sprites['bolha'], (35, 35))
    except:
        print("⚠️ Sprite da bolha não encontrado. Usando fallback.")
        sprites['bolha'] = pygame.Surface((35, 35), pygame.SRCALPHA)
        pygame.draw.circle(sprites['bolha'], CIANO, (17, 17), 15)
        pygame.draw.circle(sprites['bolha'], BRANCO, (17, 17), 10)
        pygame.draw.circle(sprites['bolha'], (200, 255, 255), (17, 17), 5)
    
    try:
        # Sprite da energia escura
        sprites['energia_escura'] = pygame.image.load("assets/images/cristais/cristalpreto.png").convert_alpha()
        sprites['energia_escura'] = pygame.transform.scale(sprites['energia_escura'], (100, 100))
    except:
        print("⚠️ Sprite da energia escura não encontrado. Usando fallback.")
        sprites['energia_escura'] = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Círculo roxo externo
        pygame.draw.circle(sprites['energia_escura'], (75, 0, 130), (15, 15), 12)
        # Círculo roxo médio
        pygame.draw.circle(sprites['energia_escura'], (128, 0, 128), (15, 15), 8)
        # Círculo roxo claro interno
        pygame.draw.circle(sprites['energia_escura'], (200, 100, 255), (15, 15), 4)
        # Brilho central
        pygame.draw.circle(sprites['energia_escura'], (255, 255, 255), (15, 15), 2)
    
    try:
        # Sprite da energia escura coletável (pode ser diferente)
        sprites['energia_coletavel'] = pygame.image.load("assets/images/energia_coletavel.png").convert_alpha()
        sprites['energia_coletavel'] = pygame.transform.scale(sprites['energia_coletavel'], (28, 28))
    except:
        # Se não tiver sprite específico, usa o mesmo da energia escura
        sprites['energia_coletavel'] = sprites['energia_escura']
    
    return sprites

def tela_vitoria(tela, clock, personagem, estatisticas):
    """Tela de vitória quando todas as energias são coletadas"""
    try:
        background_vitoria = pygame.image.load("assets/images/backgrounds.png").convert()
        background_vitoria = pygame.transform.scale(background_vitoria, (LARGURA, ALTURA))
    except:
        # Fallback: gradiente azul
        background_vitoria = pygame.Surface((LARGURA, ALTURA))
        for i in range(ALTURA):
            cor = (0, max(0, 100 - i//15), max(0, 200 - i//10))
            pygame.draw.line(background_vitoria, cor, (0, i), (LARGURA, i))

    font_titulo = pygame.font.SysFont("arial", 72, bold=True)
    font_subtitulo = pygame.font.SysFont("arial", 36)
    font_texto = pygame.font.SysFont("arial", 28)
    font_info = pygame.font.SysFont("arial", 24)

    running = True
    alpha = 0
    tempo_inicio = pygame.time.get_ticks()

    # Estatísticas
    bolhas_coletadas = estatisticas['bolhas_coletadas']
    energias_coletadas = estatisticas['energias_coletadas']
    total_bolhas = estatisticas['total_bolhas']
    total_energias = estatisticas['total_energias']
    tempo_total = estatisticas['tempo_total']

    while running:
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = tempo_atual - tempo_inicio

        # Fade in
        if tempo_decorrido < 3000:
            alpha = min(255, int(255 * (tempo_decorrido / 3000)))
        else:
            alpha = 255

        tela.blit(background_vitoria, (0, 0))

        # Superfície para efeito de transparência
        superficie_alpha = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)

        # Título de vitória
        texto_vitoria = font_titulo.render("VITÓRIA!", True, DOURADO)
        texto_vitoria_rect = texto_vitoria.get_rect(center=(LARGURA//2, 120))
        
        # Caixa do título
        pygame.draw.rect(superficie_alpha, (0, 0, 0, 180), 
                        (texto_vitoria_rect.x - 30, texto_vitoria_rect.y - 20,
                         texto_vitoria_rect.width + 60, texto_vitoria_rect.height + 40),
                        border_radius=20)
        pygame.draw.rect(superficie_alpha, DOURADO, 
                        (texto_vitoria_rect.x - 30, texto_vitoria_rect.y - 20,
                         texto_vitoria_rect.width + 60, texto_vitoria_rect.height + 40),
                        3, border_radius=20)
        superficie_alpha.blit(texto_vitoria, texto_vitoria_rect)

        # Mensagem de parabéns
        texto_parabens = font_subtitulo.render("Parabéns! Você salvou os oceanos!", True, BRANCO)
        texto_parabens_rect = texto_parabens.get_rect(center=(LARGURA//2, 200))
        superficie_alpha.blit(texto_parabens, texto_parabens_rect)

        # Caixa de estatísticas
        caixa_rect = pygame.Rect(LARGURA//2 - 200, 260, 400, 300)
        pygame.draw.rect(superficie_alpha, (0, 0, 0, 180), caixa_rect, border_radius=20)
        pygame.draw.rect(superficie_alpha, DOURADO, caixa_rect, 3, border_radius=20)

        # === LAYOUT ORGANIZADO DENTRO DA CAIXA ===
        y_pos = caixa_rect.y + 30

        # Personagem
        nome_personagem = "AELYON" if personagem == "masculino" else "THALIC"
        texto_personagem = font_texto.render(f"Personagem: {nome_personagem}", True, VERDE_CLARO)
        personagem_rect = texto_personagem.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_personagem, personagem_rect)
        y_pos += 40

        # Linha separadora
        pygame.draw.line(superficie_alpha, CINZA, (caixa_rect.x + 50, y_pos), (caixa_rect.x + 350, y_pos), 1)
        y_pos += 20

        # Estatísticas de coleta
        texto_bolhas = font_texto.render(f"Bolhas coletadas: {bolhas_coletadas}/{total_bolhas}", True, CIANO)
        bolhas_rect = texto_bolhas.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_bolhas, bolhas_rect)
        y_pos += 35

        # Calcular porcentagens
        perc_bolhas = (bolhas_coletadas / total_bolhas) * 100 if total_bolhas > 0 else 0
        texto_perc_bolhas = font_info.render(f"({perc_bolhas:.1f}% das bolhas)", True, CIANO_CLARO)
        perc_bolhas_rect = texto_perc_bolhas.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_perc_bolhas, perc_bolhas_rect)
        y_pos += 40

        texto_energias = font_texto.render(f"Energias escuras: {energias_coletadas}/{total_energias}", True, ROXO)
        energias_rect = texto_energias.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_energias, energias_rect)
        y_pos += 35

        perc_energias = (energias_coletadas / total_energias) * 100 if total_energias > 0 else 0
        texto_perc_energias = font_info.render(f"({perc_energias:.1f}% das energias)", True, ROXO_CLARO)
        perc_energias_rect = texto_perc_energias.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_perc_energias, perc_energias_rect)
        y_pos += 40

        # Linha separadora
        pygame.draw.line(superficie_alpha, CINZA, (caixa_rect.x + 50, y_pos), (caixa_rect.x + 350, y_pos), 1)
        y_pos += 20

        # Tempo total
        minutos = tempo_total // 60000
        segundos = (tempo_total % 60000) // 1000
        texto_tempo = font_texto.render(f"Tempo total: {minutos:02d}:{segundos:02d}", True, BRANCO)
        tempo_rect = texto_tempo.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_tempo, tempo_rect)
        y_pos += 40

        # Mensagem de avaliação
        if perc_energias == 100 and perc_bolhas >= 80:
            avaliacao = "PERFEITO! Coleta completa!"
            cor_avaliacao = DOURADO
        elif perc_energias >= 90:
            avaliacao = "EXCELENTE! Quase perfeito!"
            cor_avaliacao = VERDE
        elif perc_energias >= 70:
            avaliacao = "BOM TRABALHO!"
            cor_avaliacao = VERDE
        else:
            avaliacao = "MISSÃO CUMPRIDA!"
            cor_avaliacao = BRANCO

        texto_avaliacao = font_subtitulo.render(avaliacao, True, cor_avaliacao)
        avaliacao_rect = texto_avaliacao.get_rect(center=(LARGURA//2, 580))
        superficie_alpha.blit(texto_avaliacao, avaliacao_rect)

        # Instrução para continuar
        if tempo_decorrido > 2000:
            piscar = (tempo_decorrido // 500) % 2
            if piscar:
                texto_continuar = font_info.render("Pressione ESPAÇO para voltar ao menu", True, BRANCO)
                continuar_rect = texto_continuar.get_rect(center=(LARGURA//2, ALTURA - 60))
                superficie_alpha.blit(texto_continuar, continuar_rect)

        # Aplicar alpha
        superficie_alpha.set_alpha(alpha)
        tela.blit(superficie_alpha, (0, 0))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and tempo_decorrido > 2000:
                    return "menu"

        pygame.display.flip()
        clock.tick(FPS)

def tela_gameover(tela, clock, personagem, estatisticas, motivo):
    """Tela de game over quando o jogador morre"""
    
    try:
        background_gameover = pygame.image.load("assets/images/backgrounds.png").convert()
        background_gameover = pygame.transform.scale(background_gameover, (LARGURA, ALTURA))
    except:
        # Fallback: gradiente vermelho
        background_gameover = pygame.Surface((LARGURA, ALTURA))
        for i in range(ALTURA):
            cor = (max(0, 100 - i//20), max(0, 20 - i//30), max(0, 20 - i//30))
            pygame.draw.line(background_gameover, cor, (0, i), (LARGURA, i))

    # CARREGAR IMAGEM DO TÍTULO GAME OVER
    try:
        titulo_gameover = pygame.image.load("assets/images/gameover_transparent.png").convert_alpha()
        # Redimensionar se necessário
        titulo_gameover = pygame.transform.scale(titulo_gameover, (400, 300))
    except:
        # Fallback: criar título programaticamente
        titulo_gameover = pygame.Surface((400, 100), pygame.SRCALPHA)
        pygame.draw.rect(titulo_gameover, (0, 0, 0, 180), (0, 0, 400, 100), border_radius=20)
        pygame.draw.rect(titulo_gameover, VERMELHO, (0, 0, 400, 100), 3, border_radius=20)
        font_titulo_fallback = pygame.font.SysFont("arial", 72, bold=True)
        texto_fallback = font_titulo_fallback.render("GAME OVER", True, VERMELHO)
        texto_rect = texto_fallback.get_rect(center=(200, 50))
        titulo_gameover.blit(texto_fallback, texto_rect)

    font_subtitulo = pygame.font.SysFont("arial", 36)
    font_texto = pygame.font.SysFont("arial", 28)
    font_info = pygame.font.SysFont("arial", 24)

    running = True
    alpha = 0
    tempo_inicio = pygame.time.get_ticks()

    # Estatísticas
    bolhas_coletadas = estatisticas['bolhas_coletadas']
    energias_coletadas = estatisticas['energias_coletadas']
    total_bolhas = estatisticas['total_bolhas']
    total_energias = estatisticas['total_energias']
    tempo_total = estatisticas['tempo_total']

    while running:
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = tempo_atual - tempo_inicio

        # Fade in
        if tempo_decorrido < 3000:
            alpha = min(255, int(255 * (tempo_decorrido / 3000)))
        else:
            alpha = 255

        tela.blit(background_gameover, (0, 0))

        # Superfície para efeito de transparência
        superficie_alpha = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)

        # USAR IMAGEM DO TÍTULO GAME OVER
        titulo_rect = titulo_gameover.get_rect(center=(LARGURA//2, 120))
        
        # Caixa do título (opcional - para destacar mais)
        pygame.draw.rect(superficie_alpha, (0, 0, 0, 120), 
                        (titulo_rect.x - 20, titulo_rect.y - 10,
                         titulo_rect.width + 40, titulo_rect.height + 20),
                        border_radius=25)
        
        # Aplicar efeito de pulsação no título
        pulsacao = 1.0 + 0.1 * math.sin(tempo_decorrido * 0.01)  # Efeito sutil de pulsação
        titulo_pulsante = pygame.transform.scale(
            titulo_gameover, 
            (int(titulo_rect.width * pulsacao), int(titulo_rect.height * pulsacao))
        )
        titulo_pulsante_rect = titulo_pulsante.get_rect(center=(LARGURA//2, 120))
        
        superficie_alpha.blit(titulo_pulsante, titulo_pulsante_rect)

        # Motivo da morte
        if motivo == "vida":
            texto_motivo = font_subtitulo.render("Sua vida chegou a zero!", True, VERMELHO)
        elif motivo == "oxigenio":
            texto_motivo = font_subtitulo.render("Você ficou sem oxigênio!", True, CIANO)
        else:
            texto_motivo = font_subtitulo.render("Missão fracassada!", True, VERMELHO)
        
        motivo_rect = texto_motivo.get_rect(center=(LARGURA//2, 200))
        superficie_alpha.blit(texto_motivo, motivo_rect)

        # Caixa de estatísticas - AUMENTADA para caber todos os textos
        caixa_rect = pygame.Rect(LARGURA//2 - 200, 240, 400, 320)  # Aumentei a altura
        pygame.draw.rect(superficie_alpha, (0, 0, 0, 180), caixa_rect, border_radius=20)
        pygame.draw.rect(superficie_alpha, VERMELHO, caixa_rect, 3, border_radius=20)

        # === LAYOUT CORRIGIDO DENTRO DA CAIXA ===
        y_pos = caixa_rect.y + 30  # Posição Y inicial dentro da caixa

        # Personagem
        nome_personagem = "AELYON" if personagem == "masculino" else "THALIC"
        texto_personagem = font_texto.render(f"Personagem: {nome_personagem}", True, BRANCO)
        personagem_rect = texto_personagem.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_personagem, personagem_rect)
        y_pos += 40

        # Linha separadora
        pygame.draw.line(superficie_alpha, CINZA, (caixa_rect.x + 50, y_pos), (caixa_rect.x + 350, y_pos), 1)
        y_pos += 20

        # Estatísticas de coleta - CORRIGIDO
        texto_bolhas = font_texto.render(f"Bolhas coletadas: {bolhas_coletadas}/{total_bolhas}", True, CIANO)
        bolhas_rect = texto_bolhas.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_bolhas, bolhas_rect)
        y_pos += 35

        # Calcular porcentagens
        perc_bolhas = (bolhas_coletadas / total_bolhas) * 100 if total_bolhas > 0 else 0
        texto_perc_bolhas = font_info.render(f"({perc_bolhas:.1f}% das bolhas)", True, CIANO_CLARO)
        perc_bolhas_rect = texto_perc_bolhas.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_perc_bolhas, perc_bolhas_rect)
        y_pos += 40

        texto_energias = font_texto.render(f"Energias escuras: {energias_coletadas}/{total_energias}", True, ROXO)
        energias_rect = texto_energias.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_energias, energias_rect)
        y_pos += 35

        perc_energias = (energias_coletadas / total_energias) * 100 if total_energias > 0 else 0
        texto_perc_energias = font_info.render(f"({perc_energias:.1f}% das energias)", True, ROXO_CLARO)
        perc_energias_rect = texto_perc_energias.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_perc_energias, perc_energias_rect)
        y_pos += 40

        # Linha separadora
        pygame.draw.line(superficie_alpha, CINZA, (caixa_rect.x + 50, y_pos), (caixa_rect.x + 350, y_pos), 1)
        y_pos += 20

        # Tempo total
        minutos = tempo_total // 60000
        segundos = (tempo_total % 60000) // 1000
        texto_tempo = font_texto.render(f"Tempo sobrevivido: {minutos:02d}:{segundos:02d}", True, BRANCO)
        tempo_rect = texto_tempo.get_rect(center=(LARGURA//2, y_pos))
        superficie_alpha.blit(texto_tempo, tempo_rect)
        y_pos += 40

        # Mensagem de encorajamento
        if perc_energias >= 50:
            mensagem = "Você estava indo bem! Tente novamente!"
        elif perc_energias >= 25:
            mensagem = "Bom progresso! Continue tentando!"
        else:
            mensagem = "Não desista! Cada tentativa é um aprendizado!"
        
        texto_mensagem = font_subtitulo.render(mensagem, True, AMARELO)
        mensagem_rect = texto_mensagem.get_rect(center=(LARGURA//2, 580))  # Posição fixa abaixo da caixa
        superficie_alpha.blit(texto_mensagem, mensagem_rect)

        # Instrução para continuar
        if tempo_decorrido > 2000:
            piscar = (tempo_decorrido // 500) % 2
            if piscar:
                texto_continuar = font_info.render("Pressione ESPAÇO para tentar novamente", True, BRANCO)
                continuar_rect = texto_continuar.get_rect(center=(LARGURA//2, ALTURA - 60))
                superficie_alpha.blit(texto_continuar, continuar_rect)

        # Aplicar alpha
        superficie_alpha.set_alpha(alpha)
        tela.blit(superficie_alpha, (0, 0))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and tempo_decorrido > 2000:
                    return "reiniciar"

        pygame.display.flip()
        clock.tick(FPS)

def transicao_fase(tela, clock, numero_fase, personagem):
    """Função de transição entre fases"""
    # Carregar background da transição
    try:
        background_transicao = pygame.image.load("assets/images/transicao_bg.png").convert()
        background_transicao = pygame.transform.scale(background_transicao, (LARGURA, ALTURA))
    except:
        # Fallback: gradiente escuro
        background_transicao = pygame.Surface((LARGURA, ALTURA))
        for i in range(ALTURA):
            cor = (max(0, 20 - i//20), max(0, 40 - i//15), max(0, 60 - i//10))
            pygame.draw.line(background_transicao, cor, (0, i), (LARGURA, i))

    # Fontes
    font_titulo = pygame.font.SysFont("arial", 72, bold=True)
    font_texto = pygame.font.SysFont("arial", 28)
    font_instrucao = pygame.font.SysFont("arial", 24)

    # Texto da fase
    texto_fase = font_titulo.render(f"FASE {numero_fase}", True, DOURADO)
    texto_descricao = TEXTOS_FASES.get(numero_fase, f"Fase {numero_fase} - Prepare-se para o desafio!")
    
    # Quebrar texto da descrição em linhas
    linhas_descricao = []
    palavras = texto_descricao.split(' ')
    linha_atual = ""
    
    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        if font_texto.size(teste_linha)[0] < LARGURA - 100:
            linha_atual = teste_linha
        else:
            linhas_descricao.append(linha_atual)
            linha_atual = palavra + " "
    if linha_atual:
        linhas_descricao.append(linha_atual)

    # Animação de entrada
    alpha = 0
    running = True
    tempo_inicio = pygame.time.get_ticks()
    
    while running:
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = tempo_atual - tempo_inicio
        
        # Controlar animação de fade in
        if tempo_decorrido < 2000:  # 2 segundos de fade in
            alpha = min(255, int(255 * (tempo_decorrido / 2000)))
        else:
            alpha = 255

        # Desenhar background
        tela.blit(background_transicao, (0, 0))
        
        # Desenhar elementos com alpha
        superficie_alpha = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        
        # Título da fase
        texto_fase_rect = texto_fase.get_rect(center=(LARGURA//2, 150))
        pygame.draw.rect(superficie_alpha, (0, 0, 0, 150), 
                        (texto_fase_rect.x - 20, texto_fase_rect.y - 10, 
                         texto_fase_rect.width + 40, texto_fase_rect.height + 20),
                        border_radius=15)
        superficie_alpha.blit(texto_fase, texto_fase_rect)
        
        # Caixa de texto da descrição
        altura_caixa = len(linhas_descricao) * 40 + 40
        caixa_rect = pygame.Rect(50, 250, LARGURA - 100, altura_caixa)
        pygame.draw.rect(superficie_alpha, (0, 0, 0, 180), caixa_rect, border_radius=20)
        pygame.draw.rect(superficie_alpha, DOURADO, caixa_rect, 3, border_radius=20)
        
        # Texto da descrição
        for i, linha in enumerate(linhas_descricao):
            texto_linha = font_texto.render(linha, True, BRANCO)
            texto_linha_rect = texto_linha.get_rect(center=(LARGURA//2, 270 + i * 40))
            superficie_alpha.blit(texto_linha, texto_linha_rect)
        
        # Personagem selecionado
        nome_personagem = "AELYON" if personagem == "masculino" else "THALIC"
        texto_personagem = font_texto.render(f"Personagem: {nome_personagem}", True, BRANCO)
        personagem_rect = texto_personagem.get_rect(center=(LARGURA//2, 350 + len(linhas_descricao) * 40))
        superficie_alpha.blit(texto_personagem, personagem_rect)
        
        # Instrução para continuar
        if tempo_decorrido > 1500:  # Mostrar instrução após 1.5 segundos
            piscar = (tempo_decorrido // 500) % 2  # Piscar a cada 500ms
            if piscar:
                texto_continuar = font_instrucao.render("Pressione ESPAÇO para continuar...", True, BRANCO)
                continuar_rect = texto_continuar.get_rect(center=(LARGURA//2, ALTURA - 100))
                superficie_alpha.blit(texto_continuar, continuar_rect)
        
        # Aplicar alpha
        superficie_alpha.set_alpha(alpha)
        tela.blit(superficie_alpha, (0, 0))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and tempo_decorrido > 1500:
                    running = False
                elif evento.key == pygame.K_ESCAPE:
                    return "menu"

        pygame.display.flip()
        clock.tick(FPS)

    print(f"🎮 Iniciando Fase {numero_fase} com personagem {personagem}")
    return f"mapa{numero_fase}"

# --- FUNÇÕES DE DESENHO COM SPRITES ---
def desenhar_portas_com_sprites(tela, mapa_atual_data, sprites):
    """Desenha as portas do mapa atual com sprites"""
    for porta in mapa_atual_data["portas"]:
        if porta["ativa"]:
            # Usar sprite da porta aberta
            tela.blit(sprites['porta_aberta'], porta["rect"])
            
            # Texto indicativo
            font = pygame.font.SysFont(None, 20)
            
            # Efeito de brilho na porta aberta
            if pygame.time.get_ticks() % 1000 < 500:  # Piscar a cada segundo
                brilho = pygame.Surface((80, 20), pygame.SRCALPHA)
                brilho.fill((255, 255, 255, 100))
                tela.blit(brilho, (porta["rect"].x, porta["rect"].y - 10))
        else:
            # Usar sprite da porta fechada
            tela.blit(sprites['porta_fechada'], porta["rect"])
            
            # Texto indicativo
            font = pygame.font.SysFont(None, 18)
            
            # Mostrar quantas energias faltam
            energias_restantes = len(mapa_atual_data["energias_escuras"])

def desenhar_bolhas_com_sprites(tela, mapa_atual_data, sprites):
    """Desenha as bolhas do mapa atual com sprites"""
    for bolha in mapa_atual_data["bolhas"]:
        # Efeito de flutuação suave
        offset_y = pygame.math.Vector2(0, math.sin(pygame.time.get_ticks() * 0.005) * 3)
        posicao_flutuante = bolha.topleft + offset_y
        
        tela.blit(sprites['bolha'], posicao_flutuante)
        
        # Efeito de brilho ocasional
        if pygame.time.get_ticks() % 2000 < 200:
            brilho = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(brilho, (255, 255, 255, 80), (20, 20), 20)
            tela.blit(brilho, (bolha.x - 5, bolha.y - 5))

def desenhar_energias_com_sprites(tela, mapa_atual_data, sprites):
    """Desenha as energias escuras do mapa atual com sprites"""
    for energia in mapa_atual_data["energias_escuras"]:
        # Efeito de pulsação
        escala = 1.0 + math.sin(pygame.time.get_ticks() * 0.008) * 0.2
        largura_pulsante = int(30 * escala)
        altura_pulsante = int(30 * escala)
        
        # Centralizar o sprite pulsante
        offset_x = (energia.width - largura_pulsante) // 2
        offset_y = (energia.height - altura_pulsante) // 2
        
        # Criar sprite redimensionado para o efeito de pulsação
        energia_pulsante = pygame.transform.scale(
            sprites['energia_escura'], 
            (largura_pulsante, altura_pulsante)
        )
        
        tela.blit(energia_pulsante, (energia.x + offset_x, energia.y + offset_y))
        
        # Efeito de brilho rotativo
        tempo = pygame.time.get_ticks() * 0.01
        raio_brilho = 20
        pontos_brilho = 6
        
        for i in range(pontos_brilho):
            angulo = tempo + (i * (2 * math.pi / pontos_brilho))
            x_brilho = energia.centerx + math.cos(angulo) * raio_brilho
            y_brilho = energia.centery + math.sin(angulo) * raio_brilho
            
            alpha = int(128 + 127 * math.sin(tempo * 2 + i))
            cor_brilho = (200, 100, 255, alpha)
            
            # Desenhar ponto de brilho
            pygame.draw.circle(tela, cor_brilho, (int(x_brilho), int(y_brilho)), 3)

# --- INICIALIZAÇÃO PRINCIPAL ---
pygame.init()

# Carregar sprites
sprites = carregar_sprites()

# Sistema de mapas
map_system = MapSystem()
map_system.carregar_backgrounds()

# Chama o menu principal
escolha_menu = menu(TELA, clock)

# Se escolheu jogar, vai para seleção de personagem
if escolha_menu == "selecao_personagem":
    personagem_escolhido = selecao_personagem(TELA, clock)
    
    if personagem_escolhido is None:
        # Usuário voltou ao menu ou fechou a janela
        pygame.quit()
        exit()
else:
    pygame.quit()
    exit()

# Mostra transição para a primeira fase
fase_atual = 1
proximo_mapa = transicao_fase(TELA, clock, fase_atual, personagem_escolhido)

# Cria o jogador com o personagem escolhido
player = Player(100, 300, personagem_escolhido)
player_group = pygame.sprite.Group(player)

print(f"🎮 Personagem selecionado: {personagem_escolhido}")

# Grupo para inimigos e criar inimigos do mapa inicial
enemy_group = map_system.criar_inimigos_para_mapa(map_system.mapa_atual)

# Variáveis do jogo
vida = 100
oxigenio = 100
energia_coletada = 0
energia_total = sum(len(mapa["energias_escuras"]) for mapa in map_system.maps.values())

# === VARIÁVEIS DE ESTATÍSTICAS PARA AS TELAS ===
bolhas_coletadas_total = 0
energias_coletadas_total = 0
total_bolhas_jogo = sum(len(mapa["bolhas"]) for mapa in map_system.maps.values())
total_energias_jogo = sum(len(mapa["energias_escuras"]) for mapa in map_system.maps.values())
tempo_inicio_jogo = pygame.time.get_ticks()

# Invencibilidade
INVENCIBILIDADE = 1000
ultimo_dano = 0

# Função para verificar se todas as energias do mapa atual foram coletadas
def verificar_energias_coletadas(mapa_atual_data):
    """Verifica se todas as energias do mapa atual foram coletadas"""
    return len(mapa_atual_data["energias_escuras"]) == 0

# Função para atualizar estado das portas
def atualizar_portas(mapa_atual_data, energias_coletadas_mapa):
    """Atualiza o estado das portas baseado nas energias coletadas"""
    for porta in mapa_atual_data["portas"]:
        # Se a porta leva para outro mapa, só libera se coletou todas as energias
        if porta["destination"] != "mapa1":  # Exceto portas que voltam para o início
            porta["ativa"] = verificar_energias_coletadas(mapa_atual_data)
    
    return mapa_atual_data

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
        
        # Atualiza a fase atual baseada no mapa
        global fase_atual
        fase_atual = int(novo_mapa.replace("mapa", ""))
        
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

    # Atualizar estado das portas
    mapa_atual_data = atualizar_portas(mapa_atual_data, energias_coletadas_total)

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
        tempo_total = pygame.time.get_ticks() - tempo_inicio_jogo
        estatisticas = {
            'bolhas_coletadas': bolhas_coletadas_total,
            'energias_coletadas': energias_coletadas_total,
            'total_bolhas': total_bolhas_jogo,
            'total_energias': total_energias_jogo,
            'tempo_total': tempo_total
        }
        resultado = tela_gameover(TELA, clock, personagem_escolhido, estatisticas, "oxigenio")
        if resultado == "reiniciar":
            # Reiniciar o jogo
            vida = 100
            oxigenio = 100
            energia_coletada = 0
            bolhas_coletadas_total = 0
            energias_coletadas_total = 0
            tempo_inicio_jogo = pygame.time.get_ticks()
            # Reposicionar player e recriar inimigos
            player.rect.x = 100
            player.rect.y = 300
            enemy_group.empty()
            enemy_group.add(map_system.criar_inimigos_para_mapa(map_system.mapa_atual))
        else:
            rodando = False

    # Colisão com inimigos
    colisoes = pygame.sprite.spritecollide(player, enemy_group, False)
    if colisoes and tempo_atual - ultimo_dano > INVENCIBILIDADE:
        vida -= 10
        ultimo_dano = tempo_atual
        print(f"Você foi atingido! Vida: {vida}")
        
        if vida <= 0:
            tempo_total = pygame.time.get_ticks() - tempo_inicio_jogo
            estatisticas = {
                'bolhas_coletadas': bolhas_coletadas_total,
                'energias_coletadas': energias_coletadas_total,
                'total_bolhas': total_bolhas_jogo,
                'total_energias': total_energias_jogo,
                'tempo_total': tempo_total
            }
            resultado = tela_gameover(TELA, clock, personagem_escolhido, estatisticas, "vida")
            if resultado == "reiniciar":
                # Reiniciar o jogo
                vida = 100
                oxigenio = 100
                energia_coletada = 0
                bolhas_coletadas_total = 0
                energias_coletadas_total = 0
                tempo_inicio_jogo = pygame.time.get_ticks()
                # Reposicionar player e recriar inimigos
                player.rect.x = 100
                player.rect.y = 300
                enemy_group.empty()
                enemy_group.add(map_system.criar_inimigos_para_mapa(map_system.mapa_atual))
            else:
                rodando = False

    # Colisão com bolhas
    bolhas_para_remover = []
    for bolha in mapa_atual_data["bolhas"]:
        if player.rect.colliderect(bolha):
            oxigenio = min(100, oxigenio + 20)
            bolhas_coletadas_total += 1  # ← CONTADOR DE BOLHAS
            bolhas_para_remover.append(bolha)
            print("Bolha coletada! Oxigênio recuperado.")
    
    # Remove bolhas coletadas
    for bolha in bolhas_para_remover:
        if bolha in mapa_atual_data["bolhas"]:
            mapa_atual_data["bolhas"].remove(bolha)

    # Colisão com energias escuras
    energias_para_remover = []
    for energia in mapa_atual_data["energias_escuras"]:
        if player.rect.colliderect(energia):
            energia_coletada += 1
            energias_coletadas_total += 1  # ← CONTADOR DE ENERGIA
            energias_para_remover.append(energia)
            print(f"⚡ Energia escura coletada! Total: {energia_coletada}/{energia_total}")

    # Remove energias coletadas
    for energia in energias_para_remover:
        if energia in mapa_atual_data["energias_escuras"]:
            mapa_atual_data["energias_escuras"].remove(energia)

    # Colisão com portas (troca de mapa) - SÓ FUNCIONA SE PORTA ESTIVER ATIVA
    for porta in mapa_atual_data["portas"]:
        if porta["ativa"] and player.rect.colliderect(porta["rect"]):
            print(f"🚪 Entrando na porta para {porta['destination']}!")
            
            # Mostra transição antes de trocar de fase
            nova_fase = int(porta['destination'].replace('mapa', ''))
            transicao_fase(TELA, clock, nova_fase, personagem_escolhido)
            
            # Trocar mapa e recriar inimigos
            if trocar_mapa_e_recriar_inimigos(porta["destination"], player, map_system):
                mapa_atual_data = map_system.get_mapa_atual()
            
            break

    # Colisão com saída (opcional - para vencer o jogo)
    if "saida" in mapa_atual_data and player.rect.colliderect(mapa_atual_data["saida"]):
        print("Você encontrou a saída! Vitória!")
        rodando = False

    # Verificar vitória por coleta completa de energia
    if energia_coletada >= energia_total:
        tempo_total = pygame.time.get_ticks() - tempo_inicio_jogo
        estatisticas = {
            'bolhas_coletadas': bolhas_coletadas_total,
            'energias_coletadas': energias_coletadas_total,
            'total_bolhas': total_bolhas_jogo,
            'total_energias': total_energias_jogo,
            'tempo_total': tempo_total
        }
        resultado = tela_vitoria(TELA, clock, personagem_escolhido, estatisticas)
        if resultado == "menu":
            rodando = False
        else:
            # Continuar jogando ou reiniciar
            pass

    # --- DESENHAR ELEMENTOS ---
    
    # Desenhar portas com sprites
    desenhar_portas_com_sprites(TELA, mapa_atual_data, sprites)
    
    # Desenhar bolhas com sprites
    desenhar_bolhas_com_sprites(TELA, mapa_atual_data, sprites)
    
    # Desenhar energias escuras com sprites
    desenhar_energias_com_sprites(TELA, mapa_atual_data, sprites)
    
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
    cor_oxigenio = CIANO if oxigenio > 30 else VERMELHO   # Muda cor se estiver baixo
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

    # Contador de energia escura
    texto_energia = font_ui.render(f"Energia: {energia_coletada}/{energia_total}", True, ENERGIA_ESCURA)
    TELA.blit(texto_energia, (10, 70))

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

    # Informação das portas
    energias_restantes_mapa = len(mapa_atual_data["energias_escuras"])
    texto_portas = font_ui.render(f"Energias no mapa: {energias_restantes_mapa}", True, AMARELO)
    TELA.blit(texto_portas, (LARGURA - 200, 80))

    # Instruções
    texto_instrucoes = font_ui.render("WASD: Mover | ESC: Sair", True, BRANCO)
    TELA.blit(texto_instrucoes, (LARGURA - 200, ALTURA - 30))

    pygame.display.update()

pygame.quit()