class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        int i=0;
        for(int val:nums){
            if(val!=0){
                nums[i]=val;
                i++;
            }
        }
        for(int j=i;j<nums.size();j++)
            nums[j]=0;
    }
};