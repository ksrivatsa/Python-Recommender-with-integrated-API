# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 14:16:24 2014

@author: karthik
"""

from DistanceAlgorithms import *
from Dataset import dataset as dset



class UserRecommender:
    
    _similarUserDictionary = {}
    _dataset = {}
    
#    def __init__(self,dataset):
#        print "Ingesting the dataset..."
#        self._dataset=dataset
#        self.getUserSimilarity()
#        print "Recommender Initialised!"
    
    def __init__(self,filepath):
        print "Formatting the dataset.."
        self.createDataset(filepath)
        print "Dataset Formatted! Creating Dictionary.."
        self.getUserSimilarity()
        print "Recommender Initialised!"
           
    def getTopMatches(self,person,n = 3,similarityAlgo = PearsonCorrelation()):
        scores=[]
        users = self._dataset.keys()
        if person in users:
            users.remove(person)
        
        for user in users:
            similarity = similarityAlgo.getSimilarity(self._dataset,person,user)
            scores.append((similarity,user))
        
        scores.sort()
        scores.reverse()
        return scores[0:n]
    
    def getUserSimilarity(self):
        
        users = self._dataset.keys()
        topMatches = {}
        topMatchesList = []
        
        for user in users:
            topMatchesList = self.getTopMatches(user)
            for l in topMatchesList:
                topMatches[l[1]]=l[0]
            self._similarUserDictionary[user]=topMatches
            topMatches={}
        #print self._similarUserDictionary
    
    def recommend(self,user):
        
        similaritySum = {}
        simRatingProduct = {}
        similarUsers = {}
        ratings = {}
        if user in self._similarUserDictionary.keys():
            similarUsers = self._similarUserDictionary[user]
        else:
            return []
                
        for person in similarUsers:
            for item in self._dataset[person]:
                if item not in self._dataset[user]:
                    similaritySum.setdefault(item,0.0)
                    simRatingProduct.setdefault(item,0.0)
                    
                    similaritySum[item] += similarUsers[person]
                    simRatingProduct[item] += (similarUsers[person]*self._dataset[person][item])
        
        for item in simRatingProduct:
            ratings[item] = simRatingProduct[item]/similaritySum[item]
        
        print ratings 
    
    def createDataset(self,filepath):
        
        dataFile = open(filepath,"r")
        count = 0
        
        for line in dataFile:
            if (count % 5000) == 0:
                print count
            data = line.split("\t")
            if data[0] in self._dataset.keys():
                if data[1] not in self._dataset[data[0]].keys():
                    self._dataset[data[0]][data[1]] = int(data[2])
            else:
                rating = {}
                rating[data[1]] = int(data[2])
                self._dataset[data[0]] = rating
            count += 1
    
    
if __name__ == "__main__":
    r = UserRecommender("Resources/ml-100k/u.data")
    r.recommend('100')
            
        
        
        



