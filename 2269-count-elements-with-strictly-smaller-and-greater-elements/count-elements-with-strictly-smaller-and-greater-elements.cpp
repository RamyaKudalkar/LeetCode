class Solution {
public:
    int countElements(vector<int>& nums) {
        int small=INT_MAX,large=INT_MIN;
        for(int val:nums){
            small=min(val,small);
            large=max(val,large);
        }
        int cnt=0;
        for(int val:nums){
            if(val>small&&val<large)
            cnt++;
        }
        return cnt;
    }
};