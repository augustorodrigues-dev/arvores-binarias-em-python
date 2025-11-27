from typing import Dict, Tuple, Optional
from config import LARGURA, ALTURA

def calcular_layout_binario(tree, root_id: int) -> Dict[int, Tuple[int, int]]:
    """Calcula posições para Árvores Binárias (Rubro-Negra)"""
    positions = {}
    if root_id is None: 
        return positions

    def _recursive(nid, depth, x_min, x_max):
        if nid is None or nid not in tree.nodes: 
            return
        
        x = (x_min + x_max) // 2
        y = 120 + depth * 80
        positions[nid] = (x, y)
        
        
        if hasattr(tree, '_left'):
            l = tree._left(nid)
            r = tree._right(nid)
        else:
            
            l = getattr(tree, '_get_left', lambda x: None)(nid)
            r = getattr(tree, '_get_right', lambda x: None)(nid)

        if l is not None: _recursive(l, depth + 1, x_min, x - 40)
        if r is not None: _recursive(r, depth + 1, x + 40, x_max)

    _recursive(root_id, 0, 50, LARGURA - 50)
    return positions

def calcular_layout_234(tree, root_id: int) -> Dict[int, Tuple[int, int]]:
    """Calcula posições para Árvore 2-3-4"""
    positions = {}
    if root_id is None: 
        return positions

    def _recursive(nid, depth, x_min, x_max):
        if nid not in tree.nodes: return
        node = tree.nodes[nid]
        y = 120 + depth * 90
        
        if node.leaf or not node.children:
            x = (x_min + x_max) // 2
            positions[nid] = (x, y)
        else:
            n_children = len(node.children)
            child_centers = []
            width = x_max - x_min
            span = max(width // n_children, 80)
            cur_x = x_min
            
            for child_id in node.children:
                _recursive(child_id, depth + 1, cur_x, cur_x + span)
                if child_id in positions:
                    child_centers.append(positions[child_id][0])
                cur_x += span
            
            if child_centers:
                x = sum(child_centers) // len(child_centers)
            else:
                x = (x_min + x_max) // 2
            positions[nid] = (x, y)

    _recursive(root_id, 0, 80, LARGURA - 80)
    return positions