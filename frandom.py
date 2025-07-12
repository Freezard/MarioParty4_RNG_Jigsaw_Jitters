def frandom(param):
    rand2 = param // 0x1F31D
    rand3 = param - (rand2 * 0x1F31D)
    param = (rand2 * 0xB14) - (rand3 * 0x41A7)

    return param & 0xFFFFFFFF

class FrandRNG:
    def __init__(self, seed):
        self.seed = seed & 0xFFFFFFFF
        self.hit_seed_zero = self.seed == 0

    def frand(self):
        if self.seed == 0:
            self.hit_seed_zero = True
            self.seed = 0xD826BC89  # Fallback seed
        self.seed = frandom(self.seed)
        return self.seed

    def frandmod(self, mod):
        return (self.frand() & 0x7FFFFFFF) % mod

    def preroll(self, count):
        for _ in range(count):
            self.frand()
