from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix as cm
# from scipy.sparse import csr_matrix
import networkx as nx
import numpy as np
import sys

# from scipy.special.tests.test_data import data


def detect_clusters_small(g):
    '''
    Metoda koja koristi klasu 'CompBFS' kako bi detektovala komponente povezanosti,
    vise o tome u opisu klase
    :param g: - pocetni graf kojem trebe detektovati klastere
    :return: - vraca skup skupova koji sadrze cvorove u istoj komponenti povezanosti
    '''
    c = CompBFS(g)
    return c.identify_components()


class CompBFS:
    '''
    Klasa koja sluzi za detektovanje povezanih komponenti i klastera
    unutar grafa, koristi BFS algoritam i primenjuje se samo za male mreze...
    '''

    visited = None
    components = None

    def __init__(self, g):
        self.G = g

    def identify_components(self):
        '''
        Metoda identifikuje povezane komponente unutar zadatog grafa koji je polje klase
        :return: - vraca skup skupova koji sadrze cvorove u istoj komponenti povezanosti
        '''
        self.visited = set()
        self.components = set()
        for n in self.G.nodes:
            if n not in self.visited:
                self.components.add(self.bfs(n))
        print(f"Graf ima {len(list(self.components))} klastera")
        return frozenset(self.components)

    def bfs(self, start):
        '''
        Metoda implementira BFS algoritam...
        :param start: cvor od koga krece pretraga
        :return: - vraca skup cvorova koji cine jednu komponentu povezanosti
        '''
        comp = set()
        queue = []
        comp.add(start)
        self.visited.add(start)
        queue.append(start)

        while len(queue) > 0:
            curr = queue.pop(0)
            neighbours = list(nx.neighbors(self.G, curr))
            for n in neighbours[:]:
                d1 = self.G.get_edge_data(curr, n)
                d2 = self.G.get_edge_data(n, curr)
                if d1['affinity'] is "-" or d2['affinity'] is "-":
                    neighbours.remove(n)
            for n in neighbours:
                if n not in self.visited:
                    comp.add(n)
                    self.visited.add(n)
                    queue.append(n)
        return frozenset(comp)


def detect_clusters_big_v3(g):
    '''
    Metoda koja detektuje klastere u velikim grafovima,
    ali opet ne prevelikim jer matrica bi jos i mogla da primi toliki broj podataka
    ali metoda 'np.indices(mat.shape).T[:, :, [1, 0]]' ne moze da primi i obradi
    preveliku matricu...
    :param g: - graf za koji treba detektovati klastere
    :return: - vraca skup skupova koji sadrze cvorove u istoj komponenti povezanosti
    '''
    # ideja mozda: predstaviti niz mapu... kljuc je pozicija I, value naziv cvora...
    n = len(g.nodes)
    # pokusavano sa raznim matricama zbog memorije...nakraju stavljena SPARSE, ali...
    row = []
    col = []
    data = []
    # mat = np.zeros((n, n), dtype=np.int8)
    # mat = cm((n, n), dtype=np.int8)
    # niz zbog brzeg pristupa elementu na zadatom indeksu
    nodes = np.asarray(g.nodes)
    # pronalazak max elementa zbok prepravke velicine matrice...
    # tmp = [int(x) for x in list(g.nodes)]
    # tmp = np.asarray(tmp)
    # tmp = np.amax(tmp)
    # print(tmp)
    for i in range(n):
        sys.stdout.write(f"{i}/{n}")
        sys.stdout.flush()
        for j in range(n):
            if i == j:
                # da li popuniti dijagonalu jedinicama???
                # mat.itemset((i, j), 1)
                continue
            n1 = nodes[i]
            n2 = nodes[j]
            if g.has_edge(n1, n2):
                if g.get_edge_data(n1, n2)['affinity'] is "+":
                    # pokusaj stelovanja da same poziije budi cvorovi (problem kod ne integer cvorova)
                    # poz_r, = np.where(nodes == n1)
                    # row.append(int(n1))  # i
                    # col.append(int(n2))  # j
                    row.append(i)
                    col.append(j)
                    data.append(1)
        sys.stdout.write("\r")
    # ERROR..(n, n) - velicina matrice (mozda najveci element ali i to puca...)
    mat = cm((np.asarray(data), (np.asarray(row), np.asarray(col))), shape=(n, n))
    # metoda koja se najcesce koristi kod procesuiranja slika...
    n_comps, lbls = connected_components(mat, False)
    print(f"Graf ima {n_comps} klastera")

    command = input("Analizirati ih (Y/N) -> ")
    components = None
    if command is "Y" or command is "y":
        indices = np.indices(mat.shape).T[:, :, [1, 0]]
        components = set()
        for i in range(n_comps):
            components.add(tuple([x[0][0]+1 for x in indices[lbls == i]]))
    return components


