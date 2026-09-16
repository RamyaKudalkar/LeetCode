class Solution {
public:
    vector<int> replaceElements(vector<int>& arr) {
        int great=-1;
        for(int i=arr.size()-1;i>=0;i--){
            int cur=arr[i];
            arr[i]=great;
            great=max(cur,great);
        }
        return arr;
    }
};