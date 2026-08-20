int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    int* ptr;
    ptr = (int*)malloc(2 * sizeof(int));
    if (ptr == NULL) {
        *returnSize = 0;
        return NULL;
    }
    for (int i = 0; i < numsSize; i++) {
        for (int j = i + 1; j < numsSize; j++) {
            if (nums[i] + nums[j] == target) {
                ptr[0] = i;
                ptr[1] = j;
                *returnSize = 2;
                return ptr;
            }
        }
    }
    *returnSize = 0;
    free(ptr);
    return NULL;
}