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
            if nxt == parent[curr]:
                continue
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

    events = []
    curr_path = []
    if prev_len != 1e7:
        curr_path.append(src)
        events.append({"events":"Fluctuations detected, table updated", "table":table, "at_node":src})

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
        if prev_len != 1e7:
            events.append({"event":"Major fluctuations observed, new trajectory", "path":path})
    else:
        path = rem
        cost = new_len
        events.append({"event":"Some minor fluctuations observed, resuming same path", "path":path})

    if not path:
        events.append({"event":"No path exists", "node":dst, "cost":None})
        return {"path": None, "cost": None, "events": events}
    
    print(f"Decided path: {path} with projected cost: {cost}")

    indx,curr_pos,prev_pos = 0,src,prev
    while hops < trigger and indx < len(path):
        if curr_pos == src:
            indx += 1
            hops += 1
            curr_pos = path[indx]
            total += dist[curr_pos]
            curr_path.append(curr_pos)
            events.append({"event":"packet arrived", "node":curr_pos, "cost":total})
            continue
        if curr_pos == dst:
            events.append({"event":"Arrived at destination", "node":dst, "cost":total})
            return {"path":curr_path, "cost":total, "events":events}
        
        indx += 1
        hops += 1
        prev_pos = curr_pos
        curr_pos = path[indx]
        total += dist[curr_pos] - dist[prev_pos]
        curr_path.append(curr_pos)
        events.append({"event":"packet arrived", "node":curr_pos, "cost":total})
    
    if curr_pos == dst:
        events.append({"event":"Arrived at destination", "node":dst, "cost":total})
        return {"path":curr_path, "cost":total, "events":events}
    if not que:
        events.append({"event":"Packet expired","node":curr_pos,"cost":total})
        return {"path":curr_path, "cost":total, "events":events}
    
    rem_pathlen = dist[dst] - dist[curr_pos]
    new_rem = []
    while indx < len(path):
        new_rem.append(path[indx])
        indx += 1
    print("coming trajectory of packet: ",new_rem)
    res = sim(curr_pos,v,dst,edges,que,hops,prev_pos,total,rem_pathlen,prev_tab_ind,new_rem)
   
    all_events = events + res["events"]
    all_paths = curr_path[:-1] + res["path"]
    return {"path":all_paths, "cost":res["cost"], "events": all_events}

if __name__ == "__main__":
    
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

    sol = sim(src,v,dst,edges,que,0,src,0)

    sol["path"].insert(0,src)
    print("path traversed: ",sol["path"])
    print("total cost observed: ",sol["cost"])
    print("Events chronology: ",sol["events"])





