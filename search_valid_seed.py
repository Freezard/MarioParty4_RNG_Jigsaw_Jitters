from frandom import frandom

def is_target_reachable(start_seed, target):
    seen = set()
    current = start_seed
    rolls = 0

    while True:
        if current == 0:
            print(f"Seed {start_seed:08X} hit zero in {rolls} rolls, stopping search")
            return None 
        if current == target:
            print(f"Seed {start_seed:08X} reached {target:08X} in {rolls} rolls")
            return rolls
        if current in seen:
            print(f"Seed {start_seed:08X} entered a loop {current:08X} after {rolls} rolls, stopping search")
            return None
        seen.add(current)
        current = frandom(current)
        rolls += 1

# 3165 rolls to reach the mini-game
# 3429 total rolls for initial seed 02F7EBEE = 3165 + 6 * grey
# 44 rolls forward / back grey
# 56 rolls forward / back blue

def main():
    start = 0x02F7EBEE # -> 9D5DA839 after initial roll
    target = 0xAE398399

    is_target_reachable(start, target)

if __name__ == "__main__":
    main()
