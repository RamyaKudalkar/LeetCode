class Solution {
public:
    int findMiddleIndex(vector<int>& nums) {
        int TS=0;
        for(int val:nums)
            TS+=val;
        int LS=0;
        for(int i=0;i<nums.size();i++){
            int RS=TS-LS-nums[i];
            if(LS==RS)
                return i;
            LS+=nums[i];
        }
        return -1;
    }
};