#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from MLpkgMA.Interface import ML_Model
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn import neighbors

mnist = fetch_openml('mnist_784') # use the MNIST image dataset of figures between 0 and 9.
x_train, x_test, y_train, y_test = train_test_split(mnist.data, mnist.target, test_size=100) # split data to keep 100 for model testing

knn = neighbors.KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train, y_train) # train the model

class ConcreteML_Model(ML_Model):
    """Implementation of the ML_Model interface for the k-nearest neighbors (k-NN) model from the sklearn library.
    This model is pretrained on the MNIST dataset.
    """        
    def fit(self, x_train, y_train):
        """Train the model on the dataset 'x_train' and the corresponding targets 'y_train'.
        Parameters
        ----------
        x_train : array-like
            Training data.
        y_train : array-like
            Class labels.
        """
        knn.fit(x=x_train,y=y_train)
        return
    
    def predict(self, x):
        """Predict the class labels of 'x' from the model.
        Parameters
        ----------
        x : array-like
            Test data.
        Returns
        -------
        ndarray
            Predicted class labels.
        """
        return knn.predict(x)
    
