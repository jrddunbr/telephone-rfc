#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

uint16_t checksum(void *data, size_t size) {
    uint32_t sum = 0;
    /* Cast to uint16_t for pointer arithmetic */
    uint16_t *data16 = data;

    while(size > 1) {
        sum += *data16++;
        size -= 2;
    }

    /* For the extraneous byte, if any: */
    if(size > 0) sum += *((uint8_t *) data16);

    /* Fold the sum as needed */
    while(sum >> 16) sum = (sum & 0xFFFF) + (sum >> 16);

    /* One's complement is binary inversion: */
    return ~sum;
}

int main() {
  char* data = "DOOT!";
  uint16_t result = checksum(data, 5);
  printf("%04x\n", result);
  return 0;
}
