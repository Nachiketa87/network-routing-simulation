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

def GraphVisualisation(events,edges):
    g = nx.Graph()
    for u,v,w in edges[0]:
        g.add_edge(u,v,weight=w)
    
    pos = nx.spring_layout(g)
    nx.draw(g,pos,with_labels=True,node_color="lightblue",node_size=700,font_size=10)
    nx.draw_networkx_edge_labels(g,pos,edge_labels=nx.get_edge_attributes(g,"weight"))
    
    for i,Event in enumerate(events,start=1):
        evnt = Event["event"]

        if evnt == "packet arrived":
            node = Event["node"]
            nx.draw_networkx_nodes(g,pos,nodelist=[node],node_color="red",node_size=850)
            plt.pause(2)

        elif "trajectory" in evnt or "resuming" in evnt:
            pathlis = Event["path"]
            edgelis = list(zip(pathlis,pathlis[1:]))
            if pathlis:
                nx.draw_networkx_edges(g,pos,edgelist=edgelis,edge_color="green",width=3)
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
print(type(events))

GraphVisualisation(events,edges)