from typing import Optional, Tuple, Dict

class KDNode:
    def __init__(self, point: Tuple[int, int], axis: int):
        self.point = point  
        self.axis = axis    
        self.left: Optional['KDNode'] = None
        self.right: Optional['KDNode'] = None
        self.freq = 1

class KDTree:
    def __init__(self):
        self.root: Optional[KDNode] = None
        self.nodes: Dict[int, KDNode] = {}
        self.adj: Dict[int, Tuple[Optional[int], Optional[int]]] = {}
        self._next_id = 1

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
            return self._new_node(point, axis)

        node = self.nodes[nid]
        
        
        if point == node.point:
            node.freq += 1
            return nid

        
        axis = node.axis
        val = point[axis]
        node_val = node.point[axis]

        l_child, r_child = self.adj[nid]

        if val < node_val:
            new_left = self._insert_rec(l_child, point, depth + 1)
            self.adj[nid] = (new_left, r_child)
            node.left = self.nodes[new_left] 
        else:
            new_right = self._insert_rec(r_child, point, depth + 1)
            self.adj[nid] = (l_child, new_right)
            node.right = self.nodes[new_right]

        return nid

    def insert(self, point: Tuple[int, int]) -> None:
        self.root = self._insert_rec(self.root, point, 0)

    
    def _get_left(self, nid: int) -> Optional[int]:
        return self.adj[nid][0]

    def _get_right(self, nid: int) -> Optional[int]:
        return self.adj[nid][1]

    def search(self, point: Tuple[int, int]) -> Optional[int]:
       
        cur = self.root
        while cur is not None:
            node = self.nodes[cur]
            if node.point == point:
                return cur
            axis = node.axis
            if point[axis] < node.point[axis]:
                cur = self.adj[cur][0]
            else:
                cur = self.adj[cur][1]
        return None