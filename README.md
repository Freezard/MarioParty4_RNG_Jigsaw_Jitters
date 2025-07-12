# Mario Party 4 RNG and solving Jigsaw Jitters
I was thinking it would be fun to make an auto-solver for Jigsaw Jitters, a puzzle mini-game in Mario Party 4 involving a lot of RNG, and when I found out about the [MP4 decompilation](https://github.com/mariopartyrd/marioparty4), I decided to deep dive into it. Hopefully what I learned can help other people, and the RNG system might apply to other Mario Party GameCube titles as well, here's for example some info about [MP5](https://github.com/NicholasMoser/MarioParty5_RNG).  

This was done on game version GMPE01_01: Rev 1 (USA) and Dolphin 5.0.

## RNG
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

[m451.c](https://github.com/mariopartyrd/marioparty4/blob/main/src/REL/m451Dll/m451.c)
