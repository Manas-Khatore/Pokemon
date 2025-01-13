import pandas as pd
import networkx as nx
import math
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

pk_type_chart = pd.read_csv("Pokemon Type Chart.csv")
pk_type_chart = pk_type_chart.rename(columns={"Unnamed: 0": "Type"})

pokemon_data = pd.read_csv("pokemon.csv")
pokemon_data = pokemon_data[["name", "type1", "type2"]]

type_list = list(pk_type_chart.columns)[1:]
pk_type_chart_melt = pd.melt(pk_type_chart, id_vars='Type', value_vars=type_list)
pk_type_chart_melt = pk_type_chart_melt.rename(columns={"Type": "Type 1", "variable": "Type 2", "value": "weight"})
pk_type_chart_no_neutral = pk_type_chart_melt[pk_type_chart_melt["weight"] != 1]

pk_type_chart_effective = pk_type_chart_no_neutral[pk_type_chart_no_neutral["weight"] == 2] # super effective
pk_type_chart_not_effective = pk_type_chart_no_neutral[pk_type_chart_no_neutral["weight"] == 0.5] # not very effective
pk_type_chart_immunity = pk_type_chart_no_neutral[pk_type_chart_no_neutral["weight"] == 0]

Effective_Attack_Graph = nx.from_pandas_edgelist(pk_type_chart_effective, "Type 1", "Type 2", create_using=nx.DiGraph())
Weakness_Graph = nx.from_pandas_edgelist(pk_type_chart_effective, "Type 2", "Type 1", create_using=nx.DiGraph())
Not_Effective_Graph = nx.from_pandas_edgelist(pk_type_chart_not_effective, "Type 1", "Type 2", create_using=nx.DiGraph())
Resistance_Graph = nx.from_pandas_edgelist(pk_type_chart_not_effective, "Type 2", "Type 1", create_using=nx.DiGraph())
Immunity_Graph = nx.from_pandas_edgelist(pk_type_chart_immunity, "Type 2", "Type 1", create_using=nx.DiGraph())

def create_graph_visual(Graph, graph_name):
    # dictionary of each type and its out degree
    graph_dict = dict(Graph.out_degree())
    graph_dict = dict(sorted(graph_dict.items(), key=lambda x:x[1], reverse=True))

    # creating color coding for each of the nodes according to their out degree
    # used the OrRd colormap -- darker reds correspond to a larger out degree
    norm = mcolors.Normalize(vmin=min(graph_dict.values()), vmax=max(graph_dict.values()))
    colormap = plt.cm.OrRd
    node_colors = [colormap(norm(graph_dict[node])) for node in Graph.nodes()]

    # representing the graph in Kamada-Kawai Layout
    fig, axes = plt.subplots(1, 2, figsize=(12, 6)) 
    nx.draw_networkx(Graph, ax=axes[0], pos=nx.kamada_kawai_layout(Graph), with_labels=True, arrows=True, arrowstyle='-|>', node_size=700, font_size=9,
                    node_color=node_colors)
    axes[0].set_title(f"{graph_name} - Kamada Kawai Layout")

    # representing the graph in Spring Layout
    nx.draw_networkx(Graph, ax=axes[1], pos=nx.spring_layout(Graph), with_labels=True, arrows=True, arrowstyle='-|>', node_size=700, font_size=9,
                    node_color=node_colors)
    axes[1].set_title(f"{graph_name} - Spring Layout")

    # plotting the graphs
    plt.tight_layout()
    plt.show()

    graph_df = pd.DataFrame.from_dict({"Type": list(graph_dict.keys()), "Out Degree": list(graph_dict.values())})
    print(graph_df)

