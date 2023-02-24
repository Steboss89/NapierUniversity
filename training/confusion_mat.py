# generate the confusion matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt 


def generate_plot(clf, X_test, y_test, model_name):
    r"""Given an input model clf and a test dataset X_test
    compute the confusion matrix and save it
    
    Parameters
    ----------
    clf: input sklearn model 
    X_test: input array for test 
    y_test: input array with labels
    model_name: str, name of the model, for saving
    """

    y_pred = clf.predict(X_test)
    y_true = y_test
    cm = confusion_matrix(y_true, y_pred)
    #fig, ax = plt.subplots()
    
    # plot 
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
    disp.plot(cmap=plt.cm.Blues)
    plt.savefig(f"metrics/{model_name}.png",dpi=300)