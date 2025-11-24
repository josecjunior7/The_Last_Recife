import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, personagem="masculino"):
        super().__init__()
        self.personagem = personagem
        self.frames = []
        self.carregar_sprites()
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = 5
        self.anim_speed = 250  # milissegundos entre frames
        self.last_update = pygame.time.get_ticks()

    def carregar_sprites(self):
        # Define os nomes dos sprites baseado no personagem escolhido
        if self.personagem == "feminino":
            nomes = ["thalic1.png", "thalic2.png", "thalic3.png", "thalic4.png", "thalic5.png"]
            caminho_base = os.path.join("assets", "images", "sprites", "move")
        else:  # masculino (padrão)
            nomes = ["aelyonSP1.jpeg", "aelyonSP2.jpeg", "aelyonSP3.jpeg", "aelyonSP4.jpeg"]
            caminho_base = os.path.join("assets", "images", "sprites", "move")

        # Tenta carregar os sprites específicos
        sprites_carregados = 0
        for nome in nomes:
            img_path = os.path.join(caminho_base, nome)
            
            # Se não encontrar no caminho específico, tenta no caminho padrão
            if not os.path.exists(img_path):
                img_path = os.path.join("assets", "images", "sprites", "move", nome)
            
            if os.path.exists(img_path):
                try:
                    img = pygame.image.load(img_path).convert()
                    img.set_colorkey((0, 0, 0))  # Remove fundo preto
                    img = pygame.transform.scale(img, (50, 60))
                    self.frames.append(img)
                    sprites_carregados += 1
                    print(f"✅ Sprite carregado: {img_path}")
                except Exception as e:
                    print(f"⚠️ Erro ao carregar sprite {img_path}: {e}")
            else:
                print(f"⚠️ Sprite não encontrado: {img_path}")

        # Fallback: cria sprites coloridos se nenhum for encontrado
        if sprites_carregados == 0:
            print("🚨 Nenhum sprite encontrado. Criando sprites coloridos...")
            cores = []
            if self.personagem == "feminino":
                # Cores para personagem feminino (tons de rosa/roxo)
                cores = [(255, 182, 193), (219, 112, 147), (199, 21, 133), (186, 85, 211)]
            else:
                # Cores para personagem masculino (tons de azul)
                cores = [(30, 144, 255), (65, 105, 225), (70, 130, 180), (100, 149, 237)]
            
            for cor in cores:
                surf = pygame.Surface((50, 60))
                surf.fill(cor)
                # Adiciona um "rosto" simples para diferenciar
                pygame.draw.circle(surf, (255, 255, 255), (25, 20), 8)  # Cabeça
                pygame.draw.rect(surf, (255, 255, 255), (15, 35, 20, 15))  # Corpo
                self.frames.append(surf)

    def mover(self, teclas, largura, altura):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < largura:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.rect.bottom < altura:
            self.rect.y += self.velocidade

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.last_update > self.anim_speed:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.last_update = agora

    def update(self, teclas, largura, altura):
        self.mover(teclas, largura, altura)
        self.animar()

    def get_personagem(self):
        """Retorna o tipo de personagem selecionado"""
        return self.personagem