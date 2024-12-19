import matplotlib.pyplot as plt
import networkx as nx

def plot_hex_game(board_state, graphs_train, graph_id, board_size):
    G = nx.Graph()
    
    scale_factor = 20 
    hex_width = 2  
    hex_height = 3 ** 0.5
    
    positions = {}
    for row in range(board_size):
        for col in range(board_size):
            node_name = f"Node_{row}_{col}"
            G.add_node(node_name)

            positions[node_name] = (
                (col + row * 0.5) * hex_width * scale_factor,  
                -row * hex_height * scale_factor           
            )

    for row in range(board_size):
        for col in range(board_size):
            node_name = f"Node_{row}_{col}"
            neighbors = [
                (row - 1, col + 1),  
                (row - 1, col),      
                (row, col - 1),      
                (row, col + 1),      
                (row + 1, col + 1),  
                (row + 1, col + 2)   
                ]
            for n_row, n_col in neighbors:
                if 0 <= n_row < board_size and 0 <= n_col < board_size:
                    neighbor_name = f"Node_{n_row}_{n_col}"
                    G.add_edge(node_name, neighbor_name)

    fig, ax = plt.subplots(figsize=(12, 10))
    nx.draw(
        G,
        pos=positions,
        with_labels=False,
        node_size=1500,  
        node_color="lightblue",
        edge_color="gray",
        ax=ax
    )

    for row, line in enumerate(board_state):
        for col, symbol in enumerate(line):
            node_name = f"Node_{row}_{col}"
            if symbol == "X":
                ax.text(
                    positions[node_name][0],
                    positions[node_name][1],
                    "X",
                    fontsize=20,
                    ha="center",
                    va="center",
                    color="red",
                    fontweight="bold",
                )
            elif symbol == "O":
                ax.text(
                    positions[node_name][0],
                    positions[node_name][1],
                    "O",
                    fontsize=20,
                    ha="center",
                    va="center",
                    color="blue",
                    fontweight="bold",
                )

    ax.set_title(f"Hex Game - Graph {graph_id}")
    ax.axis("off")
    plt.savefig(f"hex_game_graph_{graph_id}.png", dpi=300, bbox_inches='tight')
    plt.show()
