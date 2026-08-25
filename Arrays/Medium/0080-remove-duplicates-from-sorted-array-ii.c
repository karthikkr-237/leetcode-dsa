int removeDuplicates(int* nums, int numsSize) {
    int write = 2;
    int i = 2;
    if (numsSize <= 2)
        return numsSize;
    while (i < numsSize) {
        if (nums[i] != nums[write - 2]) {
            nums[write++] = nums[i];
        }
        i++;
    }
    return write;
}