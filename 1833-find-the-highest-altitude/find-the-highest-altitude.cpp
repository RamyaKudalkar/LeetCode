class Solution {
public:
    int largestAltitude(vector<int>& gain) {
        int curAlt=0,highAlt=0;
        for(int val:gain){
            curAlt+=val;
            if(curAlt>highAlt)
                highAlt=curAlt;
        }
        return highAlt;
    }
};