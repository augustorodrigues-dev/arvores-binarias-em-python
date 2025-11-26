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
        nid = self._next_id; self._next_id += 1
        self.nodes[nid] = Node234(keys, children, leaf)
        return nid

    
    def insert(self, key: int) -> None:
        self._animate([], f"Inserindo {key}...")
        if self.root is None:
            self.root = self._new_node([key], [], True)
            self._animate([self.root], "Raiz criada.")
            return
        root = self.nodes[self.root]
        if len(root.keys) == 3:
            self._animate([self.root], "Raiz cheia. Split.")
            old_root_id = self.root
            mid = root.keys[1]
            l_keys = [root.keys[0]]; r_keys = [root.keys[2]]
            if root.leaf: lc=[]; rc=[]
            else: lc=root.children[:2]; rc=root.children[2:]
            lid = self._new_node(l_keys, lc, root.leaf)
            rid = self._new_node(r_keys, rc, root.leaf)
            self.root = self._new_node([mid], [lid, rid], False)
        self._insert_nonfull(self.root, key)

    def _insert_nonfull(self, nid: int, key: int) -> None:
        node = self.nodes[nid]
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]; i-=1
            node.keys[i+1] = key
            self._animate([nid], f"Inserido na folha: {node.keys}")
        else:
            while i >= 0 and key < node.keys[i]: i-=1
            i += 1
            child_id = node.children[i]
            if len(self.nodes[child_id].keys) == 3:
                self._animate([nid, child_id], "Filho cheio. Split ao descer.")
                self._split_child(nid, i)
                if key > node.keys[i]: i += 1
            self._insert_nonfull(node.children[i], key)

    def _split_child(self, pid: int, i: int):
        parent = self.nodes[pid]
        cid = parent.children[i]
        child = self.nodes[cid]
        mid = child.keys[1]
        l_keys = [child.keys[0]]; r_keys = [child.keys[2]]
        if child.leaf: lc=[]; rc=[]
        else: lc=child.children[:2]; rc=child.children[2:]
        lid = self._new_node(l_keys, lc, child.leaf)
        rid = self._new_node(r_keys, rc, child.leaf)
        parent.keys.insert(i, mid)
        parent.children[i] = lid
        parent.children.insert(i+1, rid)

    
    def remove(self, key: int) -> bool:
        if self.root is None: return False
        self._animate([], f"Removendo {key}...")
        self._delete(self.root, key)
        
        if len(self.nodes[self.root].keys) == 0:
            if not self.nodes[self.root].leaf:
                self.root = self.nodes[self.root].children[0]
            else:
                self.root = None
        return True

    def _delete(self, nid: int, key: int):
        node = self.nodes[nid]
        idx = -1
        for i, k in enumerate(node.keys):
            if k == key: idx = i; break
        
        if idx != -1: 
            if node.leaf:
                self._animate([nid], f"Removendo {key} da folha.")
                node.keys.pop(idx)
            else:
                self._animate([nid], f"Chave {key} em nó interno. Substituindo.")
                
                pred_child = node.children[idx]
                cur = pred_child
                while not self.nodes[cur].leaf:
                    cur = self.nodes[cur].children[-1]
                pred_key = self.nodes[cur].keys[-1]
                node.keys[idx] = pred_key
                self._animate([nid], f"Substituído por {pred_key}. Deletando recursivamente.")
                self._delete(pred_child, pred_key)
        else:
            
            i = 0
            while i < len(node.keys) and key > node.keys[i]: i+=1
            child_id = node.children[i]
            child = self.nodes[child_id]
            
            
            if len(child.keys) == 1:
                self._animate([nid, child_id], "Filho com 1 chave. Tentando emprestar/merge.")
                self._fix_underflow(nid, i)
                
                if i > len(node.keys): i -= 1 
                child_id = node.children[i] 
            
            self._delete(child_id, key)

    def _fix_underflow(self, pid: int, idx: int):
        parent = self.nodes[pid]
        child_id = parent.children[idx]
        child = self.nodes[child_id]
        
        
        if idx > 0:
            left_sib_id = parent.children[idx-1]
            left_sib = self.nodes[left_sib_id]
            if len(left_sib.keys) >= 2:
                self._animate([pid, left_sib_id, child_id], "Emprestando da esquerda.")
                child.keys.insert(0, parent.keys[idx-1])
                parent.keys[idx-1] = left_sib.keys.pop()
                if not child.leaf:
                    child.children.insert(0, left_sib.children.pop())
                return

        
        if idx < len(parent.children) - 1:
            right_sib_id = parent.children[idx+1]
            right_sib = self.nodes[right_sib_id]
            if len(right_sib.keys) >= 2:
                self._animate([pid, right_sib_id, child_id], "Emprestando da direita.")
                child.keys.append(parent.keys[idx])
                parent.keys[idx] = right_sib.keys.pop(0)
                if not child.leaf:
                    child.children.append(right_sib.children.pop(0))
                return

        
        self._animate([pid], "Merge (Fusão) necessário.")
        if idx > 0:
            
            left_sib_id = parent.children[idx-1]
            left_sib = self.nodes[left_sib_id]
            left_sib.keys.append(parent.keys.pop(idx-1))
            left_sib.keys.extend(child.keys)
            if not left_sib.leaf: left_sib.children.extend(child.children)
            parent.children.pop(idx) 
        else:
            
            right_sib_id = parent.children[idx+1]
            right_sib = self.nodes[right_sib_id]
            child.keys.append(parent.keys.pop(idx))
            child.keys.extend(right_sib.keys)
            if not child.leaf: child.children.extend(right_sib.children)
            parent.children.pop(idx+1)

    def search_step_by_step(self, key: int) -> List[int]:
        path = []
        if self.root is None: return path
        cur = self.root
        while True:
            path.append(cur)
            node = self.nodes[cur]
            self._animate([cur], f"Visitando {node.keys}...")
            i = 0
            while i < len(node.keys) and key > node.keys[i]: i += 1
            if i < len(node.keys) and key == node.keys[i]:
                self._animate([cur], "Encontrado!")
                return path
            if node.leaf: return []
            cur = node.children[i]