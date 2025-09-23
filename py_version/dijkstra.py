import heapq

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

src,v,dst = 0,5,3

edges = [[0, 1, 4], [0, 2, 8], [1, 4, 6], [2, 3, 2], [3, 4, 10]] 
parent = [-1] * v
parent[src] = src
dist = dijkstra(src,v,edges,parent)

for i in range(len(dist)):
    print(f"{src} -> {i} = {dist[i]}")

path = constructpath(src,dst,parent)
print(f"path from {src} to {dst}: ")
print(f"{path} with a cost of {dist[dst]}")




