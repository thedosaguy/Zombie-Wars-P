
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

##### Place to configure TCP

ip    = 'localhost'#'127.0.0.1'
port  = 2018


##### Low-Level functions to interact with SBOX

def sbox_connect(ip=ip, port=port):  
    """
    Connects to the SBOX and returns the socket
    """
    soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((ip,port))
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
    
def send_data(soc,data):
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
                    #You've to respond with your move
                    response = {"dataType":"response","fromCell":[0,0], "toCell": [1,1]}


            elif received_data["dataType"] == "acknowledge":
                #You've got the acknowledgement
                continue

            elif received_data["dataType"] == "result":
                #You've got the result
                continue

            else:
                #You've got something else!!
                continue


            send_data(soc,response)
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
        try:
            if soc:
                soc.close()
        except: pass
        print("EXCEPTION",e) 
