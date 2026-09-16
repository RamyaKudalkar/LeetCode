class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int cnt=0,majEle;
        for(int val:nums){
            if(cnt==0)
                majEle=val;
            if(val==majEle)
                cnt++;
            else
                cnt--;
        }
        return majEle;
    }
};