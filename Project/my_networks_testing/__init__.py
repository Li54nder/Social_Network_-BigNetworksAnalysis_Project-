import warnings
import networkx as nx

from os import path

from Project.my_library_extensions.load_graph import read_bitcoin, read_wiki, read_slashdot, \
    load_from_graphml, load_simple_example, generate_clusterable_graph

from Project.my_library_extensions.detect_graph_clusters import detect_clusters_small, \
    detect_clusters_big_v3, detect_clusters_big_v4, make_clusters, detect_coalitions, detect_bad_links, \
    make_network_of_clusters

from Project.my_library_extensions.draw_graph import draw_small, draw_big

from Project.my_library_extensions.save_graph import save_graph_as_graphml

from Project.my_library_extensions.clusters_analysis import rac


def main():
    """Analiza socijalnih mreza"""
    warnings.filterwarnings("ignore")  # MatplotlibDeprecationWarning
    G = load()
    print(f"\nGraf je ucitan i sadrzi {len(list(G.nodes))} cvorova i {len(list(G.edges))} linkova")
    num_connected_c = nx.number_connected_components(G)
    print(f"Broj povezanih komponenti u grafu: {num_connected_c}")
    if num_connected_c == 1:
        print(f"Duzina dijametra u grafu iznosi: {nx.diameter(G)}")
    else:
        comps_tmp = nx.connected_component_subgraphs(G)
        print(f"Graf cini {len(list(nx.connected_component_subgraphs(G)))} komponenti, pa je dijametar neizracunljiv (gigantsku komponentu cini "
              f"{len(sorted(comps_tmp, key=len, reverse=True)[0].nodes)*100.0/len(G.nodes)}% ukupnog broja cvorova)")

    print("\nProvera klasterabilnosti...")
    if len(G.nodes) < 500:
        clusters_set = detect_clusters_small(G)
        title = input("Uneti naziv grafa -> ")
        if len(G.nodes) > 100:
            draw_big(G, title)
        else:
            draw_small(G, title)
    else:
        # clusters_set = detect_with_deleting(G)
        # clusters_set = detect_clusters_big_v3(G)
        clusters_set = detect_clusters_big_v4(G)
        print("Graf je preveliki da bi se graficki prikazao")

    if clusters_set is not None:
        # print(clusters_set)
        print("\nPravljene klastera...")
        clusters = make_clusters(clusters_set, G)  # Ove klastere treba analizirati

        print("\nDetektovanje koalicija...")
        double_set = detect_coalitions(clusters)

        # print([len(Gc) for Gc in clusters])  # Velicina klastera

        coalitions = double_set[0]
        anticoalitions = double_set[1]

        print(f"\nU grafu se nalazi {len(coalitions)} kolalicija i {len(anticoalitions)} antikoalicija")

        rac(coalitions, anticoalitions)  # 00000000000000000000000000000000000000000000000000000000000000000000

        choice = input("Prikazati sadrzaj klastera (Y/N) -> ")
        if choice is "Y" or choice is "y":
            print(f"Klasteri koalicije (br. {len(coalitions)}):")
            for c in coalitions:
                print(c.nodes)
            print(f"Klasteri antikoalicije (br. {len(anticoalitions)}):")
            for c in anticoalitions:
                print(c.nodes)

        # Analiza mreze klastera
        print("\nPravljenje mreze klastera...")
        new_g = make_network_of_clusters(G, clusters)
        print("Analiziranje mreze klastera...")
        network_of_clusters_analysis(new_g)

        # Detektovanje linkova koji narusavaju klasterabilnost
        if len(anticoalitions) > 0:
            bad_links = detect_bad_links(anticoalitions)
            print(f"\nLinkova koji narusavaju klasterabilnost (balansiranost) ima: {len(bad_links)} (njih treba ukloniti da bi mreza bila klasterabilna)")
            choice = input("Prikazati ih (Y/N) -> ")
            if choice is "Y" or choice is "y":
                for link in bad_links:
                    print(link, end=" ")
                print()
        else:
            print("Mreza je klasterabilna i balansirana (u grafu ne postoje likovi koji narusavaju klasterabilnost)")

        # Sacuvati i klastere (recimo koalicije samo kao graphml)

        # Cuvanje grafa
        choice = input("\nSacuvati graf u 'graphml' formatu (Y/N) -> ")
        if choice is "Y" or choice is "y":
            path = input("Zeljena lokacija fajla (za podrazumevano: ' ' ili putanja po semi: 'C:\\\\path...\\\\name.graphml')\n -> ")
            save_graph_as_graphml(G, path)


