class Solution {
public:
    int peakIndexInMountainArray(vector<int>& arr) {
        int srt=1,end=arr.size()-2;
        while(srt<=end){
            int mid=srt+(end-srt)/2;
            if(arr[mid-1]<arr[mid]&&arr[mid]>arr[mid+1])
                return mid;
            if(arr[mid-1]<arr[mid])
                srt=mid+1;
            else
                end=mid-1;
        }
        return -1;
    }
};