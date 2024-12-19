import numpy as np
import time
from Hex_game import HexGame
from Prepare_Hex_Data import extract_features_list, extract_features
from Graph_T_init_ import Graph_Tsetlin_init_
from GraphTsetlinMachine.tm import GraphTsetlinMachine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from visualize import plot_hex_game


clauses = 1 #1, 10, 50, 100, 500, 1000, 5000, 10000
BOARD_DIM = 3 # 3, 9, 27
total_graphs = 1000
s = 0.6
threshold = 7000
num_games = 10
depth = 1

print("Generate game data...")
graphs, hex_data, graph_ids = Graph_Tsetlin_init_(total_graphs, BOARD_DIM, num_games)

print("Prepare game data...")
game_states = [game[0] for game in hex_data]

features = extract_features_list(
    game_states,
    graphs,
    graph_ids
)
labels = np.array([game[1] for game in hex_data])

graph_ids = np.array(graph_ids, dtype=np.int32)

data_indices = np.arange(len(features))

print("Spliting game data...")
train_indices, test_indices, y_train, y_test = train_test_split(
    data_indices, labels, test_size=0.2, random_state=50
)

print("Initial Tsetlin machine...")
TM = GraphTsetlinMachine(
    number_of_clauses=clauses,
    T=threshold,
    s=s,
    depth=depth,
    message_size=284,
    message_bits=2
)

print("Train...")
start_time = time.time()
TM.fit(graphs, features[train_indices]) 
training_time = (time.time() - start_time) / 60

print("Evaluate...")
predictions = TM.predict(graphs)

expanded_predictions = np.repeat(predictions, num_games)

test_features = features[test_indices]

predictions_test = expanded_predictions[test_indices]

accuracy = accuracy_score(y_test, predictions_test) * 100
print(f"Modellens nøyaktighet: {accuracy:.2f}%")

num_graphs_to_plot = 5 

for i in range(num_graphs_to_plot):
    board_state, winner = hex_data[i]
    plot_hex_game(board_state, graphs, graph_ids[i], BOARD_DIM)

# Logg resultater
with open("3x3_Results_end_game.txt", "a") as log_file:
    log_file.write("-----------------------------------------\n")
    log_file.write("Result for HEXGAME\n")
    log_file.write("-----------------------------------------\n")
    log_file.write(f"Training time: {training_time:.2f} min\n")
    log_file.write(f"Boardsize: {BOARD_DIM}x{BOARD_DIM}\n")
    log_file.write(f"Acurracy: {accuracy:.2f}%\n")
    log_file.write(f"Clauses: {clauses}\n")
    log_file.write(f"Threshold (T): {threshold}\n")
    log_file.write(f"s-value: {s}\n")
    log_file.write("\n")


