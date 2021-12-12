#include <cstdio>
#include <cstdlib>

const unsigned int HALF_SIZE = 100000;
const unsigned int ARRAY_SIZE = HALF_SIZE * 2;

int array[ARRAY_SIZE];

int main() {

    for (int i = 0; i < ARRAY_SIZE; i++) {
        printf("Initializing array[%u]\n", i);
        array[i] = 0;
    }

    for (int i = 0; i < HALF_SIZE; i++) {
        printf("Setting array[%u]\n", i);
        array[i] = i;
    }

    for (int i = 0; i < HALF_SIZE; i++) {
        printf("Coping data from array[%u] to array[%u]\n", i, i + HALF_SIZE);
        array[i + HALF_SIZE] = array[i];
    }

    return 0;
}