import pygame
import os
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo="gyarados", area_largura=200, area_altura=150):
        super().__init__()
        self.tipo = tipo
        self.frames = []
        self.carregar_sprites()
        
        if not self.frames:
            self.frames = [self.criar_placeholder()]
            
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        
        # Área de movimento
        self.area_centro_x = x
        self.area_centro_y = y
        self.area_largura = area_largura
        self.area_altura = area_altura
        
        # Movimento - velocidade varia por tipo
        self.velocidade = self.definir_velocidade_por_tipo()
        self.anim_speed = 200
        self.last_update = pygame.time.get_ticks()
        
        # Direção atual
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.tempo_para_mudar = random.randint(1500, 4000)
        self.ultima_mudanca = pygame.time.get_ticks()

    def definir_velocidade_por_tipo(self):
        """Define velocidade baseada no tipo de inimigo"""
        velocidades = {
            "gyarados": random.uniform(1.0, 1.5),
            "golisopod": random.uniform(1.2, 1.8),
            "elektross": random.uniform(1.5, 2.0),
            "sharpedo": random.uniform(1.8, 2.5),
        }
        return velocidades.get(self.tipo, random.uniform(1.0, 2.0))

    def carregar_sprites(self):
        """Carrega sprites baseados no tipo de inimigo e remove fundo"""
        try:
            # Define os arquivos de sprite para cada tipo
            sprites_por_tipo = {
                "gyarados": ["gyaradosSP1.jpeg", "gyaradosSP2.jpeg", "gyaradosSP3.jpeg", "gyaradosSP4.jpeg"],
                "golisopod": ["golisopodSP1.jpeg", "golisopodSP2.jpeg", "golisopodSP3.jpeg", "golisopodSP4.jpeg"],
                "elektross": ["elektrossSP1.jpeg", "elektrossSP2.jpeg", "elektrossSP3.jpeg"],
                "sharpedo": ["sharpedoSP1.jpeg", "sharpedoSP2.jpeg", "sharpedoSP3.jpeg"],
            }
            
            # Tenta diferentes caminhos possíveis
            caminhos_tentativos = [
                os.path.join("assets", "images", "sprites", "vilains"),
                os.path.join("src", "assets", "images", "sprites", "vilains"),
                os.path.join("..", "assets", "images", "sprites", "vilains"),
                os.path.join(os.path.dirname(__file__), "..", "..", "assets", "images", "sprites", "vilains")
            ]
            
            caminho_encontrado = None
            for caminho in caminhos_tentativos:
                if os.path.exists(caminho):
                    caminho_encontrado = caminho
                    break
            
            if not caminho_encontrado:
                print(f"[AVISO] Pasta de vilões não encontrada para: {self.tipo}")
                return
            
            # Pega a lista de sprites para este tipo
            arquivos_sprites = sprites_por_tipo.get(self.tipo, ["gyaradosSP1.jpeg"])
            
            for nome_arquivo in arquivos_sprites:
                img_path = os.path.join(caminho_encontrado, nome_arquivo)
                if os.path.exists(img_path):
                    try:
                        # Carrega a imagem
                        img = pygame.image.load(img_path)
                        
                        # Converte para formato com alpha (transparência)
                        img = img.convert_alpha()
                        
                        # Remove o fundo baseado na cor
                        img = self.remover_fundo(img, nome_arquivo)
                        
                        # Ajusta o tamanho baseado no tipo
                        tamanho = self.definir_tamanho_por_tipo()
                        img = pygame.transform.scale(img, tamanho)
                        
                        self.frames.append(img)
                        print(f"[SUCESSO] Sprite carregado e processado: {img_path}")
                        
                    except Exception as e:
                        print(f"[ERRO] Falha ao carregar {img_path}: {e}")
                else:
                    print(f"[AVISO] Sprite não encontrado: {img_path}")
            
            # Se não encontrou sprites específicos, usa sprites genéricos
            if not self.frames:
                print(f"[AVISO] Usando sprites genéricos para {self.tipo}")
                self.carregar_sprites_genericos(caminho_encontrado)
                
        except Exception as e:
            print(f"[ERRO] Erro geral no carregamento de sprites: {e}")

    def remover_fundo(self, surface, nome_arquivo):
        """Remove o fundo da imagem baseado em cores específicas"""
        # Cria uma cópia da surface para trabalhar
        result = surface.copy()
        
        # Define cores de fundo para remover (preto, branco, e tons de cinza)
        cores_fundo = [
            (0, 0, 0),      # Preto
            (255, 255, 255), # Branco
            (240, 240, 240), # Branco quase puro
            (10, 10, 10),    # Preto quase puro
        ]
        
        # Para arquivos JPEG, assumimos que o fundo é preto ou branco
        if nome_arquivo.lower().endswith('.jpeg') or nome_arquivo.lower().endswith('.jpg'):
            # Adiciona mais tons para JPEG
            cores_fundo.extend([
                (1, 1, 1), (2, 2, 2), (3, 3, 3),  # Pretos muito próximos
                (254, 254, 254), (253, 253, 253),  # Brancos muito próximos
            ])
        
        # Percorre todos os pixels e torna transparentes os que são da cor de fundo
        for x in range(result.get_width()):
            for y in range(result.get_height()):
                pixel = result.get_at((x, y))
                # Verifica se o pixel é uma das cores de fundo (ignorando alpha)
                for cor_fundo in cores_fundo:
                    if self.pixels_similares(pixel, cor_fundo, tolerancia=10):
                        result.set_at((x, y), (0, 0, 0, 0))  # Torna totalmente transparente
                        break
        
        return result

    def pixels_similares(self, pixel1, pixel2, tolerancia=10):
        """Verifica se dois pixels são similares dentro de uma tolerância"""
        r1, g1, b1, a1 = pixel1
        r2, g2, b2 = pixel2
        
        return (abs(r1 - r2) <= tolerancia and 
                abs(g1 - g2) <= tolerancia and 
                abs(b1 - b2) <= tolerancia)

    def definir_tamanho_por_tipo(self):
        """Define tamanho do sprite baseado no tipo"""
        tamanhos = {
            "gyarados": (60, 70),
            "golisopod": (55, 65),
            "elektross": (50, 50),
            "sharpedo": (70, 60),
        }
        return tamanhos.get(self.tipo, (60, 70))

    def carregar_sprites_genericos(self, caminho_base):
        """Carrega sprites genéricos como fallback"""
        # Tenta encontrar qualquer arquivo de imagem na pasta
        extensoes = ('.png', '.jpg', '.jpeg', '.bmp')
        arquivos_encontrados = []
        
        for arquivo in os.listdir(caminho_base):
            if arquivo.lower().endswith(extensoes):
                arquivos_encontrados.append(arquivo)
        
        if arquivos_encontrados:
            # Usa no máximo 4 sprites
            for arquivo in arquivos_encontrados[:4]:
                img_path = os.path.join(caminho_base, arquivo)
                try:
                    img = pygame.image.load(img_path).convert_alpha()
                    img = self.remover_fundo(img, arquivo)  # Remove fundo também nos genéricos
                    img = pygame.transform.scale(img, (60, 70))
                    self.frames.append(img)
                except Exception as e:
                    print(f"[ERRO] Falha ao carregar sprite genérico {img_path}: {e}")

    def criar_placeholder(self):
        """Cria um sprite placeholder colorido baseado no tipo"""
        surf = pygame.Surface((60, 70), pygame.SRCALPHA)
        
        # Cores diferentes para cada tipo
        cores_por_tipo = {
            "gyarados": (255, 0, 0, 180),      # Vermelho
            "golisopod": (0, 0, 255, 180),    # Azul
            "elektross": (255, 255, 0, 180),     # Amarelo
            "sharpedo": (0, 128, 128, 180),    # Verde-azulado
        }
        
        cor = cores_por_tipo.get(self.tipo, (255, 0, 255, 180))  # Magenta padrão
        surf.fill(cor)
        
        # Desenha contorno e texto
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, 60, 70), 2)
        font = pygame.font.SysFont(None, 16)
        text = font.render(self.tipo[:8], True, (255, 255, 255))
        text_rect = text.get_rect(center=(30, 35))
        surf.blit(text, text_rect)
        
        return surf

    def mover_na_area(self):
        agora = pygame.time.get_ticks()
        
        # Calcular limites da área
        min_x = self.area_centro_x - self.area_largura // 2
        max_x = self.area_centro_x + self.area_largura // 2
        min_y = self.area_centro_y - self.area_altura // 2
        max_y = self.area_centro_y + self.area_altura // 2
        
        # Mover
        self.rect.x += self.direction_x * self.velocidade
        self.rect.y += self.direction_y * self.velocidade
        
        # Verificar limites horizontais
        if self.rect.left <= min_x or self.rect.right >= max_x:
            self.direction_x *= -1
            self.rect.x = max(min_x, min(self.rect.x, max_x - self.rect.width))
        
        # Verificar limites verticais
        if self.rect.top <= min_y or self.rect.bottom >= max_y:
            self.direction_y *= -1
            self.rect.y = max(min_y, min(self.rect.y, max_y - self.rect.height))
        
        # Mudar direção aleatoriamente de vez em quando
        if agora - self.ultima_mudanca > self.tempo_para_mudar:
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])
            self.ultima_mudanca = agora
            self.tempo_para_mudar = random.randint(1500, 4000)

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.last_update > self.anim_speed:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.last_update = agora

    def update(self, largura, altura):
        self.mover_na_area()
        self.animar()