__author__ = 'Xin'
#2014.04.07

import numpy as np
# Import the function in MyFunction Module
from MyFunction import midpoint, localMaxima, localMinima


class Node:
    #define class variables

    # dx[i] = distance between node[i][j] to node[i+1][j]
    # dy[j] = distance between node[i][j] to node[i][j+1]

    dx = None
    dy = None
    # shiftx and shifty are dx and dy times 100 for the shifting
    shiftx = None
    shifty = None
    # delta and wedge_matrix meaning
    delta = None
    wedge_matrix = None

    # initial node class and the object variables
    def __init__(self, x, y):
        # location of node(x,y)
        """
        :param x: Rows of the Node Array
        :param y: Columns of Nod eArray
        """
        self.x = x
        self.y = y
        # Time the block of reach node from West\East\North\South
        self.ae = 0
        self.ars = 0
        self.aw = 0
        self.an = 0
        self.gotime = 0
        self.delaytime = 0
        # Message Input from East\South\West\North direction node
        self.msgIn_e = np.zeros(Node.delta)
        self.msgIn_s = np.zeros(Node.delta)
        self.msgIn_w = np.zeros(Node.delta)
        self.msgIn_b = np.zeros(Node.delta)
        # Message Input from East\South\West\North direction node
        self.msgOut_e = np.zeros(Node.delta)
        self.msgOut_s = np.zeros(Node.delta)
        self.msgOut_w = np.zeros(Node.delta)
        self.msgOut_n = np.zeros(Node.delta)
        # Bulit the Wedge Matrix
        if Node.wedge_matrix == None:
            self.TmpWedge = np.concatenate((range(Node.delta // 2 + 1), range(Node.delta // 2-1, 0, -1))) / Node.delta
            # Open delta x delta Matrix Space
            Node.wedge_matrix = np.zeros((Node.delta, Node.delta))
            for i in range(Node.delta):
                Node.wedge_matrix[i] = np.concatenate((self.TmpWedge[-i:], self.TmpWedge[:-i]))
                #test the matrix
                print Node.wedge_matrix[i]

    # Calculate waiting time when gotime is set
    def GetDelayTime(self):
        if abs(self.aw - self.gotime) <= 0.5:
            # waiting time
            ww = abs(self.aw - self.gotime)
        else:
            ww = 1 - abs(self.aw - self.gotime)

        if abs(self.an - self.gotime) <= 0.5:
            wn = abs(self.an - self.gotime)
        else:
            wn = 1 - abs(self.an - self.gotime)

        delaytime = ww + wn
        self.delaytime = delaytime
        return delaytime

    # generate messages and get gotime
    def GenerateMsgs(self):
        # combine the message from east and south
        """

        :rtype : object
        """
        base = self.msgIn_e + self.msgIn_s
        # set the factor(normal the factor=0.5) and value temp
        factor = 1

        valuew = []
        valuen = []

        aw2 = self.aw + 1
        if (self.aw > 0.5):
            aw2 = self.aw - 1

        an2 = self.an + 1
        if (self.an > 0.5):
            an2 = self.an - 1

        t = np.array(range(Node.delta)) / Node.delta
        # calculate the min valuew and valuen
        valuew = np.min(np.array([abs(t - self.aw), abs(t - aw2)]), 0)
        valuen = np.min(np.array([abs(t - self.an), abs(t - an2)]), 0)

        # threshold is used to deetermine the gotime for the current node
        # Caclulate the middle point value between the threshold and gotime
        threshold = base + valuew + valuen
        self.gotime = midpoint(np.argmin(threshold) / Node.delta, self.gotime)

        #generate output message to the North and West
        self.msgOut_n = factor * np.min(base + valuew + self.wedge_matrix, 1)
        self.msgOut_n = self.msgOut_n - np.min(self.msgOut_n)
        self.msgOut_w = factor * np.min(base + valuen + self.wedge_matrix, 1)
        self.msgOut_w = self.msgOut_w - np.min(self.msgOut_w)

    def MessageComplexity(self):
        return localMinima(self.msgOut_w) + localMinima(self.msgOut_n) + localMaxima(self.msgOut_w) + localMaxima(
            self.msgOut_n)





