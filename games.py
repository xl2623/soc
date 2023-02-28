import networkx as nx
import matplotlib.pyplot as plt
from statistics import median
import random
import numpy as np
import PIL

class Player:
    def __init__(self, resource, port, vp, dev, roads, cities, settlements):
        self.resource = resource
        self.port = port
        self.vp = vp
        self.dev = dev
        self.roads = roads
        self.cities = cities
        self.settlement = settlements
        self.players = []
        self.dice = 0

    def rolldice(self):
        self.dice = random.randint(0,7)+random.randint(0,7)

    def inital_place(self):
        random.randint(0,54)


class Game:
    def __init__(self):
        self.tile = Tile()
        self.numbermap = self.createnumbermap()
        self.map = self.createmap()
        self.settlements = 0
        self.cities = 0
        self.roads = 0
        self.bank = 0
        self.robber = 0
        self.dice = 0
        # self.resource = np.diag(self.tile.index[:,0])


    def createnumbermap(self):
        numbermap = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12,7]
        random.shuffle(numbermap)
        Desert_index = self.tile.name.index("Desert")
        Seven_index = numbermap.index(7)
        temp = numbermap[Desert_index]
        numbermap[Desert_index] = 7
        numbermap[Seven_index] = temp
        return numbermap

    def createmap(self):
        icons = {
            "Lumber": "/home/thomas_ubuntu/soc/tiles/lumber.png",
            "Wool": "/home/thomas_ubuntu/soc/tiles/sheep.png",
            "Grain": "/home/thomas_ubuntu/soc/tiles/wheat.png",
            "Brick": "/home/thomas_ubuntu/soc/tiles/brick.png",
            "Ore": "/home/thomas_ubuntu/soc/tiles/ore.png",
            "Desert": "/home/thomas_ubuntu/soc/tiles/desert.png"
        }
        images  = {k: PIL.Image.open(fname) for k, fname in icons.items()}
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
            G.add_node(i, pos=(x, y), Type='Edge', image=None)
            G.add_edge(edge[0], i)
            G.add_edge(edge[1], i)
            G.remove_edge(edge[0], edge[1])
            i = i+1

        i = 1000
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
            G.add_node(new_tile, pos=(x,y),node_shape='s', Type='Tiles', image=images[self.tile.name[i%1000]])
            for node in base:
                G.add_edge(node, new_tile, Type='Tiles')
            i = i+1

        # add port
        base1 = (1, 7)
        base2 = (2, 7)
        G.add_node(3000, pos=((positions[base1][0]+positions[base2][0])/2, positions[base2][1]+deltay), Type='Port', image=None)
        G.add_edge(base1, 3000, Type='Port')
        G.add_edge(base2, 3000, Type='Port')

        base1 = (3, 7)
        base2 = (4, 7)
        G.add_node(3001, pos=((positions[base1][0]+positions[base2][0])/2, positions[base2][1]+deltay), Type='Port')
        G.add_edge(base1, 3001, Type='Port')
        G.add_edge(base2, 3001, Type='Port')
        
        base1 = (0, 6)
        base2 = (0, 5)
        G.add_node(3002, pos=(positions[base1][0]-deltax, positions[base1][1]), Type='Port')
        G.add_edge(base1, 3002, Type='Port')
        G.add_edge(base2, 3002, Type='Port')

        base1 = (5, 6)
        base2 = (5, 5)
        G.add_node(3003, pos=(positions[base1][0]+deltax, positions[base1][1]), Type='Port')
        G.add_edge(base1, 3003, Type='Port')
        G.add_edge(base2, 3003, Type='Port')

        base1 = (0, 3)
        base2 = (0, 2)
        G.add_node(3004, pos=(positions[base2][0]-deltax, positions[base2][1]), Type='Port')
        G.add_edge(base1, 3004, Type='Port')
        G.add_edge(base2, 3004, Type='Port')

        base1 = (5, 3)
        base2 = (5, 2)
        G.add_node(3005, pos=(positions[base2][0]+deltax, positions[base2][1]), Type='Port')
        G.add_edge(base1, 3005, Type='Port')
        G.add_edge(base2, 3005, Type='Port')

        base1 = (1, 0)
        base2 = (1, -1)
        G.add_node(3006, pos=(positions[base2][0]-deltax, positions[base2][1]), Type='Port')
        G.add_edge(base1, 3006, Type='Port')
        G.add_edge(base2, 3006, Type='Port')

        base1 = (4, 0)
        base2 = (4, -1)
        G.add_node(3007, pos=(positions[base2][0]+deltax, positions[base2][1]), Type='Port')
        G.add_edge(base1, 3007, Type='Port')
        G.add_edge(base2, 3007, Type='Port')

        base1 = (2, -2)
        base2 = (3, -2)
        G.add_node(3008, pos=((positions[base1][0]+positions[base2][0])/2, positions[base2][1]-deltay), Type='Port')
        G.add_edge(base1, 3008, Type='Port')
        G.add_edge(base2, 3008, Type='Port')

        # extract nodes with specific setting of the attribute
        tile_nodes = [n for (n,ty) in \
            nx.get_node_attributes(G,'Type').items() if ty == 'Tiles']
        edge_nodes = [n for (n,ty) in \
            nx.get_node_attributes(G,'Type').items() if ty == 'Edge']
        port_nodes = [n for (n,ty) in \
            nx.get_node_attributes(G,'Type').items() if ty == 'Port']
        # and find all the remaining nodes.edge_nodes
        other_nodes = list(set(G.nodes()) - set(tile_nodes) - set(edge_nodes) - set(port_nodes))
        target = [i for i in range(0,len(other_nodes))]
        res = {other_nodes[i]: target[i] for i in range(len(other_nodes))}
        nx.relabel_nodes(G, res, False)
        return G

    def roll_dice(self):
        self.dice = random.randint(0,7)+random.randint(0,7)
        # self.dice = 7

    def dice2resource(self):
        # dice to tile and then tile to resource
        selectedTiles = [i+1000 for i,x in enumerate(self.numbermap) if x==self.dice]
        return [self.tile.name[x%1000] for x in selectedTiles], selectedTiles

    # def play(self):
    #     self.roll_dice()
    #     if self.dice != 7:
        
    #     else:
    #         _, tiles = self.dice2resource()
    #         players = neighbor(tiles)

    # def neighbor(tiles):
        
    # def tile2player(tile):
        
    #     return 



