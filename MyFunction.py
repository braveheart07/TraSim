__author__ = 'Xin'
# 2014.04.07

import numpy as np

####################
#Calculate the middle point between a and b
#return middle value
#####################
def midpoint(a,b):
    if abs(a - b) < 0.5:
        return (a + b)/2
    else:
        return(a + b + 1)/2

#####################
#Calculate the minimum value ??
#return
#####################
def localMinima(a):
    a = np.arount(a,7)
    return np.sum((np.r_[True,a[1:] < a[:-1]] & np.r_[a[:-1] <= a[1:],True]))|\
           (np.r_[True,a[1:] <= a[:-1]] & np.r_a[:-1] < a[1:], True)
#####################
#Calculate the minimum value ??
#return
#####################
def localMaxima(a):
    a = np.arount(a,7)
    return np.sum((np.r_[True,a[1:] > a[:-1]] & np.r_[a[:-1] >= a[1:],True]))|\
           (np.r_[True,a[1:] >= a[:-1]] & np.r_a[:-1] > a[1:], True)

#####################
#Cyclic shift function shift to the left by n
#return
#####################
def shift(a,n):
    n = n % len(a)
    return np.concatenate((a[n:],a[:n]))


