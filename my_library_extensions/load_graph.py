import networkx as nx
import random


def load_simple_example():
    '''
    Ucitava gotov jednostavan graf...
    :return: - vraca neusmeren afinitetan graf
    '''
    g = nx.tutte_graph()
    # g = nx.gnp_random_graph(num, 0.06)
    make_affinity(g)
    return g


def make_affinity(g):
    '''
    Metoda koja random generise afinitet za neafinitetan graf sa predodredjenom
    verovatnocom da dva cvora budu povezana negativnom granom od 33%
    :param g: - neafinitetan graf
    :return: - vraca afinitetan graf
    '''
    g.edges(data=True)
    nx.set_edge_attributes(g, "+", "affinity")
    epsilon = 0.33
    for (u, v) in g.edges():
        if random.uniform(0, 1) < epsilon:
            g.add_edge(u, v, affinity="-")


def load_from_graphml(path):
    '''
    Metoda ucitava neusmeren afinitetan graf iz 'graphml' fajla sa zadate lokacije.
    Uglavnom namenjeno za citanje vec obradjivanih grafova u ovom programu koji
    su sacuvani kao 'graphml' fajl na kraju izvrsavanja programa
    :param path: - lokacija fajla za citanje
    :return: - vraca afinitetan graf
    '''
    return nx.read_graphml(path)


def read_bitcoin(path):
    '''
    Metoda ucitava usmeren graf sa 'Stanforda' i pretvara ga u neusmeren
    :param path: - lokacija fajla za citanje
    :return: - braca afinitetan graf
    '''
    G = nx.DiGraph()
    import csv
    print("Loading graph (1/2)...")
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if int(row[2]) > 0:
                aff = "+"
            else:
                aff = "-"
            G.add_edge(row[0], row[1], affinity=aff)
    csv_file.close()
    return make_undirected(G)


def read_wiki(path):
    '''
    Metoda ucitava usmeren graf sa 'Stanforda' i pretvara ga u neusmeren
    :param path: - lokacija fajla za citanje
    :return: - braca afinitetan graf
    '''
    file = open(path, "r", encoding="utf8")
    G = nx.DiGraph()
    lines = file.read().splitlines()
    print("Loading graph (1/2)...")
    src = None
    tgt = None
    for line in lines:
        if line.startswith("SRC"):
            src = line.split(":")[1]
            # G.add_node(src)
        if line.startswith("TGT"):
            tgt = line.split(":")[1]
            # G.add_node(tgt)
        if line.startswith("RES"):
            res = line.split(":")[1]
            if res is "1":
                res = "+"
            else:
                res = "-"
            G.add_edge(src, tgt, affinity=res)
    return make_undirected(G)


def read_slashdot(path):
    '''
    Metoda ucitava usmeren graf sa 'Stanforda' i pretvara ga u neusmeren
    :param path: - lokacija fajla za citanje
    :return: - braca afinitetan graf
    '''
    file = open(path, "r")
    lines = file.read().splitlines()
    tmp_list = []
    print("Loading graph (1/2)...")
    for line in lines:
        if line.startswith("#"):
            continue
        line = line.split("\t")
        if "-1" in line[2]:
            sign = "-"
        else:
            sign = "+"
        item = (line[0].strip(), line[1].strip(), {'affinity': sign})
        tmp_list.append(item)
    g1 = nx.DiGraph()
    g1.add_edges_from(tmp_list)
    return make_undirected(g1)


def make_undirected(g1):
    '''
    Metoda od usmerenog grafa pravi neusmeren. Ako je u bilo kojem od
    dva smera bio minus, minus i ostaje; u sputrotnom se stavlja '+'
    :param g1: - usmeren afinitetan graf
    :return: - vraca neusmeren afinitetan graf
    '''
    g2 = nx.Graph()
    g2.add_edges_from(g1.edges(), affinity="")
    print("Loading graph (2/2)...")
    for u, v, d in g1.edges(data=True):
        aff1 = g1[u][v]['affinity']
        aff2 = ""
        if (v, u) in g1.edges:
            aff2 = g1[v][u]['affinity']
        if aff1 is "-" or aff2 is "-":
            g2[u][v]['affinity'] = "-"
        else:
            g2[u][v]['affinity'] = "+"
    print("Loading done!")
    return g2


