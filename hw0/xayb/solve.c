#include <stdio.h>

void game_logic(char* param) {
    for(int i = 0; i < 0x2e; i++)
    {
        param[i] ^= 0xf2;
    }
    param[0x2e] = '\0';
    printf("%s\n", param);
}

int main() {
    void* arr[10] = {
        0x9dc2a589b5b3beb4,
        0xa7c2abada5b3a5ad,
        0xb99184beadc2c7ad,
        0xad9a91869385ad8b,
        0xcbc6a4b0beadad84,
        0x8f95b7b0a2a6,
    };

    game_logic(&arr);
}

// FLAG{W0o_WAW_Y0U_50_LvcKy_watch_v__LBV49TPBEg}