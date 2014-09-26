# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 11:44:19 2014

@author: karthik
"""

from math import sqrt,pow
from Dataset import dataset as dset

class EuclideanDistance:
    
    def __init__(self):
        print "Using Euclidean Distance!"
        
    def getSimilarity(self,dataset,person1,person2):
        sharedItems = []
        
        for item in dataset[person1]:
            if item in dataset[person2]:
                sharedItems.append(item)
                
        if len(sharedItems) == 0:
            return 0
        
        sumOfSquares = 0.0
        
        for item in sharedItems:
            sumOfSquares += pow((dataset[person1][item]-dataset[person2][item]),2)
                   
        return 1/(1+sqrt(sumOfSquares))
    
class PearsonCorrelation:
    
    def __init__(self):
        print "Using Pearson Correlation!"
        
    def getSimilarity(self,dataset,person1,person2):
        sharedItems = []
        similaritySum1 = 0.0
        similaritySum2 = 0.0
        squareSum1 = 0.0
        squareSum2 = 0.0
        productSum = 0.0 
        
        for item in dataset[person1]:
            if item in dataset[person2]:
                sharedItems.append(item)
                
        if len(sharedItems) == 0:
            return 0
        
        n = len(sharedItems)
        
        for item in sharedItems:
            similaritySum1 += dataset[person1][item]
            similaritySum2 += dataset[person2][item]
            
            squareSum1 += pow(dataset[person1][item],2)
            squareSum2 += pow(dataset[person2][item],2)
            
            productSum += (dataset[person1][item]*dataset[person2][item])
        
        numerator = (n*productSum)-(similaritySum1*similaritySum2)
        
        denominator = ((n*squareSum1)-pow(similaritySum1,2))*((n*squareSum2)-pow(similaritySum2,2))
        denominator = sqrt(denominator)
        
        if denominator == 0:
            return 0
                
        return numerator/denominator
        
       
if __name__ == "__main__":
    ed = PearsonCorrelation()
    #print dset
    print ed.getSimilarity(dset,'Toby Daniels','Toby Daniels')
    
    