class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int maxProfit=0,bestBuy=prices[0];
        for(int i=1;i<prices.size();i++){
            if(prices[i]>bestBuy){
                if(prices[i]-bestBuy>maxProfit)
                    maxProfit=prices[i]-bestBuy;
            }
            else if(prices[i]<bestBuy)
                bestBuy=prices[i];
        }
        return maxProfit;
    }
};