from pyalgo.basic_modules import default_functions, default_values

class RSA():
    def __init__(self, p, q, e):
        self.p = p
        self.q = q
        self.e = e

        self.Phi = ((self.p - 1) * (self.q - 1))

        if e >= self.Phi:  raise ValueError(f"'e' cannot be bigger that phi({self.Phi})")

        self.check_if_e_is_valid(e, p, q)
        if default_functions.prime_check(e) == False:  raise ValueError("'e' should be prime")
        if default_functions.prime_check(p) == False:  raise ValueError("'p' should be prime")
        if default_functions.prime_check(q) == False:  raise ValueError("'q' should be prime")

        self.N = p * q  # compute N

    def check_if_e_is_valid(self, e=None, p=None, q=None):

        if e == None:  e == self.e
        if p == None:  p == self.p
        if q == None:  q == self.q
        if not (default_functions.gcd(e, self.Phi) == 1):
            raise ValueError("'e' should not have a gcd with φ(p, q) that is not 1")

    def find_private_key(self):

        d = 1

        while not ((self.e * d) % self.Phi == 1):
            d += 1

            if d >= self.Phi:
                raise ValueError("'d' cannot exceed phi({self.Phi})")

            if d % 1000000 == 0:
                print(d)

        self.d = d
        print("final d =", d)

    def encrypt(self, M, N=None, e=None):

        StringType = default_values.StringType

        if N == None:  N = self.N
        if e == None:  e = self.e

        if not isinstance(M, StringType):  raise TypeError("'M' should be a string")

        M = [ord(char) for char in M]  # transfer into bytes

        return [((value ** e) % N) for value in M]

    def decrypt(self, C, N=None, d=None):
        ListType = default_values.ListType

        if N == None:  N = self.N
        if d == None:  d = self.d

        if not isinstance(C, ListType):  raise TypeError("'C' should be a List")

        M = ""

        for idx, value in enumerate(C):
            M += chr((value**d)%N)
            print(f"Iteration {idx+1} \\ {len(C)}")

        return M

    @property
    def private_key(self):
        return {"d":self.d, "e":self.e}

    @property
    def public_key(self):
        return {"N":self.N, "e":self.e}

    @property
    def key(self):
        return {"N":self.N, "d":self.d, "e":self.e}


    def save_key_to_dir(self, dir=None, filename="key.rsa"):

        dir += "\\" + str(filename)

        content = ""
        for i in self.key:
            content += "{} {} \n".format(i, self.key[i])

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")

    def save_public_key_to_dir(self, dir=None, filename="public_key.rsa"):

        dir += "\\" + str(filename)

        content = ""
        for i in self.public_key:
            content += "{} {} \n".format(i, self.key[i])

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")

    def save_private_key_to_dir(self, dir=None, filename="private_key.rsa"):

        dir += "\\" + str(filename)

        content = ""
        for i in self.private_key:
            content += "{} {} \n".format(i, self.key[i])

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")

    def load_keys(self, dir):
        with open(dir) as file:
            content = file.readlines()

        for i in content:
            if i[0] == "e":
                self.e = int(i[2:-2])
            if i[0] == "d":
                self.d = int(i[2:-2])
            if i[0] == "N":
                self.N = int(i[2:-2])

        print("loaded")

    def clear_keys(self):
        del self.e
        del self.d
        del self.N


    def print_public_key(self):
        print(f"N = {self.N}")
        print(f"e = {self.e}")

    def print_private_key(self):
        print(f"N = {self.N}")
        print(f"d = {self.d}")

    def print_key(self):
        print(f"N = {self.N}")
        print(f"e = {self.e}")
        print(f"d = {self.d}")