from collections import OrderedDict, Counter
import hashlib
from utils import gethostname, getpath
import networkx as nx
import matplotlib.pyplot as plt


class SimpleSiteMap(object):
    gr = None
    tokens = OrderedDict()
    tokens_counter = 0
    edges = []

    def __init__(self, site, exceptions=None):
        self.gr = nx.DiGraph()
        self.map = nx.DiGraph()
        self.site = site
        self.exceptions = exceptions

    def append_tokens(self, tuple):
        self.tokens_counter += 1
        if tuple == ():
            if '/' in self.tokens[0]:
                self.tokens[0]['/'] += 1
            else:
                self.tokens[0]['/'] = 1
        step = 0
        for i in tuple:
            if step not in self.tokens.keys():
                self.tokens[step] = OrderedDict()
            if i in self.tokens[step]:
                self.tokens[step][i] += 1
            else:
                self.tokens[step][i] = 1
            step += 1

    def reduce_tokens(self):
        sorted_tokens = OrderedDict()
        for k in self.tokens.keys():
            sorted_tokens[k] = OrderedDict(sorted(self.tokens[k].items(), key=lambda t: t[1], reverse=True))
        self.tokens = sorted_tokens

    def normalize_tokens_weight(self):
        for k in self.tokens.keys():
            local_tokens_counter = 0
            for token in self.tokens[k].keys():
                local_tokens_counter += self.tokens[k][token]
            for token in self.tokens[k].keys():
                self.tokens[k][token] /= float(local_tokens_counter)

    def get_simplified_node(self, node, cut_limit):
        simplified_node = []
        step = 0
        if node == ():
            node = ('/',)
        for token in node:
            try:
                if self.tokens[step][token] < cut_limit:
                    simplified_node.append("*")
                else:
                    simplified_node.append(token)
            except:
                simplified_node.append(token)
            step += 1
        if Counter(simplified_node)['*'] > 1:
            print node, simplified_node
        return tuple(simplified_node)

    def get_simplified_edge(self, tokens, cut_limit):
        nin, nout = tokens
        return self.get_simplified_node(nin, cut_limit), self.get_simplified_node(nout, cut_limit)

    def reduce_graph(self, cut_limit=0.005):
        self.map.clear()
        visits = len(self.edges)
        for edge in self.edges:
            e = self.get_simplified_edge(edge, cut_limit)
            self.map.add_edge(e[0], e[1])
            try:
                self.map[e[0]][e[1]]['weight'] += 1/float(visits)
            except KeyError:
                self.map[e[0]][e[1]]['weight'] = 1/float(visits)
        print(self.map.number_of_nodes())

    def add_node(self, uri, referer):
        for ex in self.exceptions:
            if uri.startswith(ex):
                return
        if referer and gethostname(referer) == gethostname(self.site):
            referer = getpath(referer)
            input_chain = filter(None, referer.split('/'))
        else:
            input_name = 'external'
            m = hashlib.md5()
            m.update(referer)
            input_chain = [input_name]
        output_chain = filter(None, getpath(uri).split('/'))
        tic, toc = tuple(input_chain), tuple(output_chain)
        self.append_tokens(toc)
        self.edges.append((tic, toc))
        self.gr.add_edge(tic, toc)

    def get_graph(self):
        self.map = self.gr.copy()
        self.reduce_tokens()
        self.normalize_tokens_weight()
        self.reduce_graph()
        return self.map

    def get_weight(self, uri, referer):
        pass

    def draw_graph(self):
        G = self.get_graph()
        pos=nx.spring_layout(G, iterations=10)
        e = G.edges()
        weights = [int(1+G[u][v]['weight']*30) for u, v in e]
        nx.draw_networkx_edges(G, pos=pos, alpha=0.3, width=weights, edge_color='m')
        nx.draw_networkx_labels(G, pos=pos, font_size=12)
        plt.show()
