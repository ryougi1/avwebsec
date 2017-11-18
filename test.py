from binascii import unhexlify, hexlify
import hashlib
import sys

def main():
	result = bytearray()

	for line in sys.stdin:
		print("start")
		print(line)

		#line = line[:-1]
		line = line.strip()
		formatted = line

		if line[:1] is 'R':
			formatted = line[1:]
		elif line[:1] is 'L':
			formatted = line[1:]

		print(formatted)
		print(len(formatted))

		byteline = unhexlify(formatted)#formatted.decode("hex")
		#byteline = bytes(bytearray.fromhex(formatted))

		if line[:1] is 'R':
			result += byteline
			n = hashlib.sha1()
			n.update(result)
			result = unhexlify(n.hexdigest())#bytes(bytearray.fromhex(n.hexdigest()))
		elif line[:1] is 'L':
			result = byteline + result;
			n = hashlib.sha1()
			n.update(result)
			result = unhexlify(n.hexdigest())
		else:
			result = byteline

		print(result)

	print("resulting hash: ")
	print(result)
	print(hexlify(result))

if __name__ == "__main__":
main()
