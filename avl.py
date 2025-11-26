from typing import Dict, Optional, Tuple, List, Callable

class Node:
    def __init__(self, key: int):
        self.key = key
        self.freq = 1
        self.height = 1

class AVLTreeAdj:
    def __init__(self, animation_callback: Optional[Callable] = None):
        self.nodes: Dict[int, Node] = {}
        self.adj: Dict[int, Tuple[Optional[int], Optional[int]]] = {}
        self.root: Optional[int] = None
        self._next_id: int = 1
        
        self.anim_cb = animation_callback

    
    def _animate(self, nodes: List[int], msg: str):
        if self.anim_cb:
            
            valid_nodes = [n for n in nodes if n is not None]
            if valid_nodes:
                self.anim_cb(valid_nodes, msg)

    def _new_node(self, key: int) -> int:
        nid = self._next_id
        self._next_id += 1
        self.nodes[nid] = Node(key)
        self.adj[nid] = (None, None)
        return nid

    def _get_left(self, nid: int) -> Optional[int]: return self.adj[nid][0]
    def _get_right(self, nid: int) -> Optional[int]: return self.adj[nid][1]
    def _set_left(self, nid: int, child: Optional[int]) -> None:
        _, r = self.adj[nid]; self.adj[nid] = (child, r)
    def _set_right(self, nid: int, child: Optional[int]) -> None:
        l, _ = self.adj[nid]; self.adj[nid] = (l, child)

    def _height(self, nid: Optional[int]) -> int:
        return 0 if nid is None else self.nodes[nid].height

    def _update_height(self, nid: int) -> None:
        l, r = self._get_left(nid), self._get_right(nid)
        self.nodes[nid].height = 1 + max(self._height(l), self._height(r))

    def _balance_factor(self, nid: int) -> int:
        return self._height(self._get_left(nid)) - self._height(self._get_right(nid))

    def _rotate_right(self, y: int) -> int:
        x = self._get_left(y)
        if x is None: return y
        
        
        self._animate([y, x], f"Rotacionando DIREITA em {self.nodes[y].key}")
        
        
        t2 = self._get_right(x)
        self._set_left(y, t2)
        self._set_right(x, y)
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: int) -> int:
        y = self._get_right(x)
        if y is None: return x
        
        
        self._animate([x, y], f"Rotacionando ESQUERDA em {self.nodes[x].key}")
       

        t2 = self._get_left(y)
        self._set_right(x, t2)
        self._set_left(y, x)
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, nid: int) -> int:
        bf = self._balance_factor(nid)
        if bf > 1:
            left_id = self._get_left(nid)
            if left_id is not None and self._balance_factor(left_id) < 0:
                
                self._animate([nid, left_id], "Desbalanceado. Preparando Rotação Dupla Esq-Dir...")
                self._set_left(nid, self._rotate_left(left_id))
            return self._rotate_right(nid)
        if bf < -1:
            right_id = self._get_right(nid)
            if right_id is not None and self._balance_factor(right_id) > 0:
                 
                self._animate([nid, right_id], "Desbalanceado. Preparando Rotação Dupla Dir-Esq...")
                self._set_right(nid, self._rotate_right(right_id))
            return self._rotate_left(nid)
        return nid

    def _insert_rec(self, nid: Optional[int], key: int) -> int:
        if nid is None: return self._new_node(key)
        node = self.nodes[nid]
        if key == node.key:
            node.freq += 1
            self._animate([nid], f"Chave {key} já existe. Frequência++")
            return nid
        elif key < node.key:
            child = self._insert_rec(self._get_left(nid), key)
            self._set_left(nid, child)
        else:
            child = self._insert_rec(self._get_right(nid), key)
            self._set_right(nid, child)
            
        self._update_height(nid)
        return self._rebalance(nid)

    def insert(self, key: int) -> None:
        self.root = self._insert_rec(self.root, key)
        if self.root:
             self._animate([self.root], "Inserção concluída. Árvore balanceada.")

    def search(self, key: int) -> Optional[int]:
        cur = self.root
        while cur is not None:
            node = self.nodes[cur]
            if key == node.key: return cur
            elif key < node.key: cur = self._get_left(cur)
            else: cur = self._get_right(cur)
        return None
    
    def _min_value_node(self, nid: int) -> int:
        cur = nid
        while self._get_left(cur) is not None: cur = self._get_left(cur)
        return cur

    def _remove_rec(self, nid: Optional[int], key: int) -> Optional[int]:
        if nid is None: return None
        node = self.nodes[nid]
        if key < node.key: self._set_left(nid, self._remove_rec(self._get_left(nid), key))
        elif key > node.key: self._set_right(nid, self._remove_rec(self._get_right(nid), key))
        else:
            if node.freq > 1:
                node.freq -= 1
                return nid
            left = self._get_left(nid)
            right = self._get_right(nid)
            if left is None or right is None:
                temp = left if left is not None else right
                if temp is None:
                    del self.nodes[nid]; del self.adj[nid]
                    return None
                else:
                    del self.nodes[nid]; del self.adj[nid]
                    return temp
            else:
                succ_id = self._min_value_node(right)
                succ_node = self.nodes[succ_id]
                node.key = succ_node.key; node.freq = succ_node.freq
                succ_node.freq = 1
                self._set_right(nid, self._remove_rec(right, node.key))
        if nid is None: return None
        self._update_height(nid)
        return self._rebalance(nid)

    def remove(self, key: int) -> None:
        self.root = self._remove_rec(self.root, key)