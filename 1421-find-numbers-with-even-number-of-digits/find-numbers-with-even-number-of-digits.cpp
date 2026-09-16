class Solution {
public:
    int findNumbers(vector<int>& nums) {
        int even=0;
        for(int val:nums){
            int cnt=0;
            while(val>0){
                cnt++;
                val/=10;
            }
            if(cnt%2==0)
                even++;
        }
        return even;
    }
};