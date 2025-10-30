import pygame
from config import *
import os

class MapSystem:
    def __init__(self):
        self.maps = {
            "mapa1": {
                "name": "Base Subaquática",
                "background": "assets/images/mapas/Mapa1.png",
                "player_start": (100, 300),
                "portas": [
                    {
                        "rect": pygame.Rect(1220, 250, 80, 100),
                        "destination": "mapa2",
                        "color": MARROM,
                        "ativa": True
                    },
                    {
                        "rect": pygame.Rect(50, 150, 80, 100), 
                        "destination": "mapa3",
                        "color": CIANO,
                        "ativa": False
                    }
                ],
                "inimigos": [
                    pygame.Rect(300, 200, 50, 50),
                    pygame.Rect(500, 400, 50, 50)
                ],
                "bolhas": [
                    pygame.Rect(200, 100, 30, 30),
                    pygame.Rect(400, 300, 30, 30),
                    pygame.Rect(600, 500, 30, 30)
                ],
                "saida": pygame.Rect(350, 500, 100, 80)
            },
            "mapa2": {
                "name": "Caverna Submersa",
                "background": "assets/images/mapas/mapa2.png",
                "player_start": (100, 100),
                "portas": [
                    {
                        "rect": pygame.Rect(50, 250, 80, 100),
                        "destination": "mapa1",
                        "color": None,
                        "ativa": True
                    },
                    {
                        "rect": pygame.Rect(650, 400, 80, 100),
                        "destination": "mapa3",
                        "color": VERDE,
                        "ativa": True
                    }
                ],
                "inimigos": [
                    pygame.Rect(200, 300, 50, 50),
                    pygame.Rect(450, 200, 50, 50),
                    pygame.Rect(600, 100, 50, 50)
                ],
                "bolhas": [
                    pygame.Rect(150, 400, 30, 30),
                    pygame.Rect(300, 150, 30, 30)
                ],
                "saida": pygame.Rect(700, 500, 80, 80)
            },
            "mapa3": {
                "name": "Recife de Coral",
                "background": "assets/images/mapas/mapa3.png",
                "player_start": (400, 300),
                "portas": [
                    {
                        "rect": pygame.Rect(100, 500, 80, 100),
                        "destination": "mapa4",
                        "color": None,
                        "ativa": True
                    },
                    {
                        "rect": pygame.Rect(500, 100, 80, 100),
                        "destination": "mapa2",
                        "color": None,
                        "ativa": True
                    }
                ],
                "inimigos": [
                    pygame.Rect(100, 200, 50, 50),
                    pygame.Rect(300, 400, 50, 50),
                    pygame.Rect(600, 300, 50, 50),
                    pygame.Rect(200, 100, 50, 50)
                ],
                "bolhas": [
                    pygame.Rect(250, 250, 30, 30),
                    pygame.Rect(450, 450, 30, 30),
                    pygame.Rect(650, 150, 30, 30),
                    pygame.Rect(150, 350, 30, 30)
                ],
                "saida": pygame.Rect(50, 50, 100, 80)
            },
            "mapa4": {
                "name": "Jardim Submarino",
                "background": "assets/images/mapas/mapa4.png",
                "player_start": (400, 300),
                "portas": [
                    {
                        "rect": pygame.Rect(100, 500, 80, 100),
                        "destination": "mapa5",
                        "color": None,
                        "ativa": True
                    },
                    {
                        "rect": pygame.Rect(500, 100, 80, 100),
                        "destination": "mapa1",
                        "color": None,
                        "ativa": True
                    }
                ],
                "inimigos": [
                    pygame.Rect(100, 200, 50, 50),
                    pygame.Rect(300, 400, 50, 50),
                    pygame.Rect(600, 300, 50, 50),
                    pygame.Rect(200, 100, 50, 50)
                ],
                "bolhas": [
                    pygame.Rect(250, 250, 30, 30),
                    pygame.Rect(450, 450, 30, 30),
                    pygame.Rect(650, 150, 30, 30),
                    pygame.Rect(150, 350, 30, 30)
                ],
                "saida": pygame.Rect(50, 50, 100, 80)
            },
            "mapa5": {
                "name": "Sala de Máquinas Submersa",
                "background": "assets/images/mapas/Mapa5.png",
                "player_start": (400, 300),
                "portas": [
                    {
                        "rect": pygame.Rect(100, 500, 80, 100),
                        "destination": "mapa6",
                        "color": None,
                        "ativa": True
                    },
                    {
                        "rect": pygame.Rect(500, 100, 80, 100),
                        "destination": "mapa4",
                        "color": None,
                        "ativa": True
                    }
                ],
                "inimigos": [
                    pygame.Rect(100, 200, 50, 50),
                    pygame.Rect(300, 400, 50, 50),
                    pygame.Rect(600, 300, 50, 50),
                    pygame.Rect(200, 100, 50, 50)
                ],
                "bolhas": [
                    pygame.Rect(250, 250, 30, 30),
                    pygame.Rect(450, 450, 30, 30),
                    pygame.Rect(650, 150, 30, 30),
                    pygame.Rect(150, 350, 30, 30)
                ],
                "saida": pygame.Rect(50, 50, 100, 80)
            },
            "mapa6": {
                "name": "Sala do rei",
                "background": "assets/images/mapas/Mapa6.png",
                "player_start": (400, 300),
                "portas": [
                    {
                        "rect": pygame.Rect(100, 500, 80, 100),
                        "destination": "mapa1",
                        "color": None,
                        "ativa": True
                    },
                    {
                        "rect": pygame.Rect(500, 100, 80, 100),
                        "destination": "mapa5",
                        "color": None,
                        "ativa": True
                    }
                ],
                "inimigos": [
                    pygame.Rect(100, 200, 50, 50),
                    pygame.Rect(300, 400, 50, 50),
                    pygame.Rect(600, 300, 50, 50),
                    pygame.Rect(200, 100, 50, 50)
                ],
                "bolhas": [
                    pygame.Rect(250, 250, 30, 30),
                    pygame.Rect(450, 450, 30, 30),
                    pygame.Rect(650, 150, 30, 30),
                    pygame.Rect(150, 350, 30, 30)
                ],
                "saida": pygame.Rect(50, 50, 100, 80)
            }
        }

        self.mapa_atual = "mapa1"
        self.backgrounds = {}

    # 🔧 Agora o método está dentro da classe
    def carregar_backgrounds(self):
        """Carrega todas as imagens de background"""
        caminho_base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # volta até a raiz

        for mapa_id, mapa_data in self.maps.items():
            try:
                caminho_completo = os.path.join(caminho_base, mapa_data["background"])
                self.backgrounds[mapa_id] = pygame.image.load(caminho_completo).convert()
                print(f"✅ Background de {mapa_id} carregado com sucesso!")
            except Exception as e:
                print(f"⚠️ Erro ao carregar background de {mapa_id}: {e}")
                surf = pygame.Surface((LARGURA, ALTURA))
                if mapa_id == "mapa1":
                    surf.fill((0, 0, 100))  # Azul escuro
                elif mapa_id == "mapa2":
                    surf.fill((50, 50, 50))  # Cinza escuro  
                else:
                    surf.fill((0, 100, 0))  # Verde escuro
                self.backgrounds[mapa_id] = surf

    def trocar_mapa(self, novo_mapa, player):
        """Troca para um novo mapa e reposiciona o jogador"""
        if novo_mapa in self.maps:
            self.mapa_atual = novo_mapa
            start_x, start_y = self.maps[novo_mapa]["player_start"]
            player.x = start_x
            player.y = start_y
            return True
        return False

    def get_mapa_atual(self):
        """Retorna os dados do mapa atual"""
        return self.maps[self.mapa_atual]

    def get_background_atual(self):
        """Retorna o background do mapa atual"""
        return self.backgrounds.get(self.mapa_atual, None)

    def desenhar_portas(self, tela):
        """Desenha as portas do mapa atual"""
        mapa_data = self.get_mapa_atual()
        for porta in mapa_data["portas"]:
            if porta["ativa"]:
                if porta["color"]:
                    pygame.draw.rect(tela, porta["color"], porta["rect"])
                pygame.draw.rect(tela, BRANCO, porta["rect"], 2)

                font = pygame.font.SysFont(None, 24)
                text = font.render("Porta", True, BRANCO)
                tela.blit(text, (porta["rect"].x + 10, porta["rect"].y + 40))
