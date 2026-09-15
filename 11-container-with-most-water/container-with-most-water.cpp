class Solution {
public:
    int maxArea(vector<int>& height) {
        int maxWater=0,i=0,j=height.size()-1;
        while(i<j){
            int ht,w=j-i;
            if(height[i]<height[j]){
                ht=height[i];
                i++;
            }
            else{
                ht=height[j];
                j--;
            }
            int curWater=w*ht;
            if(curWater>maxWater)
                maxWater=curWater;
        }
        return maxWater;
    }
};