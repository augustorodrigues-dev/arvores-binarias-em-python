from typing import List, Optional, Union, Tuple, Callable
from avl import AVLTreeAdj
from rb import RBTreeAdj
from t234 import Tree234
from kd import KDTree 
from splay import SplayTreeAdj # <--- IMPORT NOVO

class EstruturaArvore:
    def __init__(self, tipo: str, animation_callback: Optional[Callable] = None):
        self.tipo = tipo
        if tipo == "AVL": self.tree = AVLTreeAdj(animation_callback)
        elif tipo == "RB": self.tree = RBTreeAdj(animation_callback)
        elif tipo == "234": self.tree = Tree234(animation_callback)
        elif tipo == "KDT": self.tree = KDTree(animation_callback)
        elif tipo == "SPLAY": self.tree = SplayTreeAdj(animation_callback) # <--- NOVO
        else: raise ValueError("Tipo desconhecido")

    def inserir(self, key: Union[int, Tuple[int, int]]):
        self.tree.insert(key)

    def remover(self, key) -> bool:
        return self.tree.remove(key)

    def buscar_caminho_animado(self, key) -> List[int]:
        # Splay também suporta busca animada
        if self.tipo in ("AVL", "RB", "KDT", "234", "SPLAY"):
            return self.tree.search_step_by_step(key)
        return []
    
    # Legado (pode remover se já limpou tudo)
    def buscar_caminho_binaria(self, key): return []
    def buscar_caminho_234(self, key): return []