#ifndef __BACKEND_H
#define __BACKEND_H

#include <graal_isolate.h>
#include <jheaps_capi_types.h>

#if defined(__cplusplus)
extern "C" {
#endif

// library init

void jheaps_init();

void jheaps_cleanup();

int jheaps_is_initialized();

// error

void jheaps_error_clear_errno();

int jheaps_error_get_errno();

char *jheaps_error_get_errno_msg();

void jheaps_error_print_stack_trace();

// vm

void jheaps_vmLocatorSymbol();

int jheaps_AHeap_D_insert_key(void *, double, void**);

int jheaps_AHeap_L_insert_key(void *, long long int, void**);

int jheaps_AHeap_D_insert_key_value(void *, double, long long int, void**);

int jheaps_AHeap_L_insert_key_value(void *, long long int, long long int, void**);

int jheaps_AHeap_find_min(void *, void**);

int jheaps_AHeap_delete_min(void *, void**);

int jheaps_AHeap_size(void *, long long*);

int jheaps_AHeap_isempty(void *, int*);

int jheaps_AHeap_clear(void *);

int jheaps_AHeapHandle_D_get_key(void *, double*);

int jheaps_AHeapHandle_L_get_key(void *, long long*);

int jheaps_AHeapHandle_get_value(void *, long long*);

int jheaps_AHeapHandle_set_value(void *, long long int);

int jheaps_AHeapHandle_D_decrease_key(void *, double);

int jheaps_AHeapHandle_L_decrease_key(void *, long long int);

int jheaps_AHeapHandle_delete(void *);

int jheaps_DEAHeap_find_max(void *, void**);

int jheaps_DEAHeap_delete_max(void *, void**);

int jheaps_DEAHeapHandle_D_increase_key(void *, double);

int jheaps_DEAHeapHandle_L_increase_key(void *, long long int);

int jheaps_DEHeap_D_find_max(void *, double*);

int jheaps_DEHeap_L_find_max(void *, long long*);

int jheaps_DEHeap_D_delete_max(void *, double*);

int jheaps_DEHeap_L_delete_max(void *, long long*);

int jheaps_handles_destroy(void *);

int jheaps_Heap_create(heap_type_t, void**);

int jheaps_dary_Heap_create(heap_type_t, int, void**);

int jheaps_soft_Heap_create(heap_type_t, double, void**);

int jheaps_double_radix_Heap_create(heap_type_t, double, double, void**);

int jheaps_long_radix_Heap_create(heap_type_t, long long int, long long int, void**);

int jheaps_Heap_comparator_create(heap_type_t, void *, void**);

int jheaps_dary_Heap_comparator_create(heap_type_t, void *, int, void**);

int jheaps_soft_Heap_comparator_create(heap_type_t, void *, double, void**);

int jheaps_Heap_D_insert_key(void *, double);

int jheaps_Heap_L_insert_key(void *, long long int);

int jheaps_Heap_D_find_min(void *, double*);

int jheaps_Heap_L_find_min(void *, long long*);

int jheaps_Heap_D_delete_min(void *, double*);

int jheaps_Heap_L_delete_min(void *, long long*);

int jheaps_Heap_size(void *, long long*);

int jheaps_Heap_isempty(void *, int*);

int jheaps_Heap_clear(void *);

int jheaps_Heap_D_heapify(heap_type_t, double*, long long*, int, void**);

int jheaps_Heap_L_heapify(heap_type_t, long long*, long long*, int, void**);

int jheaps_dary_Heap_D_heapify(heap_type_t, int, double*, long long*, int, void**);

int jheaps_dary_Heap_L_heapify(heap_type_t, int, long long*, long long*, int, void**);

int jheaps_Heap_L_comparator_heapify(heap_type_t, void *, long long*, long long*, int, void**);

int jheaps_dary_Heap_L_comparator_heapify(heap_type_t, void *, int, long long*, long long*, int, void**);

int jheaps_MAHeap_D_meld(void *, void *);

int jheaps_MAHeap_L_meld(void *, void *);

int jheaps_MDEAHeap_D_meld(void *, void *);

int jheaps_MDEAHeap_L_meld(void *, void *);


#if defined(__cplusplus)
}
#endif
#endif
