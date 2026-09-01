int maxProfit(int* prices, int pricesSize) {
    if (pricesSize <= 1)
        return 0;
    int min_price = prices[0];
    int max_pro = 0;
    for (int i = 0; i < pricesSize; i++) {
        if (min_price > prices[i])
            min_price = prices[i];
        else if (max_pro < prices[i] - min_price)
            max_pro = prices[i] - min_price;
    }

    return max_pro;
}

