#include<iostream>
#include<vector>
#include<queue>
#include<algorithm>
using namespace std;

vector<int> dijkstra(int src, int v, vector<vector<int>>& edges, vector<int>& parent){
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
            if(dis + nxtdis < dist[nxt]){
                dist[nxt] = nxtdis + dis;
                parent[nxt] = curr;
                pq.push({dist[nxt],nxt});
                cout << curr << "->" << nxt << endl;
            }
        }
    }
    return dist;
}

vector<int> constructpath(int src, int dst, vector<int>& parent){
    if(parent[dst] == -1) return {};
    int node = dst;
    vector<int> path = {dst};
    while(parent[node] != src){
        path.push_back(parent[node]);
        node = parent[node];
    }
    path.push_back(src);
    reverse(path.begin(),path.end());
    return path;
}

int main(){
    int src = 0, v = 5, dst = 3;
    vector<vector<int>> edges = {{0, 1, 4}, {0, 2, 8}, {1, 4, 6}, {2, 3, 2}, {3, 4, 10}};
    vector<int> parent(v);
    parent[src] = src;
    
    vector<int> dist = dijkstra(src,v,edges,parent);
    cout << "[ \n";
    for(int i=0; i<dist.size(); i++){
       cout << src << "->" << i << '=' << dist[i] << endl;
    }
    cout << "]";
    
    cout << "[ ";
    vector<int> path = constructpath(src,dst,parent);
    for(int pt: path){
        cout << pt << " ";
    }
    cout << "]";
}