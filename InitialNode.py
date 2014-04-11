__author__ = 'Xin'
# 2014.04.07

from NODE import Node
from MyFunction import shift
from random import randint,seed
from itertools import product
from matplotlib.patches import Wedge
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
#seed(255)
import math
from multiprocessing import Process,Queue

# define the variables of InitialNodeArray
RDM_DELAYS = True                     # Random Delay time of simulator
RDM_ARRIVALS = True                   # Random Arrivals time of simulator
RDM_START = True                      # Random Start times of simulator
ARRY_DIMS = 2                      # dimensions of the system,which is 1D or 2D
ARRY_ROW = 10                       # Rows of the Parallel traffic System
ARRY_COLUMN = 10                    # Columns of the Parallel traffic System
ARRY_DIRECTION = 1                 # direction of traffic flow, now is two directions W->E and N->S
DELTA = 100

# Create the NodeArray for the intersections
# initialize NodeArray[i][j] of all intersections

# NodeArray = Node

def InitialNodeArray():
    global NodeArray

    if ARRY_DIMS == 1:
        Node.dx = np.zeros(ARRY_ROW - 1)
        Node.dy = np.zeros(ARRY_COLUMN - 1)
        Node.shiftx = np.zeros(ARRY_ROW - 1, np.int32)
        Node.shifty = np.zeros(ARRY_COLUMN - 1, np.int32)
    elif ARRY_DIMS == 2:
        Node.dx = np.zeros((ARRY_ROW, ARRY_COLUMN-1))
        Node.dy = np.zeros((ARRY_ROW-1, ARRY_COLUMN))
        Node.shiftx = np.zeros((ARRY_ROW, ARRY_COLUMN-1), np.int32)
        Node.shifty = np.zeros((ARRY_ROW-1, ARRY_COLUMN), np.int32)
    else:
        # Warning the error parameters
        pass

    Node.delta = DELTA

    NodeArray = [[Node(x,y) for y in range(ARRY_COLUMN)] for x in range(ARRY_ROW)]

def InitialDistanceNodeToNode():
     # Initialize the distances
    if ARRY_DIMS == 1:
        # 1-D system Row =1 and Column = N
        for j in range(ARRY_COLUMN - 1):
            tmpa = 20
            tmpb = 60
            if RDM_DELAYS:
                tmpa = randint(0, DELTA - 1)
                tmpb = randint(0, DELTA - 1)
            Node.dx[j] = tmpa/DELTA
            Node.shiftx[j] = tmpa
            Node.dy[j] = tmpb/DELTA
            Node.shifty[j] = tmpb
    else:
        for i in range(ARRY_ROW):
            for j in range(ARRY_COLUMN):
                tmpa = 20
                tmpb = 60
                # random delay Mode
                if RDM_DELAYS:
                    tmpa = randint(0, DELTA - 1)
                    tmpb = randint(0, DELTA - 1)
                try:
                    Node.dx[i][j] = tmpa/DELTA
                    Node.shiftx[i][j] = tmpa
                except: pass
                try:
                    Node.dy[i][j] = tmpb/DELTA
                    Node.shifty[i][j] = tmpb
                except:pass

def InitialArrivalTime():
    # initialize arrival time at the intersections
    # Start with the first Row, Set the arrival time from North
    global NodeArray
    for j in range(ARRY_COLUMN):
        # Set the initial value
        NodeArray[0][j].an = 0.6
        if RDM_ARRIVALS:
            NodeArray[0][j].an = randint(0, DELTA-1)/DELTA
        NodeArray[0][j].gotime = NodeArray[0][j].an
        if RDM_START:
            NodeArray[0][j].gotime = randint(0, DELTA - 1)/DELTA

    # Set arrival time from West for the first Column
    for i in range(ARRY_ROW - 1):
        NodeArray[i][0].aw = 0.2
        if RDM_ARRIVALS:
            NodeArray[i][0].aw = randint(0,DELTA - 1)/DELTA
        if ARRY_DIMS == 1:
            NodeArray[i+1][0].an = (NodeArray[i][0].gotime + Node.dy[i])%1
        else:
            NodeArray[i+1][0].an = (NodeArray[i][0].gotime + Node.dy[i][0])%1
        NodeArray[i+1][0].gotime = NodeArray[i+1][0].an

        if RDM_START:
            NodeArray[i+1][0].gotime = randint(0,DELTA-1)/DELTA


    # Set the down bound of arrival time from West for the first Columm
    NodeArray[ARRY_COLUMN - 1][0].aw = 0.2
    if RDM_ARRIVALS:
        NodeArray[ARRY_COLUMN - 1][0].aw = randint(0,DELTA - 1)/DELTA
    # use the midpoint(NodeArray[][0].aw, NodeArray[][0].an)


    # Now Go back to set the arrival time from West to East for the first Row
    for j in range(ARRY_COLUMN - 1):
        if ARRY_DIMS == 1:
            NodeArray[0][j+1].aw = (NodeArray[0][j].gotime + Node.dx[j])%1
        else:
            NodeArray[0][j+1].aw = (NodeArray[0][j].gotime + Node.dx[j][0])%1

    # Initialize arrival time for all other nodes, Setting their gotime

    for i in range(1, ARRY_ROW):
        for j in range(1, ARRY_COLUMN):
            if ARRY_DIMS == 1:
                NodeArray[i][j].an = (NodeArray[i-1][j].gotime + Node.dy[i-1])%1
                NodeArray[i][j].aw = (NodeArray[i][j-1].gotime + Node.dx[j-1])%1
            else:
                NodeArray[i][j].an = (NodeArray[i-1][j].gotime + Node.dy[i-1][j])%1
                NodeArray[i][j].aw = (NodeArray[i][j-1].gotime + Node.dx[i][j-1])%1
            NodeArray[i][j].gotime = NodeArray[i][j].an

            if RDM_START:
                NodeArray[i][j].gotime = randint(0,DELTA-1)/DELTA


 # Calculate the total delaying time
