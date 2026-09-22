class Solution {
public:
    vector<int> leftRightDifference(vector<int>& nums) {
        int TS=0;
        for(int val:nums)
            TS+=val;
        int LS=0;
        for(int i=0;i<nums.size();i++){
            int x=nums[i],RS=TS-LS-nums[i];
            nums[i]=abs(LS-RS);
            LS+=x;
        }
        return nums;
    }
};