import pygame
import sys
import random
import math
import time
from typing import Dict, Optional, Tuple, List, Callable


from config import *
from ui import UIManager
from fachada import EstruturaArvore
from rb import RBColor
import layout 

COR_DESTAQUE_OPERACAO = (255, 165, 0) 

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Helldivers: Árvores da Super-Terra - Modular")
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
        
        self.intro_text = [
            "> Conexão estabelecida.",
            "> Bem-vindo, Helldiver.",
            "> Sistema Modularizado V2.0",
            "> [A] Auto | [F] Fast Fill | [M] Mix | [R] Reset",
            "> [I] Inserir | [X] Remover | [B] Buscar",
            "> Pela Democracia Gerenciada!"
        ]
        self.typed_chars = 0
        self.last_char_time = 0

        self.animating_nodes: List[int] = []
        self.current_op_msg: str = ""
        self.memoria_fases = {} 

        self.msgs: List[str] = []
        self.mostrar_tutorial = True
        self.selected_id: Optional[int] = None
        self.selected_key = None 
        self.path_destacado: List[int] = []
        
        self.node_positions: Dict[int, Tuple[int, int]] = {}
        
        self.auto_inserindo = False
        self.turbo_mode = False
        self.fila_normal = list(LISTA_DEMO)
        self.fila_kd = list(LISTA_DEMO_KD)
        self.indice_demo = 0 

        self.estrutura = EstruturaArvore("AVL", self._animar_passo_tree)
        self._carregar_demo_inicial() 
        self.memoria_fases[1] = self.estrutura

    def _animar_passo_tree(self, nodes_ids: List[int], msg: str):
        self.animating_nodes = nodes_ids
        self.current_op_msg = msg
        
        if not self.turbo_mode:
            self._say(f"[ANIM] {msg}")
        
        self.draw()
        pygame.display.flip()
        
        if self.turbo_mode:
            time.sleep(0.05) 
        else:
            tempo = 0.5 if self.auto_inserindo else 1.2
            time.sleep(tempo)
        
        self.animating_nodes = []
        self.current_op_msg = ""
        pygame.event.pump() 

    def _say(self, texto: str):
        if len(self.msgs) > 6: self.msgs.pop(0)
        self.msgs.append(texto)

    def _get_fila_atual(self):
        if self.fase in (4, 5): return self.fila_kd
        return self.fila_normal

    def _set_fila_atual(self, nova_fila):
        if self.fase in (4, 5): self.fila_kd = nova_fila
        else: self.fila_normal = nova_fila

    def _carregar_demo_inicial(self):
        self.indice_demo = 0
        fila = self._get_fila_atual()
        if fila:
            prim = fila[0]
            self.estrutura.inserir(prim)
            self.indice_demo = 1 
            self._say(f"Raiz {prim} inicializada.")

    def _resetar_arvore(self):
        self._say("!!! RESETANDO SISTEMA !!!")
        self.auto_inserindo = False
        self.turbo_mode = False
        self.path_destacado = []
        self.selected_id = None
        self.selected_key = None
        self.indice_demo = 0 
        
        if self.fase in (4, 5):
            self.fila_kd = list(LISTA_DEMO_KD)
            self.estrutura = EstruturaArvore("KDT", self._animar_passo_tree)
            if self.fila_kd:
                self.estrutura.inserir(self.fila_kd[0])
                self.indice_demo = 1
            self.memoria_fases['KDT'] = self.estrutura
        else:
            self.fila_normal = list(LISTA_DEMO)
            tipos = {1: "AVL", 2: "RB", 3: "234"}
            self.estrutura = EstruturaArvore(tipos[self.fase], self._animar_passo_tree)
            if self.fila_normal:
                self.estrutura.inserir(self.fila_normal[0])
                self.indice_demo = 1
            self.memoria_fases[self.fase] = self.estrutura

    def _misturar_fila(self):
        fila = self._get_fila_atual()
        qtd_restante = len(fila) - self.indice_demo
        if qtd_restante > 0:
            if self.fase in (4, 5):
                novos = [(random.randint(5, 95), random.randint(5, 95)) for _ in range(qtd_restante)]
            else:
                novos = [random.randint(1, 99) for _ in range(qtd_restante)]
            nova_fila = fila[:self.indice_demo] + novos
            self._set_fila_atual(nova_fila)
            self._say(">> NOVOS VALORES GERADOS <<")
        else:
            self._say("Fila acabou.")

    def set_fase(self, f: int):
        self.fase = f
        self.selected_id = None
        self.selected_key = None
        self.path_destacado = []
        self.mostrar_tutorial = True
        self.auto_inserindo = False 
        self.turbo_mode = False
        
        if f in (4, 5):
            if 'KDT' not in self.memoria_fases:
                nova_kdt = EstruturaArvore("KDT", self._animar_passo_tree)
                self.estrutura = nova_kdt
                if self.fila_kd:
                    nova_kdt.inserir(self.fila_kd[0])
                    self.indice_demo = 1
                self.memoria_fases['KDT'] = nova_kdt
            else:
                self.estrutura = self.memoria_fases['KDT']
                self.indice_demo = len(self.estrutura.tree.nodes)
            
            vis_nome = "Hierarquia" if f == 4 else "Plano 2D"
            self._say(f"Fase KD: {vis_nome}")
            return

        if f not in self.memoria_fases:
            tipos = {1: "AVL", 2: "RB", 3: "234"}
            self.estrutura = EstruturaArvore(tipos[f], self._animar_passo_tree)
            self.estrutura = self.estrutura
            if self.fila_normal:
                self.estrutura.inserir(self.fila_normal[0])
                self.indice_demo = 1
            self.memoria_fases[f] = self.estrutura 
            self._say(f"Fase {f} iniciada.")
        else:
            self.estrutura = self.memoria_fases[f]
            self.indice_demo = len(self.estrutura.tree.nodes) if self.estrutura.tree.root else 0
            self._say(f"Fase {f} recuperada.")

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit(0)
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: pygame.quit(); sys.exit(0)

            if self.game_state == "INTRO":
                if ev.type == pygame.KEYDOWN: self.game_state = "JOGO"
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
                elif ev.key == pygame.K_i: self._acao_inserir_manual()
                elif ev.key == pygame.K_x: self._acao_remover()
                elif ev.key == pygame.K_b: self._acao_buscar()
                elif ev.key == pygame.K_a: 
                    self.auto_inserindo = True
                    self.turbo_mode = False
                    self._say(">> AUTO-INSERÇÃO (LENTA) <<")
                elif ev.key == pygame.K_f:
                    self.auto_inserindo = True
                    self.turbo_mode = True 
                    self._say(">> PREENCHIMENTO RÁPIDO <<")
                elif ev.key == pygame.K_SPACE:
                    self.auto_inserindo = False
                    self.turbo_mode = False
                    self._say(">> PAUSADO <<")
                elif ev.key == pygame.K_r: self._resetar_arvore()
                elif ev.key == pygame.K_m: self._misturar_fila()

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self._clique(ev.pos)

    def _acao_inserir_manual(self):
        fila = self._get_fila_atual()
        if self.indice_demo < len(fila):
            val = fila[self.indice_demo]
            self.estrutura.inserir(val)
            self.indice_demo += 1 
            self.path_destacado = []
        else:
            if self.fase in (4, 5): v = (random.randint(5, 95), random.randint(5, 95))
            else: v = random.randint(1, 99)
            self.estrutura.inserir(v)
            self._say(f"Extra: {v}")
            self.path_destacado = []

    def _processar_auto_insercao(self):
        if not self.auto_inserindo: return
        fila = self._get_fila_atual()
        
        if self.indice_demo >= len(fila):
            self.auto_inserindo = False
            self.turbo_mode = False
            self._say("Fila concluída.")
            return
        
        val = fila[self.indice_demo]
        self.estrutura.inserir(val)
        self.indice_demo += 1

    def _acao_remover(self):
        if self.selected_key is None: self._say("Selecione um nó."); return
        self._say(f"Removendo {self.selected_key}...")
        res = self.estrutura.remover(self.selected_key)
        if res:
            self._say(f"Removido {self.selected_key}.")
            self.selected_id = None; self.selected_key = None; self.path_destacado = []
        else:
            self._say("Erro/Não encontrado.")

    def _acao_buscar(self):
        if self.selected_key is None: self._say("Selecione um nó."); return
        self._say(f"Buscando {self.selected_key}...")
        caminho = self.estrutura.buscar_caminho_animado(self.selected_key)
        if not caminho: self._say("Não encontrado.")
        else:
            self.path_destacado = caminho
            self._say(f"Encontrado.")

    def _clique(self, pos):
        x, y = pos
        self._atualizar_layout()
        if self.fase == 3:
            for nid, (nx, ny) in self.node_positions.items():
                rect = pygame.Rect(nx - 25, ny - 15, 50, 30)
                if rect.collidepoint(x, y):
                    node = self.estrutura.tree.nodes[nid]
                    if node.keys:
                        self.selected_id = nid; self.selected_key = node.keys[0]
                        self.path_destacado = []; self._say(f"Sel: {node.keys[0]}")
                    return
            return
        alvo = None; menor = 999999
        for nid, (nx, ny) in self.node_positions.items():
            d = math.hypot(nx - x, ny - y)
            raio = RAIO_NO + 5 if self.fase != 5 else 15 
            if d <= raio and d < menor: menor = d; alvo = nid
        if alvo is not None:
            self.selected_id = alvo
            self.selected_key = self.estrutura.tree.nodes[alvo].point if self.fase in (4,5) else self.estrutura.tree.nodes[alvo].key
            self._say(f"Selecionado: {self.selected_key}")
            self.path_destacado = []

    def update(self):
        if self.game_state == "INTRO":
            now = pygame.time.get_ticks()
            if now - self.last_char_time > 30:
                self.typed_chars += 1; self.last_char_time = now
        if self.auto_inserindo: self._processar_auto_insercao()

    def _atualizar_layout(self):
        if self.estrutura.tree.root is None:
            self.node_positions = {}
            return

        if self.fase in (1, 2, 4):
            self.node_positions = layout.calcular_layout_binario(self.estrutura.tree, self.estrutura.tree.root, self.fase)
        elif self.fase == 5:
            self.node_positions = layout.calcular_layout_kd_espacial(self.estrutura.tree, self.estrutura.tree.root)
        elif self.fase == 3:
            self.node_positions = layout.calcular_layout_234(self.estrutura.tree, self.estrutura.tree.root)

    def _draw_kdtree_lines(self, nid, x_min, y_min, x_max, y_max):
        if nid is None: return
        node = self.estrutura.tree.nodes[nid]
        MARGEM_X = 250; MARGEM_Y = 150
        L_UTIL = LARGURA - 2 * MARGEM_X; A_UTIL = ALTURA - MARGEM_Y - 50
        OFFSET_X = MARGEM_X; OFFSET_Y = 130
        def to_screen(vx, vy): return (OFFSET_X + (vx / 100) * L_UTIL, OFFSET_Y + (vy / 100) * A_UTIL)
        px, py = node.point
        sx, sy = to_screen(px, py)
        s_xmin, s_ymin = to_screen(x_min, y_min); s_xmax, s_ymax = to_screen(x_max, y_max)
        axis = node.axis; cor = COR_EIXO_X if axis == 0 else COR_EIXO_Y
        if axis == 0: 
            pygame.draw.line(self.tela, cor, (sx, s_ymin), (sx, s_ymax), 2)
            self._draw_kdtree_lines(self.estrutura.tree.adj[nid][0], x_min, y_min, px, y_max)
            self._draw_kdtree_lines(self.estrutura.tree.adj[nid][1], px, y_min, x_max, y_max)
        else:
            pygame.draw.line(self.tela, cor, (s_xmin, sy), (s_xmax, sy), 2)
            self._draw_kdtree_lines(self.estrutura.tree.adj[nid][0], x_min, y_min, x_max, py)
            self._draw_kdtree_lines(self.estrutura.tree.adj[nid][1], x_min, py, x_max, y_max)

    def _draw_lista_demo(self):
       
        y_pos = ALTURA - 30; start_x = 20
        self.ui._draw_text("FILA:", start_x, y_pos - 5, font=self.fonte_pequena, color=AMARELO)
        start_x += 40
        
        fila = self._get_fila_atual()
        
        for i, num in enumerate(fila):
            color = VERDE if i < self.indice_demo else CINZA_CLARO
            
            if i == self.indice_demo: 
                color = BRANCO
                txt_w = 45 if self.fase in (4, 5) else 20
                rect = pygame.Rect(start_x - 3, y_pos - 8, txt_w + 6, 22)
                pygame.draw.rect(self.tela, COR_DESTAQUE_OPERACAO, rect, 2)
            
            txt = f"{num}" if self.fase in (4, 5) else str(num)
            spacing = 55 if self.fase in (4, 5) else 28

            self.ui._draw_text(txt, start_x, y_pos - 5, font=self.fonte_pequena, color=color)
            start_x += spacing

    def draw(self):
        if self.background: self.tela.blit(self.background, (0, 0))
        else: self.tela.fill(PRETO)
        if self.game_state == "INTRO":
            self.ui.draw_intro(self.typed_chars, self.intro_text); pygame.display.flip(); return
        
        self._atualizar_layout()
        if self.fase == 5:
            MARGEM_X = 250; MARGEM_Y = 150
            L_UTIL = LARGURA - 2 * MARGEM_X; A_UTIL = ALTURA - MARGEM_Y - 50
            rect_fundo = pygame.Rect(MARGEM_X, 130, L_UTIL, A_UTIL)
            s = pygame.Surface((rect_fundo.width, rect_fundo.height)); s.set_alpha(150); s.fill(COR_PLANO_FUNDO)
            self.tela.blit(s, rect_fundo.topleft); pygame.draw.rect(self.tela, CINZA, rect_fundo, 2)
            self._draw_kdtree_lines(self.estrutura.tree.root, 0, 0, 100, 100)
            for nid, (x, y) in self.node_positions.items():
                if nid in self.path_destacado: pygame.draw.circle(self.tela, AMARELO, (x, y), 8)
                pygame.draw.circle(self.tela, BRANCO, (x, y), 4)
                if self.selected_id == nid: pygame.draw.circle(self.tela, VERDE, (x, y), 8, 2)
                node = self.estrutura.tree.nodes[nid]
                txt = f"{node.point[0]},{node.point[1]}"
                cor = BRANCO if (nid == self.selected_id or nid in self.path_destacado) else CINZA_CLARO
                self.ui._draw_text(txt, x, y - 12, center_x=True, font=self.fonte_pequena, color=cor)
        
        elif self.fase in (1, 2, 4):
            for nid, (x, y) in self.node_positions.items():
                if self.fase == 2: l, r = self.estrutura.tree._left(nid), self.estrutura.tree._right(nid)
                else:
                    l = self.estrutura.tree._get_left(nid)
                    r = self.estrutura.tree._get_right(nid)
                for child in (l, r):
                    if child and child in self.node_positions:
                        cx, cy = self.node_positions[child]
                        pygame.draw.line(self.tela, CINZA_CLARO, (x, y), (cx, cy), 2)
            for nid, (x, y) in self.node_positions.items():
                node = self.estrutura.tree.nodes[nid]
                cor = AZUL 
                if self.fase == 2: cor = VERMELHO if node.color == RBColor.RED else PRETO
                elif self.fase == 4: 
                    if hasattr(node, 'axis'): cor = COR_EIXO_X if node.axis == 0 else COR_EIXO_Y
                if nid in self.animating_nodes: pygame.draw.circle(self.tela, COR_DESTAQUE_OPERACAO, (x, y), RAIO_NO + 8)
                if nid in self.path_destacado: pygame.draw.circle(self.tela, AMARELO, (x, y), RAIO_NO + 4)
                pygame.draw.circle(self.tela, cor, (x, y), RAIO_NO)
                pygame.draw.circle(self.tela, BRANCO, (x, y), RAIO_NO, 2)
                if self.selected_id == nid: pygame.draw.circle(self.tela, VERDE, (x, y), RAIO_NO + 6, 2)
                if self.fase == 4:
                    txt = f"{node.point[0]},{node.point[1]}"
                    self.ui._draw_text(txt, x, y - 6, center_x=True, font=self.fonte_pequena)
                else:
                    txt = str(node.key)
                    if getattr(node, 'freq', 1) > 1: txt += f"({node.freq})"
                    self.ui._draw_text(txt, x, y - 6, center_x=True)
        
        elif self.fase == 3:
            for nid, (x, y) in self.node_positions.items():
                node = self.estrutura.tree.nodes[nid]
                if not node.leaf and node.children:
                    for child in node.children:
                        if child in self.node_positions:
                            cx, cy = self.node_positions[child]
                            pygame.draw.line(self.tela, CINZA_CLARO, (x, y + 10), (cx, cy - 15), 2)
            for nid, (x, y) in self.node_positions.items():
                node = self.estrutura.tree.nodes[nid]
                w, h = 26 * len(node.keys), 30
                rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
                if nid in self.animating_nodes: pygame.draw.rect(self.tela, COR_DESTAQUE_OPERACAO, rect.inflate(12,12))
                if nid in self.path_destacado: pygame.draw.rect(self.tela, AMARELO, rect.inflate(8,8), 2)
                pygame.draw.rect(self.tela, CINZA, rect)
                pygame.draw.rect(self.tela, BRANCO, rect, 2)
                if self.selected_id == nid: pygame.draw.rect(self.tela, VERDE, rect.inflate(6,6), 2)
                for i, k in enumerate(node.keys):
                    self.ui._draw_text(k, rect.left + 10 + i * 24, y - 6)
        
        self.ui.draw_hud(self.fase, self.msgs)
        self._draw_lista_demo() 
        if self.current_op_msg:
             txt_surf = self.fonte_titulo.render(f"OPERANDO: {self.current_op_msg}", True, COR_DESTAQUE_OPERACAO)
             rect = txt_surf.get_rect(center=(LARGURA/2, ALTURA - 70))
             bg_rect = rect.inflate(20, 10)
             pygame.draw.rect(self.tela, PRETO, bg_rect)
             pygame.draw.rect(self.tela, COR_DESTAQUE_OPERACAO, bg_rect, 1)
             self.tela.blit(txt_surf, rect)
        if self.mostrar_tutorial: self.ui.draw_tutorial(self.fase)

    def run(self):
        while True:
            self.handle_events(); self.update(); self.draw(); pygame.display.flip(); self.clock.tick(FPS)