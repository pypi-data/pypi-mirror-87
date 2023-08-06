#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

def Heatmap(data):    
    """Plot the correlation heatmap of a dataset.
    Parameters
    ----------
    data: DataFrame
        Dataset to analyse. 
    Returns
    -------
    fig: plot
        Correlation heatmap of the dataset.
    """
    data = pd.DataFrame(data)
    fig = data.corr().style.background_gradient(cmap='coolwarm')
    fig.caption = 'Correlation heatmap'
    return fig
