from typing import List, Optional, Union, Tuple, Callable
from avl import AVLTreeAdj
from rb import RBTreeAdj
from t234 import Tree234
from kd import KDTree 

class EstruturaArvore:
    def __init__(self, tipo: str, animation_callback: Optional[Callable] = None):
        self.tipo = tipo
        if tipo == "AVL": self.tree = AVLTreeAdj(animation_callback)
        elif tipo == "RB": self.tree = RBTreeAdj(animation_callback)
        elif tipo == "234": self.tree = Tree234(animation_callback)
        elif tipo == "KDT": self.tree = KDTree(animation_callback)
        else: raise ValueError("Tipo desconhecido")

    def inserir(self, key: Union[int, Tuple[int, int]]):
        self.tree.insert(key)

    def remover(self, key) -> bool:
        
        return self.tree.remove(key)

    def buscar_caminho_animado(self, key) -> List[int]:
        if self.tipo in ("AVL", "RB", "KDT", "234"):
            return self.tree.search_step_by_step(key)
        return []

    
    def buscar_caminho_binaria(self, key): return []
    def buscar_caminho_234(self, key): return []