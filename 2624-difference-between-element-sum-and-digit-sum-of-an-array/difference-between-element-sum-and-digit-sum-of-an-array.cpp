class Solution {
public:
    int differenceOfSum(vector<int>& nums) {
        int eleSum=0,digitSum=0;
        for(int val:nums){
            eleSum+=val;
            while(val>0){
                digitSum+=val%10;
                val/=10;
            }
        }
        return eleSum-digitSum;
    }
};