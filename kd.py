from typing import Optional, Tuple, Dict, Callable, List

class KDNode:
    def __init__(self, point: Tuple[int, int], axis: int):
        self.point = point  
        self.axis = axis    
        self.freq = 1

class KDTree:
    def __init__(self, animation_callback: Optional[Callable] = None):
        self.root: Optional[int] = None
        self.nodes: Dict[int, KDNode] = {}
        self.adj: Dict[int, Tuple[Optional[int], Optional[int]]] = {}
        self._next_id = 1
        self.anim_cb = animation_callback

    def _animate(self, nodes: List[Optional[int]], msg: str):
        if self.anim_cb:
            valid_nodes = [n for n in nodes if n is not None]
            if valid_nodes: self.anim_cb(valid_nodes, msg)

    def _new_node(self, point: Tuple[int, int], axis: int) -> int:
        nid = self._next_id
        self._next_id += 1
        node = KDNode(point, axis)
        self.nodes[nid] = node
        self.adj[nid] = (None, None)
        return nid

    
    def _insert_rec(self, nid: Optional[int], point: Tuple[int, int], depth: int) -> int:
        if nid is None:
            axis = depth % 2
            new_id = self._new_node(point, axis)
            self._animate([new_id], f"Criado nó {point}.")
            return new_id
        node = self.nodes[nid]
        if point == node.point:
            node.freq += 1
            self._animate([nid], f"Ponto {point} repetido. Freq: {node.freq}")
            return nid
        axis = node.axis
        val = point[axis]
        node_val = node.point[axis]
        l_child, r_child = self.adj[nid]
        if val < node_val:
            self._animate([nid], "Indo para a ESQUERDA/BAIXO...")
            new_left = self._insert_rec(l_child, point, depth + 1)
            self.adj[nid] = (new_left, r_child)
        else:
            self._animate([nid], "Indo para a DIREITA/CIMA...")
            new_right = self._insert_rec(r_child, point, depth + 1)
            self.adj[nid] = (l_child, new_right)
        return nid

    def insert(self, point: Tuple[int, int]) -> None:
        self._animate([], f"Inserindo {point}...")
        self.root = self._insert_rec(self.root, point, 0)

    
    def _find_min(self, nid: Optional[int], axis: int, depth: int) -> Optional[int]:
        """Encontra o nó com o menor valor na dimensão 'axis'."""
        if nid is None: return None
        
        node = self.nodes[nid]
        curr_axis = node.axis
        
        
        if curr_axis == axis:
            l_child = self.adj[nid][0]
            if l_child is None: return nid
            return self._find_min(l_child, axis, depth + 1)
        
        
        l_child = self.adj[nid][0]
        r_child = self.adj[nid][1]
        
        res_l = self._find_min(l_child, axis, depth + 1)
        res_r = self._find_min(r_child, axis, depth + 1)
        
        res = nid
        min_val = node.point[axis]
        
        if res_l is not None:
            val_l = self.nodes[res_l].point[axis]
            if val_l < min_val:
                min_val = val_l
                res = res_l
        
        if res_r is not None:
            val_r = self.nodes[res_r].point[axis]
            if val_r < min_val:
                min_val = val_r
                res = res_r
                
        return res

    def _delete_rec(self, nid: Optional[int], point: Tuple[int, int], depth: int) -> Optional[int]:
        if nid is None:
            return None
        
        node = self.nodes[nid]
        axis = node.axis
        
        self._animate([nid], f"Visitando {node.point} para remover {point}...")

        if node.point == point:
            
            l_child, r_child = self.adj[nid]
            if l_child is None and r_child is None:
                self._animate([nid], "Removendo nó folha.")
                del self.nodes[nid]
                del self.adj[nid]
                return None
            
           
            if r_child is not None:
                self._animate([nid], f"Buscando mínimo no eixo {axis} à direita...")
                min_nid = self._find_min(r_child, axis, depth + 1)
                min_point = self.nodes[min_nid].point
                
                self._animate([nid, min_nid], f"Substituindo por {min_point}")
                node.point = min_point 
                
                
                new_right = self._delete_rec(r_child, min_point, depth + 1)
                self.adj[nid] = (l_child, new_right)
                
           
            else:
                self._animate([nid], f"Buscando mínimo no eixo {axis} à esquerda (swap)...")
                min_nid = self._find_min(l_child, axis, depth + 1)
                min_point = self.nodes[min_nid].point
                
                self._animate([nid, min_nid], f"Substituindo por {min_point}")
                node.point = min_point
    

                self.adj[nid] = (None, l_child) 
                new_right = self._delete_rec(l_child, min_point, depth + 1)
                self.adj[nid] = (None, new_right) 

            return nid

        
        val = point[axis]
        node_val = node.point[axis]
        l_child, r_child = self.adj[nid]

        if val < node_val:
            new_left = self._delete_rec(l_child, point, depth + 1)
            self.adj[nid] = (new_left, r_child)
        else:
            new_right = self._delete_rec(r_child, point, depth + 1)
            self.adj[nid] = (l_child, new_right)
            
        return nid

    def remove(self, point):
        self.root = self._delete_rec(self.root, point, 0)
        return True

    
    def search_step_by_step(self, point: Tuple[int, int]) -> List[int]:
        path = []
        cur = self.root
        while cur is not None:
            path.append(cur)
            node = self.nodes[cur]
            self._animate([cur], f"Visitando {node.point}...")
            if node.point == point:
                self._animate([cur], "Ponto encontrado!")
                return path
            axis = node.axis
            if point[axis] < node.point[axis]:
                self._animate([cur], f"Eixo {axis}: < que nó. Esq.")
                cur = self.adj[cur][0]
            else:
                self._animate([cur], f"Eixo {axis}: >= que nó. Dir.")
                cur = self.adj[cur][1]
        return []

    def _get_left(self, nid): return self.adj[nid][0]
    def _get_right(self, nid): return self.adj[nid][1]
    def search(self, p): return None