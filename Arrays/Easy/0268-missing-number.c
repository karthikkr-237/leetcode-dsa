int missingNumber(int* nums, int numsSize) {
    int sum_range, sum = 0;
    sum_range = numsSize * (numsSize + 1) / 2;
    for (int i = 0; i < numsSize; i++) {
        sum += nums[i];
    }
    return sum_range - sum;
}