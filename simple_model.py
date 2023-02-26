# dataset obtained from https://archive.ics.uci.edu/ml/machine-learning-databases/00228/
from preprocessing import data_preprocessing
from training import train_and_predict, confusion_mat
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import json

def logistic_regression_to_json(lrmodel, file=None):
    if file is not None:
        serialize = lambda x: json.dump(x, file)
    else:
        serialize = json.dumps
    data = {}
    data['init_params'] = lrmodel.get_params()
    data['model_params'] = mp = {}
    for p in ('coef_', 'intercept_','classes_', 'n_iter_'):
        mp[p] = getattr(lrmodel, p).tolist()
    return serialize(data)


if __name__=="__main__":
    input_data = "dataset/SMSSpamCollection"
    df = pd.read_csv(input_data, sep='\t', names=['label', 'text'], header=None)
    # data preprocessing 
    #df = data_preprocessing.drop_columns(df, ["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"])
    #df = data_preprocessing.rename_columns(df, {"v2" : "text", "v1":"label"})
    df = data_preprocessing.target_encoder(df, 'ham', 'spam')
    text_vector = data_preprocessing.text_processing(df)

    # prepare a train/test split 
    # NB we shuold have a train, validation and test!
    X_train, X_test, y_train, y_test = train_test_split(text_vector, df['label'], test_size=0.15, random_state=42)

    # here you can choose the best model for this task
    svc = SVC(kernel='sigmoid', gamma=1.0)
    knc = KNeighborsClassifier(n_neighbors=49)
    mnb = MultinomialNB(alpha=0.2)
    dtc = DecisionTreeClassifier(min_samples_split=7, random_state=111)
    lrc = LogisticRegression(solver='liblinear', penalty='l1')
    rfc = RandomForestClassifier(n_estimators=31, random_state=111)
    clfs = {'SVC' : svc,'KN' : knc, 'NB': mnb, 'DT': dtc, 'LR': lrc, 'RF': rfc}

    for k, v in clfs.items():
        train_and_predict.train(v, X_train, y_train)
        pred = train_and_predict.predict(v, X_test)
        confusion_mat.generate_plot(v, X_test, y_test, k)
        acc_score = accuracy_score(y_test, pred)
        print(f"Model {k} prediction accuracy {acc_score}")
        # save model 
        filename = f"saved_models/{k}.joblib"
        joblib.dump(v, filename)
        if k=="LR":
            lrjson=logistic_regression_to_json(v)
            
            with open('saved_models/LR.json', 'w') as outfile:
                json.dump(lrjson, outfile)





