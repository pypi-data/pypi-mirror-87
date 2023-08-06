#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <jheaps_capi_types.h>
#include <jheaps_capi.h>

int main() { 
    graal_isolate_t *isolate = NULL;
    graal_isolatethread_t *thread = NULL;

    if (graal_create_isolate(NULL, &isolate, &thread) != 0) {
        fprintf(stderr, "graal_create_isolate error\n");
        exit(EXIT_FAILURE);
    }

    void *heap;
    jheaps_capi_Heap_create(thread, HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING, &heap);
    assert(jheaps_capi_error_get_errno(thread) == 0);

    void *handle1;
    jheaps_capi_AHeap_D_insert_key_value(thread, heap, 15.5, 15, &handle1);
    assert(jheaps_capi_error_get_errno(thread) == 0);
    void *handle2;
    jheaps_capi_AHeap_D_insert_key_value(thread, heap, 17.5, 17, &handle2);
    void *handle3;
    jheaps_capi_AHeap_D_insert_key_value(thread, heap, 20.5, 20, &handle3);
    void *handle4;
    jheaps_capi_AHeap_D_insert_key_value(thread, heap, 5.5, 5, &handle4);

    assert(jheaps_capi_error_get_errno(thread) == 0);

    long long size;
    jheaps_capi_AHeap_size(thread, heap, &size);
    assert (size == 4);

    void *handle4_0;
    jheaps_capi_AHeap_find_min(thread, heap, &handle4_0);
    assert(jheaps_capi_error_get_errno(thread) == 0);
    double key;
    jheaps_capi_AHeapHandle_D_get_key(thread, handle4_0, &key);
    assert(key == 5.5);

    long long value;
    jheaps_capi_AHeapHandle_get_value(thread, handle4_0, &value);
    assert(value == 5);
    jheaps_capi_AHeapHandle_set_value(thread, handle4_0, 105);
    jheaps_capi_AHeapHandle_get_value(thread, handle4_0, &value);
    assert(value == 105);

    // test delete
    jheaps_capi_AHeapHandle_delete(thread, handle4_0);
    assert(jheaps_capi_error_get_errno(thread) == 0);
    jheaps_capi_handles_destroy(thread, handle4_0);
    jheaps_capi_AHeap_size(thread, heap, &size);
    assert (size == 3);

    void *handle1_0;
    jheaps_capi_AHeap_find_min(thread, heap, &handle1_0);
    assert(jheaps_capi_error_get_errno(thread) == 0);
    jheaps_capi_AHeapHandle_D_get_key(thread, handle1_0, &key);
    assert(key == 15.5);
    jheaps_capi_handles_destroy(thread, handle1_0);

    // test delete min
    jheaps_capi_AHeap_delete_min(thread, heap, &handle1_0);
    assert(jheaps_capi_error_get_errno(thread) == 0);
    jheaps_capi_AHeapHandle_D_get_key(thread, handle1_0, &key);
    assert(key == 15.5);
    jheaps_capi_handles_destroy(thread, handle1_0);

    void *handle2_0;
    jheaps_capi_AHeap_find_min(thread, heap, &handle2_0);
    assert(jheaps_capi_error_get_errno(thread) == 0);
    jheaps_capi_AHeapHandle_D_get_key(thread, handle2_0, &key);
    assert(key == 17.5);
    jheaps_capi_AHeapHandle_D_decrease_key(thread, handle2_0, 16.5);
    jheaps_capi_AHeapHandle_D_get_key(thread, handle2_0, &key);
    assert(key == 16.5);
    jheaps_capi_handles_destroy(thread, handle2_0);


    jheaps_capi_handles_destroy(thread, handle1);
    jheaps_capi_handles_destroy(thread, handle2);
    jheaps_capi_handles_destroy(thread, handle3);
    jheaps_capi_handles_destroy(thread, handle4);
    assert(jheaps_capi_error_get_errno(thread) == 0);

    jheaps_capi_handles_destroy(thread, heap);
    assert(jheaps_capi_error_get_errno(thread) == 0);

    if (graal_detach_thread(thread) != 0) {
        fprintf(stderr, "graal_detach_thread error\n");
        exit(EXIT_FAILURE);
    }

    return EXIT_SUCCESS;
}