def network_of_clusters_analysis(new_g):
    import matplotlib.pyplot as plt

    num_new_nodes = len(new_g.nodes)
    num_new_edges = len(new_g.edges)
    num_new_conn_c = nx.number_connected_components(new_g)
    if num_new_conn_c == 1:
        new_diameter = nx.diameter(new_g)
    else:
        new_diameter = "beskonacno"

    degree_sequence = sorted([d for n, d in new_g.degree()], reverse=True)

    fig = plt.figure()
    fig.suptitle('Grafik raspodele stepeni cvorova u novonastalom grafu klastera', fontsize=12, fontweight='bold')

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_title(f"Broj cvorova: {num_new_nodes}, broj likova: {num_new_edges}, "
                 f"broj povezanih komponenti: {num_new_conn_c}, dijametar: {new_diameter}", fontsize=8)

    ax.set_xlabel('rang')
    ax.set_ylabel('stepen')

    plt.loglog(degree_sequence, 'b-', marker='o')
    plt.axes([0.60, 0.60, 0.30, 0.25])
    if len(new_g.nodes) < 100:
        pos = nx.spring_layout(new_g)
    else:
        pos = nx.circular_layout(new_g)
    plt.axis('off')
    nx.draw_networkx_nodes(new_g, pos, node_size=20)
    nx.draw_networkx_edges(new_g, pos, alpha=0.4)
    plt.show()


def load():
    print("*" * 34 + "\n*    Projekat Socijalne Mreze    *\n" + "*" * 34)
    return creating_graph()


def creating_graph():
    print("\nIzabrati ucitavanje: ")
    print(">>> 1 <<< Ucitaj jednostavan gotov afinitetan graf")
    print(">>> 2 <<< Ucitaj graf iz 'graphml' formata")
    print(">>> 3 <<< Ucitaj graf iz fajla")
    print(">>> 4 <<< Generisi klasterabilan graf zadate velicine")
    chosen = "0"
    while int(chosen) < 1 or int(chosen) > 4:
        chosen = input(" -> ")
    switcher = {
        1: one,
        2: two,
        3: three,
        4: four
    }
    func = switcher.get(int(chosen))
    return func()

def one():
    # num = int(input("Unesi broj cvorova\n -> "))
    return load_simple_example()
def two():
    path = input("Lokacija fajla (po semi: 'C:\\\\path...\\\\file.graphml')\n -> ")
    return load_from_graphml(path)
def three():
    import os
    print("Izabrati koji od ponudjenih grafova ucitati:")
    print("> 1 < Graf iz fajla 'bitcoinalpha.csv' sa 'Stanforda'")
    print("> 2 < Graf iz fajla 'wiki-RfA.txt' sa 'Stanforda'")
    print("> 3 < Graf iz fajla 'slashdot.txt' sa 'Stanforda'")
    chosen = "0"
    while int(chosen) < 1 or int(chosen) > 3:
        chosen = input(" -> ")
    if chosen is "1":
        parent = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
        return read_bitcoin(path.join(parent, "files_for_tests", "bitcoinalpha.csv"))
    if chosen is "2":
        parent = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
        print("Ovo ce trajati dugo...")
        return read_wiki(path.join(parent, "files_for_tests", "wiki-RfA.txt"))
    parent = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
    print("Ovo ce trajati predugo...")
    return read_slashdot(path.join(parent, "files_for_tests", "slashdot.txt"))
def four():
    num_of_nodes = int(input("Broj cvorova za graf -> "))
    num_of_clusters = int(input("Broj klastera -> "))
    while num_of_clusters > num_of_nodes:
        print(">>> Los unos! <<<")
        num_of_nodes = int(input("Broj cvorova za graf -> "))
        num_of_clusters = int(input("Broj klastera -> "))
    return generate_clusterable_graph(num_of_clusters, num_of_nodes)


print(__name__)
if __name__ == '__main__':
    main()

# Primer jednog od izlaza konzole:
'''
Project
__main__
**********************************
*    Projekat Socijalne Mreze    *
**********************************
Izabrati ucitavanje: 
>>> 1 <<< Ucitaj jednostavan gotov afinitetan graf
>>> 2 <<< Ucitaj graf iz 'graphml' formata
>>> 3 <<< Ucitaj graf iz fajla
>>> 4 <<< Generisi klasterabilan graf zadate velicine
 -> 3
Izabrati koji od ponudjenih grafova ucitati:
> 1 < Graf iz fajla 'bitcoinalpha.csv' sa 'Stanforda'
> 2 < Graf iz fajla 'wiki-RfA.txt' sa 'Stanforda'
> 3 < Graf iz fajla 'slashdot.txt' sa 'Stanforda'
 -> 1
Loading graph (1/2)...
Loading graph (2/2)...
Loading done!
Graf je ucitan i sadrzi 3783 cvorova i 14124 linkova, proverava se klasterabilnosti...
Broj povezanih komponenti u grafu: 5
Graf ima 5 klastera
Analizirati ih (Y/N) -> Y
Graf je preveliki da bi se graficki prikazao
U grafu se nalazi 5 kolalicija i 0 antikoalicija
Prikazati sadrzaj klastera (Y/N) -> N
U grafu ne postoje likovi koji narusavaju klasterabilnost
Sacuvati graf u 'graphml' formatu (Y/N) -> N

Process finished with exit code 0
'''
