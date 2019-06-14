import networkx as nx
import matplotlib.pyplot as plt


def draw(G, title, large):
    '''
    Metoda graficki prikazuje zadati graf sa zadatim naslovom,
    i u zavisnosti od treceg parametra bira 'layout' za prikaz
    (vece grafove je lakse prikazati kao 'circular' graf).
    Takodje vodi racuna o afinitetu grana, pa ih stampa kao pune linije
    ili kao isprekidane u zavisnoti od vrednosti tog atributa
    :param G: - graf za prikazivanje
    :param title: - naslov grafa
    :param large: - 'boolean' promenljiva koja bira 'layout'
    '''
    if large:
        pos = nx.circular_layout(G)
    else:
        pos = nx.spring_layout(G)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_nodes(G.nodes, pos=pos, with_labels=True)
    e_plus = [(u, v) for (u, v, d) in G.edges(data=True) if d['affinity'] is "+"]
    e_minus = [(u, v) for (u, v, d) in G.edges(data=True) if d['affinity'] is "-"]
    nx.draw_networkx_edges(G, pos, edgelist=e_plus)
    nx.draw_networkx_edges(G, pos, edgelist=e_minus, style='dashed')
    plt.title(title)
    plt.show()


def draw_small(G, title):
    '''
    Metoda poziva metodu za crtanje manjeg grafa
    :param G: - graf za graficki prikaz
    :param title: - naslov grafa
    '''
    draw(G, title, False)


def draw_big(G, title):
    '''
    Metoda poziva metodu za crtanje veceg grafa
    :param G: - graf za graficki prikaz
    :param title: - naslov grafa
    '''
    draw(G, title, True)
