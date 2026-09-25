class Solution {
public:
    bool search(vector<int>& nums, int target) {
        int srt=0,end=nums.size()-1;
        while(srt<=end){
            int mid=srt+(end-srt)/2;
            if(nums[mid]==target)
                return true;
            if(nums[srt]==nums[mid]&&nums[mid]==nums[end]){
                srt++;
                end--;
            }
            else if(nums[srt]<=nums[mid]){
                if(nums[srt]<=target&&target<nums[mid])
                    end=mid-1;
                else
                    srt=mid+1;
            }
            else{
                if(nums[mid]<target&&target<=nums[end])
                    srt=mid+1;
                else
                    end=mid-1;
            }
        }
        return false;
    }
};