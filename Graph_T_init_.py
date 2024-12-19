from joblib import Parallel, delayed
import numpy as np
import random
from Hex_game import HexGame
from GraphTsetlinMachine.graphs import Graphs

def generate_game_data(graph_id, num_games, board_size):
    hex_data = []
    graph_ids = []

    for i in range(num_games):
        game = HexGame(board_size)
        current_player = 0
        winner_game = None

        while not game.hg_full_board():
            position = game.hg_place_piece_randomly(current_player)
            if game.hg_winner(current_player, position):
                winner_game = current_player
                break
            current_player = 1 - current_player

        board_state = game.state_end() #state_two_before_end(),state_five_before_end() 
        hex_data.append((board_state, winner_game))
        graph_ids.append(graph_id)
    
    return hex_data, graph_ids

def Graph_Tsetlin_init_(total_graphs, board_size, num_games):
    graphs_train = Graphs(
        number_of_graphs=total_graphs,
        symbols=['X', 'O', '.'],
        hypervector_size = 644, 
        hypervector_bits = 2
    )

    graphs_train.signature = np.random.rand(total_graphs)

    for graph_id in range(total_graphs):
        num_nodes = board_size * board_size
        graphs_train.set_number_of_graph_nodes(graph_id, num_nodes)

    graphs_train.prepare_node_configuration()

    for graph_id in range(total_graphs):
        for row in range(board_size):
            for col in range(board_size):
                neighbors = [
                    (row - 1, col + 1),
                    (row - 1, col), 
                    (row, col - 1), 
                    (row, col + 1), 
                    (row + 1, col - 1), 
                    (row + 1, col)
                    ]
                num_neighbors = sum(
                    0 <= n_row < board_size 
                    for n_row, n_col in neighbors 
                    if 0 <= n_col < board_size
                )

                node_name = f"Node_{row}_{col}"
                graphs_train.add_graph_node(graph_id, node_name, num_neighbors)

        graphs_train.prepare_edge_configuration()
        edge_set = set()

        for row in range(board_size):
            for col in range(board_size):
                node_name = f"Node_{row}_{col}"
                neighbors = [
                    (row - 1, col + 1), 
                    (row - 1, col),
                    (row, col - 1),
                    (row, col + 1), 
                    (row + 1, col - 1),
                    (row + 1, col) 
                    ]

                for n_row, n_col in neighbors:
                    if 0 <= n_row < board_size and 0 <= n_col < board_size:
                        neighbor_name = f"Node_{n_row}_{n_col}"
                        edge_key = tuple(sorted((node_name, neighbor_name)))

                        if edge_key not in edge_set:
                            edge_set.add(edge_key)
                            graphs_train.add_graph_node_edge(graph_id, node_name, neighbor_name, "Plain")

    choices = np.random.choice(['X', 'O', '.'], size=(total_graphs, board_size * board_size))
    for graph_id in range(total_graphs):
        for row in range(board_size):
            for col in range(board_size):
                node_index = row * board_size + col
                node_property = choices[graph_id, node_index]
                node_name = f"Node_{row}_{col}"
                graphs_train.add_graph_node_property(graph_id, node_name, node_property)

    hex_data = []
    graph_ids = []

    for graph_id in range(total_graphs):
        games, ids = generate_game_data(graph_id, num_games, board_size)
        hex_data.extend(games)
        graph_ids.extend(ids)

    print(f"Antall genererte grafer: {total_graphs}")
    print(f"Antall genererte spill: {len(hex_data)}")

    return graphs_train, hex_data, graph_ids








