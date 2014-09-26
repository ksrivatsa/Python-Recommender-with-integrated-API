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
    
    def __init__(self,filepath,similarityAlgo = None):
        print "Formatting the dataset.."
        self.createDataset(filepath)
        print "Dataset Formatted! Creating Dictionary.."
        if similarityAlgo != None:
            self.getUserSimilarity(similarityAlgo)
        else:
            self.getUserSimilarity(PearsonCorrelation())
        print "Recommender Initialised!"
           
    def getTopMatches(self,person,similarityAlgo,n=3):
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
    
    def getUserSimilarity(self,similarityAlgo):
        
        users = self._dataset.keys()
        topMatches = {}
        topMatchesList = []
        
        for user in users:
            topMatchesList = self.getTopMatches(user,similarityAlgo)
            for l in topMatchesList:
                topMatches[l[1]]=l[0]
            self._similarUserDictionary[user]=topMatches
            topMatches={}
        #print self._similarUserDictionary
    
    def recommend(self,user):
        print "Recommending for : " + user
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
            itemRating = simRatingProduct[item]/similaritySum[item]
            if itemRating >= 4.0:
                ratings[item] = itemRating            
        
        return ratings
         
    
    def createDataset(self,filepath):
        
        dataFile = open(filepath,"r")
                
        for line in dataFile:            
            data = line.split("\t")
            if data[0] in self._dataset.keys():
                if data[1] not in self._dataset[data[0]].keys():
                    self._dataset[data[0]][data[1]] = int(data[2])
            else:
                rating = {}
                rating[data[1]] = int(data[2])
                self._dataset[data[0]] = rating
            
    
    
if __name__ == "__main__":
    r = UserRecommender("Resources/ml-100k/u.data")
    print r.recommend('100')
            
        
        
        