def detect_clusters_big_v4(g = nx.Graph()):
    '''
    Metoda koja detektuje klastere u velikim grafovima,
    ali opet ne prevelikim jer matrica bi jos i mogla da primi toliki broj podataka
    ali metoda 'np.indices(mat.shape).T[:, :, [1, 0]]' ne moze da primi i obradi
    preveliku matricu...
    :param g: - graf za koji treba detektovati klastere
    :return: - vraca skup skupova koji sadrze cvorove u istoj komponenti povezanosti
    '''
    # pokusavano sa raznim matricama zbog memorije...nakraju stavljena SPARSE
    row = []
    col = []
    data = []
    nodes = np.asarray(g.nodes)

    # values = list(range(len(g.nodes)))
    # nx.set_node_attributes(g, values, name='serial_num')
    g.nodes(data=True)
    nx.set_node_attributes(g, "", "serial_num")
    nx.set_node_attributes(g, "", "lbl")

    i = 0
    for n in g.nodes():
        g.add_node(n, serial_num=i)
        i += 1

    i = 0
    l = len(g.edges) - 1
    for e in g.edges(data=True):
        sys.stdout.write(f"{i}/{l}")
        sys.stdout.flush()
        row.append(dict(g.nodes(data=True)).get(e[0])['serial_num'])
        col.append(dict(g.nodes(data=True)).get(e[1])['serial_num'])
        data.append(1)
        i += 1
        sys.stdout.write("\r")
    n = len(g.nodes)
    mat = cm((np.asarray(data), (np.asarray(row), np.asarray(col))), shape=(n, n))
    # metoda koja se najcesce koristi kod procesuiranja slika...
    n_comps, lbls = connected_components(mat, False)

    i = 0
    nodes = np.asarray(g.nodes(data=True))
    print(len(lbls), "......", len(g.nodes))
    for lbl in lbls:
        nodes[i][1]['lbl'] = lbl
        i += 1

    print(nodes[3000][1]['lbl'], nodes[888][1]['lbl'], nodes[685][1]['lbl'])

    clusters = set()
    for i in range(n_comps):
        cluster = [x for (x, d) in g.nodes(data=True) if d['lbl'] == i]
        clusters.add(frozenset(cluster))

    return clusters


# def detect_clusters_big2(g):
#     n = len(g.nodes)
#     mat = np.zeros((n, n), dtype=np.int8)
#     # mat = cm((n, n), dtype=np.int8)
#     nodes = np.asarray(g.nodes)
#     for i in range(n):
#         sys.stdout.write(f"{i}/{n}")
#         sys.stdout.flush()
#         for j in range(n):
#             if i == j:
#                 mat.itemset((i, j), 1) # privremenooo...
#                 continue
#             n1 = nodes[i]
#             n2 = nodes[j]
#             if g.has_edge(n1, n2):
#                 if g.get_edge_data(n1, n2)['affinity'] is "+":
#                     mat.itemset((i, j), 1)
#                     # mat.itemset((j, i), 1)
#         sys.stdout.write("\r")
#     n_comps, lbls = connected_components(mat, False) # metoda koja se najcesce koristi kod procesuiranja slika...
#     print(f"Graf ima {n_comps} klastera")
#     command = input("Analizirati ih (Y/N) -> ")
#     components = None
#     if command is "Y" or command is "y":
#         indices = np.indices(mat.shape).T[:, :, [1, 0]]
#         components = set()
#         for i in range(n_comps):
#             components.add(tuple([x[0][0]+1 for x in indices[lbls == i]]))
#     return components


