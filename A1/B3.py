from __future__ import print_function
import sys
import hashlib

def calc_hash(left, right):
    sha = hashlib.sha1(bytearray.fromhex(left + right))
    return sha.hexdigest()


file = open(sys.argv[1], 'r')
prev_node = file.next().strip()

for line in file:
    current_node = line
    is_right = current_node[0] == 'R'

    if is_right:
        prev_node = calc_hash(prev_node, current_node[1:-1].strip())
    else:
        prev_node = calc_hash(current_node[1:].strip(), prev_node)
print(prev_node)