def type_categorize(pokemon_name):
    pok = pokemon_data[pokemon_data["name"] == pokemon_name]
    pok_types = [list(pok["type1"])[0], list(pok["type2"])[0]]
    if type(pok_types[1]) is not str: # if the Pokemon only has one typing
        pok_types.pop()
    
    weaknesses_list = []
    resistance_list = []
    immunity_list = []
    
    for t in pok_types:
        t = t.capitalize()
        weaknesses_list.extend(list(Weakness_Graph.successors(t))) # using the graphs created earlier to derive the weaknesses of that typing
        resistance_list.extend(list(Resistance_Graph.successors(t))) # same for resistances
        if Immunity_Graph.has_node(t):
            immunity_list.extend(list(Immunity_Graph.successors(t))) # same for immunities

    # dictionaries are used to account for the strength of a resistance/weakness
    # if a type appears twice in the resistance list, the Pokemon is double-resistant to that specific type
    weakness_dict = Counter(weaknesses_list)
    resistance_dict = Counter(resistance_list)
    immunity_dict = Counter(immunity_list)
    
    weakness_dict_keys = list(weakness_dict.keys())
    
    for t in weakness_dict_keys: # removing types entirely that were categorized as both a weakness and resistance (balancing out)
        if t in resistance_dict:
            del weakness_dict[t]
            del resistance_dict[t]
    
    for t in immunity_dict: # removing types from the weakness/resistance dictionaries if a Pokemon is immune to it
        if t in weakness_dict:
            del weakness_dict[t]
        if t in resistance_dict:
            del resistance_dict[t]
    
    return [weakness_dict, resistance_dict, immunity_dict, pok_types]

def draw_type_relationship(pokemon_name):
    dict_list = type_categorize(pokemon_name)
    weaknesses = dict_list[0]
    resistances = dict_list[1]
    immunities = dict_list[2]
    pok_types = dict_list[3]
    
    color_map = {pokemon_name: 'lightblue'}
    graph_edge_list = []
    
    G = nx.DiGraph()
    
    for weak in weaknesses:
        # print(weaknesses[weak])
        graph_edge_list.append((pokemon_name, weak, weaknesses[weak] ** 2))
        color_map[weak] = '#fd7a5e'
    
    for resis in resistances:
        graph_edge_list.append((pokemon_name, resis, resistances[resis] ** 2))
        color_map[resis] = '#5efd91'
    
    for immun in immunities:
        graph_edge_list.append((pokemon_name, immun, immunities[immun] ** 2))
        color_map[immun] = '#bdbdbd'
    
    G.add_weighted_edges_from(graph_edge_list)
    node_colors = [color_map[node] for node in G.nodes]
    weights = nx.get_edge_attributes(G, "weight")
    edge_widths = [weight for (u, v, weight) in G.edges(data="weight")]
    
    fig = plt.figure()
    nx.draw(G, with_labels=True, node_color=node_colors, node_size = 1500, width=edge_widths, ax=fig.add_subplot())

    if len(pok_types) == 2:
        plt.title(f"{pokemon_name} - {pok_types[0].capitalize()}/{pok_types[1].capitalize()}")
    else:
        plt.title(f"{pokemon_name} - {pok_types[0].capitalize()}")
    return fig

def populate_dict(pokemon, weak_dict, resist_dict, immune_dict):
    cat_list = type_categorize(pokemon)
    for pk_type in cat_list[0].keys(): # adding pokemon's weaknesses
        weak_dict[pk_type].append(pokemon)
    
    for pk_type in cat_list[1].keys(): # adding pokemon's resistances
        resist_dict[pk_type].append(pokemon)

    for pk_type in cat_list[2].keys(): # adding pokemon's immunities
        immune_dict[pk_type].append(pokemon)
    
    return [weak_dict, resist_dict, immune_dict]

def team_categorize(pokemon_team):
    ## TODO: pokemon_team is a list of pokemon
    ## TODO: feed each pokemon into type_categorize function
    ## TODO: tally the resistances and weaknesses of team
    ## TODO: display biggest resistances/weaknesses and all pokemon associated with each
    weaknesses_dict = {key: [] for key in type_list} # key: pokemon, value: list of weaknesses
    resistances_dict = {key: [] for key in type_list}
    immunities_dict = {key: [] for key in type_list}

    for pok in pokemon_team:
        if pok != '':
            dict_list = populate_dict(pok, weaknesses_dict, resistances_dict, immunities_dict)
            weaknesses_dict, resistances_dict, immunities_dict = dict_list[0], dict_list[1], dict_list[2]
    
    sorted_weaknesses = sorted(weaknesses_dict, key=lambda k: len(weaknesses_dict[k]))
    sorted_resistances = sorted(resistances_dict, key=lambda k: len(resistances_dict[k]))
    sorted_immunities = sorted(immunities_dict, key=lambda k: len(immunities_dict[k]))

    return [sorted_weaknesses, sorted_resistances, sorted_immunities]
        
    