##### SPL 5 Python Starter bot

"""
# coding: utf-8

# #### About bot

#Language          : Python
#Version           : 3.7
#Logic             : Responds with hardcoded value

"""

##### Let's import some modules first

import socket
import json
import time
import random
import numpy as np
from board_parser import *
from pprint import pprint

##### Place to configure TCP

IP    = 'localhost'#'127.0.0.1'
PORT  = 2018


##### Low-Level functions to interact with SBOX

def sbox_connect(ip=IP, port=PORT):  
    """
    Connects to the SBOX and returns the socket
    """
    soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((ip, port))
    return soc

def receive_all(soc, length):
    """
    Function to recv n bytes or return None if EOF is hit
    """
    data = b''
    while len(data) < length:
        packet = soc.recv(length - len(data))
        if not packet:
            return None
        data += packet
    return data

def get_data(soc):
    """
    receives data from sbox and returns it as a dictionary
    """
    #soc.settimeout(2)
    size=soc.recv(4)
    #soc.settimeout(None)
    
    if size:
        length=int.from_bytes(size, byteorder='big')
        data_from_server = receive_all(soc, length)
        data_dict = json.loads(data_from_server)
        return data_dict
    else:
        return {}
    
def send_data(soc, data):
    """
    formats and sends the given dictionary to the sbox
    """
    msg = json.dumps(data).encode('utf-8')
    soc.send(len(msg).to_bytes(4, byteorder='big'))
    soc.send(msg)


def get_neighbours(board, position, dist, targetID):
    row_start = max(position[0]-dist,0)
    row_end = min(position[0]+dist,board.shape[0]-1) + 1
    col_start = max(position[1]-dist,0)
    col_end = min(position[1]+dist,board.shape[1]-1) + 1
    return [(neighbour[0]+row_start,neighbour[1]+col_start) \
            for neighbour in zip(*np.where(board[row_start:row_end, col_start:col_end] == targetID))]


#Driver code

while True:  #Loop to reconnect to SBOX if disconnected
    try:
        soc = sbox_connect()
        while True:   #Game loop
            received_data = get_data(soc)

            print ("*"*100)
            print ("SBOX >>> BOT : ", received_data)
            

            if not received_data:
                raise Exception("No Response from Server")

            if received_data["dataType"] == "authentication":
                #You've to respond with the one time password
                response = {"dataType": "oneTimePassword", 
                            "oneTimePassword":received_data["oneTimePassword"]}

            elif received_data["dataType"] == "command":
                if received_data["dataExpected"] == "move":
                                                            
                    def ret_pos_moves(el):
                        pass_dict = {}
                        pass_dict["Empty"] = get_neighbours(board.board_data, el, 2, 0)
                        pass_dict["Block"] = get_neighbours(board.board_data, el, 2, -1)
                        pass_dict["Opp_Zom"] = get_neighbours(board.board_data, el, 2, 2)
                        pass_dict["My_Zom"] = get_neighbours(board.board_data, el, 2, 1)
                        return pass_dict





                    board = Board_Parser(received_data)
                    # board.possible_moves()
                    my_moves = []
                    my_moves = [ dict((el, ret_pos_moves(el)) for el in board.my_zombies)]                   
                    pprint("Hey Wassup: "+str(my_moves))
                    
                    











                    print('Hello: ' + str(get_neighbours(board.board_data, board.my_zombies[0], 2, 0)))
                    # print('Possible moves: ' + str(board.clone))
                    #You've to respond with your move
                    from_cell = list(map(int, board.my_zombies[0]))
                    to_cell = list(map(int, get_neighbours(board.board_data, board.my_zombies[0], 2, 0)[0]))
                    response = {"dataType":"response","fromCell":from_cell, "toCell": to_cell}
                    print(response)


            elif received_data["dataType"] == "acknowledge":
                #You've got the acknowledgement
                continue

            elif received_data["dataType"] == "result":
                #You've got the result
                continue

            else:
                #You've got something else!!
                continue


            send_data(soc, response)
            print ("BOT >>> SBOX : ", response)
            #time.sleep(0.2)
            
    except KeyboardInterrupt:
        try:
            if soc:
                soc.close()
        except: pass
        print("BOT Stopped Manually!!")
        break

    except Exception as e:
        #Handle Exceptions here
        raise e
        try:
            if soc:
                soc.close()
        except: pass
        print("EXCEPTION",e) 