def make_clusters(clusters_set, g):
    '''
    Metoda od prosledjenog skupa skupova cvorova, koji predstavljaju klastere, pravi
    klastere kao grafove same za sebe, a na osnovu grafa 'g' koji je polazni graf
    //radi prilicno brzo i sa ovim kopiranjem...(mada bi moglo da se napravi graf samo
    //sa tim cvorovima i na osnovu povezanosti u pocetnom grafu ih povezati ili ne u novom
    //ali je pitanje da li bi bilo brze jer treba da se proverava za svaka dva cvora da
    //da li su bila povezana...)
    :param clusters_set: - skup skupova cvorova
    :param g: - polazni graf
    :return: - skup klastera_grafova
    '''
    counter = 0
    counterMax = len(clusters_set) * len(g.nodes)
    sys.stdout.write(f"{counter}/{counterMax}")
    sys.stdout.flush()

    clusters = set()
    i = 1
    br = len(list(clusters_set))
    for c in clusters_set:
        sys.stdout.write(f"{i}/{br}")
        sys.stdout.flush()
        tmp1 = [int(x) for x in c]
        tmp = set(tmp1)
        # tmp = list(c)
        # print(tmp)
        newG = g.copy()
        for n in list(newG.nodes)[:]:  # list()
            sys.stdout.write("\r")
            counter += 1
            sys.stdout.write(f"{counter}/{counterMax}")
            sys.stdout.flush()

            if int(n) not in tmp:
                # print(n, end=", ")
                newG.remove_node(n)
            else:
                pass
                # print(n, end=", ")
        # print()
        clusters.add(newG)
        # sys.stdout.write("\r")
        i += 1
    sys.stdout.write("\r")
    print("...napravljeni")
    return clusters


def detect_coalitions(clusters):
    '''
    Metoda detektuje koalicije i antikoalicije tako sto proveri svaki klaster da li sadrzi
    '-' granu koja bi od njega napravila antikoaliciju
    :param clusters: - skup klastera koji su mreza za sebe
    :return: - vraca listu koja na prvom mestu ima skup coalicija a na drugom skup antikoalicija
    '''

    double_set = []
    coalitions = set()
    anticoalitions = set()
    for g in clusters:
        badEdges = [(u, v) for (u, v, d) in g.edges(data=True) if d['affinity'] is "-"]
        if len(badEdges) == 0:
            coalitions.add(g)
        else:
            anticoalitions.add(g)
    double_set.append(coalitions)
    double_set.append(anticoalitions)
    print("...detektovane")
    return double_set


def make_network_of_clusters(g, clusters):
    '''
    Pravljene mreze klastera...
    :param g: - pocetni graf na osnovu koga se proverava da li su klateri povezani medjusobno
    :param clusters: - skup klastera
    :return: - graf klastera
    '''
    new_g = nx.Graph()
    br = 1
    for c in clusters:
        c.graph['name'] = str(br)
        br += 1
        new_g.add_node(c)
    for c1 in clusters:
        for c2 in clusters:
            if c1 == c2:
                continue
            povezani = False
            br = 0
            while not povezani and br < len(c1.nodes):
                n1 = list(c1.nodes)[br]
                br += 1
                for n2 in c2:
                    if n1 in nx.neighbors(g, n2):
                        povezani = True
            if povezani:
                new_g.add_edge(c1, c2)
    nx.set_edge_attributes(new_g, "-", "affinity")
    return new_g


def detect_bad_links(anticoalitions):
    '''
    Detektovanje grana koje narusavaju klasterabilnost
    :param anticoalitions: - svi klasteri antikoalicija koji sadrze '-' grane
    :return: - vraca se lista grana (parova cvorova) koje su '-' a unutar klastera su
    '''
    tmp_list = []
    for g in anticoalitions:
        bad_edges = [(u, v) for (u, v, d) in g.edges(data=True) if d['affinity'] is "-"]
        tmp_list.append(bad_edges)
    return [item for sub_list in tmp_list for item in sub_list]