def CalculateDelayTime():
    global NodeArray
    TotalDelay = 0
    for i in range(ARRY_ROW):
        for j in range(ARRY_COLUMN):
            TotalDelay = TotalDelay + NodeArray[i][j].GetDelayTime()
    # Test Print the TotalDelay
    print("Initial Total Delay Time =", TotalDelay)

    return TotalDelay

#Calculate the arrival time for every node
def CalculateTimeofArrival():
    global NodeArray

    # 1-D simulator
    if ARRY_DIMS == 1:
        for i in range(1, ARRY_ROW):
            NodeArray[i][0].an = (NodeArray[i-1][0].gotime + Node.dy[i-1])%1
            NodeArray[0][i].aw = (NodeArray[0][i-1].gotime + Node.dy[i-1])%1
            for j in range(1, ARRY_COLUMN):
                NodeArray[i][j].an = (NodeArray[i-1][j].gotime + Node.dy[i-1])%1
                NodeArray[i][j].aw = (NodeArray[i][j-1].gotime + Node.dx[j-1])%1

    # 2-D simulator
    else:
        for i in range(1, ARRY_ROW):
            NodeArray[i][0].an = (NodeArray[i-1][0].gotime + Node.dy[i-1][0])%1
            NodeArray[0][i].aw = (NodeArray[0][i-1].gotime + Node.dy[0][i-1])%1
            for j in range(1, ARRY_COLUMN):
                NodeArray[i][j].an = (NodeArray[i-1][j].gotime + Node.dy[i-1][j])%1
                NodeArray[i][j].aw = (NodeArray[i][j-1].gotime + Node.dx[i][j-1])%1


def TransferMessagesOut():

    global NodeArray

    for i in range(ARRY_ROW):
            for j in range(ARRY_COLUMN):
                NodeArray = Node(i, j).GenerateMsgs()


# Calculate the message transfered to the upstream and downstream nodes
def TransferMessagesIn():
    global NodeArray
    # define the messages array of transferring to the upstream and downstream nodes
    NodeArray[ARRY_ROW-1][ARRY_COLUMN-1].msgIn_e = np.zeros(DELTA)
    NodeArray[ARRY_ROW-1][ARRY_COLUMN-1].msgIn_s = np.zeros(DELTA)

    # fill the interior nodes
    if ARRY_DIMS == 1:
        for i in range(ARRY_ROW-1, 0, -1):
            NodeArray[ARRY_ROW-1][i-1].msgIn_e = shift(NodeArray[ARRY_ROW-1][i].msgOut_w, Node.shiftx[i-1])
            NodeArray[i-1][ARRY_ROW-1].msgIn_s = shift(NodeArray[i][ARRY_ROW-1].msgOut_n, Node.shifty[i-1])
            for j in range(ARRY_COLUMN-1, 0, -1):
                NodeArray[i-1][j-1].msgIn_e = shift(NodeArray[i-1][j].msgOut_w, Node.shiftx[j-1])
                NodeArray[i-1][j-1].msgIn_s = shift(NodeArray[i][j-1].msgOut_n, Node.shifty[i-1])
    else:
        for i in range(ARRY_ROW-1, 0, -1):
            NodeArray[ARRY_ROW-1][i-1].msgIn_e = shift(NodeArray[ARRY_ROW-1][i].msgOut_w, Node.shiftx[ARRY_ROW-2][i-1])
            NodeArray[i-1][ARRY_ROW-1].msgIn_s = shift(NodeArray[i][ARRY_ROW-1].msgOut_n, Node.shifty[i-1][ARRY_ROW-2])
            for j in range(ARRY_COLUMN-1, 0, -1):
                NodeArray[i-1][j-1].msgIn_e = shift(NodeArray[i-1][j].msgOut_w, Node.shiftx[i-1][j-1])
                NodeArray[i-1][j-1].msgIn_s = shift(NodeArray[i][j-1].msgOut_n, Node.shifty[i-1][j-1])




















