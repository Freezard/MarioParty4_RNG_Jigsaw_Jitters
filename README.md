# Mario Party 4 RNG and solving Jigsaw Jitters
I was thinking it would be fun to make an auto-solver for Jigsaw Jitters, an RNG heavy puzzle mini-game in Mario Party 4, and when I found out about the [MP4 decompilation](https://github.com/mariopartyrd/marioparty4), I decided to dive deeper into it. Hopefully what I learned can help other people, and the RNG system might apply to other Mario Party GameCube titles as well (here's for example some info about [MP5](https://github.com/NicholasMoser/MarioParty5_RNG)).  

This was done on game version GMPE01_01: Rev 1 (USA) and Dolphin 5.0.

## RNG
Seed address: 0x801D3D10  

Mario Party 4 uses the [Lehmer RNG](https://en.wikipedia.org/wiki/Lehmer_random_number_generator), specifically the MINSTD version where a = 16807 and m = 2^31 - 1. This means that not every seed in the 2^32 space is valid, and the cycles are somewhat short, usually moving towards common repeating seeds after around 1 million seeds. It also means the initial seed has a big role in which seeds are traversed.  

Here's the decompiled implementation of frand and frandom in [frand.c](https://github.com/mariopartyrd/marioparty4/blob/main/src/game/frand.c), and to advance the RNG one can use this formula: `nextx = 2^32 - (16807 * X % (2^31 - 1))` where X is the current seed. The formula for reversing Lehmer RNG is: `prevx = ainverse * x mod m`. With some adjustments including using two reverse formulas and adding 2m if the result is negative I managed to implement a working version for MP4, seen in [reverse_seed.c](https://github.com/Freezard/MarioParty4_RNG_Jigsaw_Jitters/blob/main/reverse_seed.c).

### Initial seed
There is a special case for when the seed is 0:

    if (param == 0) {
        param = rand8();
        param = param ^ (s64)OSGetTime();
        param ^= 0xD826BC89;
    }

The seed is set to 0 when the game is started, and in extremely rare cases a seed can roll into 0 as well. The rand8 function can be found in [main.c](https://github.com/mariopartyrd/marioparty4/blob/main/src/game/main.c), and it will return a value from 0-255, but on startup it will always be 0x11. Then a value is generated based on the system clock during startup, and on Dolphin it will use seconds, where every second adds 40.5 million. You can read more about how it works in this [Melee TAS](https://tasvideos.org/7174S) under RNG Initialization, which is very similar.  

I used this information to make a function which searches for an initial seed and displays the dates of when this seed is generated during startup in [search_initial_seed.py](https://github.com/Freezard/MarioParty4_RNG_Jigsaw_Jitters/blob/main/search_initial_seed.py). One can then for example edit the date of a DTM to get the desired initial seed. It appears the seeds initialized can only end in {EVEN_DIGIT}E although this seems to vary depending on Dolphin version. Also note that after the initial seed is set, the frandom function will progress as normal and advance the seed once.

## Jigsaw Jitters
The decompiled code for the mini-game is in [m451.c](https://github.com/mariopartyrd/marioparty4/blob/main/src/REL/m451Dll/m451.c), although it's hard to read because of anonymous variable and function names. Basically the order of puzzle pieces and their starting rotations are generated at the start, based on the starting seed, so it's possible to generate all puzzle patterns and solve them programmatically. The puzzle board is 460x340 units big and the first piece always starts at (0, 0). The insertion zones are circles with a radius of 40 units from the slot origin of each piece. The next piece always starts at the slot origin of the just inserted piece. The animation for inserting a piece takes 1 second. Rotating a piece takes 19 frames, so double rotating a piece is especially bad for the 20 pieces puzzle.  

The slot origin positions for all pieces were extracted from memory, and stick to vector movement mappings were saved to file as well (movement is linear). After that, it was possible to solve a puzzle by finding the shortest distance between pieces and summing the movement times in frames (both of which were precomputed), along with adding eventual delays from rotations. [main.py](https://github.com/Freezard/MarioParty4_RNG_Jigsaw_Jitters/blob/main/main.py) contains the main function for generating and solving puzzles for ranges of starting seeds. The fastest solutions were printed to file.

### 30 pieces TAS
The fastest solution found had multiple starting seeds, but the only valid one was 0xAE398399. It could be reversed enough times so that an initial seed 0x02F7EBEE could be chosen, by setting the date of the DTM to 2029-06-21 23:58:58, in order to reach the starting seed in 3429 rolls. To reach Jigsaw Jitters from startup, it takes 3165 rolls, and the remaining 264 rolls were done by selecting the gray Whomp and backing out six times (44 rolls each). Finally, the Lua input to auto-solve the puzzle in-game was generated in [generate_lua_inputs.py](https://github.com/Freezard/MarioParty4_RNG_Jigsaw_Jitters/blob/main/generate_lua_inputs.py), although it's not entirely accurate so I had to manually adjust input timings.  

The resulting TAS in 41"55 can be found [here](https://youtu.be/1MxhSY2qiK0).

### 40 pieces TAS
Starting seed was 0xD3BC0D7E. Date was set to 2027-03-15 04:55:09 which initialized with seed 0xDA10F14E. The starting seed could then be reached by selecting the gray Whomp and backing out ten times.  

The resulting TAS in 55"73 can be found [here](https://youtu.be/8Q31RY3D6jA).
