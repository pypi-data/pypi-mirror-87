import os
import sys
import time
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import shutil
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,roc_auc_score,recall_score,precision_score

from .Shapley import ShapNN
from .DShap import DShap
from .shap_utils import *

MEM_DIR = './'
warnings.filterwarnings("ignore")


class ShapleyModelBuilding:
    def model_metrics(test_labels, model_predict):
        model_accuracy = round(accuracy_score(test_labels, model_predict), 2)
        model_recall = round(recall_score(test_labels, model_predict), 2)
        model_precision = round(precision_score(test_labels, model_predict), 2)
        roc_auc_score_model = round(roc_auc_score(test_labels,model_predict), 2)
        return {'accuracy':model_accuracy,'model_recall':model_recall,'model_precision':model_precision,'roc_auc_score_model':roc_auc_score_model}

class Shap:
    
    def __init__(self,data,model="logistic",num_test=500):
        """Trains the data for shapley values and outputs them in a csv file. Target column needs to present as the last column(rightmost column) in the data.
         
        data: CSV filepath or dataframe
        model: The model family used for learning algorithm.
        num_test: Number of data points used for evaluation metric."""
        self.data=data
        self.model=model
        self.num_test=num_test
        
    def run(self):
            if type(self.data)==type("csv"):
                diabetes = pd.read_csv(self.data,encoding='unicode_escape')
            elif isinstance(self.data, pd.DataFrame):
                diabetes = self.data
            diabetes = diabetes.loc[:,diabetes.isna().mean() <= .5]
            diabetes = diabetes.fillna(diabetes.mean())
            x = diabetes.iloc[:,:-1]
            y = diabetes.iloc[:,[-1]]
            y = y.astype(int)
            x_train,x_test,y_train,y_test = train_test_split(x, y, test_size=0.3, random_state=0)
            x_train = x_train.values
            y_train = y_train.values
            x_test = x_test.to_numpy()
            y_test = y_test.to_numpy()
            Y_train = []
            for i in y_train:
                Y_train.extend(i)
            Y_test = []
            for i in y_test:
                Y_test.extend(i)
            Y_train = np.asarray(Y_train)
            Y_test = np.asarray(Y_test)
            model = self.model
            problem = 'classification'
            num_test = self.num_test
            directory = './temp'
            shutil.rmtree(directory, ignore_errors=True)
            #seed0
            dshap = DShap(x_train, Y_train, x_test, Y_test,num_test, sources=None, model_family=model, metric='accuracy',
              directory=directory, seed=0)
            dshap.run(100, 0.1, loo_run=False)
            #seed1
            dshap = DShap(x_train, Y_train, x_test, Y_test, num_test, model_family=model, metric='accuracy',
              directory=directory, seed=1)
            dshap.run(100, 0.1, loo_run=False)
            #seed2
            dshap = DShap(x_train, Y_train, x_test, Y_test, num_test, model_family=model, metric='accuracy',
              directory=directory, seed=2)
            dshap.run(100, 0.1, g_run=False, loo_run=False)
            dshap.merge_results()
            dataTMC = pd.DataFrame({'Column1': dshap.vals_tmc[:]})
            dataTMC.to_csv("dataTMC.csv")
            dataNEG_TMC = dataTMC[(dataTMC['Column1']<0)]
            drop_list_TMC = list(dataNEG_TMC.index.values)
            modDf_TMC = diabetes.drop(drop_list_TMC)
            modDf_TMC.to_csv("modDf_TMC.csv")
            scORG = StandardScaler()
            xORG_train = scORG.fit_transform(x_train)
            xORG_test = scORG.transform(x_test)
            classifierORG = LogisticRegression(random_state = 0)
            classifierORG.fit(xORG_train, Y_train)
            yORG_pred = classifierORG.predict(xORG_test)
            yORG_pred = yORG_pred.astype(int)
            x_TMC = modDf_TMC.iloc[:,:-1]
            y_TMC = modDf_TMC.iloc[:,[-1]]
            xTMC_train,xTMC_test,yTMC_train,yTMC_test = train_test_split(x_TMC, y_TMC, test_size=0.3, random_state=0)
            xTMC_train = xTMC_train.values
            yTMC_train = yTMC_train.values
            scTMC = StandardScaler()
            classifierTMC = LogisticRegression(random_state = 0)
            xTMC_train = scTMC.fit_transform(xTMC_train)
            xTMC_test = scTMC.transform(xTMC_test)
            classifierTMC.fit(xTMC_train, yTMC_train)
            yTMC_pred = classifierTMC.predict(xTMC_test)
            yTMC_pred = yTMC_pred.astype(int)
            
            
            list_data = [
                            {
                                'name':'Before Shapley Base Metrics ',
                                'metrics':ShapleyModelBuilding.model_metrics(y_test, yORG_pred),
                            },
                            {
                                'name':'After Shapley Base Metrics (TMC)',
                                'metrics':ShapleyModelBuilding.model_metrics(yTMC_test, yTMC_pred),
                            }
                            

                        ]
            return list_data