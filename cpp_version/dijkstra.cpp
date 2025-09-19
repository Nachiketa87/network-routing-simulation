#include<iostream>
#include<vector>
#include<queue>
using namespace std;

vector<int> dijkstra(int src, int v, vector<vector<int>>& edges){
    vector<vector<pair<int,int>>> adj(v);
    for(int i=0; i<edges.size(); i++){
        int curr = edges[i][0], dest = edges[i][1], dist = edges[i][2];
        adj[curr].push_back({dest,dist});
        adj[dest].push_back({curr,dist});
    }
    vector<int> dist(v,INT_MAX);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    pq.push({0,src}); dist[src] = 0;

    while(!pq.empty()){
        int dis = pq.top().first;
        int curr = pq.top().second;
        pq.pop();

        for(auto& iter: adj[curr]){
            int nxt = iter.first, nxtdis = iter.second;
            if(dist[nxt] > nxtdis + dis){
                dist[nxt] = nxtdis + dis;
                pq.push({dist[nxt],nxt});
            }
        }
    }
    return dist;
}

int main(){
    int src = 0, v = 5;
    vector<vector<int>> edges = {{0, 1, 4}, {0, 2, 8}, {1, 4, 6}, {2, 3, 2}, {3, 4, 10}};
    vector<int> dist = dijkstra(src,v,edges);
    cout << "[ \n";
    for(int i=0; i<dist.size(); i++){
       cout << src << "->" << i << '=' << dist[i] << endl;
    }
    cout << "]";
}