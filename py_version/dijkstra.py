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
        return None
    path = [node]
    while parent[node] != src:
        path.append(parent[node])
        node = parent[node]
    path.append(src)
    path.reverse()
    return path

def sim(src,v,dst,edges,que,hops,prev,total):
    table,trigger = que.popleft()    
    parent = [-1] * v
    parent[src] = src
    dist = dijkstra(src,v,edges[table],parent)
    path = constructpath(src,dst,parent)

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
    sim(curr_pos,v,dst,edges,que,hops,prev_pos,total)


src,v,dst = 0,5,3

edges = [
    [[0,1,4],[0,2,8],[1,4,6],[2,3,2],[3,4,10],[1,2,1]],
    [[0,1,4],[0,2,15],[1,4,6],[2,3,30],[3,4,10],[1,2,1]],
    [[0,1,4],[0,2,15],[1,4,12],[2,3,30],[3,4,5],[1,2,1]]
] 
que = deque()
que.append({0,2})
que.append({1,3})
que.append({2,7})

sim(src,v,dst,edges,que,0,src,0)





