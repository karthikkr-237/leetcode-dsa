int removeElement(int* nums, int numsSize, int val) {
    int freq = 0;
    for (int i = 0; i < numsSize; i++) {
        if (nums[i] == val) {
            freq++;
            nums[i] = 101;
        }
    }
    for (int i = 0; i < numsSize - 1; i++) {
        int min_ind = i;
        int temp;
        for (int j = i + 1; j < numsSize; j++) {
            if (nums[j] < nums[min_ind])
                min_ind = j;
        }
        temp = nums[i];
        nums[i] = nums[min_ind];
        nums[min_ind] = temp;
    }
    return numsSize - freq;
}