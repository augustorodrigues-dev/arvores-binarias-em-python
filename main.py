import pygame
import sys
import random
import math
from typing import Dict, Optional, Tuple, List

from config import *
from ui import UIManager
from fachada import EstruturaArvore
from rb import RBColor

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Helldivers: Árvores da Super-Terra")
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock = pygame.time.Clock()

        self.fonte_titulo = pygame.font.SysFont("consolas", 22, bold=True)
        self.fonte_normal = pygame.font.SysFont("consolas", 14)
        self.fonte_pequena = pygame.font.SysFont("consolas", 11)

        self.ui = UIManager(self.tela, self.fonte_titulo, self.fonte_normal, self.fonte_pequena)

        try:
            bg = pygame.image.load("assets/background.png").convert()
            self.background = pygame.transform.scale(bg, (LARGURA, ALTURA))
        except Exception:
            self.background = None

        self.game_state = "INTRO"
        self.fase = 1
        self.estrutura = EstruturaArvore("AVL")
        self.msgs: List[str] = []
        self.mostrar_tutorial = True

        self.selected_id: Optional[int] = None
        self.selected_key = None 
        self.path_destacado: List[int] = []

        self.node_positions: Dict[int, Tuple[int, int]] = {}
        self.node_positions_234: Dict[int, Tuple[int, int]] = {}

        self.intro_text = [
            "> Conexão estabelecida.",
            "> Bem-vindo, Helldiver.",
            "> Fases 1-3: Árvores Binárias e Multi-way.",
            "> Fase 4: KD-Tree (Visão Hierárquica).",
            "> Fase 5: KD-Tree (Visão Espacial 2D).",
            "> Pela Democracia Gerenciada!"
        ]
        self.typed_chars = 0
        self.last_char_time = 0

        self._carregar_demo_inicial()

    def _say(self, texto: str):
        if len(self.msgs) > 6: self.msgs.pop(0)
        self.msgs.append(texto)
        print("LOG:", texto)

    def _carregar_demo_inicial(self):
        # Fase 4 e 5 usam KDTree com tuplas
        if self.fase in (4, 5):
            for _ in range(12):
                x = random.randint(5, 95)
                y = random.randint(5, 95)
                self.estrutura.inserir((x, y))
            self._say("Dados espaciais (X, Y) carregados.")
        else:
            valores = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
            for v in valores:
                self.estrutura.inserir(v)
            self._say("Chaves numéricas carregadas.")

    def set_fase(self, f: int):
        self.fase = f
        # Mapeamento: 4 e 5 usam a mesma estrutura lógica 'KDT'
        tipos = {1: "AVL", 2: "RB", 3: "234", 4: "KDT", 5: "KDT"}
        
        self.estrutura = EstruturaArvore(tipos[f])
        self.selected_id = None
        self.selected_key = None
        self.path_destacado = []
        
        self._carregar_demo_inicial()
        self._say(f"Fase {f} iniciada. [T] para ajuda.")
        self.mostrar_tutorial = True

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit(0)
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: pygame.quit(); sys.exit(0)

            if self.game_state == "INTRO":
                if ev.type == pygame.KEYDOWN:
                    self.game_state = "JOGO"
                continue

            if self.mostrar_tutorial:
                if ev.type == pygame.KEYDOWN: self.mostrar_tutorial = False
                continue

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1: self.set_fase(1)
                elif ev.key == pygame.K_2: self.set_fase(2)
                elif ev.key == pygame.K_3: self.set_fase(3)
                elif ev.key == pygame.K_4: self.set_fase(4)
                elif ev.key == pygame.K_5: self.set_fase(5)
                elif ev.key == pygame.K_t: self.mostrar_tutorial = True
                elif ev.key == pygame.K_i: self._acao_inserir()
                elif ev.key == pygame.K_x: self._acao_remover()
                elif ev.key == pygame.K_b: self._acao_buscar()

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self._clique(ev.pos)

    def _acao_inserir(self):
        if self.fase in (4, 5):
            x = random.randint(1, 99)
            y = random.randint(1, 99)
            val = (x, y)
            self.estrutura.inserir(val)
            self._say(f"Inserido ponto {val}.")
        else:
            v = random.randint(1, 99)
            self.estrutura.inserir(v)
            self.path_destacado = []
            self._say(f"Inserida chave {v}.")

    def _acao_remover(self):
        if self.fase in (4, 5):
            self._say("Remoção indisponível na KD-Tree.")
            return
        if self.selected_key is None:
            self._say("Selecione um nó.")
            return
        if not self.estrutura.remover(self.selected_key):
            self._say("Remoção apenas para AVL (Fase 1).")
        else:
            self._say(f"Removido {self.selected_key}.")
            self.selected_id = None
            self.selected_key = None
            self.path_destacado = []

    def _acao_buscar(self):
        if self.selected_key is None:
            self._say("Selecione um nó para buscar.")
            return
        
        if self.fase == 3:
            caminho = self.estrutura.buscar_caminho_234(self.selected_key)
        else:
            caminho = self.estrutura.buscar_caminho_binaria(self.selected_key)
            
        if not caminho:
            self._say("Não encontrado.")
        else:
            self.path_destacado = caminho
            self._say(f"Caminho encontrado: {len(caminho)} nós.")

    def _clique(self, pos):
        x, y = pos
        self._atualizar_layout() # Garante que node_positions está atualizado para a fase atual
        
        # Lógica 2-3-4
        if self.fase == 3:
            for nid, (nx, ny) in self.node_positions_234.items():
                rect = pygame.Rect(nx - 25, ny - 15, 50, 30)
                if rect.collidepoint(x, y):
                    node = self.estrutura.tree.nodes[nid]
                    if node.keys:
                        self.selected_id = nid
                        self.selected_key = node.keys[0]
                        self.path_destacado = []
                        self._say(f"Selecionado 2-3-4: {node.keys[0]}...")
                    return
            return
        alvo = None
        menor = 999999
        for nid, (nx, ny) in self.node_positions.items():
            d = math.hypot(nx - x, ny - y)
            # Na fase 5 os pontos são pequenos, aumenta a precisão do clique
            raio_clique = RAIO_NO + 5 if self.fase != 5 else 15 
            if d <= raio_clique and d < menor:
                menor = d
                alvo = nid
        
        if alvo is not None:
            self.selected_id = alvo
            if self.fase in (4, 5):
                self.selected_key = self.estrutura.tree.nodes[alvo].point
                self._say(f"Ponto KD: {self.selected_key}")
            else:
                self.selected_key = self.estrutura.tree.nodes[alvo].key
                self._say(f"Chave: {self.selected_key}")
            self.path_destacado = []

    def update(self):
        if self.game_state == "INTRO":
            now = pygame.time.get_ticks()
            if now - self.last_char_time > 30:
                self.typed_chars += 1
                self.last_char_time = now

    def _atualizar_layout(self):
        self.node_positions = {}
        if self.estrutura.tree.root is None: return

        # === LAYOUT HIERÁRQUICO (Fases 1, 2, 4) ===
        if self.fase in (1, 2, 4):
            def layout_bin(nid, depth, x_min, x_max):
                if nid is None: return
                x = (x_min + x_max) // 2
                y = 120 + depth * 80
                self.node_positions[nid] = (x, y)
                
                if self.fase == 2: # RB
                    l = self.estrutura.tree._left(nid)
                    r = self.estrutura.tree._right(nid)
                else: # AVL e KD
                    l = self.estrutura.tree._get_left(nid)
                    r = self.estrutura.tree._get_right(nid)

                if l is not None: layout_bin(l, depth + 1, x_min, x - 40)
                if r is not None: layout_bin(r, depth + 1, x + 40, x_max)
            
            layout_bin(self.estrutura.tree.root, 0, 50, LARGURA - 50)

        # === LAYOUT ESPACIAL 2D (Fase 5) ===
        elif self.fase == 5:
            # Aqui mapeamos as coordenadas do DADO (0-100) para PIXELS da tela
            # Isso permite que o clique funcione na fase 5
            MARGEM_X = 250
            MARGEM_Y = 150
            L_UTIL = LARGURA - 2 * MARGEM_X
            A_UTIL = ALTURA - MARGEM_Y - 50
            OFFSET_X = MARGEM_X
            OFFSET_Y = 130

            def mapear_todos(nid):
                if nid is None: return
                node = self.estrutura.tree.nodes[nid]
                px, py = node.point
                sx = OFFSET_X + (px / 100) * L_UTIL
                sy = OFFSET_Y + (py / 100) * A_UTIL
                self.node_positions[nid] = (int(sx), int(sy))
                
                mapear_todos(self.estrutura.tree._get_left(nid))
                mapear_todos(self.estrutura.tree._get_right(nid))
            
            mapear_todos(self.estrutura.tree.root)

        # === LAYOUT 2-3-4 (Fase 3) ===
        elif self.fase == 3:
             self.node_positions_234 = {}
             def layout_234(nid, depth, x_min, x_max):
                node = self.estrutura.tree.nodes[nid]
                y = 120 + depth * 90
                if node.leaf or not node.children:
                    x = (x_min + x_max) // 2
                    self.node_positions_234[nid] = (x, y)
                else:
                    n_children = len(node.children)
                    child_centers = []
                    width = x_max - x_min
                    span = max(width // n_children, 80)
                    cur_x = x_min
                    for child_id in node.children:
                        layout_234(child_id, depth + 1, cur_x, cur_x + span)
                        if child_id in self.node_positions_234:
                            child_centers.append(self.node_positions_234[child_id][0])
                        cur_x += span
                    if child_centers: x = sum(child_centers) // len(child_centers)
                    else: x = (x_min + x_max) // 2
                    self.node_positions_234[nid] = (x, y)
             layout_234(self.estrutura.tree.root, 0, 80, LARGURA - 80)

    # Função de desenho recursivo do plano (apenas linhas e fundo)
    def _draw_kdtree_lines(self, nid, x_min, y_min, x_max, y_max):
        if nid is None: return
        node = self.estrutura.tree.nodes[nid]
        
        # Reutilizamos a lógica de conversão para consistência
        MARGEM_X = 250
        MARGEM_Y = 150
        L_UTIL = LARGURA - 2 * MARGEM_X
        A_UTIL = ALTURA - MARGEM_Y - 50
        OFFSET_X = MARGEM_X
        OFFSET_Y = 130

        def to_screen(vx, vy):
            return (OFFSET_X + (vx / 100) * L_UTIL, OFFSET_Y + (vy / 100) * A_UTIL)

        px, py = node.point
        sx, sy = to_screen(px, py)
        s_xmin, s_ymin = to_screen(x_min, y_min)
        s_xmax, s_ymax = to_screen(x_max, y_max)

        axis = node.axis
        cor = COR_EIXO_X if axis == 0 else COR_EIXO_Y
        
        if axis == 0: # Corte Vertical
            pygame.draw.line(self.tela, cor, (sx, s_ymin), (sx, s_ymax), 2)
            self._draw_kdtree_lines(self.estrutura.tree.adj[nid][0], x_min, y_min, px, y_max)
            self._draw_kdtree_lines(self.estrutura.tree.adj[nid][1], px, y_min, x_max, y_max)
        else: # Corte Horizontal
            pygame.draw.line(self.tela, cor, (s_xmin, sy), (s_xmax, sy), 2)
            self._draw_kdtree_lines(self.estrutura.tree.adj[nid][0], x_min, y_min, x_max, py)
            self._draw_kdtree_lines(self.estrutura.tree.adj[nid][1], x_min, py, x_max, y_max)


    def draw(self):
        if self.background: self.tela.blit(self.background, (0, 0))
        else: self.tela.fill(PRETO)

        if self.game_state == "INTRO":
            self.ui.draw_intro(self.typed_chars, self.intro_text)
            pygame.display.flip()
            return

        self._atualizar_layout()

        # === FASE 5: DESENHO DO PLANO 2D (Fundo + Linhas + Pontos) ===
        if self.fase == 5:
            # Fundo da área do gráfico
            MARGEM_X = 250
            MARGEM_Y = 150
            L_UTIL = LARGURA - 2 * MARGEM_X
            A_UTIL = ALTURA - MARGEM_Y - 50
            rect_fundo = pygame.Rect(MARGEM_X, 130, L_UTIL, A_UTIL)
            
            s = pygame.Surface((rect_fundo.width, rect_fundo.height))
            s.set_alpha(150)
            s.fill(COR_PLANO_FUNDO)
            self.tela.blit(s, rect_fundo.topleft)
            pygame.draw.rect(self.tela, CINZA, rect_fundo, 2)

            # Linhas de corte
            self._draw_kdtree_lines(self.estrutura.tree.root, 0, 0, 100, 100)

            # Pontos (usando node_positions calculado no layout espacial)
            for nid, (x, y) in self.node_positions.items():
                if nid in self.path_destacado:
                    pygame.draw.circle(self.tela, AMARELO, (x, y), 8)
                
                pygame.draw.circle(self.tela, BRANCO, (x, y), 4)
                
                if self.selected_id == nid:
                    pygame.draw.circle(self.tela, VERDE, (x, y), 8, 2)
                    # Mostrar coordenadas ao selecionar
                    node = self.estrutura.tree.nodes[nid]
                    txt = f"({node.point[0]}, {node.point[1]})"
                    self.ui._draw_text(txt, x, y - 20, center_x=True)

        # === FASES 1, 2, 4: DESENHO DA ÁRVORE (Hierarquia) ===
        elif self.fase in (1, 2, 4):
            # Arestas
            for nid, (x, y) in self.node_positions.items():
                if self.fase == 2:
                    l = self.estrutura.tree._left(nid)
                    r = self.estrutura.tree._right(nid)
                else:
                    l = self.estrutura.tree._get_left(nid)
                    r = self.estrutura.tree._get_right(nid)
                
                for child in (l, r):
                    if child and child in self.node_positions:
                        cx, cy = self.node_positions[child]
                        pygame.draw.line(self.tela, CINZA_CLARO, (x, y), (cx, cy), 2)

            # Nós
            for nid, (x, y) in self.node_positions.items():
                node = self.estrutura.tree.nodes[nid]
                
                cor = AZUL # Default AVL
                if self.fase == 2: cor = VERMELHO if node.color == RBColor.RED else PRETO
                elif self.fase == 4: cor = COR_EIXO_X if node.axis == 0 else COR_EIXO_Y

                if nid in self.path_destacado:
                    pygame.draw.circle(self.tela, AMARELO, (x, y), RAIO_NO + 4)

                pygame.draw.circle(self.tela, cor, (x, y), RAIO_NO)
                pygame.draw.circle(self.tela, BRANCO, (x, y), RAIO_NO, 2)

                if self.selected_id == nid:
                    pygame.draw.circle(self.tela, VERDE, (x, y), RAIO_NO + 6, 2)

                # Texto
                if self.fase == 4:
                    txt = f"{node.point[0]},{node.point[1]}"
                    self.ui._draw_text(txt, x, y - 6, center_x=True, font=self.fonte_pequena)
                else:
                    txt = str(node.key)
                    if getattr(node, 'freq', 1) > 1: txt += f"({node.freq})"
                    self.ui._draw_text(txt, x, y - 6, center_x=True)

        # === FASE 3: 2-3-4 ===
        elif self.fase == 3:
            for nid, (x, y) in self.node_positions_234.items():
                node = self.estrutura.tree.nodes[nid]
                if not node.leaf and node.children:
                    for child in node.children:
                        if child in self.node_positions_234:
                            cx, cy = self.node_positions_234[child]
                            pygame.draw.line(self.tela, CINZA_CLARO, (x, y + 10), (cx, cy - 15), 2)
            
            for nid, (x, y) in self.node_positions_234.items():
                node = self.estrutura.tree.nodes[nid]
                w, h = 26 * len(node.keys), 30
                rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
                
                if nid in self.path_destacado: pygame.draw.rect(self.tela, AMARELO, rect.inflate(8,8), 2)
                pygame.draw.rect(self.tela, CINZA, rect)
                pygame.draw.rect(self.tela, BRANCO, rect, 2)
                if self.selected_id == nid: pygame.draw.rect(self.tela, VERDE, rect.inflate(6,6), 2)
                
                for i, k in enumerate(node.keys):
                    self.ui._draw_text(k, rect.left + 10 + i * 24, y - 6)

        self.ui.draw_hud(self.fase, self.msgs)
        if self.mostrar_tutorial: self.ui.draw_tutorial(self.fase)
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Jogo().run()