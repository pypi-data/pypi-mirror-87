#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc

class ML_Model(metaclass=abc.ABCMeta):
    """An interface for an abstract machine learning model for use in a quality analysis.
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'fit') and 
                callable(subclass.fit) and 
                hasattr(subclass, 'predict') and 
                callable(subclass.predict) or 
                NotImplemented)
        
    @abc.abstractmethod        
    def fit(self,x_train, y_train):
        raise NotImplementedError
        
    @abc.abstractmethod  
    def predict(self, x):
        raise NotImplementedError
        