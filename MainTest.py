__author__ = 'Xin'

import InitialNode
import numpy as np
from NODE import Node
from MyFunction import shift
from random import randint, seed
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.lines import Line2D
from multiprocessing import Process, Queue
from itertools import product

#seed(255)
import math


if __name__ == "__main__":
    global NodeArray

    NodeArray = []

    # Initialize the Node Array & Distance from Node to Node & Arrival Time to the Nodes
    InitialNode.InitialNodeArray()

    InitialNode.InitialDistanceNodeToNode()

    InitialNode.InitialArrivalTime()

    for IterationIndex in range(50):

        InitialNode.TransferMessagesOut()

        # Calculate the message was transfered from the downstream node, example from RightEast and DownSouth
        # Output the message NodeArray[i][j].msgIn_x from every direction
        InitialNode.TransferMessagesIn()

        # Calculate the arrival times to each node
        # Output the arrival time of NodeArray[i][j].ax  and x represents the direction
        InitialNode.CalculateTimeofArrival()

        # Calculate the total delay time
        DelayTime = InitialNode.CalculateDelayTime()

        print("Total waiting time in iteration", IterationIndex, "is ", np.sum(DelayTime))




