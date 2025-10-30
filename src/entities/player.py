import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        self.carregar_sprites()
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = 5
        self.anim_speed = 250  # milissegundos entre frames
        self.last_update = pygame.time.get_ticks()

    def carregar_sprites(self):
        caminho = os.path.join("assets", "images", "sprites")
        nomes = ["aelyonSP1.jpeg", "aelyonSP2.jpeg", "aelyonSP3.jpeg", "aelyonSP4.jpeg"]
        for nome in nomes:
            img_path = os.path.join(caminho, nome)
            if os.path.exists(img_path):
                img = pygame.image.load(os.path.join(caminho, nome)).convert()
                img.set_colorkey((0, 0, 0))
                img = pygame.transform.scale(img, (50, 60))
                self.frames.append(img)
            else:
                print(f"[ERRO] Sprite não encontrado: {img_path}")

        if not self.frames:
            # Evita erro caso nenhuma imagem seja encontrada
            self.frames = [pygame.Surface((50, 60))]
            self.frames[0].fill((255, 0, 255))

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
