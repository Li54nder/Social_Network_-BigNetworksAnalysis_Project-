import networkx as nx
import math


def rac(coalition, anti_coalition):

    print("\nAnaliziranje sličnosti i razlike u strukturi koalicija i anti-koalicija...\n")

    coalitions_score = racunaj_metrike_za_(coalition)
    anti_coalitions_score = racunaj_metrike_za_(anti_coalition)

    koalicije_su_kohezivnije = proveri_(coalitions_score['average_degree'], anti_coalitions_score['average_degree'])
    anti_koalicije_su_kohezivnije = proveri_(anti_coalitions_score['average_degree'], coalitions_score['average_degree'])

    koalicije_su_relativno_redje = proveri_POSEBNO(coalitions_score['network_density'], anti_coalitions_score['network_density'])
    anti_koalicije_su_relativno_redje = proveri_POSEBNO(anti_coalitions_score['network_density'], coalitions_score['network_density'])

    anti_koalicije_imaju_manji_dijametar = proveri_(coalitions_score['diameter'], anti_coalitions_score['diameter'])
    koalicije_imaju_manji_dijametar = proveri_(anti_coalitions_score['diameter'], coalitions_score['diameter'])

    cvorovi_koalicija_su_vise_distancirani = proveri_(coalitions_score['average_distance'], anti_coalitions_score['average_distance'])
    cvorovi_anti_koalicija_su_vise_distancirani = proveri_(anti_coalitions_score['average_distance'], coalitions_score['average_distance'])

    if not koalicije_su_kohezivnije and not anti_koalicije_su_kohezivnije:
        print("Koalicije i anti-koalicije se generalno ne razlikuju po kohezivnosti")
    elif koalicije_su_kohezivnije:
        print("Koalicije su kohezivnije mreze")
    else:
        print("Anti-koalicije su kohezivnije mreze")

    if not koalicije_su_relativno_redje and not anti_koalicije_su_relativno_redje:
        print("Koalicije i anti-koalicije se generalno ne razlikuju po gustini mreze")
    elif koalicije_su_relativno_redje:
        print("Koalicije su redje mreze od anti-koalicija")
    else:
        print("Anti-koalicije su redje mreze od koalicija")

    if not koalicije_imaju_manji_dijametar and not anti_koalicije_imaju_manji_dijametar:
        print("Koalicije i anti-koalicije se generalno ne razlikuju po duzini dijametra")
    elif koalicije_imaju_manji_dijametar:
        print("Koalicije imaju manji dijametar")
    else:
        print("Anti-koalicije imaju manji dijametar")

    if not cvorovi_koalicija_su_vise_distancirani and not cvorovi_anti_koalicija_su_vise_distancirani:
        print("Koalicije i anti-koalicije se generalno ne razlikuju po distanciranosti cvorova")
    elif cvorovi_koalicija_su_vise_distancirani:
        print("Cvorovi koalicija su vise distancirani u odnosu na cvorove anti-koalicija")
    else:
        print("Cvorovi anti-koalicija su vise distancirani u odnosu na cvorove koalicija")


def proveri_(arr1, arr2):
    for score1 in arr1:
        for score2 in arr2:
            if score1 < score2:
                return False
    return True


def proveri_POSEBNO(arr1, arr2):
    score1 = sum(arr1)/len(arr1)
    score2 = sum(arr2)/len(arr2)
    if score1 < score2:
        return True
    else:
        return False


def racunaj_metrike_za_(set_of_cluster):
    arr = {'average_degree': [], 'network_density': [], 'diameter': [], 'average_distance': []}
    for cluster in set_of_cluster:
        tmp = prosecan_stepen(cluster)
        if tmp != 0:
            tmp = math.log10(tmp)
        arr['average_degree'].append(tmp)  # Sa ili bez math.log10()?
        arr['network_density'].append(gustina_mreze(cluster))               # Ne treba math.log10()
        tmp = dijametar(cluster)
        if tmp != 0:
            tmp = math.log10(tmp)
        arr['diameter'].append(tmp)
        tmp = prosecna_distanca(cluster)
        if tmp != 0:
            tmp = math.log10(tmp)
        arr['average_distance'].append(tmp)
    return arr


def prosecan_stepen(cluster = nx.Graph()):
    ukupno = 0
    for node in cluster.nodes:
        ukupno += cluster.degree(node)
    return ukupno*1.0/len(cluster.nodes)


def gustina_mreze(cluster):  # prosecan_stepen,
    p_stepen = prosecan_stepen(cluster)
    if p_stepen == 0:
        return 1
    if math.log10(p_stepen) < math.log10(len(cluster.nodes) - 1):  # strogo manje...(pa ubacen log...)
        return 1
    else:
        return 0


def dijametar(cluster):
    return nx.diameter(cluster)


def prosecna_distanca(cluster):
    # ukupna_distanca = 0
    # for x, y in cluster.nodes:
    #     if nx.has_path(cluster, x, y):
    #         ukupna_distanca += nx.shortest_path_length(cluster, x, y)
    return nx.average_shortest_path_length(cluster)
