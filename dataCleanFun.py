# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:35:44 2019

@author: scheng
"""
import pandas as pd



class dataCleanFun:

    def __init__(self):
        pass
    
    #drop columns
    def dropColumns(self, data, droplist):
        for column in droplist:
            data.drop(column,axis='columns',inplace=True)
        return data
    
    #transferStringToNumber(01)
    #dummies is column name
    #value is string value
    def transferStringTo01(self, data, columns, stringValueList): 
        for valueD in columns: 
           print("before")       
           print(data[valueD].head())
           data[valueD]= data[valueD].apply(lambda x: self.funStringto01(x, stringValueList))
           print("after")   
           print(data[valueD].head())
        return data

    #transferStringToDummies(multi value)
    def transferStringToOneHot(self, data, columns):
        merged = data
        for column in columns:
            #onehot with drop

            newcolumn = pd.get_dummies(merged[column],drop_first=True)
            merged = pd.concat([merged, newcolumn], axis = 'columns')
            merged.drop(column, axis='columns', inplace=True)

        return merged

    #give value a title
    def giveValueTile(self, data, columns):
        for value in columns:
            data.ix[data[value]=='Y',value]= 'Y'+value
            data.ix[data[value]=='N',value]= 'N'+value         
        return data



    def fillwithNumber(self, data, columns, number):
        for column in columns:
            
            data[column].fillna(number, inplace=True)
     
        return data
    
    def createNullFlag(self, data, columns):
        for column in columns:
            data[column+'_flag']= data[column].apply(lambda x: self.isNull(x))
            #merged = pd.concat([data, flagColumn], axis = 'columns')
        return data
            

    #categorical to numberic
    def funStringto01(self, y, stringValueList):
        for value in stringValueList:
            if (y == value) is True:
                return 1
            else:
                return 0
            
    def isNull(self, x):
        if pd.isnull(x) is True:
            return 0
        else:
            return 1