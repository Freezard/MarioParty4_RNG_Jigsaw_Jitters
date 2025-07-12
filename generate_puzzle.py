from frandom import FrandRNG
# from utils import get_absolute_path

def generate_puzzle(pieces, starting_seed):
    rng = FrandRNG(starting_seed)
    rng.preroll(300)

    pattern = list(range(pieces))
    rotations = list(range(pieces))
    for i in range(pieces):
        pattern[i] = i
        rotations[i] = rng.frandmod(4)

    for _ in range(50):
        i = rng.frandmod(pieces)
        j = rng.frandmod(pieces)
        pattern[i], pattern[j] = pattern[j], pattern[i]

    # if rng.hit_seed_zero:
    #     file_path = get_absolute_path("zero_seeds.log")
    #     with open(file_path, "a", encoding="utf-8") as log:
    #         log.write(f"{starting_seed:08X}\n")
    # print(f"{pattern} {rotations} {starting_seed:08X}{note}")

    return pattern, rotations
