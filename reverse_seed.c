#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

#define A 16807
#define M 2147483647
#define A_INV 1407677000 // Modular inverse of A mod M

static inline uint32_t frandom(uint32_t param)
{
    int32_t rand2, rand3;

    rand2 = param / (uint32_t)0x1F31D;
    rand3 = param - (rand2 * 0x1F31D);
    param = rand2 * 0xB14;
    param =  param - rand3 * 0x41A7;
    return param;
}

FILE* outFile;

// Recursive reversal checker. Should simplify
int reverse_chain(uint32_t current_seed, int depth, int max_depth) {
    if (depth == max_depth) {
        return 1;
    }

    int32_t unmasked = -current_seed;
    
    // First reversal method
    int64_t prev1 = ((int64_t)A_INV * unmasked) % M;
    if (prev1 < 0) prev1 += 2 * M;
    if (frandom(prev1) == current_seed) {
        if (reverse_chain(prev1, depth + 1, max_depth)) {
            fprintf(outFile, "Reverse [%d]: 0x%08X\n", depth + 1, (uint32_t)prev1);

            return 1;
        }
    }

    // Second method with M offset
    int64_t prev2 = M + ((int64_t)A_INV * unmasked) % M;
    if (prev2 < 0) prev2 += 2 * M; // Probably not needed
    if (frandom(prev2) == current_seed) {
        if (reverse_chain(prev2, depth + 1, max_depth)) {
            fprintf(outFile, "Reverse [%d]: 0x%08X\n", depth + 1, (uint32_t)prev2);

            return 1;
        }
    }

    return 0;
}

// Valid initial seeds end with {EVEN_DIGIT}E
int main() {
    outFile = fopen("reverse_output.txt", "w");
    if (!outFile) {
        perror("Failed to open output file");
        return 1;
    }
    
    uint32_t seed = 0xAE398399; // 0x02F7EBEE after 3429 reverse rolls
    int success = reverse_chain(seed, 0, 3500);
    
    if (!success) {
        printf("No valid reverse path found.\n");
    } else {
        printf("Seed successfully reversed.\n");
    }
    fclose(outFile);

    return 0;
}
