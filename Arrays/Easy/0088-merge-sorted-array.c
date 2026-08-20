void merge(int* nums1, int nums1Size, int m, int* nums2, int nums2Size, int n) {
    int i = 0, j = 0, k = 0;
    int arr[m + n];
    if (m == 0) {
        for (int i = 0; i < n; i++) {
            nums1[i] = nums2[i];
        }
    } else if (n == 0) {
        for (int a = 0; a < m + n; a++) {
            printf("%d", &nums1[a]);
        }
    } else {
        while (i < m && j < n) {
            if (nums1[i] < nums2[j])
                arr[k++] = nums1[i++];
            else
                arr[k++] = nums2[j++];
        }
        while (i < m)
            arr[k++] = nums1[i++];
        while (j < n)
            arr[k++] = nums2[j++];
        for (int l = 0; l < m + n; l++) {
            nums1[l] = arr[l];
        }
    }
}