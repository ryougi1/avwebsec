import random
import hashlib

#take two inputs plain1 and plain2, concatenate and hash, returns integer value base 16
def h(plain1, plain2):
    return int(hashlib.md5(str(plain1).encode('utf-8')+str(plain2).encode('utf-8')).hexdigest(), 16)

#returns a random prime
def get_random_prime():
    primes = open('primes', 'r')
    random_int = random.randint(1, 70)
    line = primes.readline()
    for i in range (0, random_int):
        line = primes.readline()
    return line

#euclidian algorithm
def modular_inverse(e, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, e, n = e // n, n, e % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0

class Bank:
    n = 0
    k = 0
    #calculate RSA modulus n and security param k
    def __init__(self):
        p = 0
        q = 0
        p = int(get_random_prime())
        q = int(get_random_prime())
        while (q == p):
            q = get_random_prime()
        self.n = p * q
        self.k = 5

    #return RSA modulus n
    def get_n(self):
        return self.n

    #return security param k
    def get_k(self):
        return self.k

    #returns a k long list of randomly chosen indexes where 0 <= index <=2k
    def get_indices(self):
        indices = []
        while len(indices) < self.k:
            index = random.randint(0, self.k*2-1)
            if (index not in indices):
                indices.append(index)

        print("Requested indexes for check:", indices)

        return indices

    def check(self, acdr, ID):
        print("------CHECKING------")
        for i in range(0, len(acdr)):
            given_B = acdr[i][4]
            x = h(acdr[i][0], acdr[i][1])
            y = h(acdr[i][0] ^ ID, acdr[i][2])
            calculated_B = acdr[i][3] ** 3 * h(x, y) % self.n
            print("Given B:", given_B, "Calculated B:", calculated_B, "is", given_B == calculated_B)
            if given_B != calculated_B:
                print("y u lie")
                return False
        print("------CHECK OK------")
        return True

    def blind_sign(self, remaining_B):
        d = modular_inverse(3, self.n)
        print("Inverse of 3 mod" , self.n, "=", d)
        signature = 1
        for B in remaining_B:
            signature *= B ^ d
        print("Bank signature: ", signature % self.n)
        return signature % self.n


class Client:
    #generates 2k number of B values
    def __init__(self, ID, n, k):
        self.ID = ID
        self.r = []
        self.x = []
        self.y = []
        self.B = []

        for i in range(0, 2*k):
            r = random.randint(1,1000)
            self.r.append(r)
            a = random.randint(1,1000)
            c = random.randint(1,1000)
            d = random.randint(1,1000)

            tempx = [a, c, h(a, c)]
            self.x.append(tempx)
            tempy = [d, h(a ^ ID, d)]
            self.y.append(tempy)
            self.B.append(r ** 3 * h(h(a,c), h(a ^ ID, d)) % n)

            print("Index", i, "contains B:", self.B[i], "a:", a, "c:", c, "d:", d, "r:", r)


    def reveal(self, indices):
        acdr = []
        for index in indices:
            a = self.x[index][0]
            c = self.x[index][1]
            d = self.y[index][0]
            r = self.r[index]
            B = self.B[index]
            acdr.append([a, c, d, r, B])
            print("Index requested:", index, "--- revealead: ", "B:", B, "a:", a, "c:", c, "d:", d, "r:", r)
        return acdr

    def get_ID(self):
        return int(self.ID)

    def get_remaining_values(self, indices):
        remaining_B = []
        for i in range(0, 2*k):
            if i not in indices:
                remaining_B.append(self.B[i])
        print("Remaining B values are:", remaining_B)
        return remaining_B

    def compute_serial(self, remaining_B):
        serial = 1
        for B in remaining_B:
            i = self.B.index(B)
            serial *= h(self.x[i], self.y[i]) ^ modular_inverse(self.r[i], n)
        print("Serial number =", serial)
        return serial


if __name__ == '__main__':
    bank = Bank()
    n = bank.get_n()
    k = bank.get_k()
    print("n =", n, "k =", k)
    alice = Client(666, n, k)
    indices = bank.get_indices()
    userID = alice.get_ID()
    if bank.check(alice.reveal(indices), userID):
        B_remaining = alice.get_remaining_values(indices)
        bank_signature = bank.blind_sign(B_remaining)
        alice.compute_serial(B_remaining)
    else:
        print("nonono")
