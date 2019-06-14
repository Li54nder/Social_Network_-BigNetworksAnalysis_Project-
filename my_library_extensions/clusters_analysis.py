import networkx as nx
import math


def analysis(coalition, anti_coalition):

    print("\nAnaliziranje sličnosti i razlike u strukturi koalicija i anti-koalicija...\n")

    coalitions_score = calculate_metics_of(coalition)
    anti_coalitions_score = calculate_metics_of(anti_coalition)

    coalitions_are_more_cohesive = check_1(coalitions_score['average_degree'], anti_coalitions_score['average_degree'])
    anti_coalitions_are_more_cohesive = check_1(anti_coalitions_score['average_degree'], coalitions_score['average_degree'])

    coalitions_are_relatively_rare = check_2(coalitions_score['network_density'], anti_coalitions_score['network_density'])
    anti_coalitions_are_relatively_rare = check_2(anti_coalitions_score['network_density'], coalitions_score['network_density'])

    anti_coalitions_have_a_smaller_diameter = check_1(coalitions_score['diameter'], anti_coalitions_score['diameter'])
    coalitions_have_a_smaller_diameter = check_1(anti_coalitions_score['diameter'], coalitions_score['diameter'])

    nodes_of_coalitions_are_more_distant = check_1(coalitions_score['average_distance'], anti_coalitions_score['average_distance'])
    nodes_of_anti_coalitions_are_more_distant = check_1(anti_coalitions_score['average_distance'], coalitions_score['average_distance'])

    if not coalitions_are_more_cohesive and not anti_coalitions_are_more_cohesive:
        print("Koalicije i anti-koalicije se generalno ne razlikuju po kohezivnosti")
    elif coalitions_are_more_cohesive:
        print("Koalicije su kohezivnije mreze")
    else:
        print("Anti-koalicije su kohezivnije mreze")

    if not coalitions_are_relatively_rare and not anti_coalitions_are_relatively_rare:
        print("Koalicije i anti-koalicije se generalno ne razlikuju po gustini mreze")
    elif coalitions_are_relatively_rare:
        print("Koalicije su redje mreze od anti-koalicija")
    else:
        print("Anti-koalicije su redje mreze od koalicija")

    if not coalitions_have_a_smaller_diameter and not anti_coalitions_have_a_smaller_diameter:
        print("Koalicije i anti-koalicije se generalno ne razlikuju po duzini dijametra")
    elif coalitions_have_a_smaller_diameter:
        print("Koalicije imaju manji dijametar")
    else:
        print("Anti-koalicije imaju manji dijametar")

    if not nodes_of_coalitions_are_more_distant and not nodes_of_anti_coalitions_are_more_distant:
        print("Koalicije i anti-koalicije se generalno ne razlikuju po distanciranosti cvorova")
    elif nodes_of_coalitions_are_more_distant:
        print("Cvorovi koalicija su vise distancirani u odnosu na cvorove anti-koalicija")
    else:
        print("Cvorovi anti-koalicija su vise distancirani u odnosu na cvorove koalicija")


def check_1(arr1, arr2):
    for score1 in arr1:
        for score2 in arr2:
            if score1 < score2:
                return False
    return True


def check_2(arr1, arr2):
    score1 = sum(arr1)/len(arr1)
    score2 = sum(arr2)/len(arr2)
    if score1 < score2:
        return True
    else:
        return False


def calculate_metics_of(set_of_cluster):
    arr = {'average_degree': [], 'network_density': [], 'diameter': [], 'average_distance': []}
    for cluster in set_of_cluster:
        tmp = average_degree(cluster)
        if tmp != 0:
            tmp = math.log10(tmp)
        arr['average_degree'].append(tmp)                           # Sa ili bez math.log10()? - sa
        arr['network_density'].append(density_of_network(cluster))  # Ne treba math.log10()
        tmp = diameter_(cluster)
        if tmp != 0:
            tmp = math.log10(tmp)
        arr['diameter'].append(tmp)
        tmp = average_distance(cluster)
        if tmp != 0:
            tmp = math.log10(tmp)
        arr['average_distance'].append(tmp)
    return arr


def average_degree(cluster = nx.Graph()):
    sum = 0
    for node in cluster.nodes:
        sum += cluster.degree(node)
    return sum*1.0/len(cluster.nodes)


def density_of_network(cluster):
    avg_degree = average_degree(cluster)
    if avg_degree == 0:
        return 1
    if math.log10(avg_degree) < math.log10(len(cluster.nodes) - 1):  # strogo manje...(pa ubacen log...)
        return 1
    else:
        return 0


def diameter_(cluster):
    return nx.diameter(cluster)


def average_distance(cluster):
    return nx.average_shortest_path_length(cluster)


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
