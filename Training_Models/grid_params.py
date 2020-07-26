# One could create a simple dictionary e.g a ={}.

class GridParams ():
    
    def __init__ (self):
        
        self.svr = {'regressor___svr__c':range(1, 10), 'regressor___svr__gamma': [0.001, 0.005, 0.1, 0.5] }
        
        self.xgboost =  {'regressor__xgb__max_depth': [3, 4, 5, 6, 7, 8, 10],
                         'regressor__xgb__learning_rate': [0.01, 0.05, 0.1, 0.2],
                         'regressor__xgb__colsample_bytree': [0.6, 0.7, 0.8],
                         'regressor__xgb__min_child_weight': [0.4, 0.5, 0.6],
                         'regressor__xgb__gamma': [0.0, 0.01, 0.1],
                         'regressor__xgb__reg_lambda': range(2, 10, 2),
                         'regressor__xgb__n_estimators': [100, 150, 200, 250],
                         'colsample_bytree':[0.3, 0.4, 0.5, 0.6]}
        
        
        self.gradientboost = {'regressor__gradientboostingregressor__n_estimators': [100, 150, 200, 250],
                              'regressor__gradientboostingregressor__learning_rate':[0.01, 0.05, 0.1, 0.2], 
                              'regressor__gradientboostingregressor__min_samples_leaf':[2, 3],  
                              'regressor__gradientboostingregressor__min_samples_split':[14], 
                              'regressor__gradientboostingregressor__max_features':[0.7, .1, .05]
                             }
        
        self.randomforest = {'regressor__randomforestregressor__n_estimators':[150, 300, 600], 
                             'regressor__randomforestregressor__min_samples_leaf':[2, 3],  
                             'regressor__randomforestregressor__min_samples_split':[14, 12], 
                             'regressor__randomforestregressor__max_features':[0.7, 1],
                            'regressor__randomforestregressor__criterion': ['mse', 'mae']}
        
        self.extratrees= {'regressor__extratreesregressor__n_estimators': [100, 150, 200, 250], 
                          'regressor__extratreesregressor__criterion': ['mse', 'mae'],
                          'regressor__extratreesregressor__max_depth': range(2, 9, 1), 
                          'regressor__extratreesregressor__max_features': ['auto','sqrt', 'log2']}
        
        self.kneighbors = {'regressor__kneighborsregressor__regressor_algorithm':['auto', 'ball_tree', 'kd_tree'],
                           'regressor__kneighborsregressor__leaf_size': range(5, 40, 3),
                           'regressor__kneighborsregressor__metric':['minkowski', 'precomputed'],
                           'regressor__kneighborsregressor__n_neighbors':range(2, 15, 1),
                           'regressor__kneighborsregressor__p': [2, 3, 5]}
