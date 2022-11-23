#include <iostream>
using namespace std;
typedef long long ll;
const ll mod=1e9+7;
int pri[50],idx;
ll ksm(ll a,ll b)
{
    ll res=1;
    while(b)
    {
        if(b&1) res=(ll)res*a%mod;
        a=(ll)a*a%mod;
        b>>=1;
    }
    return res;
}
ll mul(ll a,ll b)
{
    a%=mod,b%=mod;
    return a*b%mod;
}
void divide(int k)
{
    for(int i=2;i<=k/i;i++)
    {
        if(k%i==0){
            pri[idx++]=i;
            while(k%i==0) k/=i;
        }
    }
    if(k!=1) pri[idx++]=k;
}
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    int n,m;
    while(cin>>n>>m){
        idx=0;
    divide(m);
    ll inv2=ksm(2,mod-2),inv6=ksm(6,mod-2);
    ll ans=(mul(n,n+1)*inv2%mod+mul(mul(n,n+1),2*n+1)*inv6%mod)%mod;
    for(int i=1;i<(1<<idx);i++)
    {
        int s=0;
        ll t=1;
        for(int j=0;j<idx;j++)
        {
            if(i >> j&1)
            {
                if(t*pri[j]>n)
                {
                    t=-1;
                    break;
                }
                t*=pri[j];
                s++;
            }
        }
        if(t!=-1)
        {   ll cnt=n/t;
            if(s%2) ans-=(t*mul(cnt,cnt+1)%mod*inv2%mod+t*t%mod*mul(mul(cnt,cnt+1),2*cnt+1)%mod*inv6%mod)%mod;
            else ans+=(t*mul(cnt,cnt+1)%mod*inv2%mod+t*t%mod*mul(mul(cnt,cnt+1),2*cnt+1)%mod*inv6%mod)%mod;
            if(ans<0) ans=ans+mod;
        }
    }
    cout<<(ans+mod)%mod<<'\n';
    }
    return 0;
}