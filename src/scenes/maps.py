import pygame
from config import *
import os
from src.entities.enemy import Enemy

class MapSystem:
    def __init__(self):
        self.maps = {
            "mapa1": {
                "name": "Velho Recife",
                "background": "assets/images/mapas/mapa.png",
                "player_start": (100, 300),
                "portas": [
                    {
                        "rect": pygame.Rect(578, 38, 80, 100),
                        "destination": "mapa2",
                        "color": CIANO,
                        "ativa": True
                    }
                ],
                "tipos_inimigos": ["gyarados", "gyarados", "golisopod", "golisopod", "gyarados", "golisopod"],
                "inimigos": [
                     {"x": 300, "y": 200},
                     {"x": 500, "y": 400},
                     {"x": 600, "y": 600},
                     {"x": 800, "y": 300},
                     {"x": 400, "y": 500},
                     {"x": 700, "y": 150}
                ],
                "bolhas": [
                    pygame.Rect(200, 100, 30, 30),
                    pygame.Rect(400, 300, 30, 30),
                    pygame.Rect(600, 500, 30, 30),
                    pygame.Rect(700, 600, 30, 30),
                    pygame.Rect(670, 400, 30, 30),
                    pygame.Rect(850, 200, 30, 30)
                ],
                "energias_escuras": [
                    pygame.Rect(300, 350, 25, 25),
                    pygame.Rect(550, 250, 25, 25),
                    pygame.Rect(750, 450, 25, 25),
                    pygame.Rect(900, 350, 25, 25)
                ],
                "saida": pygame.Rect(1300, 100, 100, 80)
            },
            "mapa2": {
                "name": "Caverna Submersa",
                "background": "assets/images/mapas/mapa2.png",
                "player_start": (100, 100),
                "portas": [
                    {
                        "rect": pygame.Rect(578, 650, 100, 50),
                        "destination": "mapa3",
                        "color": VERDE,
                        "ativa": True
                    }
                ],
                "tipos_inimigos": ["golisopod", "elektross", "golisopod", "elektross", "golisopod", "elektross"],
                "inimigos": [
                    {"x": 200, "y": 300},
                    {"x": 450, "y": 200},
                    {"x": 600, "y": 100},
                    {"x": 800, "y": 400},
                    {"x": 350, "y": 500},
                    {"x": 550, "y": 600}
                ],
                "bolhas": [
                    pygame.Rect(150, 400, 30, 30),
                    pygame.Rect(300, 150, 30, 30),
                    pygame.Rect(500, 350, 30, 30),
                    pygame.Rect(700, 250, 30, 30),
                    pygame.Rect(850, 550, 30, 30)
                ],
                "energias_escuras": [
                    pygame.Rect(250, 300, 25, 25),
                    pygame.Rect(450, 450, 25, 25),
                    pygame.Rect(650, 200, 25, 25),
                    pygame.Rect(800, 500, 25, 25)
                ],
                "saida": pygame.Rect(1400, 200, 120, 120)
            },
            "mapa3": {
                "name": "Recife de Coral",
                "background": "assets/images/mapas/mapa3.png",
                "player_start": (400, 300),
                "portas": [
                    {
                        "rect": pygame.Rect(578, 300, 80, 100),
                        "destination": "mapa4",
                        "color": None,
                        "ativa": True
                    }
                ],
                "tipos_inimigos": ["gyarados", "elektross", "sharpedo", "golisopod", "elektross"],
                "inimigos": [
                    {"x": 100, "y": 200},
                    {"x": 300, "y": 400},
                    {"x": 600, "y": 300},
                    {"x": 200, "y": 100},
                    {"x": 500, "y": 500}
                ],
                "bolhas": [
                    pygame.Rect(250, 250, 30, 30),
                    pygame.Rect(450, 450, 30, 30),
                    pygame.Rect(650, 150, 30, 30),
                    pygame.Rect(150, 350, 30, 30),
                    pygame.Rect(800, 400, 30, 30)
                ],
                "energias_escuras": [
                    pygame.Rect(350, 200, 25, 25),
                    pygame.Rect(500, 350, 25, 25),
                    pygame.Rect(700, 280, 25, 25),
                    pygame.Rect(300, 450, 25, 25)
                ],
                "saida": pygame.Rect(1500, 50, 100, 80)
            },
            "mapa4": {
                "name": "Jardim Submarino",
                "background": "assets/images/mapas/mapa4.png",
                "player_start": (800, 300),
                "portas": [
                    {
                        "rect": pygame.Rect(960, 300, 80, 100),
                        "destination": "mapa5",
                        "color": VERDE,
                        "ativa": True
                    }
                ],
                "tipos_inimigos": ["sharpedo", "sharpedo", "elektross", "sharpedo"],
                "inimigos": [
                    {"x": 100, "y": 200},
                    {"x": 300, "y": 400},
                    {"x": 600, "y": 300},
                    {"x": 200, "y": 100}
                ],
                "bolhas": [
                    pygame.Rect(250, 250, 30, 30),
                    pygame.Rect(450, 450, 30, 30),
                    pygame.Rect(650, 150, 30, 30),
                    pygame.Rect(150, 350, 30, 30)
                ],
                "energias_escuras": [
                    pygame.Rect(400, 300, 25, 25),
                    pygame.Rect(600, 200, 25, 25),
                    pygame.Rect(800, 400, 25, 25)
                ],
                "saida": pygame.Rect(1500, 50, 100, 80)
            },
            "mapa5": {
                "name": "Sala de Máquinas Submersa",
                "background": "assets/images/mapas/mapa5.png",
                "player_start": (400, 300),
                "portas": [
                    {
                        "rect": pygame.Rect(1030, 500, 80, 100),
                        "destination": "mapa6",
                        "color": None,
                        "ativa": True
                    }
                ],
                "tipos_inimigos": ["elektross", "sharpedo", "golisopod", "elektross"],
                "inimigos": [
                    {"x": 100, "y": 200},
                    {"x": 300, "y": 400},
                    {"x": 600, "y": 300},
                    {"x": 200, "y": 100}
                ],
                "bolhas": [
                    pygame.Rect(250, 250, 30, 30),
                    pygame.Rect(450, 450, 30, 30),
                    pygame.Rect(650, 150, 30, 30),
                    pygame.Rect(150, 350, 30, 30)
                ],
                "energias_escuras": [
                    pygame.Rect(350, 250, 25, 25),
                    pygame.Rect(550, 350, 25, 25),
                    pygame.Rect(750, 150, 25, 25),
                    pygame.Rect(450, 450, 25, 25)
                ],
                "saida": pygame.Rect(1500, 50, 100, 80)
            },
            "mapa6": {
                "name": "Sala do Rei",
                "background": "assets/images/mapas/mapa6.png",
                "player_start": (400, 300),
                "portas": [
                    # Último mapa não tem portas para frente
                ],
                "tipos_inimigos": ["sharpedo", "elektross", "golisopod", "gyarados"],
                "inimigos": [
                    {"x": 100, "y": 200},
                    {"x": 300, "y": 400},
                    {"x": 600, "y": 300},
                    {"x": 200, "y": 100}
                ],
                "bolhas": [
                    pygame.Rect(250, 250, 30, 30),
                    pygame.Rect(450, 450, 30, 30),
                    pygame.Rect(650, 150, 30, 30),
                    pygame.Rect(150, 350, 30, 30)
                ],
                "energias_escuras": [
                    pygame.Rect(300, 200, 25, 25),
                    pygame.Rect(500, 300, 25, 25),
                    pygame.Rect(700, 400, 25, 25),
                    pygame.Rect(400, 500, 25, 25)
                ],
                "saida": pygame.Rect(1500, 50, 100, 80)
            }
        }

        self.mapa_atual = "mapa1"
        self.backgrounds = {}

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

    def criar_inimigos_para_mapa(self, mapa_id):
        """Cria instâncias de Enemy para um mapa específico com tipos diferentes"""
        inimigos_group = pygame.sprite.Group()
        if mapa_id in self.maps:
            mapa_data = self.maps[mapa_id]
            
            # Defina áreas diferentes baseadas no mapa
            areas_por_mapa = {
                "mapa1": [
                    {"area_largura": 150, "area_altura": 100},
                    {"area_largura": 200, "area_altura": 120}
                ],
                "mapa2": [
                    {"area_largura": 180, "area_altura": 150},
                    {"area_largura": 160, "area_altura": 100},
                    {"area_largura": 200, "area_altura": 120}
                ],
                "mapa3": [
                    {"area_largura": 150, "area_altura": 100},
                    {"area_largura": 200, "area_altura": 120},
                    {"area_largura": 180, "area_altura": 150},
                    {"area_largura": 160, "area_altura": 100}
                ],
                "mapa4": [
                    {"area_largura": 150, "area_altura": 100},
                    {"area_largura": 200, "area_altura": 120},
                    {"area_largura": 180, "area_altura": 150},
                    {"area_largura": 160, "area_altura": 100}
                ],
                "mapa5": [
                    {"area_largura": 150, "area_altura": 100},
                    {"area_largura": 200, "area_altura": 120},
                    {"area_largura": 180, "area_altura": 150},
                    {"area_largura": 160, "area_altura": 100}
                ],
                "mapa6": [
                    {"area_largura": 150, "area_altura": 100},
                    {"area_largura": 200, "area_altura": 120},
                    {"area_largura": 180, "area_altura": 150},
                    {"area_largura": 160, "area_altura": 100}
                ]
            }
            
            areas = areas_por_mapa.get(mapa_id, [{"area_largura": 200, "area_altura": 150}])
            tipos_inimigos = mapa_data.get("tipos_inimigos", ["gyarados"])  # Padrão caso não exista
            
            for i, inimigo_data in enumerate(mapa_data["inimigos"]):
                # Usar área específica ou padrão
                area = areas[i] if i < len(areas) else {"area_largura": 200, "area_altura": 150}
                
                # Usar tipo específico ou padrão
                tipo = tipos_inimigos[i] if i < len(tipos_inimigos) else "gyarados"
                
                enemy = Enemy(
                    inimigo_data["x"], 
                    inimigo_data["y"],
                    tipo=tipo,  # PASSA O TIPO ESPECÍFICO
                    area_largura=area["area_largura"],
                    area_altura=area["area_altura"]
                )
                inimigos_group.add(enemy)
                
                print(f"✅ Criado inimigo {tipo} na posição ({inimigo_data['x']}, {inimigo_data['y']})")
                
        return inimigos_group

    def trocar_mapa(self, novo_mapa, player):
        """Troca para um novo mapa e reposiciona o jogador"""
        if novo_mapa in self.maps:
            self.mapa_atual = novo_mapa
            start_x, start_y = self.maps[novo_mapa]["player_start"]
            player.x = start_x
            player.y = start_y
            print(f"🎮 Jogador movido para {novo_mapa} na posição {start_x}, {start_y}")
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

    def desenhar_energias_escuras(self, tela):
        """Desenha as energias escuras do mapa atual"""
        mapa_data = self.get_mapa_atual()
        for energia in mapa_data["energias_escuras"]:
            # Desenha um círculo roxo escuro com brilho
            pygame.draw.circle(tela, ENERGIA_ESCURA, energia.center, energia.width // 2)
            pygame.draw.circle(tela, (150, 50, 200), energia.center, energia.width // 3)
            pygame.draw.circle(tela, (200, 100, 255), energia.center, energia.width // 6)