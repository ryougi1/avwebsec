from __future__ import print_function
import sys

sa = int(sys.argv[1], 16)
sb = int(sys.argv[2], 16)
da = int(sys.argv[3], 16)
db = int(sys.argv[4], 16)
m = int(sys.argv[5], 16)
b = int(sys.argv[6], 16)

sxor = sa ^ sb

if(b == 1):
    print("Output: ", hex(sxor ^ m)[2:])
else:
    end = hex(sxor ^ da ^ db)[2:]
    if len(end) < 4:
        end += "000"
    print("Output: ", hex(sxor)[2:] + end)
