from urlparse import urlparse


def parse_headers(headers):
    res = {}
    h = headers.split("', '")
    for sh in h:
        header = sh.split("': '")[0]
        if header[0] == "'":
            header = header[1:]
        data = sh.split("': '")[1]
        try:
            if data[-1] == "'":
                data = data[:-1]
        except IndexError:
            data = ''
        res[header] = data
    res['header_count'] = len(res) - 1
    return res


def lower_keys(x):
    if isinstance(x, list):
        return [lower_keys(v) for v in x]
    elif isinstance(x, dict):
        return dict((k.lower(), lower_keys(v)) for k, v in x.iteritems())
    else:
        return x


def gethostname(uri):
    up = urlparse(uri)
    return up.hostname


def getpath(uri):
    up = urlparse(uri)
    return up.path


def merge_nodes(G, nodes, new_node, attr_dict=None, **attr):

    G.add_node(new_node, attr_dict, **attr)

    for n1, n2, data in G.edges(data=True):
        if n1 in nodes:
            G.add_edge(new_node, n2, data)
        elif n2 in nodes:
            G.add_edge(n1, new_node, data)

    for n in nodes:
        G.remove_node(n)
