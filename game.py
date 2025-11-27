import pygame
import sys
import random
import time
import math
from typing import Dict, Tuple, List

from config import *
from ui import UIManager
from gerenciador import EstruturaArvore
from rb import RBColor
import layout

COR_DESTAQUE_OPERACAO = (255, 165, 0) 

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Helldivers: RB & 2-3-4 Tree Visualizer")
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
            "> Visualizador Especializado:",
            "> [1] Rubro-Negra | [2] Árvore 2-3-4",
            "> [A] Auto | [F] Turbo | [M] Mix | [R] Reset",
            "> Pela Democracia Gerenciada!"
        ]
        self.typed_chars = 0
        self.last_char_time = 0

        self.animating_nodes: List[int] = []
        self.current_op_msg: str = ""
        self.memoria_fases = {} 

        self.msgs: List[str] = []
        self.mostrar_tutorial = True
        self.selected_id = None
        self.selected_key = None 
        self.path_destacado: List[int] = []
        self.node_positions: Dict[int, Tuple[int, int]] = {}
        
        self.auto_inserindo = False
        self.turbo_mode = False
        self.fila = list(LISTA_DEMO)
        self.indice_demo = 0 

        
        self.estrutura = EstruturaArvore("RB", self._animar_passo_tree)
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
            tempo = 1.5 if self.auto_inserindo else 1.2
            time.sleep(tempo)
        
        self.animating_nodes = []
        self.current_op_msg = ""
        pygame.event.pump() 

    def _say(self, texto: str):
        if len(self.msgs) > 6: self.msgs.pop(0)
        self.msgs.append(texto)

    def _carregar_demo_inicial(self):
        self.indice_demo = 0
        if self.fila:
            prim = self.fila[0]
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
        self.fila = list(LISTA_DEMO)
        
        tipos = {1: "RB", 2: "234"}
        self.estrutura = EstruturaArvore(tipos[self.fase], self._animar_passo_tree)
        self._carregar_demo_inicial()
        self.memoria_fases[self.fase] = self.estrutura

    def _misturar_fila(self):
        qtd_restante = len(self.fila) - self.indice_demo
        if qtd_restante > 0:
            novos = [random.randint(1, 99) for _ in range(qtd_restante)]
            self.fila = self.fila[:self.indice_demo] + novos
            self._say(">> NOVOS VALORES GERADOS <<")
        else:
            self._say("Fila acabou.")

    def set_fase(self, f: int):
        if f not in (1, 2): return
        
        self.fase = f
        self.selected_id = None
        self.selected_key = None
        self.path_destacado = []
        self.mostrar_tutorial = True
        self.auto_inserindo = False 
        self.turbo_mode = False
        
        tipos = {1: "RB", 2: "234"}
        
        if f not in self.memoria_fases:
            self.estrutura = EstruturaArvore(tipos[f], self._animar_passo_tree)
            if self.fila:
                self.estrutura.inserir(self.fila[0])
                self.indice_demo = 1
            self.memoria_fases[f] = self.estrutura 
            self._say(f"Fase {f} iniciada.")
        else:
            self.estrutura = self.memoria_fases[f]
            # Tenta sincronizar o índice da fila com a árvore recuperada
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
                elif ev.key == pygame.K_t: self.mostrar_tutorial = True
                elif ev.key == pygame.K_i: self._acao_inserir_manual()
                elif ev.key == pygame.K_x: self._acao_remover()
                elif ev.key == pygame.K_b: self._acao_buscar()
                elif ev.key == pygame.K_a: 
                    self.auto_inserindo = True
                    self.turbo_mode = False
                    self._say(">> AUTO-INSERÇÃO <<")
                elif ev.key == pygame.K_f:
                    self.auto_inserindo = True
                    self.turbo_mode = True 
                    self._say(">> MODO TURBO <<")
                elif ev.key == pygame.K_SPACE:
                    self.auto_inserindo = False
                    self.turbo_mode = False
                    self._say(">> PAUSADO <<")
                elif ev.key == pygame.K_r: self._resetar_arvore()
                elif ev.key == pygame.K_m: self._misturar_fila()

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self._clique(ev.pos)

    def _acao_inserir_manual(self):
        if self.indice_demo < len(self.fila):
            val = self.fila[self.indice_demo]
            self.estrutura.inserir(val)
            self.indice_demo += 1 
            self.path_destacado = []
        else:
            v = random.randint(1, 99)
            self.estrutura.inserir(v)
            self._say(f"Extra: {v}")
            self.path_destacado = []

    def _processar_auto_insercao(self):
        if not self.auto_inserindo: return
        if self.indice_demo >= len(self.fila):
            self.auto_inserindo = False
            self.turbo_mode = False
            self._say("Fila concluída.")
            return
        
        val = self.fila[self.indice_demo]
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
        if self.fase == 2: # 2-3-4
            for nid, (nx, ny) in self.node_positions_234.items():
                rect = pygame.Rect(nx - 25, ny - 15, 50, 30)
                if rect.collidepoint(x, y):
                    node = self.estrutura.tree.nodes[nid]
                    if node.keys:
                        self.selected_id = nid; self.selected_key = node.keys[0]
                        self.path_destacado = []; self._say(f"Sel: {node.keys[0]}")
                    return
            return
        
        # RB (Fase 1)
        alvo = None; menor = 999999
        for nid, (nx, ny) in self.node_positions.items():
            d = math.hypot(nx - x, ny - y)
            if d <= RAIO_NO + 5 and d < menor: menor = d; alvo = nid
        if alvo is not None:
            self.selected_id = alvo
            self.selected_key = self.estrutura.tree.nodes[alvo].key
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

        if self.fase == 1:
            self.node_positions = layout.calcular_layout_binario(self.estrutura.tree, self.estrutura.tree.root)
        elif self.fase == 2:
            self.node_positions = layout.calcular_layout_234(self.estrutura.tree, self.estrutura.tree.root)

    def _draw_lista_demo(self):
        y_pos = ALTURA - 30; start_x = 20
        self.ui._draw_text("FILA:", start_x, y_pos - 5, font=self.fonte_pequena, color=AMARELO)
        start_x += 40
        for i, num in enumerate(self.fila):
            color = VERDE if i < self.indice_demo else CINZA_CLARO
            if i == self.indice_demo: 
                color = BRANCO
                rect = pygame.Rect(start_x - 3, y_pos - 8, 26, 22)
                pygame.draw.rect(self.tela, COR_DESTAQUE_OPERACAO, rect, 2)
            self.ui._draw_text(str(num), start_x, y_pos - 5, font=self.fonte_pequena, color=color)
            start_x += 28

    def draw(self):
        if self.background: self.tela.blit(self.background, (0, 0))
        else: self.tela.fill(PRETO)
        if self.game_state == "INTRO":
            self.ui.draw_intro(self.typed_chars, self.intro_text); pygame.display.flip(); return
        
        self._atualizar_layout()
        
        # --- DRAW RB ---
        if self.fase == 1:
            for nid, (x, y) in self.node_positions.items():
                l = self.estrutura.tree._left(nid)
                r = self.estrutura.tree._right(nid)
                for child in (l, r):
                    if child and child in self.node_positions:
                        cx, cy = self.node_positions[child]
                        pygame.draw.line(self.tela, CINZA_CLARO, (x, y), (cx, cy), 2)
            for nid, (x, y) in self.node_positions.items():
                node = self.estrutura.tree.nodes[nid]
                cor = VERMELHO if node.color == RBColor.RED else PRETO
                
                if nid in self.animating_nodes: pygame.draw.circle(self.tela, COR_DESTAQUE_OPERACAO, (x, y), RAIO_NO + 8)
                if nid in self.path_destacado: pygame.draw.circle(self.tela, AMARELO, (x, y), RAIO_NO + 4)
                pygame.draw.circle(self.tela, cor, (x, y), RAIO_NO)
                pygame.draw.circle(self.tela, BRANCO, (x, y), RAIO_NO, 2)
                if self.selected_id == nid: pygame.draw.circle(self.tela, VERDE, (x, y), RAIO_NO + 6, 2)
                
                txt = str(node.key)
                if getattr(node, 'freq', 1) > 1: txt += f"({node.freq})"
                self.ui._draw_text(txt, x, y - 6, center_x=True)
        
        # --- DRAW 2-3-4 ---
        elif self.fase == 2:
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