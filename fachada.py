# fachada.py
from typing import List, Optional, Union, Tuple
from avl import AVLTreeAdj
from rb import RBTreeAdj
from t234 import Tree234
from kd import KDTree 

class EstruturaArvore:
    def __init__(self, tipo: str):
        self.tipo = tipo
        if tipo == "AVL":
            self.tree = AVLTreeAdj()
        elif tipo == "RB":
            self.tree = RBTreeAdj()
        elif tipo == "234":
            self.tree = Tree234()
        elif tipo == "KDT":  # <--- NOVO TIPO
            self.tree = KDTree()
        else:
            raise ValueError("Tipo desconhecido")

    def inserir(self, key: Union[int, Tuple[int, int]]):
        self.tree.insert(key)

    def remover(self, key) -> bool:
        if self.tipo == "AVL":
            self.tree.remove(key)
            return True
        return False

    def buscar(self, key) -> Optional[int]:
        return self.tree.search(key)

    def buscar_caminho_binaria(self, key) -> List[int]:
        # Funciona para AVL, RB e KD (KD é binária estruturalmente)
        caminho = []
        if self.tipo in ("AVL", "RB", "KDT"):
            cur = self.tree.root
            while cur is not None:
                caminho.append(cur)
                node = self.tree.nodes[cur]
                
                # Adaptação para KD (chave é tupla) vs Outras (int)
                if self.tipo == "KDT":
                     val_node = node.point
                     val_busca = key
                     # Lógica KD
                     if val_node == val_busca:
                         break
                     axis = node.axis
                     if val_busca[axis] < val_node[axis]:
                         cur = self.tree._get_left(cur)
                     else:
                         cur = self.tree._get_right(cur)
                else:
                    # Lógica AVL/RB
                    if key == node.key: break
                    elif key < node.key: cur = (self.tree._left(cur) if self.tipo=="RB" else self.tree._get_left(cur))
                    else: cur = (self.tree._right(cur) if self.tipo=="RB" else self.tree._get_right(cur))
        return caminho
    
    # ... manter buscar_caminho_234 igual ...
    def buscar_caminho_234(self, key: int) -> List[int]:
        ids = []
        if self.tipo != "234" or self.tree.root is None:
            return ids
        def _search(nid: int, key: int):
            node = self.tree.nodes[nid]
            ids.append(nid)
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and key == node.keys[i]: return
            if node.leaf: return
            _search(node.children[i], key)
        _search(self.tree.root, key)
        return ids