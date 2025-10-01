import heapq
from collections import deque

def dijkstra(src,v,edges,parent) -> list:
    adj = [[] for _ in range(v)]
    for u,dest,dist in edges:
        adj[u].append((dest,dist))
        adj[dest].append((u,dist))

    dist = [float('inf')] * v
    dist[src] = 0
    pq = []
    heapq.heappush(pq,(0,src))
    
    while len(pq) > 0:
        dis,curr = heapq.heappop(pq)
        for nxt,nxtdis in adj[curr]:
            if dis + nxtdis < dist[nxt]:
                dist[nxt] = dis + nxtdis
                parent[nxt] = curr
                heapq.heappush(pq,(dist[nxt],nxt))
    return dist

def constructpath(src,node,parent):
    if parent[node] == -1:
        print()
        return None
    path = [node]
    while parent[node] != src:
        path.append(parent[node])
        node = parent[node]
    path.append(src)
    path.reverse()
    return path

def deltalen(prev_pathlen,new_pathlen) -> bool:
    if new_pathlen == 0: return True
    if new_pathlen > 1.2 * prev_pathlen: return True
    if new_pathlen < 0.8 * prev_pathlen: return True
    return False

def sim(src,v,dst,edges,que,hops,prev,total,prev_len=1e7,prev_tab_ind=0,rem=[]):
    table,trigger = que.popleft()    
    parent = [-1] * v
    parent[src] = src
    dist = dijkstra(src,v,edges[table],parent)
    
    new_len = 0
    if(table > 0):
        n,cur,nxt = len(edges[table]),0,1
        while nxt < len(rem):
            for i in range(n):
                if (rem[cur] == edges[table][i][0] and rem[nxt] == edges[table][i][1]) or (rem[cur] == edges[table][i][1] and rem[nxt] == edges[table][i][0]):
                    new_len += edges[table][i][2]
                    print(f"new distance between node {rem[cur]} and node {rem[nxt]} is {edges[table][i][2]}")
                    break
            cur += 1
            nxt += 1
    
    print(f"previous length of old path: {prev_len} changed with new length of old path: {new_len}")
    use_currtable = deltalen(prev_len,new_len)

    print("curr_table decision is:" ,use_currtable)
    path,cost = [],0
    if use_currtable:
        prev_tab_ind = table
        path = constructpath(src,dst,parent)
        cost = dist[dst]
    else:
        path = rem
        cost = new_len

    if not path:
        print(f"No path exists between {src} and {dst}")
        return
    
    print(f"Decided path: {path} with projected cost: {cost}")

    indx,curr_pos,prev_pos = 0,src,prev
    while hops < trigger and indx < len(path):
        if curr_pos == src:
            indx += 1
            hops += 1
            curr_pos = path[indx]
            total += dist[curr_pos]
            print(f"packet arrived at node: {curr_pos} with total cost at: {total}")
            continue
        if curr_pos == dst:
            print(f"packet reach destination node: {dst} with total cost of {total}")
            return
        indx += 1
        hops += 1
        prev_pos = curr_pos
        curr_pos = path[indx]
        total += dist[curr_pos] - dist[prev_pos]
        print(f"packet arrived at node: {curr_pos} with total cost at: {total}")
    
    if curr_pos == dst:
        print(f"packet reach destination node: {dst} with total cost of {total}")
        return
    if not que:
        print(f"packet expired at node: {curr_pos}")
        return
    rem_pathlen = dist[dst] - dist[curr_pos]
    new_rem = []
    while indx < len(path):
        new_rem.append(path[indx])
        indx += 1
    print("coming trajectory of packet: ",new_rem)
    sim(curr_pos,v,dst,edges,que,hops,prev_pos,total,rem_pathlen,prev_tab_ind,new_rem)


src,v,dst = 0,5,3

edges = [
    [[0,1,4],[0,2,8],[1,4,6],[2,3,2],[3,4,10],[1,2,1]],
    [[0,1,4],[0,2,15],[1,4,6],[2,3,30],[3,4,10],[1,2,1]],
    [[0,1,4],[0,2,15],[1,4,12],[2,3,30],[3,4,5],[1,2,1]]
] 
que = deque()
que.append((0,2))
que.append((1,3))
que.append((2,7))

sim(src,v,dst,edges,que,0,src,0,1e7,0,[])





