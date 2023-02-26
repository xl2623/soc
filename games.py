import networkx as nx
import matplotlib.pyplot as plt
from statistics import median


class Player:
    def __init__(self, resource, port, vp, dev, roads, cities, settlements):
        self.resource = resource
        self.port = port
        self.vp = vp
        self.dev = dev
        self.roads = roads
        self.cities = cities
        self.settlement = settlements

class Game:
    def __init__(self):
        # create a 3 by 5 hex lattice graph
        G = nx.hexagonal_lattice_graph(3,5)
        # add necessary nodes and edges to form catan map
        positions = nx.get_node_attributes(G,'pos')
        deltay =  positions[(2, 7)][1]-positions[(2, 6)][1]
        deltax = positions[(2, 7)][0]-positions[(1, 7)][0]
        G.add_node((2, 8), pos=(positions[(2, 6)][0], positions[(2, 7)][1]+deltay))
        G.add_edge((2, 7), (2, 8))
        G.add_node((3, 8), pos=(positions[(3, 6)][0], positions[(3, 7)][1]+deltay))
        G.add_edge((3, 7), (3, 8))
        G.add_edge((2, 8), (3, 8))
        positions = nx.get_node_attributes(G,'pos')
        G.add_node((1, -1), pos=(positions[(1, 1)][0], positions[(1, 0)][1]-deltay))
        G.add_edge((1, 0), (1, -1))
        G.add_node((2, -1), pos=(positions[(2, 1)][0], positions[(2, 0)][1]-deltay))
        G.add_edge((2, 0), (2, -1))
        G.add_edge((1, -1), (2, -1))
        positions = nx.get_node_attributes(G,'pos')
        G.add_node((3, -1), pos=(positions[(3, 1)][0], positions[(3, 0)][1]-deltay))
        G.add_edge((3, 0), (3, -1))
        G.add_node((4, -1), pos=(positions[(4, 1)][0], positions[(4, 0)][1]-deltay))
        G.add_edge((4, 0), (4, -1))
        G.add_edge((3, -1), (4, -1))
        positions = nx.get_node_attributes(G,'pos')
        G.add_node((2, -2), pos=(positions[(2, 0)][0], positions[(2, -1)][1]-deltay))
        G.add_edge((2, -2), (2, -1))
        G.add_node((3, -2), pos=(positions[(3, 0)][0], positions[(3, -1)][1]-deltay))
        G.add_edge((3, -1), (3, -2))
        G.add_edge((2, -2), (3, -2))
        positions = nx.get_node_attributes(G,'pos')
        cycle_basis = nx.minimum_cycle_basis(G)

        i = 2000
        for edge in list(G.edges):
            x = (positions[edge[0]][0]+positions[edge[1]][0])/2
            y = (positions[edge[1]][1]+positions[edge[0]][1])/2
            G.add_node(i, pos=(x, y), Type='Edge')
            G.add_edge(edge[0], i)
            G.add_edge(edge[1], i)
            G.remove_edge(edge[0], edge[1])
            i = i+1

        # Add nodes for the tiles
        for base in cycle_basis:
            new_tile = i
            x = []
            y = []
            for node in base:
                x.append(positions[node][0])
                y.append(positions[node][1])
            x = median(x)
            y = median(y)
            G.add_node(new_tile, pos=(x,y),node_shape='s', Type='Tiles')
            for node in base:
                G.add_edge(node, new_tile)
            i = i+1

        # add port
        base1 = (1, 7)
        base2 = (2, 7)
        G.add_node(3000, pos=((positions[base1][0]+positions[base2][0])/2, positions[base2][1]+deltay), Type='Port')
        G.add_edge(base1, 3000)
        G.add_edge(base2, 3000)

        base1 = (3, 7)
        base2 = (4, 7)
        G.add_node(3001, pos=((positions[base1][0]+positions[base2][0])/2, positions[base2][1]+deltay), Type='Port')
        G.add_edge(base1, 3001)
        G.add_edge(base2, 3001)
        
        base1 = (0, 6)
        base2 = (0, 5)
        G.add_node(3002, pos=(positions[base1][0]-deltax, positions[base1][1]), Type='Port')
        G.add_edge(base1, 3002)
        G.add_edge(base2, 3002)

        base1 = (5, 6)
        base2 = (5, 5)
        G.add_node(3003, pos=(positions[base1][0]+deltax, positions[base1][1]), Type='Port')
        G.add_edge(base1, 3003)
        G.add_edge(base2, 3003)

        base1 = (0, 3)
        base2 = (0, 2)
        G.add_node(3004, pos=(positions[base2][0]-deltax, positions[base2][1]), Type='Port')
        G.add_edge(base1, 3004)
        G.add_edge(base2, 3004)

        base1 = (5, 3)
        base2 = (5, 2)
        G.add_node(3005, pos=(positions[base2][0]+deltax, positions[base2][1]), Type='Port')
        G.add_edge(base1, 3005)
        G.add_edge(base2, 3005)

        base1 = (1, 0)
        base2 = (1, -1)
        G.add_node(3006, pos=(positions[base2][0]-deltax, positions[base2][1]), Type='Port')
        G.add_edge(base1, 3006)
        G.add_edge(base2, 3006)

        base1 = (4, 0)
        base2 = (4, -1)
        G.add_node(3007, pos=(positions[base2][0]+deltax, positions[base2][1]), Type='Port')
        G.add_edge(base1, 3007)
        G.add_edge(base2, 3007)

        base1 = (2, -2)
        base2 = (3, -2)
        G.add_node(3008, pos=((positions[base1][0]+positions[base2][0])/2, positions[base2][1]-deltay), Type='Port')
        G.add_edge(base1, 3008)
        G.add_edge(base2, 3008)

        # Draw the graph
        # extract nodes with specific setting of the attribute
        tile_nodes = [n for (n,ty) in \
            nx.get_node_attributes(G,'Type').items() if ty == 'Tiles']
        edge_nodes = [n for (n,ty) in \
            nx.get_node_attributes(G,'Type').items() if ty == 'Edge']
        port_nodes = [n for (n,ty) in \
            nx.get_node_attributes(G,'Type').items() if ty == 'Port']
        # and find all the remaining nodes.edge_nodes
        other_nodes = list(set(G.nodes()) - set(tile_nodes) - set(edge_nodes) - set(port_nodes))

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw_networkx_nodes(G, pos, nodelist=tile_nodes, \
            node_color='red', node_shape='s')
        nx.draw_networkx_nodes(G, pos, nodelist=edge_nodes, \
            node_color='blue', node_shape='s')
        nx.draw_networkx_nodes(G, pos, nodelist=other_nodes, \
            node_color='black', node_shape='o')
        nx.draw_networkx_nodes(G, pos, nodelist=port_nodes, \
            node_color='purple', node_shape='o')
        nx.draw_networkx_edges(G, pos)
        # nx.draw_networkx(G, pos=nx.get_node_attributes(G, 'pos'))
        plt.show()
        self.map = G
        self.settlements = 0
        self.cities = 0
        self.roads = 0
        self.bank = 0
        self.robber = 0

    def start(self):
        self.map
        
G = Game()