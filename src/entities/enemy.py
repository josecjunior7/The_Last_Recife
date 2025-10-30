import pygame
import os
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, area_largura=200, area_altura=150):
        super().__init__()
        self.frames = []
        self.carregar_sprites()
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        
        # Área de movimento
        self.area_centro_x = x
        self.area_centro_y = y
        self.area_largura = area_largura
        self.area_altura = area_altura
        
        # Movimento
        self.velocidade = random.uniform(1.0, 2.0)
        self.anim_speed = 250
        self.last_update = pygame.time.get_ticks()
        
        # Direção atual
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.tempo_para_mudar = random.randint(1500, 4000)
        self.ultima_mudanca = pygame.time.get_ticks()

    def carregar_sprites(self):
        caminho = os.path.join("assets", "images", "sprites", "vilains")
        nomes = ["gyaradosSP1.jpeg", "gyaradosSP2.jpeg", "gyaradosSP3.jpeg", "gyaradosSP4.jpeg"]
        for nome in nomes:
            img_path = os.path.join(caminho, nome)
            if os.path.exists(img_path):
                img = pygame.image.load(img_path).convert()
                img.set_colorkey((0, 0, 0))
                img = pygame.transform.scale(img, (50, 60))
                self.frames.append(img)
            else:
                print(f"[ERRO] Sprite não encontrado: {img_path}")

        if not self.frames:
            self.frames = [pygame.Surface((50, 60))]
            self.frames[0].fill((255, 0, 255))

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