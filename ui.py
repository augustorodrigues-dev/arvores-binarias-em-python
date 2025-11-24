# ui.py
import pygame
from config import *

class UIManager:
    def __init__(self, tela, fonte_titulo, fonte_normal, fonte_pequena):
        self.tela = tela
        self.fonte_titulo = fonte_titulo
        self.fonte_normal = fonte_normal
        self.fonte_pequena = fonte_pequena

        try:
            self.logo = pygame.image.load("assets/logo.png").convert_alpha()
            self.logo = pygame.transform.scale(
                self.logo,
                (300, int(300 * self.logo.get_height() / self.logo.get_width()))
            )
        except Exception:
            self.logo = None

        self.tutoriais = {
            1: [
                "FASE 1: ÁRVORE AVL",
                "",
                "CONCEITO: Árvore Binária de Busca com balanceamento por altura.",
                "Toda inserção/remoção é seguida de rotações para manter |FB| <= 1.",
                "",
                "CONTROLES:",
                " • [I] Insere valor aleatório.",
                " • Clique em um nó para selecioná-lo.",
                " • [X] Remove a chave do nó selecionado.",
                " • [B] Destaca o caminho de busca.",
            ],
            2: [
                "FASE 2: ÁRVORE RUBRO-NEGRA",
                "",
                "CONCEITO: Balanceamento por cores (Vermelho/Preto).",
                "Garante que nenhum caminho seja muito mais longo que outro.",
                "",
                "CONTROLES:",
                " • [I] Insere valor aleatório.",
                " • Clique para selecionar.",
                " • [B] Caminho de busca.",
            ],
            3: [
                "FASE 3: ÁRVORE 2-3-4",
                "",
                "CONCEITO: Árvore multi-way (Nós podem ter 1, 2 ou 3 chaves).",
                "Cresce 'para cima' dividindo nós cheios.",
                "",
                "CONTROLES:",
                " • [I] Insere valor.",
                " • Clique para selecionar.",
                " • [B] Busca.",
            ],
            4: [
                "FASE 4: KD-TREE (VISÃO HIERÁRQUICA)",
                "",
                "CONCEITO: Visualização da ESTRUTURA da árvore k-dimensional.",
                "Observe como a profundidade aumenta conforme inserimos pontos.",
                "Nós pares cortam X (Vermelho), Ímpares cortam Y (Azul).",
                "",
                "Esta visão ignora a posição espacial real para focar",
                "nas relações pai-filho.",
                "",
                "CONTROLES:",
                " • [I] Insere ponto (X, Y).",
                " • [B] Busca ponto.",
            ],
            5: [
                "FASE 5: KD-TREE (VISÃO ESPACIAL 2D)",
                "",
                "CONCEITO: Visualização do ESPAÇO particionado.",
                "Aqui vemos onde os pontos realmente estão no plano 2D.",
                "",
                " • Linhas Vermelhas: Cortes verticais (Eixo X).",
                " • Linhas Azuis: Cortes horizontais (Eixo Y).",
                "",
                "Cada linha divide a região atual em duas novas regiões.",
                "",
                "CONTROLES:",
                " • [I] Insere ponto.",
                " • Clique nos pontos para ver suas coordenadas.",
            ]
        }

    def _draw_text(self, txt, x, y, color=BRANCO, font=None, center_x=False, center_y=False):
        if font is None: font = self.fonte_normal
        surf = font.render(str(txt), True, color)
        rect = surf.get_rect()
        if center_x and center_y: rect.center = (x, y)
        elif center_x:
            rect.centerx = x
            rect.top = y
        elif center_y:
            rect.left = x
            rect.centery = y
        else: rect.topleft = (x, y)
        self.tela.blit(surf, rect)

    def draw_intro(self, typed_chars, intro_text):
        self.tela.fill(PRETO)
        if self.logo:
            self.tela.blit(self.logo, self.logo.get_rect(center=(LARGURA / 2, ALTURA / 3)))

        chars_to_render = typed_chars
        for i, line in enumerate(intro_text):
            if chars_to_render <= 0: break
            render_text = line[:int(chars_to_render)]
            self._draw_text(render_text, LARGURA / 2, ALTURA * 0.6 + i * 30, center_x=True)
            chars_to_render -= len(line)

        total_chars = sum(len(s) for s in intro_text)
        if typed_chars >= total_chars:
            self._draw_text("Pressione qualquer tecla para iniciar.", 
                            LARGURA / 2, ALTURA - 60, color=AMARELO, center_x=True)

    def draw_hud(self, fase, msgs):
        panel_surf = pygame.Surface((LARGURA, 80))
        panel_surf.set_alpha(COR_PAINEL[3])
        panel_surf.fill(COR_PAINEL[:3])
        self.tela.blit(panel_surf, (0, 0))
        pygame.draw.line(self.tela, AMARELO, (0, 80), (LARGURA, 80), 2)

        fase_nomes = {
            1: "AVL (Estrutura)", 
            2: "Rubro-Negra (Estrutura)", 
            3: "2-3-4 (Estrutura)", 
            4: "KD-Tree (Hierarquia)",
            5: "KD-Tree (Plano 2D)"
        }
        
        titulo = "HELLDIVERS: OPERAÇÃO ÁRVORES | FASE %d: %s" % (fase, fase_nomes.get(fase, "Desconhecida"))
        self._draw_text(titulo, 20, 15, font=self.fonte_titulo)
        
        controles = "[1-5] Fase | [I] Inserir | [X] Remover | [B] Buscar | [T] Tutorial"
        self._draw_text(controles, 20, 50)

        if msgs:
            last_msg = msgs[-1]
            surf = self.fonte_normal.render("LOG: " + last_msg, True, BRANCO)
            rect = surf.get_rect(topright=(LARGURA - 20, 50))
            self.tela.blit(surf, rect)

    def draw_tutorial(self, fase):
        panel_w, panel_h = 700, 420
        panel_x, panel_y = (LARGURA - panel_w) / 2, (ALTURA - panel_h) / 2
        panel_surf = pygame.Surface((panel_w, panel_h))
        panel_surf.set_alpha(COR_PAINEL[3])
        panel_surf.fill(COR_PAINEL[:3])
        self.tela.blit(panel_surf, (panel_x, panel_y))
        pygame.draw.rect(self.tela, AMARELO, (panel_x, panel_y, panel_w, panel_h), 3)

        tutorial_text = self.tutoriais.get(fase, ["Tutorial não encontrado."])
        for i, line in enumerate(tutorial_text):
            font = self.fonte_titulo if i == 0 else self.fonte_normal
            color = AMARELO if i == 0 or "CONTROLES" in line else BRANCO
            self._draw_text(line, LARGURA / 2, panel_y + 40 + i * 22, color=color, font=font, center_x=True)

        self._draw_text("Pressione qualquer tecla para fechar.", LARGURA / 2, panel_y + panel_h - 30, color=CINZA_CLARO, center_x=True)