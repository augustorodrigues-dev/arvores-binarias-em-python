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
                "FASE 1: ÁRVORE AVL (Adelson-Velsky e Landis)",
                "",
                "--- TEORIA ---",
                "É uma árvore binária de busca auto-balanceável.",
                "Regra: A diferença de altura entre as subárvores esquerda",
                "e direita de qualquer nó não pode ser maior que 1.",
                "Correção: Usa Rotações (Simples ou Duplas) após inserção/remoção.",
                "",
                "--- COMANDOS ---",
                "[I] Inserir: Adiciona o próximo número (verde) da fila.",
                "[X] Remover: Clique em um nó com o mouse, depois tecle X.",
                "[B] Buscar: Clique em um nó, depois tecle B para ver o caminho.",
                "[A] Auto: Inicia inserção automática lenta (Passo a passo).",
                "[F] Fast (Turbo): Preenche a árvore inteira em alta velocidade.",
                "[M] Misturar: Gera novos números aleatórios na fila.",
                "[R] Reset: Limpa a árvore e restaura a fila original.",
                "[Espaço] Pausar: Interrompe a inserção automática.",
            ],
            2: [
                "FASE 2: ÁRVORE RUBRO-NEGRA (Red-Black)",
                "",
                "--- TEORIA ---",
                "Balanceamento baseado em cores (Vermelho/Preto) nos nós.",
                "Regras principais:",
                "1. A raiz é sempre preta.",
                "2. Não podem existir dois nós vermelhos seguidos (Pai-Filho).",
                "3. Todo caminho da raiz até uma folha tem o mesmo número de nós pretos.",
                "",
                "--- COMANDOS ---",
                "[I] Inserir: Adiciona o próximo da fila (inicia Vermelho).",
                "[X] Remover: Remove nó selecionado (rebalanceamento complexo).",
                "[A] / [F]: Modos de preenchimento automático.",
                "[M] / [R]: Gerenciar fila e resetar.",
            ],
            3: [
                "FASE 3: ÁRVORE 2-3-4 (B-Tree Ordem 4)",
                "",
                "--- TEORIA ---",
                "Uma árvore multi-caminho (Multi-way).",
                "• Nó 2: 1 chave, 2 filhos.",
                "• Nó 3: 2 chaves, 3 filhos.",
                "• Nó 4: 3 chaves, 4 filhos.",
                "Crescimento: Divide nós cheios (Splits) e cresce para cima.",
                "",
                "--- COMANDOS ---",
                "[I] Inserir: Adiciona chave. Divide nós cheios ao descer.",
                "[B] Buscar: Mostra em qual nó a chave está.",
                "[X] Remover: Tenta remover (Merge ou Empréstimo de irmãos).",
                "Nota: A visualização usa retângulos para representar nós agrupados.",
            ],
            4: [
                "FASE 4: KD-TREE (VISÃO HIERÁRQUICA)",
                "",
                "--- TEORIA ---",
                "Árvore binária para particionamento de espaço k-dimensional.",
                "Neste exemplo, k=2 (Pontos X, Y).",
                "• Nível Par (0, 2...): Compara coordenada X (Corte Vertical).",
                "• Nível Ímpar (1, 3...): Compara coordenada Y (Corte Horizontal).",
                "",
                "--- COMANDOS ---",
                "[I] Inserir: Insere o próximo ponto (X, Y) da fila.",
                "[M] Misturar: Gera novos pontos aleatórios (X, Y).",
                "[F] Fast Fill: Preenche o espaço rapidamente.",
                "Esta visão mostra a estrutura de pais e filhos da árvore.",
            ],
            5: [
                "FASE 5: KD-TREE (VISÃO ESPACIAL 2D)",
                "",
                "--- TEORIA ---",
                "Mesma árvore da Fase 4, mas visualizada geometricamente.",
                "• Linha Vermelha: Corte no eixo X.",
                "• Linha Azul: Corte no eixo Y.",
                "Cada nó divide a região do plano em duas partes menores.",
                "",
                "--- COMANDOS ---",
                "[I] Inserir: Adiciona ponto e traça a linha de corte.",
                "[B] Buscar: Anima a navegação pelos retângulos do espaço.",
                "[R] Reset: Limpa o plano.",
                "Observe como os pontos se organizam no espaço.",
            ],
            6: [
                "FASE 6: SPLAY TREE (Árvore Auto-Ajustável)",
                "",
                "--- TEORIA ---",
                "Árvore que move o elemento acessado para a RAIZ.",
                "Usa operações 'Splay' (Zig, Zig-Zig, Zig-Zag).",
                "Ótima para caches: dados acessados frequentemente ficam no topo.",
                "",
                "--- COMANDOS ESPECIAIS ---",
                "[B] Buscar: Ao buscar, o nó caminha até virar a RAIZ.",
                "[I] Inserir: O novo nó sempre termina como RAIZ.",
                "[X] Remover: Faz Splay no nó, remove, e une as árvores.",
                "Experimente buscar o mesmo número várias vezes!",
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
            1: "AVL", 
            2: "Rubro-Negra", 
            3: "2-3-4", 
            4: "KD-Tree (Hierarquia)",
            5: "KD-Tree (Plano 2D)",
            6: "Splay"
        }
        
        titulo = f"HELLDIVERS: OPERAÇÃO ÁRVORES | FASE {fase}: {fase_nomes.get(fase, 'Desconhecida')}"
        self._draw_text(titulo, 20, 15, font=self.fonte_titulo)
        
        
        controles = "[1-6]Fase [M]Misturar [I]inserir [A]Auto Inserção [F]Preencher [B]Busca [X]Remover [R]Reset [T]Ajuda"
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
        panel_w, panel_h = 800, 550 
        panel_x, panel_y = (LARGURA - panel_w) / 2, (ALTURA - panel_h) / 2
        panel_surf = pygame.Surface((panel_w, panel_h))
        panel_surf.set_alpha(COR_PAINEL[3])
        panel_surf.fill(COR_PAINEL[:3])
        self.tela.blit(panel_surf, (panel_x, panel_y))
        pygame.draw.rect(self.tela, AMARELO, (panel_x, panel_y, panel_w, panel_h), 3)

        tutorial_text = self.tutoriais.get(fase, ["Tutorial não encontrado."])
        
        y_offset = 40
        for i, line in enumerate(tutorial_text):
            font = self.fonte_titulo if i == 0 else self.fonte_normal
            
           
            if i == 0: color = AMARELO 
            elif line.startswith("---"): color = AZUL 
            elif "[" in line and "]" in line: color = VERDE 
            else: color = BRANCO 

            self._draw_text(line, LARGURA / 2, panel_y + y_offset, color=color, font=font, center_x=True)
            y_offset += 25

        self._draw_text("Pressione qualquer tecla para fechar.", LARGURA / 2, panel_y + panel_h - 30, color=CINZA_CLARO, center_x=True)