bool sumGame(char* num) {
    int numlen = strlen(num);
    int f_q = 0;
    int l_q = 0;
    for (int i = 0; i < numlen / 2; i++) {
        if (num[i] == '?')
            f_q++;
    }
    for (int i = numlen / 2; i < numlen; i++) {
        if (num[i] == '?')
            l_q++;
    }
    int s_f = 0;
    int s_l = 0;

    for (int i = 0; i < numlen / 2; i++) {
        if (num[i] >= '0' && num[i] <= '9') {
            s_f += ((int)num[i] - '0');
        }
    }
    for (int i = numlen / 2; i < numlen; i++) {
        if (num[i] >= '0' && num[i] <= '9')
            s_l += ((int)num[i] - '0');
    }
    int d_q = l_q - f_q;
    int d_s = s_f - s_l;
    if (2 * d_s == 9 * d_q)
        return false;
    else
        return true;
}
