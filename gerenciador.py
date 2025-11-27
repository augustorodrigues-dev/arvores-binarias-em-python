from typing import List, Optional, Union, Tuple, Callable
from rb import RBTreeAdj
from t234 import Tree234

class EstruturaArvore:
    def __init__(self, tipo: str, animation_callback: Optional[Callable] = None):
        self.tipo = tipo
        if tipo == "RB": 
            self.tree = RBTreeAdj(animation_callback)
        elif tipo == "234": 
            self.tree = Tree234(animation_callback)
        else:
            raise ValueError(f"Tipo desconhecido: {tipo}")

    def inserir(self, key: int):
        self.tree.insert(key)

    def remover(self, key: int) -> bool:
        return self.tree.remove(key)

    def buscar_caminho_animado(self, key: int) -> List[int]:
        if hasattr(self.tree, 'search_step_by_step'):
            return self.tree.search_step_by_step(key)
        return []