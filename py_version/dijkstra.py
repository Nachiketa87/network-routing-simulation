import heapq

def dijkstra(src,v,edges) -> list:
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
                heapq.heappush(pq,(dist[nxt],nxt))
    return dist

src = 0 
v = 5
edges = [[0, 1, 4], [0, 2, 8], [1, 4, 6], [2, 3, 2], [3, 4, 10]] 
dist = dijkstra(src,v,edges)

for i in range(len(dist)):
    print(f"{src} -> {i} = {dist[i]}")


