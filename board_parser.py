import numpy as np

class Board_Parser:

    def __init__(self, received_data):

        self.received_data = received_data

        self.board_data = np.array(self.received_data['boardInfo'])
        print('Board Data: ')
        print(self.board_data)

        self.my_zombies = np.argwhere(self.board_data == self.received_data['yourID'])
        print('My Zombies: ')
        print(self.my_zombies)

        self.opponent_zombies = np.argwhere(self.board_data == (3 - self.received_data['yourID']))
        print('Opponent Zombies: ')
        print(self.opponent_zombies)

        self.block_cells = np.argwhere(self.board_data == -1)
        print('Block Cells: ')
        print(self.block_cells)
        
        self.open_cells = np.argwhere(self.board_data == 0)
        print('Open Cells: ')
        print(self.open_cells)