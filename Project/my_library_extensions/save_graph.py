import networkx as nx


def save_graph_as_graphml(g, path):
    '''
    Metoda koja cuva prosledjen graf
    :param g: - graf za cuvanje
    :param path: - lokacija na kojoj ce se graf snimiti
    '''
    if path is ' ':
        nx.write_graphml(g, "graph.graphml")
        print("Graf uspesno sacuvan")
    else:
        nx.write_graphml(g, path)
        print("Graf uspesno sacuvan")
