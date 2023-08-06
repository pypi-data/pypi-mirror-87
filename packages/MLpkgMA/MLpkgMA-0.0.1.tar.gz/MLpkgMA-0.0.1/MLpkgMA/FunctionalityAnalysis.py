#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def Accuracy(y_test=[], y_predict=[], confusion=[]):
    """Compute the classification accuracy of a machine learning model on a testing set. 
    The method needs either both y_test and y_predict or confusion.
    Parameters
    ----------
    y_test: array-like, optional
        True classes of the training set. The default is [].
    y_predict: array-like, optional
        Predictions of the model. The default is []
    confusion: array-like, optional
       Confusion matrix. The default is []. If 'confusion' is not provided, 'y_test' and 'y_predict' are mandatory.
    Returns
    -------
    rate: float
        Accuracy of the model.
    """
    try:
        assert(len(y_test) == len(y_predict))
    except:
        raise AssertionError('The inputs must be of same size.')
        
    if len(confusion) != 0:
        confusion = np.array(confusion)
        rate = np.divide(np.trace(confusion), np.sum(confusion))
    else:
        success = np.count_nonzero(np.array(y_predict) == np.array(y_test)) # number of correct predictions    
        rate = np.divide(success, len(y_test)) # accuracy computation
    return rate


def Confusion(y_test, y_predict, labels=[]):
    """Compute the confusion matrix of a machine learning model on a testing set. It can be used for multi-class problems.
    Parameters
    ----------
    y_test: array-like
        True classes of the training set.
    y_predict: array-like
        Predictions of the model.
    labels: array-like
        Names of the classes.
    Returns
    -------
    matrix: DataFrame
        Confusion matrix of the model.
    """
    try:
        assert(len(y_test) == len(y_predict))
    except:
        raise AssertionError('y_test and y_predict must be of same size.')
        
    if len(labels) == 0:
        # Extract classes from y_test and y_predict
        labels = list(y_test) + list(y_predict)
        labels = list(dict.fromkeys(labels))
        
    " Initialization of the matrix through a dictionnary of dictionnaries "
    " Each first-level key represent the class to be predicted "
    " The second-level keys represent the classes actually predicted by the model "
    matrix = {} 
    for j, class_name in enumerate(labels):
        submatrix = {}
        for k, subclass_name in enumerate(labels):
            submatrix['Predicted ' + str(subclass_name)] = 0
        matrix['Actual ' + str(class_name)] = submatrix
        
    # Completion of 'matrix'                    
    for j, class_name in enumerate(y_test):
        matrix['Actual ' + str(class_name)]['Predicted ' +  str(y_predict[j])] += 1
        
    matrix = pd.DataFrame(data=matrix)
    return matrix
