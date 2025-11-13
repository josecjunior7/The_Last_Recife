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
        """Carrega sprites baseados no tipo de inimigo"""
        try:
            # Define os arquivos de sprite para cada tipo
            sprites_por_tipo = {
                "gyarados": ["gyaradosSP1.png", "gyaradosSP2.png", "gyaradosSP3.png", ],
                "golisopod": ["golisopodSP1.png", "golisopodSP2.png", "golisopodSP3.png", "golisopodSP4.png"],
                "elektross": ["elektrossSP1.png", "elektrossSP2.png", "elektrossSP3.png"],
                "sharpedo": ["sharpedoSP1.png", "sharpedoSP2.png", "sharpedoSP3.png"],
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
                        img = pygame.image.load(img_path).convert_alpha()
                        # Ajusta o tamanho baseado no tipo
                        tamanho = self.definir_tamanho_por_tipo()
                        img = pygame.transform.scale(img, tamanho)
                        self.frames.append(img)
                        print(f"[SUCESSO] Sprite carregado: {img_path}")
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