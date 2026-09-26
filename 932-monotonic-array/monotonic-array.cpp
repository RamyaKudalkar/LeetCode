class Solution {
public:
    bool isMonotonic(vector<int>& nums) {
        bool isincreasing=true,isdecreasing=true;
        for(int i=0;i<nums.size()-1;i++){
            if(nums[i]<nums[i+1])
                isdecreasing=false;
            else if(nums[i]>nums[i+1])
                isincreasing=false;
            if(!isincreasing&&!isdecreasing)
                return false;
        }
        return true;
    }
};