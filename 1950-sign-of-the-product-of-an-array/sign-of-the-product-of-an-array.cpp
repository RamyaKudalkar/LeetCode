class Solution {
public:
    int arraySign(vector<int>& nums) {
        int sign=1;
        for(int val:nums){
            if(val==0)
                return 0;
            if(val<0)
                sign*=-1;
        }
        return sign;
    }
};