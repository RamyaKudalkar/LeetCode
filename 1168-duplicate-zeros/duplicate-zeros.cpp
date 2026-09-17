class Solution {
public:
    void duplicateZeros(vector<int>& arr) {
        int n=arr.size(),cnt=0;
        for(int val:arr){
            if(val==0)
                cnt++;
        }
        int i=n-1,j=n+cnt-1;
        while(i<j){
            if(j<n)
                arr[j]=arr[i];
            if(arr[i]==0){
                j--;
                if(j<n)
                    arr[j]=0;
            }
            i--;
            j--;
        }
    }
};