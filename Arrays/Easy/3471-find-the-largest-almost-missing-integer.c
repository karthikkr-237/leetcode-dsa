int largestInteger(int* nums, int numsSize, int k) {
    
    int a[51] = {0};
    if (k < 1 || numsSize < k)
    {
        return -1;
    }
    if (numsSize > 50 || numsSize < 1) return -2;

    int flag = 1;

    for (int i = 0; i < numsSize; i++)
    {
        if (nums[i] > 50 || nums[i] < 0) flag = 0;
    }

    if (flag == 0)
    {
        return -1;
    }

    for (int i = 0; i < numsSize; i++)
    {
        a[nums[i]]++;
    }

    if (k == 1)
    {
        int highest = -1;

        for (int i = 0; i < numsSize; i++)
        {
            if (highest < nums[i] && a[nums[i]] == 1)
                highest = nums[i];
        }

        return highest;
    }
    else if (k == numsSize)
    {
        int highest = -1;

        for (int i = 0; i < numsSize; i++)
        {
            if (highest < nums[i])
                highest = nums[i];
        }

        return highest;
    }
    else if (k > 1 && k < numsSize)
    {
        if (a[nums[0]] == 1 && a[nums[numsSize - 1]] == 1)
        {
            if (nums[0] > nums[numsSize - 1])
                return nums[0];
            else
                return nums[numsSize - 1];
        } 
        else if (a[nums[0]] == 1 && a[nums[numsSize - 1]] != 1)
        {
            return nums[0];
        }
        else if (a[nums[0]] != 1 && a[nums[numsSize - 1]] == 1)
        {
            return nums[numsSize - 1];
        }
    }

    return -1;
}