import numpy as np
import time
import pandas as pd

def extract_features(board_state, graphs_train, graph_id):
    numb_symbol = {'X': 1, 'O': 0, '.': -1}
        
    features = []
        
    for row in board_state:
        for symbol in row:
            features.append(numb_symbol[symbol])
        
    if graph_id < graphs_train.number_of_graphs:
       
        start_index = graphs_train.edge_index[graph_id]
        end_index = graphs_train.edge_index[graph_id + 1]
        
        num_edges = end_index - start_index

    else:
        num_edges = 0 
        
    features.append(num_edges)
        
    return np.array(features)

def extract_features_list(board_states, graphs_train, graph_ids):
    features_list = []
    for board_state, graph_id in zip(board_states, graph_ids):
        features = extract_features(board_state, graphs_train, graph_id)
        features_list.append(features)
    return np.array(features_list)


