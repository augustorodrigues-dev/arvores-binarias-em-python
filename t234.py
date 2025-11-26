from typing import Dict, Optional, List, Callable

class Node234:
    def __init__(self, keys: List[int], children: List[int], leaf: bool):
        self.keys = keys
        self.children = children
        self.leaf = leaf

class Tree234:
    def __init__(self, animation_callback: Optional[Callable] = None):
        self.nodes: Dict[int, Node234] = {}
        self.root: Optional[int] = None
        self._next_id = 1
        self.anim_cb = animation_callback

    def _animate(self, nodes: List[Optional[int]], msg: str):
        if self.anim_cb:
            valid_nodes = [n for n in nodes if n is not None]
            if valid_nodes: self.anim_cb(valid_nodes, msg)

    def _new_node(self, keys: List[int], children: List[int], leaf: bool) -> int:
        nid = self._next_id
        self._next_id += 1
        self.nodes[nid] = Node234(keys, children, leaf)
        return nid

    def search(self, key: int) -> Optional[int]:
        def _search_node(nid: int, key: int) -> Optional[int]:
            node = self.nodes[nid]
            i = 0
            while i < len(node.keys) and key > node.keys[i]: i += 1
            if i < len(node.keys) and key == node.keys[i]: return nid
            if node.leaf: return None
            else: return _search_node(node.children[i], key)
        if self.root is None: return None
        return _search_node(self.root, key)

    def insert(self, key: int) -> None:
        if self.root is None:
            self.root = self._new_node([key], [], True)
            self._animate([self.root], f"Raiz criada com {key}.")
            return

        root = self.nodes[self.root]
        if len(root.keys) == 3:
            self._animate([self.root], f"Raiz cheia {root.keys}. Dividindo (Split)...")
            old_root_id = self.root
            old_root = self.nodes[old_root_id]
            mid_key = old_root.keys[1]

            left_keys = [old_root.keys[0]]; right_keys = [old_root.keys[2]]
            if old_root.leaf: left_children = []; right_children = []
            else: left_children = old_root.children[:2]; right_children = old_root.children[2:]

            left_id = self._new_node(left_keys, left_children, old_root.leaf)
            right_id = self._new_node(right_keys, right_children, old_root.leaf)
            new_root_id = self._new_node([mid_key], [left_id, right_id], False)
            self.root = new_root_id
            
            self._animate([new_root_id, left_id, right_id], f"Raiz dividida. Nova raiz: {mid_key}")
            
        self._insert_nonfull(self.root, key)

    def _insert_nonfull(self, nid: int, key: int) -> None:
        node = self.nodes[nid]
        i = len(node.keys) - 1
        if node.leaf:
            self._animate([nid], f"Inserindo {key} na folha {node.keys}...")
            node.keys.append(0)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
            self._animate([nid], f"Folha atualizada: {node.keys}")
        else:
            while i >= 0 and key < node.keys[i]: i -= 1
            i += 1
            child_id = node.children[i]
            child = self.nodes[child_id]
            if len(child.keys) == 3:
                self._animate([nid, child_id], f"Filho cheio {child.keys}. Dividindo ao descer...")
                self._split_child(nid, i)
                if key > node.keys[i]: i += 1
            self._insert_nonfull(node.children[i], key)

    def _split_child(self, parent_id: int, index: int) -> None:
        parent = self.nodes[parent_id]
        child_id = parent.children[index]
        child = self.nodes[child_id]

        mid_key = child.keys[1]
        left_keys = [child.keys[0]]; right_keys = [child.keys[2]]
        if child.leaf: left_children = []; right_children = []
        else: left_children = child.children[:2]; right_children = child.children[2:]

        left_id = self._new_node(left_keys, left_children, child.leaf)
        right_id = self._new_node(right_keys, right_children, child.leaf)

        parent.keys.insert(index, mid_key)
        parent.children[index] = left_id
        parent.children.insert(index + 1, right_id)
        
        self._animate([parent_id, left_id, right_id], f"Split concluído. Chave {mid_key} subiu.")