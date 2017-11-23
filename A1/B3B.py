from __future__ import print_function
import sys
import hashlib

class Node:
    parent = None
    left_child = None
    right_child = None
    hash_value = None
    orientation = None

    def __init__(self, hash_value, left_child, right_child, orientation):
        self.hash_value = hash_value
        self.left_child = left_child
        self.right_child = right_child
        self.orientation = orientation

    def set_parent(self, parent):
        self.parent = parent

class Tree:

    def __init__(self):
        self.leaves = []
        self.root = None
        self.depth = 0

    def append_node(self, left, right):
        node = Node(calc_hash(left.hash_value, right.hash_value), left, right, None)
        left.parent = node
        left.orientation = 'L'
        right.parent = node
        right.orientation = 'R'
        return node

    def build_layer(self, list):
        self.depth += 1
        layer = []
        prev_node = None
        for current_node in list:
            if prev_node != None:
                layer.append(self.append_node(prev_node, current_node))
                prev_node = None
            else:
                prev_node = current_node

        if prev_node != None:
            layer.append(self.append_node(prev_node, prev_node))

        if len(layer) != 1:
            return self.build_layer(layer)
        return layer[0]


    def build(self, file):
        for line in file:
            self.leaves.append(Node(line.strip(), None, None, None))
        self.root = self.build_layer(self.leaves)

    def get_path(self, i, j):
        node = self.leaves[i]
        current_depth = self.depth
        while node.parent != None:
            if node.orientation == 'R':
                sibling = node.parent.left_child
            else:
                sibling = node.parent.right_child
            if j == current_depth:
                path_node = sibling.orientation + sibling.hash_value
            print(sibling.orientation + sibling.hash_value)
            node = node.parent
            current_depth -= 1
        print("\nPath Node: " + path_node)
        print("\nRoot: " + self.root.hash_value)
        print("\nDepth: " + str(self.depth))
        print("\nResult: " + path_node + self.root.hash_value)

def calc_hash(left, right):
    sha = hashlib.sha1(bytearray.fromhex(left + right))
    return sha.hexdigest()



file = open(sys.argv[1], 'r')
i = int(file.next())
j = int(file.next())

tree = Tree()
tree.build(file)
tree.get_path(i, j)
