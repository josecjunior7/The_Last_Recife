import pygame, sys

pygame.init()

print("🔹 Iniciando teste de janela...")

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Teste Pygame")

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    TELA.fill((0, 0, 128))  # Azul escuro
    pygame.display.flip()

pygame.quit()
print("✅ Fechou normalmente.")
