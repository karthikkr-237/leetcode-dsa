int removeDuplicates(int* nums, int numsSize) {
    int freq[201] = {0};
    int count = 0;
    int shift = 0;
    int write = 0;
    if (numsSize == 0)
        return 0;
    for (int i = 0; i < numsSize; i++) {
        shift = nums[i] + 100;
        freq[shift]++;
        if (freq[shift] == 1) {
            count++;
            nums[write++] = nums[i];
        }
    }
    return count;
}
