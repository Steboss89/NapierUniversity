# routine for model training and prediction 

def train(clf, features, targets):
    r""" Routine to train a given clf model 
    Parameters
    ----------
    clf: sklearn model 
    features: np.array, input tf-idf texts 
    targets: np.array, targets 1/0
    
    Return 
    ------
    """
    clf.fit(features, targets)

def predict(clf, features):
    r""" Given a model and text features return the predictions
    """
    return (clf.predict(features))