def generate_clusterable_graph(numofclusters, numofnodes):
    '''
    Metoda generise neusmeren afinitetan klasterabilan graf, sa zadatim brojem cvorova
    i zadatim brojem klastera.
    Postoji sansa da metoda nekad vrati 1-2 klastera vise nego sto je zadato,
    Taj bag se javlja jednom u 50ak slucajeva,
    Ali graf idalje ostaje klasterabilan
    (Idej__ prvo se napravi zeljeni broj klastera i popuni sa po jednim cvorom,
    potom se postave verovatnoce rasodele po klasterima... Zatim se rasporedi
    preostali broj cvorova u klastere; onda se poveze graf u potpunost, unutar
    klastera pozitivnim granama a izmedju negativnim, i na samom kraju se generise
    random broj grana za brisanje pa se toliko random grana i obrise)
    :param numofclusters: - broj klastera za zeljeni graf
    :param numofnodes: - broj cvorova za zeljeni graf
    :return: - vraca generisan neusmeren afinitetan graf koji je klasterabilan
    '''
    clusters = dict()
    spliters = []
    # Generisanje splitera i njihovo rasporedjivanje
    for i in range(numofclusters-1):
        num = round(random.uniform(0, 1), 2)
        while num in spliters:
            num = round(random.uniform(0, 1), 2)
        spliters.append(num)
    spliters.sort()
    spliters.append(1)
    # ({K1 : [spliter, item1, item2, ...]})
    for c in range(numofclusters):
        clusters["Cluster_" + str(c+1)] = [spliters[c]]

    nodes = list(range(1, numofnodes+1))
    for k in clusters:
        node = random.randint(0, len(nodes) - 1)
        clusters[k].append(nodes.pop(node))
        # Dodavanje samo po jednog cvora u svaki klaster

    # Dodavanje ostalih cvorova u klastere
    for node in nodes:
        br = 0
        num = random.uniform(0, 1)
        situated = False
        while not situated:
            br += 1
            if num < clusters["Cluster_"+str(br)][0]:
                clusters["Cluster_"+str(br)].append(node)
                situated = True

    g = nx.Graph()
    br = 0
    for k in clusters:
        br += 1
        clusters[k].pop(0)
        for n in clusters[k]:
            g.add_node(n, lbl=k)

    # Kompletan graf
    for v in g.nodes:
        for u in g.nodes:
            if v == u:
                continue
            if g.nodes[v]['lbl'] == g.nodes[u]['lbl']:
                g.add_edge(v, u, affinity="+")
            else:
                g.add_edge(v, u, affinity="-")

    # Broj grana za brisanje,
    # Brise se izmedju nijedne i maksimalnog broja grana koje mogu da se obrisu...
    # Graf ne bi morao ostati povezan kada bi se brisale samo negativne grane (postoji sansa da se to desi)
    num_deletable = random.randint(0, (numofnodes * (numofnodes - 1))/2 - (numofnodes - 1))
    edges = list(g.edges)
    for i in range(num_deletable): # (0, ...
        chosen_edge = random.choice(edges)
        deleted = False
        while not deleted:
            if g.edges[chosen_edge]['affinity'] == "-":
                g.remove_edge(chosen_edge[0], chosen_edge[1])
                edges.remove(chosen_edge)
                deleted = True
            else:
                # Vodi se racuna da se ne raspadne klaster brisanjem grane koja ga drzi u celini
                neighbors1 = g.neighbors(chosen_edge[0])
                num1 = 0
                for n in neighbors1:
                    if g.get_edge_data(chosen_edge[0], n)['affinity'] == "+":
                        num1 += 1
                neighbors2 = g.neighbors(chosen_edge[1])
                num2 = 0
                for n in neighbors2:
                    if g.get_edge_data(chosen_edge[1], n)['affinity'] == "+":
                        num2 += 1
                if num1 > 1 and num2 > 1:
                    g.remove_edge(chosen_edge[0], chosen_edge[1])
                    edges.remove(chosen_edge)
                    deleted = True
                else:
                    chosen_edge = random.choice(edges)
    return g
