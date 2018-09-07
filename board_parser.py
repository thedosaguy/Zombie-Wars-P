import numpy as np

class Board_Parser:

    def __init__(self, received_data):

        self.clone = []

        self.received_data = received_data

        self.board_data = np.array(self.received_data['boardInfo'])
        self.size = self.board_data.shape[0]
        print('Size of board: ' + str(self.size))
        # print('Board Data: ')
        # print(self.board_data)

        self.my_zombies = np.argwhere(self.board_data == self.received_data['yourID'])
        self.my_zombies = [tuple(l) for l in self.my_zombies]
        # print('My Zombies: ')
        # print(self.my_zombies)

        self.opponent_zombies = np.argwhere(self.board_data == (3 - self.received_data['yourID']))
        # print('Opponent Zombies: ')
        # print(self.opponent_zombies)

        self.block_cells = np.argwhere(self.board_data == -1)
        # print('Block Cells: ')
        # print(self.block_cells)
        
        self.open_cells = np.argwhere(self.board_data == 0)
        # print('Open Cells: ')
        # print(self.open_cells)

    def get_neighbours(self, position, dist, targetID):
        row_start = max(position[0]-dist,0)
        row_end = min(position[0]+dist,self.board_data.shape[0]-1) + 1
        col_start = max(position[1]-dist,0)
        col_end = min(position[1]+dist,self.board_data.shape[1]-1) + 1
        return [(neighbour[0]+row_start,neighbour[1]+col_start) \
                for neighbour in zip(*np.where(self.board_data[row_start:row_end, col_start:col_end] == targetID))]

    def possible_moves(self):

        self.block_cells = self.block_cells.tolist()
        for my_zombie in self.my_zombies:
            self.clone = []
            self.jump = []
            # print('My Zombie: ' + str(my_zombie))
            y = my_zombie[0]
            x = my_zombie[1]
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        pass
                    elif x+dx < 0 or x+dx >= self.size or y+dy < 0 or y+dy >= self.size:
                        pass
                    else:
                        self.clone.append([x+dx, y+dy])
            # print('Clone cells: ' + str(self.clone))
            # print('Blocked cells: ' + str(self.block_cells))
            for cell in self.clone:
                if cell in self.block_cells:
                    self.clone.remove(cell)

            print(str(my_zombie) + ': '  + str(self.clone))
        
            for dx in [-2, 0, 2]:
                for dy in [-2, 0, 2]:
                    if dx == 0 and dy == 0:
                        pass
                    elif x+dx < 0 or x+dx >= self.size or y+dy < 0 or y+dy >= self.size:
                        pass
                    else:
                        self.jump.append([x+dx, y+dy])
            # print('Clone cells: ' + str(self.clone))
            # print('Blocked cells: ' + str(self.block_cells))
            for cell in self.jump:
                if cell in self.block_cells:
                    self.clone.remove(cell)

            print(str(my_zombie) + ': '  + str(self.clone))
            
        # self.clone = np.array(self.clone)
        # self.block_cells = np.array(self.block_cells)
       
            