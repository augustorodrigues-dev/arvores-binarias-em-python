from typing import Dict, Optional, Tuple, List, Callable

class SplayNode:
    def __init__(self, key: int):
        self.key = key
        self.freq = 1

class SplayTreeAdj:
    def __init__(self, animation_callback: Optional[Callable] = None):
        self.nodes: Dict[int, SplayNode] = {}
        # adj[id] = (left_id, right_id)
        self.adj: Dict[int, Tuple[Optional[int], Optional[int]]] = {}
        self.root: Optional[int] = None
        self._next_id: int = 1
        self.anim_cb = animation_callback

    def _animate(self, nodes: List[Optional[int]], msg: str):
        if self.anim_cb:
            valid_nodes = [n for n in nodes if n is not None]
            if valid_nodes: self.anim_cb(valid_nodes, msg)

    def _new_node(self, key: int) -> int:
        nid = self._next_id; self._next_id += 1
        self.nodes[nid] = SplayNode(key)
        self.adj[nid] = (None, None)
        return nid

    # --- AUXILIARES ---
    def _get_left(self, nid: int) -> Optional[int]: return self.adj[nid][0]
    def _get_right(self, nid: int) -> Optional[int]: return self.adj[nid][1]
    def _set_left(self, nid: int, child: Optional[int]) -> None:
        _, r = self.adj[nid]; self.adj[nid] = (child, r)
    def _set_right(self, nid: int, child: Optional[int]) -> None:
        l, _ = self.adj[nid]; self.adj[nid] = (l, child)

    # --- ROTAÇÕES ---
    def _rotate_right(self, y: int) -> int:
        x = self._get_left(y)
        if x is None: return y
        t2 = self._get_right(x)
        self._set_left(y, t2)
        self._set_right(x, y)
        return x

    def _rotate_left(self, x: int) -> int:
        y = self._get_right(x)
        if y is None: return x
        t2 = self._get_left(y)
        self._set_right(x, t2)
        self._set_left(y, x)
        return y

    # --- A LÓGICA SPLAY ---
    def _splay(self, root_id: Optional[int], key: int) -> Optional[int]:
        if root_id is None: return None
        root_node = self.nodes[root_id]

        if root_node.key == key:
            return root_id

        # Esquerda
        if key < root_node.key:
            left_id = self._get_left(root_id)
            if left_id is None: return root_id
            
            left_node = self.nodes[left_id]

            # Zig-Zig (Esquerda-Esquerda)
            if key < left_node.key:
                ll_id = self._get_left(left_id)
                if ll_id is not None:
                    self._set_left(left_id, self._splay(ll_id, key))
                    self._animate([root_id, left_id], "Zig-Zig (Dir-Dir): Rotacionando Avô...")
                    root_id = self._rotate_right(root_id)
            
            # Zig-Zag (Esquerda-Direita)
            elif key > left_node.key:
                lr_id = self._get_right(left_id)
                if lr_id is not None:
                    self._set_right(left_id, self._splay(lr_id, key))
                    if self._get_right(left_id) is not None:
                        self._animate([left_id], "Zig-Zag (Esq): Rotacionando Pai...")
                        self._set_left(root_id, self._rotate_left(left_id))

            if self._get_left(root_id) is not None:
                self._animate([root_id], "Zig (Dir): Trazendo para raiz...")
                return self._rotate_right(root_id)
            else:
                return root_id

        # Direita
        else:
            right_id = self._get_right(root_id)
            if right_id is None: return root_id
            
            right_node = self.nodes[right_id]

            # Zag-Zig (Direita-Esquerda)
            if key < right_node.key:
                rl_id = self._get_left(right_id)
                if rl_id is not None:
                    self._set_left(right_id, self._splay(rl_id, key))
                    if self._get_left(right_id) is not None:
                        self._animate([right_id], "Zag-Zig (Dir): Rotacionando Pai...")
                        self._set_right(root_id, self._rotate_right(right_id))
            
            # Zag-Zag (Direita-Direita)
            elif key > right_node.key:
                rr_id = self._get_right(right_id)
                if rr_id is not None:
                    self._set_right(right_id, self._splay(rr_id, key))
                    self._animate([root_id, right_id], "Zag-Zag (Esq-Esq): Rotacionando Avô...")
                    root_id = self._rotate_left(root_id)

            if self._get_right(root_id) is not None:
                self._animate([root_id], "Zag (Esq): Trazendo para raiz...")
                return self._rotate_left(root_id)
            else:
                return root_id

    # --- OPERAÇÕES PÚBLICAS ---
    
    def search_step_by_step(self, key: int) -> List[int]:
        # Na Splay, a busca altera a árvore (move o nó para o topo)
        # Então usamos o splay como mecanismo de busca
        self._animate([self.root], f"Splaying busca pelo {key}...")
        self.root = self._splay(self.root, key)
        
        # Retorna o caminho da raiz (que agora deve ser o elemento ou o último acessado)
        if self.root is not None and self.nodes[self.root].key == key:
            self._animate([self.root], f"Encontrado e movido para a Raiz!")
            return [self.root]
        else:
            self._animate([self.root], f"Não encontrado. Último acesso na raiz.")
            return []

    def insert(self, key: int) -> None:
        self._animate([], f"Inserindo {key}...")
        
        if self.root is None:
            self.root = self._new_node(key)
            self._animate([self.root], "Raiz criada.")
            return

        # 1. Splay para trazer o mais próximo possível para a raiz
        self.root = self._splay(self.root, key)
        root_node = self.nodes[self.root]

        # 2. Se chave já existe
        if root_node.key == key:
            root_node.freq += 1
            self._animate([self.root], "Chave já existe na raiz. Frequência++")
            return

        # 3. Cria novo nó e ajusta ponteiros baseado na raiz atual (que é vizinha do valor)
        new_id = self._new_node(key)
        
        if key < root_node.key:
            self._set_right(new_id, self.root)
            self._set_left(new_id, self._get_left(self.root))
            self._set_left(self.root, None)
        else:
            self._set_left(new_id, self.root)
            self._set_right(new_id, self._get_right(self.root))
            self._set_right(self.root, None)
            
        self.root = new_id
        self._animate([self.root], f"{key} inserido e tornado Raiz.")

    def remove(self, key: int) -> bool:
        if self.root is None: return False
        
        self._animate([], f"Splaying para remover {key}...")
        self.root = self._splay(self.root, key)
        
        if self.nodes[self.root].key != key:
            self._animate([self.root], "Chave não encontrada após Splay.")
            return False
            
        # Remoção
        self._animate([self.root], "Removendo raiz...")
        left = self._get_left(self.root)
        right = self._get_right(self.root)
        
        del self.nodes[self.root]
        del self.adj[self.root]
        
        if left is None:
            self.root = right
        elif right is None:
            self.root = left
        else:
            # Temos duas subárvores. Splay no maior elemento da esquerda para virar a nova raiz
            self._animate([left], "Splaying máximo da esquerda para virar raiz...")
            new_root = self._splay(left, key) # key é maior que todos na esquerda, vai puxar o maior
            self.root = new_root
            self._set_right(self.root, right)
            
        self._animate([self.root], "Remoção concluída.")
        return True