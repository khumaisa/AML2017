from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn import preprocessing
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.metrics import r2_score
from sklearn.metrics.scorer import make_scorer
from sklearn.externals import joblib
import numpy as np
import pandas as pd
import os


def pathExists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def gridSVRegressor(X, y, model_path, c_range, gamma_range='auto', saved=True):  
    
    scoring = {'r2': make_scorer(r2_score)}
    
    #define support vector regressor     
    svr = SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
              kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
    
    #use standar scaler as normalization 
    regressor = Pipeline([('scaler', preprocessing.StandardScaler()), 
                          ('regressor', svr)])
                
    k_fold = KFold(n_splits=10, shuffle=True)
    
    if gamma_range == 'auto':
        parameters =  [{'regressor__C':c_range}]
    else:
        parameters =  [{'regressor__C':c_range, 'regressor__gamma':gamma_range}]

#    compute score from k-fold cross validation method
    grid = GridSearchCV(regressor, parameters, scoring=scoring, cv=k_fold, refit='r2')    
    
    
    grid.fit(X, y)
    
    #create model based on best C and gamma
    best_C = grid.best_params_['regressor__C']
    best_gamma = grid.best_params_['regressor__gamma']
    if saved == True:
        svr2 = SVR(C=best_C, kernel='rbf', gamma=best_gamma)
        pipe = make_pipeline(preprocessing.StandardScaler(), svr2)
        pipe.fit(X, y)
        joblib.dump(pipe, model_path)
    
    result = {}
    result['C'] = best_C; result['gamma'] = best_gamma
    result['r2_score'] = grid.best_score_
        
    return result  


def gridFeatureRegressor(data_dir, arousal_label, valence_label, model_dir, result_dir):

    features = ['rmse', 'chro', 'cens', 'ccqt','temp',
            'onst','mfcc','scon','rolf','zcrs','tonc', 'wave']
            
    for root, dirnames, filenames in os.walk(data_dir):
        arousal_scores  = {'features': []}
        valence_scores = {'features': []}
        q = 0
        for i in range(len(filenames)):   
            
            ind= filenames[i].index('_')
            name = filenames[i][:ind]
            if name in features:
                X = np.load(root+filenames[i])
                
                arousal_path = model_dir+name+'_arousal.pkl'
                arousalScore = gridSVRegressor(X, arousal_label, arousal_path, 
                                               c_range=range(1,15), 
                                                gamma_range = np.logspace(-3, 3, 15))      
                valence_path = model_dir+name+'_valence.pkl'
                valenceScore = gridSVRegressor(X, valence_label, valence_path,
                                               c_range=range(1,15),
                                                gamma_range = np.logspace(-3, 3, 15))
                
                if q == 0 :
                    for key in arousalScore.keys():
                        arousal_scores[key] = [arousalScore[key]]
                        valence_scores[key] = [valenceScore[key]]
                else:
                    for key in arousalScore.keys():
                        arousal_scores[key].append(arousalScore[key])
                        valence_scores[key].append(valenceScore[key])
                arousal_scores['features'].append(name)
                valence_scores['features'].append(name)
                q += 1
                print name 
                print arousal_scores
                print valence_scores
    print arousal_scores
    print valence_scores
                
    df_arousal = pd.DataFrame(arousal_scores)
    df_valence = pd.DataFrame(valence_scores)
    df_arousal.to_csv(result_dir+'arousal_result.csv', index=None)
    df_valence.to_csv(result_dir+'valence_result.csv', index=None)
    return df_arousal, df_valence
    