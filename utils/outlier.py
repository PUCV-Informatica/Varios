import numpy as np

def isOutlier(data):
    
    data = np.sort(data)
    Q1 = np.percentile(data, 25, interpolation = 'midpoint')  
    Q3 = np.percentile(data, 75, interpolation = 'midpoint')  
    IQR = (Q3-Q1)
    low = Q1 - 1.5 * IQR 
    upper = Q3 + 1.5 * IQR 
    
    dataNew =[]
    outlier = []
    for x in data: 
        if ~((x> upper) or (x<low)): 
             dataNew.append(x)
        else:
            outlier.append(x)
    return dataNew, outlier