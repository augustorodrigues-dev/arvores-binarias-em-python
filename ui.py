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
                "FASE 1: ÁRVORE RUBRO-NEGRA (Red-Black)",
                "",
                "--- TEORIA ---",
                "Balanceamento baseado em cores (Vermelho/Preto).",
                "Regras principais:",
                "1. A raiz é sempre preta.",
                "2. Não podem existir dois nós vermelhos seguidos.",
                "3. Todo caminho até uma folha tem o mesmo nº de nós pretos.",
                "",
                "--- COMANDOS ---",
                "[I] Inserir: Adiciona nó (inicia Vermelho).",
                "[X] Remover: Remove e rebalanceia.",
                "[A] / [F]: Auto-Inserção e Preenchimento Turbo.",
                "[M] Misturar Fila | [R] Resetar.",
            ],
            2: [
                "FASE 2: ÁRVORE 2-3-4 (B-Tree Ordem 4)",
                "",
                "--- TEORIA ---",
                "Árvore multi-caminho balanceada.",
                "• Nó 2: 1 chave, 2 filhos.",
                "• Nó 3: 2 chaves, 3 filhos.",
                "• Nó 4: 3 chaves, 4 filhos.",
                "Cresce 'para cima' dividindo nós cheios (Splits).",
                "",
                "--- COMANDOS ---",
                "[I] Inserir: Divide nós cheios ao descer.",
                "[B] Buscar: Visualiza o caminho.",
                "[X] Remover: Tenta remover (Merge/Empréstimo).",
            ]
        }

    def _draw_text(self, txt, x, y, color=BRANCO, font=None, center_x=False, center_y=False):
        if font is None: font = self.fonte_normal
        surf = font.render(str(txt), True, color)
        rect = surf.get_rect()
        if center_x and center_y: rect.center = (x, y)
        elif center_x: rect.centerx = x; rect.top = y
        elif center_y: rect.left = x; rect.centery = y
        else: rect.topleft = (x, y)
        self.tela.blit(surf, rect)

    def draw_intro(self, typed_chars, intro_text):
        self.tela.fill(PRETO)
        if self.logo:
            self.tela.blit(self.logo, self.logo.get_rect(center=(LARGURA / 2, ALTURA / 3)))

        chars = typed_chars
        for i, line in enumerate(intro_text):
            if chars <= 0: break
            rend = line[:int(chars)]
            self._draw_text(rend, LARGURA / 2, ALTURA * 0.6 + i * 30, center_x=True)
            chars -= len(line)

        if typed_chars >= sum(len(s) for s in intro_text):
            self._draw_text("Pressione qualquer tecla para iniciar.", 
                            LARGURA / 2, ALTURA - 60, color=AMARELO, center_x=True)

    def draw_hud(self, fase, msgs):
        panel_surf = pygame.Surface((LARGURA, 80))
        panel_surf.set_alpha(COR_PAINEL[3])
        panel_surf.fill(COR_PAINEL[:3])
        self.tela.blit(panel_surf, (0, 0))
        pygame.draw.line(self.tela, AMARELO, (0, 80), (LARGURA, 80), 2)

        fase_nomes = {1: "Rubro-Negra", 2: "2-3-4"}
        
        titulo = f"HELLDIVERS: OPERAÇÃO ÁRVORES | FASE {fase}: {fase_nomes.get(fase, 'Desconhecida')}"
        self._draw_text(titulo, 20, 15, font=self.fonte_titulo)
        
        controles = "[1-2]Fase [A]Auto [F]Turbo [M]Mix [I]Insert [X]Del [B]Busca [R]Reset"
        self._draw_text(controles, 20, 50, color=CINZA_CLARO, font=self.fonte_pequena)

        if msgs:
            last_msg = msgs[-1]
            txt_surf = self.fonte_normal.render("LOG: " + last_msg, True, BRANCO)
            bg_rect = txt_surf.get_rect(topleft=(20, 85))
            bg_rect.inflate_ip(10, 4)
            s = pygame.Surface((bg_rect.width, bg_rect.height))
            s.set_alpha(200); s.fill(PRETO)
            self.tela.blit(s, bg_rect.topleft)
            self.tela.blit(txt_surf, (20, 85))

    def draw_tutorial(self, fase):
        w, h = 700, 420
        x, y = (LARGURA - w) / 2, (ALTURA - h) / 2
        s = pygame.Surface((w, h)); s.set_alpha(COR_PAINEL[3]); s.fill(COR_PAINEL[:3])
        self.tela.blit(s, (x, y))
        pygame.draw.rect(self.tela, AMARELO, (x, y, w, h), 3)

        txts = self.tutoriais.get(fase, ["Tutorial não disponível."])
        y_off = 40
        for i, line in enumerate(txts):
            font = self.fonte_titulo if i==0 else self.fonte_normal
            color = AMARELO if i==0 else BRANCO
            if "---" in line: color = AZUL
            elif "[" in line: color = VERDE
            
            self._draw_text(line, LARGURA/2, y + y_off, color=color, font=font, center_x=True)
            y_off += 25
        
        self._draw_text("Pressione qualquer tecla para fechar.", LARGURA/2, y+h-30, color=CINZA_CLARO, center_x=True)