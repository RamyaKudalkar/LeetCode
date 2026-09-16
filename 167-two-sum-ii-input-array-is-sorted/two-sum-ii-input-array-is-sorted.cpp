class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int i=0,j=numbers.size()-1;
        while(i<j){
            int pairSum=numbers[i]+numbers[j];
            if(pairSum==target)
                return {i+1,j+1};
            if(pairSum<target)
                i++;
            else
                j--;
        }
        return {};
    }
};