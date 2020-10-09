#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <unordered_map>
#include <algorithm>

#define __int64 long long
typedef unsigned long long ull;
typedef unsigned int uint32;
typedef ull uint64;
typedef unsigned int uint;
#define _DWORD uint32
#define _QWORD uint64

__int64 seed;

void *read_file(char *fname, void *ptr)
{
    FILE *v3;  // rax
    FILE *v4;  // rbx
    size_t v5; // r13
    void *v6;  // rax
    void *v7;  // r12

    v3 = fopen(fname, "r");
    if (!v3)
    {
        puts("Cannot open file.");
        exit(1);
    }
    v4 = v3;
    if (!fread(ptr, 4uLL, 1uLL, v3))
    {
        puts("EOF unexpected.");
        exit(1);
    }
    v5 = *(unsigned int *)ptr;
    v6 = malloc(4 * v5);
    v7 = v6;
    if (!v6)
    {
        puts("Malloc error.");
        exit(1);
    }
    if (*(_DWORD *)ptr != fread(v6, 4uLL, v5, v4))
    {
        puts("EOF unexpected.");
        exit(1);
    }
    fclose(v4);
    return v7;
}

typedef struct{
    _DWORD index;
    _DWORD value;
    _DWORD member3;
    _QWORD jump_offset;
} node_t;

typedef enum{
    EXIT_FUNC = 1,
    COPY_PREV,
    STEP_BACK
} JUMP_STATUS;

const char *jump_status_to_char(JUMP_STATUS status){
    switch(status){
        case EXIT_FUNC:
            return "EXIT_FUNC";
        case STEP_BACK:
            return "STEP_BACK";
        case COPY_PREV:
            return "COPY_PREV";
    }

    return "NONE";
}

#ifdef DEBUG
template<typename ...Args>
	void my_print(Args...){

	}
	#define printf my_print
	#define puts my_print
#endif

#define DUMP (dump_structs(buffer, data_size + 1));
void dump_node(node_t *node){
    printf("%02u. | %02u [0x%x] %s\n",
           node->index,
           node->member3,
           node->value,
           jump_status_to_char(static_cast<JUMP_STATUS>(node->jump_offset))
    );
}

void dump_structs(node_t *data, unsigned int data_size){
    printf("\n");
    uint32 start;
    for(start = 0; start < data_size; start++){
        if(data[start].jump_offset != EXIT_FUNC){
            break;
        }
    }
    start = std::max(static_cast<uint32>(0), start-1);

    for(uint32 i = start; i < data_size; i++){
        dump_node(&data[i]);
    }
    printf("-------------------\n\n");
}

void visualize_incoming_data(uint32 *data, unsigned int data_size, uint32 current_index){
    printf("[");
    for(uint32 i = 0; i < data_size; i++){
        if(current_index == i){
            printf(">0x%x<, ", data[i]);
        }else{
            printf("0x%x, ", data[i]);
        }
    }
    printf("]\n");

    fflush(stdout);
}

uint32 crunch_data2(uint32 *data, uint data_size)
{
    uint32 return_value = 0;
    uint total_cells = data_size;
    uint32 data_indexer;
    node_t *next;
    auto *buffer = (node_t *)calloc(data_size + 1, sizeof(node_t));
    buffer[0].jump_offset = EXIT_FUNC;

    node_t *current = &buffer[0];
    while(true){
        data_indexer = current->index;

        if(data_indexer >= data_size){
            DUMP
            return_value = std::max(return_value, current->member3);
            printf("loop round finished with: %u (best: %u)\n", current->member3, return_value);

            data_indexer = data_size-1; //point at one before last

            step_back: ;
            int jump_to = current->jump_offset;
//			printf("we will %s\n", jump_status_to_char(static_cast<JUMP_STATUS>(jump_to)));
            current = &buffer[data_indexer];

            switch(jump_to){
                case EXIT_FUNC:
                    puts("successful exit");
                    goto exit;
                case COPY_PREV:
                    printf("\nCOPY_PREV\n");
                    printf("current points at: ");
                    dump_node(current);
                    goto copy_from_prev;
                case STEP_BACK:
                    data_indexer--;
                    goto step_back;
            }

            puts("ERROR!!!");
            exit(1);
        }

        if(data[data_indexer] < current->value){ // current < prev

            copy_from_prev: ;
            printf("copy from prev %d -> %d\n", current->index, current->index + 1);

            next = &buffer[current->index + 1];
            next->index = current->index + 1;
            next->value = current->value;
            next->member3 = current->member3;
            next->jump_offset = (current->value == 0) ? EXIT_FUNC : STEP_BACK;

            if(current->value == 0){
                printf("\n\n**************************\nCELL CLEARED\n");
                total_cells--;
            }
        }else{
            visualize_incoming_data(data, data_size, data_indexer);

            printf("copy from data[%d] -> %d\n", current->index, data_indexer + 1);

            next = &buffer[data_indexer + 1];
            next->index = data_indexer + 1;
            next->value = data[current->index];
            next->member3 = 1 + current->member3;
            next->jump_offset = COPY_PREV;

            DUMP
        }

        current = next;
    }

    return_value = -1;
    exit:
    free(buffer);
    return return_value;
}

#ifdef DEBUG
#undef printf
	#undef puts
#endif

uint32 crunch_data(uint32 *arr, uint n){
	uint32 *lis = new uint32[n];
    lis[0] = 1;    
  
    for (uint32 i = 1; i < n; i++ )  
    { 
        lis[i] = 1; 
        for (uint32 j = 0; j < i; j++ )   
            if ( arr[i] > arr[j] && lis[i] < lis[j] + 1)  
                lis[i] = lis[j] + 1;  
    } 
  
    uint32 r = *std::max_element(lis, lis+n);
	delete[] lis;
    return r; 
}

unsigned __int64 get_index()
{
    unsigned __int64 result; // rax
    int v1; // ecx

    result = seed % 0x3B9ACA07uLL;
    v1 = 8;
    do
    {
        result = (result * result) % 0x3B9ACA07;

        --v1;
    }
    while ( v1 );
    seed = result;
    return result;
}

void dump_data(uint32 *data, unsigned int data_size){
    printf("[");
    for(uint32 i = 0; i < data_size; i++){
        printf("%2u, ", data[i]);
    }
    printf("]\n");

    fflush(stdout);
}

int main(int argc, char *argv[])
{
    if(argc != 2){
        puts("my_cruncher data_file");
        return 1;
    }

    unsigned int data_size;
    uint32 *data;
    int loop_counter;
    unsigned __int64 ret;

    data = (uint32 *)read_file(argv[1], &data_size);
    loop_counter = 10;
    ret = 0LL;
    do
    {
        uint32 crunched_return = crunch_data(data, data_size);
        printf("return value: %u\n", crunched_return);

        ret = (crunched_return + 31 * ret) % 0x3B9ACA07;
        seed = crunched_return;
        uint inner_loop_counter = 5 * data_size;
       	// exit(0);

        // dump_data(data, data_size);
        do
        {
            uint id1 = (unsigned int)get_index() % data_size;
            uint id2 = get_index() % data_size;

            std::swap(data[id1], data[id2]);

            --inner_loop_counter;
        }
        while ( inner_loop_counter );
        // dump_data(data, data_size);

        puts("--------------------");

        --loop_counter;
    }
    while ( loop_counter );

    printf("ret: %llu\n", ret);
}