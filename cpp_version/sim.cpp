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
    cout << "dijsktra function executed" << endl;
    return dist;
}

vector<int> constructpath(int src, int dst, vector<int>& parent){
    if(parent[dst] == -1){
        cout << "constructpath: no parent found for dst " << dst << endl;
        return {};
    }
    int node = dst;
    vector<int> path = {dst};
    while(node != src){
        if(parent[node] == -1) return {}; 
        node = parent[node];
        path.push_back(node);
    }
    reverse(path.begin(), path.end());
    cout << "constructpath function executed" << endl;
    return path;
}

bool deltalen(int prev_pathlen, int new_pathlen){
    if(new_pathlen == 0) return true;
    if(new_pathlen > 1.2 * prev_pathlen) return true;
    if(new_pathlen < 0.8 * prev_pathlen) return true;
    return false;
}

void sim(int src, int dst, int v, vector<vector<vector<int>>>& edges, queue<pair<int,int>>& que, int hops, int prev, 
    int total, int prev_len, int prev_tab_ind, vector<int>& rem){
    int table = que.front().first;
    int trigger = que.front().second;

    vector<int> parent (v,-1);
    parent[src] = src;
    vector<int> dist = dijkstra(src,v,edges[table],parent);
    
    int new_len = 0;
    if(table > 0){
        int n = edges[table].size(), cur = 0, nxt = 1; 
        while(nxt < rem.size()){
            for(int i=0; i<n; i++){
                if(rem[cur] == edges[table][i][0] && rem[nxt] == edges[table][i][1] ||
                rem[cur] == edges[table][i][1] && rem[nxt] == edges[table][i][0]){
                    new_len += edges[table][i][2];
                    cout << "new distance between node " << rem[cur] << " and node " << rem[nxt] << " is: " << edges[table][i][2] << endl;
                    break;   
                }
            }
            cur++; nxt++;
        }
    }
    cout << "prev length of old path: " << prev_len << " and new length of old path: " << new_len << endl;
    bool use_currtable = deltalen(prev_len,new_len);

    cout << "use_currtable: " << use_currtable 
     << " | table: " << table 
     << " | prev_tab_ind: " << prev_tab_ind << endl;


    vector<int> path; 
    if(use_currtable){
        prev_tab_ind = table;
        path = constructpath(src,dst,parent);
    }
    else{
        dist = dijkstra(src,v,edges[prev_tab_ind],parent);
        path = constructpath(src,dst,parent);
    }
    cout << "prev_tab_ind value: " << prev_tab_ind << endl;
    if(path.empty()){
        cout << "No path exists between: " << src << " and " << dst << endl;
        return;
    }

    int curr_pos = src, prev_pos = prev, indx = 0;
    while(hops < trigger && indx < path.size()){
        if(curr_pos == src){
            indx++; hops++;
            curr_pos = path[indx];
            total += dist[curr_pos];
            cout << "packet arrived at: " << curr_pos << " from: " << src << " with total cost of: " << total << endl;
            continue;
        }
        if(curr_pos == dst){
            cout << "reached destination: " << dst << " with total cost: " << total;
            return;
        }          
        indx++; hops++;
        prev_pos = curr_pos;
        curr_pos = path[indx];
        total += dist[curr_pos] - dist[prev_pos];
        cout << "packet arrived at: " << curr_pos << " from: " << prev_pos << " with total cost of: " << total << endl;
    }
    if(curr_pos == dst){
        cout << "reached destination: " << dst << " at total cost: " << total;
        return;
    }
    que.pop();
    if(que.empty()){
        cout << "packet expired at: " << curr_pos;
        return;
    }
    int rem_pathlen = dist[dst] - dist[curr_pos];
    cout << "rem_pathlen: " << rem_pathlen << " and index: " << indx << endl;

    vector<int> new_rem; 
    cout << "path's remaining nodes: ";
    while(indx < path.size()){
        new_rem.push_back(path[indx]);
        cout << path[indx] << " ";
        indx++;
    }
    cout << endl;
    sim(curr_pos,dst,v,edges,que,hops,prev_pos,total,rem_pathlen,prev_tab_ind,new_rem);
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
    que.push({2,7});
    vector<int> empty = {};

    sim(src,dst,v,edges,que,0,src,0,1e7,0,empty); 
}
