from dijkstra import src,dst,v,sim,edges,que
from rich.console import Console
from rich.table import Table
import networkx as nx
import matplotlib.pyplot as plt

def DisplayEvents(events):
    table = Table(title="Packet event tracer")
    table.add_column("Step",justify="left",style="cyan")
    table.add_column("Event",justify="center",style="magenta")
    table.add_column("Details",justify="right",style="green")

    for step,Event in enumerate(events,start=1):
        evnt = Event.get("event","unknown")
        details = ", ".join([f"{k}={v}" for k,v in Event.items() if k != "event"])
        table.add_row(str(step),evnt,details)

    console = Console()
    console.print(table)

def GraphVisualisation(events,edges,path):
    g = nx.Graph()
    for u,v,w in edges[0]:
        g.add_edge(u,v,weight=w,width=3)
    
    pos = nx.spring_layout(g)
    nx.draw(g,pos,with_labels=True,node_color="lightblue",node_size=700,font_size=10, width=[g[u][v].get("width", 1) for u, v in g.edges()])
    nx.draw_networkx_edge_labels(g,pos,edge_labels=nx.get_edge_attributes(g,"weight"))
    
    prev, prev_pathlis = src, list(zip(path,path[1:]))
    for i,Event in enumerate(events,start=1):
        evnt = Event["event"]

        if evnt == "packet arrived" or evnt == "Packet start from source":
            node = Event["node"]
            if node == src:
                nx.draw_networkx_nodes(g,pos,nodelist=[node],node_color="magenta",node_size=850)
            elif prev == src:
                nx.draw_networkx_nodes(g,pos,nodelist=[node],node_color="red",node_size=850)
                nx.draw_networkx_edges(g,pos,edgelist=[(src,node)],edge_color="black",width=3)
                prev = node
            else:
                nx.draw_networkx_nodes(g,pos,nodelist=[node],node_color="red",node_size=850)
                nx.draw_networkx_nodes(g,pos,nodelist=[prev],node_color="lightblue",node_size=700)
                nx.draw_networkx_edges(g,pos,edgelist=[(prev,node)],edge_color="black",width=3)
                prev = node
            plt.pause(2)

        elif "trajectory" in evnt or "resuming" in evnt:
            pathlis = Event["path"]
            edgelis = list(zip(pathlis,pathlis[1:]))
            if edgelis != prev_pathlis:
                nx.draw_networkx_edges(g,pos,edgelist=prev_pathlis,edge_color="black",width=3)
            if pathlis:
                nx.draw_networkx_edges(g,pos,edgelist=edgelis,edge_color="green",width=3)
            prev_pathlis = edgelis
            plt.pause(2)
        
        elif evnt == "Arrived at destination":
            node = Event["node"]
            nx.draw_networkx_nodes(g,pos,nodelist=[node],node_color="gold",node_size=850)
            plt.pause(2)
    
    plt.show()

res = sim(src,v,dst,edges,que,0,src,0)
events = res["events"]
paths = res["path"]
total = res["cost"]

DisplayEvents(events)

GraphVisualisation(events,edges,paths)