import networkx as nx
from networkx.algorithms import chains, components


def get_n_entry(dg):
    return dict(dg.in_degree())


def get_n_exit(dg):
    return dict(dg.out_degree())


def get_diff_entry_exit(dg):
    diff_dict = {}
    out_degrees = dict(dg.out_degree())
    # print("node\t\t:absolute diff")
    for node, in_degree in dg.in_degree():
        diff = abs(in_degree-out_degrees[node])
        # print(f"{node}\t:{diff}")
        diff_dict[node] = diff
    return diff_dict


def get_gatekeeper_degree(dg):
    gatekeeper_dgree_dict = {}
    out_degrees = dict(dg.out_degree())
    # print("node\t\t:degree gatekeeper")
    for node, in_degree in dg.in_degree():
        gatekeeper = in_degree * out_degrees[node]
        gatekeeper_dgree_dict[node] = gatekeeper
    return gatekeeper_dgree_dict


def calc_degree_centralities(dg):
    degree_centers = nx.degree_centrality(dg)
    return {k:v for k,v in sorted(degree_centers.items(), key=lambda x:x[1], reverse=True)}


def calc_close_centralities(dg):
    close_centers = nx.closeness_centrality(dg)
    return {k:v for k,v in sorted(close_centers.items(), key=lambda x:x[1], reverse=True)}


def calc_between_centralities(dg):
    between_centers = nx.betweenness_centrality(dg)
    return {k:v for k,v in sorted(between_centers.items(), key=lambda x:x[1], reverse=True)}


def calc_eigen_centralities(dg):
    eigen_centers = nx.eigenvector_centrality_numpy(dg)
    return {k:v for k,v in sorted(eigen_centers.items(), key=lambda x:x[1], reverse=True)}


def get_elongation(dg):
    """伸長度の算出
    
    Arguments:
        dg {DirectedGraph} -- 有向グラフインスタンス
    
    Returns:
        dict -- ノードIDと伸長度の辞書
    """
    elogation_dict = {}
    for source, target_dict in nx.shortest_path_length(dg):
        max_length = 0
        for target, length in target_dict.items():
            if max_length < length:
                max_length = length
        elogation_dict[source] = max_length
    return elogation_dict


def get_degree_expansion(dg):
    """拡張度の算出
    
    Arguments:
        dg {DirectedGraph} -- 有向グラフのインスタンス
    
    Returns:
        dict -- ノードIDと拡張度の辞書
    """
    expansion_dict = {}
    for node in dg.nodes():
        expansion_dict[node] = len(nx.shortest_path(dg, node))-1
    return expansion_dict