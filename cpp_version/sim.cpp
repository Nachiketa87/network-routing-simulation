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
            if(nxt == parent[curr]) continue;     
            if(dis + nxtdis < dist[nxt]){
                dist[nxt] = nxtdis + dis;
                parent[nxt] = curr;
                pq.push({dist[nxt],nxt});
            }
        }
    }
    return dist;
}

vector<int> constructpath(int src, int dst, vector<int>& parent){
    if(parent[dst] == -1) return {};
    int node = dst;
    vector<int> path = {dst};
    while(node != src){
        if(parent[node] == -1) return {}; 
        node = parent[node];
        path.push_back(node);
    }
    reverse(path.begin(), path.end());
    return path;
}

void sim(int src, int dst, int v, vector<vector<vector<int>>>& edges, queue<pair<int,int>>& que, int hops, int indx, int total){
    int table = que.front().first;
    vector<int> parent (v,-1);
    parent[src] = src;
    vector<int> dist = dijkstra(src,v,edges[table],parent);    
    vector<int> path = constructpath(src,dst,parent);
    
    int curr_pos = src, trigger = que.front().second, prev = 0;
    
    while(hops < trigger && indx < path.size()){
        int prev_node = path[indx-1];
        int curr_pos = path[indx];

        int edge_cost = -1;
        for(auto& e : edges[table]){
            if((e[0] == prev_node && e[1] == curr_pos) || 
               (e[0] == curr_pos && e[1] == prev_node)){
                edge_cost = e[2];
                break;
            }
        }

        if(edge_cost == -1){
            cout << " No edge found from " << prev_node << " to " << curr_pos << endl;
            return;
        }

        total += edge_cost;
        hops++; indx++;

        cout << "current cost incurred: " << edge_cost << endl;
        cout << "packet moved to: " << curr_pos 
             << " with a total cost of: " << total << endl;

        if(curr_pos == dst){
            cout << " Reached destination " << dst 
                 << " at total cost " << total << endl;
            return;
        }
    }
    que.pop();
    if(que.empty() || curr_pos == dst) return;
    sim(curr_pos,dst,v,edges,que,hops,1,total);

}

int main(){
    int src = 0, v = 5, dst = 3;
    vector<vector<vector<int>>> edges = {
        {{0,1,4},{0,2,8},{1,4,6},{2,3,2},{3,4,10},{1,2,1}},  
        {{0,1,4},{0,2,15},{1,4,6},{2,3,30},{3,4,10},{1,2,1}},
        {{0,1,4},{0,2,15},{1,4,12},{2,3,30},{3,4,5},{1,2,1}} 
    };
    queue<pair<int,int>> que;
    que.push({0,2});
    que.push({1,3});
    que.push({2,4});

    sim(src,dst,v,edges,que,0,1,0); 
}