class Tile:
    def __init__(self):
        self.i2n = ["Lumber", "Wool", "Grain", "Brick", "Ore", "Desert"]
        self.name = ["Lumber","Lumber","Lumber","Lumber",\
                         "Wool","Wool","Wool","Wool",\
                         "Grain","Grain","Grain","Grain",\
                         "Brick","Brick","Brick",\
                         "Ore","Ore","Ore",\
                         "Desert"]
        random.shuffle(self.name)
        self.index = np.zeros((len(self.name), 1))
        for i in range(0,len(self.name)):
            if self.name[i] == "Lumber":
                self.index[i,0] = 0
            elif self.name[i] == "Wool":
                self.index[i,0] = 1
            elif self.name[i] == "Grain":
                self.index[i,0] = 2
            elif self.name[i] == "Brick":
                self.index[i,0] = 3
            elif self.name[i] == "Ore":
                self.index[i,0] = 4
            else:
                self.index[i,0] = 5

def draw(G):
    # Draw the graph
    # extract nodes with specific setting of the attribute
    tile_nodes = [n for (n,ty) in \
        nx.get_node_attributes(G,'Type').items() if ty == 'Tiles']
    edge_nodes = [n for (n,ty) in \
        nx.get_node_attributes(G,'Type').items() if ty == 'Edge']
    port_nodes = [n for (n,ty) in \
        nx.get_node_attributes(G,'Type').items() if ty == 'Port']
    tile_edges = [n for (n,ty) in \
        nx.get_edge_attributes(G,'Type').items() if ty == 'Tiles']
    # and find all the remaining nodes.edge_nodes
    other_nodes = list(set(G.nodes()) - set(tile_nodes) - set(edge_nodes) - set(port_nodes))
    plotting_edge = list(set(G.edges()) - set(tile_edges))
    fig, ax = plt.subplots()
    pos = nx.get_node_attributes(G, 'pos')
    # nx.draw_networkx_nodes(G, pos, nodelist=tile_nodes, \
    #     node_color='red', node_shape='s')
    # nx.draw_networkx_nodes(G, pos, nodelist=edge_nodes, \
    #     node_color='blue', node_shape='s')
    # nx.draw_networkx_nodes(G, pos, nodelist=other_nodes, \
    #     node_color='black', node_shape='o')
    # nx.draw_networkx_nodes(G, pos, nodelist=port_nodes, \
    #     node_color='purple', node_shape='o')
    nx.draw_networkx_edges(G, pos, edgelist = plotting_edge)
    # nx.draw_networkx_edges(
    #     G,
    #     pos=pos,
    #     ax=ax,
    #     arrows=True,
    #     arrowstyle="-",
    #     min_source_margin=15,
    #     min_target_margin=15,
    # )
    # Transform from data coordinates (scaled between xlim and ylim) to display coordinates
    tr_figure = ax.transData.transform
    # Transform from display to figure coordinates
    tr_axes = fig.transFigure.inverted().transform

    # Select the size of the image (relative to the X axis)
    icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.025
    icon_center = icon_size / 2.0
    for n in G.nodes:
        # if nx.get_node_attributes(n,"Type") == 'Tiles':
        xf, yf = tr_figure(pos[n])
        xa, ya = tr_axes((xf, yf))
        # get overlapped axes and plot icon
        a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
        if n>=1000 and n<1200:
            a.imshow(G.nodes[n]["image"])
        a.axis("off")
    plt.show()

if __name__ == '__main__':
    G = Game()
    print(G.tile.name)
    # print(G.tile.index)
    # print(G.resource)
    G.roll_dice()
    # print(G.dice)
    # print(G.numbermap)
    # print(G.dice2tile())
    print(G.dice2resource())
    draw(G.map)