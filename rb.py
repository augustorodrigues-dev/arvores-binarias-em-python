from typing import Dict, Optional, Tuple, List, Callable

class RBColor:
    RED = 0
    BLACK = 1

class RBNode:
    def __init__(self, key: int):
        self.key = key
        self.color = RBColor.RED
        self.freq = 1

class RBTreeAdj:
    def __init__(self, animation_callback: Optional[Callable] = None):
        self.nodes: Dict[int, RBNode] = {}
        self.adj: Dict[int, Tuple[Optional[int], Optional[int]]] = {}
        self.parent: Dict[int, Optional[int]] = {}
        self.root: Optional[int] = None
        self._next_id = 1
        self.anim_cb = animation_callback

    def _animate(self, nodes: List[Optional[int]], msg: str):
        if self.anim_cb:
            valid_nodes = [n for n in nodes if n is not None]
            if valid_nodes: self.anim_cb(valid_nodes, msg)

    def _new_node(self, key: int) -> int:
        nid = self._next_id
        self._next_id += 1
        self.nodes[nid] = RBNode(key)
        self.adj[nid] = (None, None)
        self.parent[nid] = None
        return nid

    def _left(self, nid: int) -> Optional[int]: return self.adj[nid][0]
    def _right(self, nid: int) -> Optional[int]: return self.adj[nid][1]
    def _set_left(self, nid: int, child: Optional[int]) -> None:
        _, r = self.adj[nid]; self.adj[nid] = (child, r)
        if child is not None: self.parent[child] = nid
    def _set_right(self, nid: int, child: Optional[int]) -> None:
        l, _ = self.adj[nid]; self.adj[nid] = (l, child)
        if child is not None: self.parent[child] = nid
    def _grandparent(self, nid: int) -> Optional[int]:
        p = self.parent.get(nid)
        return None if p is None else self.parent.get(p)

    def _rotate_left(self, x: int) -> None:
        y = self._right(x)
        if y is None: return
        self._animate([x, y], f"Rot. ESQ no pivô {self.nodes[x].key}")
        beta = self._left(y)
        self._set_right(x, beta)
        p = self.parent[x]
        self.parent[y] = p
        if p is None: self.root = y
        else:
            if x == self._left(p): self._set_left(p, y)
            else: self._set_right(p, y)
        self._set_left(y, x)

    def _rotate_right(self, y: int) -> None:
        x = self._left(y)
        if x is None: return
        self._animate([y, x], f"Rot. DIR no pivô {self.nodes[y].key}")
        beta = self._right(x)
        self._set_left(y, beta)
        p = self.parent[y]
        self.parent[x] = p
        if p is None: self.root = x
        else:
            if y == self._left(p): self._set_left(p, x)
            else: self._set_right(p, x)
        self._set_right(x, y)

    def insert(self, key: int) -> None:
        if self.root is None:
            nid = self._new_node(key)
            self.root = nid
            self.nodes[nid].color = RBColor.BLACK
            self._animate([nid], "Raiz criada (Preta).")
            return

        cur = self.root; parent = None; dir_left = False
        while cur is not None:
            parent = cur
            node = self.nodes[cur]
            if key == node.key:
                node.freq += 1; self._animate([cur], "Chave existente. Frequência++"); return
            elif key < node.key: cur = self._left(cur); dir_left = True
            else: cur = self._right(cur); dir_left = False

        nid = self._new_node(key)
        if dir_left: self._set_left(parent, nid)
        else: self._set_right(parent, nid)
        
        self._animate([nid, parent], f"Inserido {key} (Vermelho). Verificando...")
        self._fix_insert(nid)

    def _fix_insert(self, z: int) -> None:
        while z != self.root and self.nodes[self.parent[z]].color == RBColor.RED:
            p = self.parent[z]
            g = self._grandparent(z)
            if g is None: break
            
            self._animate([z, p, g], f"Conflito VR-VR detectado entre {self.nodes[z].key} e {self.nodes[p].key}!")

            if p == self._left(g):
                y = self._right(g) # Tio
                if y is not None and self.nodes[y].color == RBColor.RED:
                    self._animate([p, y, g], "Caso 1: Tio Vermelho. Recolorindo...")
                    self.nodes[p].color = RBColor.BLACK
                    self.nodes[y].color = RBColor.BLACK
                    self.nodes[g].color = RBColor.RED
                    z = g
                else:
                    if z == self._right(p):
                        self._animate([z, p], "Caso 2: Joelho LR. Preparando Rot. Esq...")
                        z = p
                        self._rotate_left(z)
                        p = self.parent[z]; g = self._grandparent(z)
                    
                    self._animate([p, g], "Caso 3: Linha LL. Recolorindo e Rot. Dir...")
                    self.nodes[p].color = RBColor.BLACK
                    if g is not None:
                        self.nodes[g].color = RBColor.RED
                        self._rotate_right(g)
            else: 
                y = self._left(g)
                if y is not None and self.nodes[y].color == RBColor.RED:
                    self._animate([p, y, g], "Caso 1: Tio Vermelho. Recolorindo...")
                    self.nodes[p].color = RBColor.BLACK
                    self.nodes[y].color = RBColor.BLACK
                    self.nodes[g].color = RBColor.RED
                    z = g
                else:
                    if z == self._left(p):
                        self._animate([z, p], "Caso 2: Joelho RL. Preparando Rot. Dir...")
                        z = p
                        self._rotate_right(z)
                        p = self.parent[z]; g = self._grandparent(z)
                    
                    self._animate([p, g], "Caso 3: Linha RR. Recolorindo e Rot. Esq...")
                    self.nodes[p].color = RBColor.BLACK
                    if g is not None:
                        self.nodes[g].color = RBColor.RED
                        self._rotate_left(g)

        if self.root is not None and self.nodes[self.root].color == RBColor.RED:
            self._animate([self.root], "Garantindo Raiz Preta.")
            self.nodes[self.root].color = RBColor.BLACK
    
    def search(self, key: int) -> Optional[int]:
        cur = self.root
        while cur is not None:
            node = self.nodes[cur]
            if key == node.key: return cur
            elif key < node.key: cur = self._left(cur)
            else: cur = self._right(cur)
        return None