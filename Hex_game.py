import random

class HexGame:
    def __init__(self, BOARD_DIM):
        
        self.BOARD_DIM = BOARD_DIM

        self.neighbors = [-(BOARD_DIM + 2) + 1, -(BOARD_DIM + 2), -1, 1, (BOARD_DIM + 2), (BOARD_DIM + 2) - 1]

    
        size = (BOARD_DIM + 2) * (BOARD_DIM + 2) * 2
        self.board = [[0 for _ in range(size)] for i in range(2)]
        
        self.open_positions = [0] * (BOARD_DIM * BOARD_DIM)
        self.number_of_open_positions = BOARD_DIM * BOARD_DIM
        
        self.moves = []  
        self.connected = [[0 for _ in range(size)] for _ in range(2)]

        self.hg_init()

    def hg_init(self):
      
        for i in range(self.BOARD_DIM + 2): # Rows
            for j in range(self.BOARD_DIM + 2): # Column
                idx = i * (self.BOARD_DIM + 2) + j
                
                self.board[0][idx] = 0
                self.board[1][idx] = 0
                if 0 < i <= self.BOARD_DIM and 0 < j <= self.BOARD_DIM:
                    index = (i - 1) * self.BOARD_DIM + (j - 1)
                    self.open_positions[index] = idx

                self.connected[0][idx] = 1 if i == 0 else 0
                self.connected[1][idx] = 1 if j == 0 else 0

        self.number_of_open_positions = self.BOARD_DIM * self.BOARD_DIM
        self.moves = []  # Resetter listen over trekk

    def hg_connect(self, player, position):

        self.connected[player][position] = 1
        if player == 0 and position // (self.BOARD_DIM + 2) == self.BOARD_DIM:
            return True
        if player == 1 and position % (self.BOARD_DIM + 2) == self.BOARD_DIM:
            return True

        for i in range(6):
            neighbor = position + self.neighbors[i]
            if self.board[player][neighbor] and not self.connected[player][neighbor]:
                if self.hg_connect(player, neighbor):
                    return True
        return False

    def hg_winner(self, player, position):
        for i in range(6):
            neighbor = position + self.neighbors[i]
            if self.connected[player][neighbor]:
                return self.hg_connect(player, position)
        return False

    def hg_place_piece_randomly(self, player):
    
        random_empty_position_index = random.randint(0, self.number_of_open_positions - 1)
        empty_position = self.open_positions[random_empty_position_index]

        self.board[player][empty_position] = 1
        self.moves.append((player, empty_position))  

       
        self.open_positions[random_empty_position_index] = self.open_positions[self.number_of_open_positions - 1]
        self.number_of_open_positions -= 1
        return empty_position

    def hg_full_board(self):
      
        return self.number_of_open_positions == 0

    def hg_print(self):
        
        for i in range(self.BOARD_DIM):
            print(" " * i, end="")
            for j in range(self.BOARD_DIM):
                idx = self.get_idx(i, j)
                if self.board[0][idx] == 1:
                    print(" X", end="")
                elif self.board[1][idx] == 1:
                    print(" O", end="")
                else:
                    print(" .", end="")  # Tom celle
            print()

    def get_idx(self, i, j):
 
        row_number = i + 1  
        col_number = j + 1 
        return row_number * (self.BOARD_DIM + 2) + col_number

    def state(self):
        
        board_state = [] 

        for i in range(self.BOARD_DIM):
            row = [] 
            for j in range(self.BOARD_DIM): 
                idx = self.get_idx(i, j)

                
                if self.board[0][idx] == 1:
                    row.append('X') 
                elif self.board[1][idx] == 1:
                    row.append('O')
                else:
                    row.append('.')
                    
            board_state.append(row) 

        return board_state
        

    def state_end(self):

        if not self.moves:
            return self.state
      
        last_move = self.moves[-1]
        player, position = last_move
        self.board[player][position] = 0
        self.open_positions.append(position)
        self.number_of_open_positions += 1

        board_state = self.state()

        self.board[player][position] = 1
        self.open_positions.remove(position)
        self.number_of_open_positions -= 1
        self.moves.append(last_move)

        return board_state
        
    def state_two_before_end(self):
        if len(self.moves) < 2:
            return self.state()
    
        two_last_moves = self.moves[-2:]
    
        board_state_two_before_end = self.state()
    
        for move in reversed(two_last_moves):
            player, position = move
            self.board[player][position] = 0 
            self.open_positions.append(position)
            self.number_of_open_positions += 1
            self.moves.pop()  
    
        board_state_two_before_end = self.state()
    
        for move in two_last_moves:
            player, position = move
            self.board[player][position] = 1  
            self.open_positions.remove(position)  
            self.number_of_open_positions -= 1
            self.moves.append(move)  

        return board_state_two_before_end

        
    def state_five_before_end(self):
        if len(self.moves) < 5:
            return self.state()
    
        five_last_moves = self.moves[-5:]
    
        board_state_five_before_end = self.state()
    
        for move in reversed(five_last_moves):
            player, position = move
            self.board[player][position] = 0 
            self.open_positions.append(position) 
            self.number_of_open_positions += 1
            self.moves.pop()  
    
        board_state_five_before_end = self.state()
    
        for move in five_last_moves:
            player, position = move
            self.board[player][position] = 1  
            self.open_positions.remove(position) 
            self.number_of_open_positions -= 1
            self.moves.append(move)

        return board_state_five_before_end

