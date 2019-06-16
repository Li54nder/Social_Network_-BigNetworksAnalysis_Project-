import warnings
import networkx as nx

from os import path

from Project.my_library_extensions.load_graph import read_bitcoin, read_wiki, read_slashdot, \
    load_from_graphml, load_simple_example, generate_clusterable_graph

from Project.my_library_extensions.detect_graph_clusters import detect_clusters_small, \
    detect_clusters_big_v4, detect_coalitions, detect_bad_links, \
    make_network_of_clusters, make_clusters2

from Project.my_library_extensions.draw_graph import draw_small, draw_big

from Project.my_library_extensions.save_graph import save_graph_as_graphml

from Project.my_library_extensions.clusters_analysis import analysis, network_of_clusters_analysis


def main():
    """Analiza socijalnih mreza"""
    warnings.filterwarnings("ignore")  # MatplotlibDeprecationWarning
    G = load()
    print(f"\nGraf je ucitan i sadrzi {len(list(G.nodes))} cvorova i {len(list(G.edges))} linkova")
    num_connected_c = nx.number_connected_components(G)
    print(f"Broj povezanih komponenti u grafu: {num_connected_c}")
    if len(G.nodes) > 4000:
        print("Graf je preveliki, pa se za pocetak izbegava racunanje dijametra...")
    else:
        if num_connected_c == 1:
            print(f"Duzina dijametra u grafu iznosi: {nx.diameter(G)}")
        else:
            comps_tmp = nx.connected_component_subgraphs(G)
            print(f"Graf cini {len(list(nx.connected_component_subgraphs(G)))} komponenti, pa je dijametar neizracunljiv (gigantsku komponentu cini "
                  f"{round(len(sorted(comps_tmp, key=len, reverse=True)[0].nodes)*100.0/len(G.nodes), 2)}% ukupnog broja cvorova)")

    print("\nProvera klasterabilnosti...")
    if len(G.nodes) < 500:
        clusters_set = detect_clusters_small(G)
        title = input("Uneti naziv grafa -> ")
        if len(G.nodes) > 100:
            draw_big(G, title)
        else:
            draw_small(G, title)
    else:
        clusters_set = detect_clusters_big_v4(G)
        print("Graf je preveliki da bi se graficki prikazao")

    if clusters_set is not None:
        print("\nPravljene klastera...")
        clusters = make_clusters2(clusters_set, G)

        print("\nDetektovanje koalicija...")
        double_set = detect_coalitions(clusters)

        coalitions = double_set[0]
        anticoalitions = double_set[1]

        print(f"\nU grafu se nalazi {len(coalitions)} kolalicija i {len(anticoalitions)} antikoalicija")

        analysis(coalitions, anticoalitions)

        choice = input("\nPrikazati sadrzaj klastera (Y/N) -> ")
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

        # Cuvanje grafa
        choice = input("\nSacuvati graf u 'graphml' formatu (Y/N) -> ")
        if choice is "Y" or choice is "y":
            path = input("Zeljena lokacija fajla (za podrazumevano: ' ' ili putanja po semi: 'C:\\\\path...\\\\name.graphml')\n -> ")
            save_graph_as_graphml(G, path)


def load():
    print("*" * 34 + "\n*    Projekat Socijalne Mreze    *\n" + "*" * 34)
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
