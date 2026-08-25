int majorityElement(int* nums, int numsSize) {
    int k = 1;
    int i = 1;
    int n = nums[0];
    if (numsSize == 1)
        return nums[0];
    while (i < numsSize) {
        if (k == 0) {
            n = nums[i];
            k = 1;
        } else if (nums[i] == n)
            k++;
        else
            k--;
        i++;
    }
    return n;
}