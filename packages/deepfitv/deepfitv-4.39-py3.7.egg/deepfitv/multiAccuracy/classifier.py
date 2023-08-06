#Code

import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, recall_score, precision_score, accuracy_score
import json
import tensorflow as tf
from .architecture import ANN
from sklearn.linear_model import Ridge
seed=128


class MultiModelBuilding:

    def __init__(self,data,group):
        """Trains the ANN model and applies multi accuracy algorithm on derived probabilities.
        
        path : path of the input data
        
        group : Which group to select among the groups present in the data
                race,gender,socioeconomic_category"""
        self.data=data
        self.group=group

    def res(p, y):
        return y * ((p>=0.1)/(p + 1e-20) + (p<0.1) * (20 - 100  * p)) +(1-y) * ((p < 0.9)/(1 - p + 1e-20) + (p>=0.9) * (100 * p - 80))

    def predict(self):
        if type(self.data)==type("csv"):
            data = pd.read_csv(self.data,encoding='unicode_escape')
        elif isinstance(self.data, pd.DataFrame):
            data = self.data
        learning_rate= 0.01
        training_epochs=10000
        def sess_run(result, x, sess,net):
            num = x.shape[0]

            num_batch = np.ceil(num/40).astype(int)
            output = np.zeros(num)
            for batch in range(num_batch):
                if batch!=(num_batch-1):
                    output[batch*40:(batch+1)*40] = sess.run(result, feed_dict={net.x:x[batch*40:(batch+1)*40],latent_ph:x[batch*40:(batch+1)*40]})
                else:
                    output[batch*40:(batch+1)*(num%40)] = sess.run(result, feed_dict={net.x:x[batch*40:(batch+1)*(num%40)],latent_ph:x[batch*40:(batch+1)*(num%40)]})
            return output

        
        data=data.rename(columns={'target':'target1'})
        data['target2']=1-data['target1']
        X_train,X_test,y_train,y_test=train_test_split(data.drop(['target1','target2'],axis=1),data[['target1','target2']],test_size=0.3,random_state=5)
        inputX=X_train.values
        inputY=y_train.values
        inputX_test=X_test.values
        inputX_test1=inputX_test[:int(inputX_test.shape[0]/2)]
        inputY_test=y_test.values
        display_step=50
        n_samples=inputY.shape[0]
        net=ANN(X_train.shape[0],X_train.shape[1])
#         net.bias_hidden1 = tf.Variable(tf.compat.v1.random_normal([64]),name='3')
#         net.weights_hidden2 = tf.Variable(tf.compat.v1.random_normal([64, 128]),name='4')
#         net.bias_hidden2 = tf.Variable(tf.compat.v1.random_normal([128]),name='5')
#         net.weights_hidden3 = tf.Variable(tf.compat.v1.random_normal([128, 64]),name='6')
#         net.bias_hidden3 = tf.Variable(tf.compat.v1.random_normal([64]),name='7')
#         net.weights_output = tf.Variable(tf.compat.v1.random_normal([64, 2]),name='8')
#         net.bias_output = tf.Variable(tf.compat.v1.random_normal([2]),name='9')
        init=tf.compat.v1.initialize_all_variables()
        sess=tf.compat.v1.Session()
        sess.run(init)
        for i in range(training_epochs):
            sess.run(net.optimizer,feed_dict={net.x:inputX,net.y_:inputY})
        pred=sess.run(net.y,feed_dict={net.x:inputX_test})
        control = tf.cast(tf.greater(net.y[:,1],net.y[:,0]), tf.float32)
        noharm = [control, 1 - control, control + 1 - control]
        logits = net.y[:,1] - net.y[:,0]
        max_T = 100
        thresh = 1e-4
        latent_ph = tf.compat.v1.placeholder(tf.float32, shape=(None, X_train.shape[1]), name="latent_var")
        best_epoch, best_acc = -1,0
        #(idxs1, idxs2, _), _ = split_data(np.arange(len(idxs_val)), ratio=[0.7,0.3,0.])
        coeffs = []
        
        for t in range(max_T):
            control = tf.cast(tf.greater(net.y[:,1], net.y[:,0]), tf.float32)
            noharm = [control, 1 - control, control + 1 - control]
            probs_heldout = sess_run(tf.nn.sigmoid(logits), inputX_test[int(inputX_test.shape[0]/2):inputX_test.shape[0]], sess=sess,net=net)
            heldout_loss = np.mean(-inputY_test[:,0][int(inputX_test.shape[0]/2):inputX_test.shape[0]] * np.log(probs_heldout + 1e-20) - (1-inputY_test[:,0][int(inputX_test.shape[0]/2):inputX_test.shape[0]]) * np.log(1-probs_heldout + 1e-20))
            heldout_acc =  np.mean((probs_heldout>0.5)==inputY_test[:,0][int(inputX_test.shape[0]/2):inputX_test.shape[0]])
            probs = sess_run(tf.nn.sigmoid(logits), inputX_test,sess,net=net)
            val_loss = np.mean(-inputY_test[:,0] * np.log(probs + 1e-20) - (1 - inputY_test[:,0]) * np.log(1 - probs + 1e-20))
            val_acc = np.mean((probs > 0.5) == inputY_test[:,0])
            if heldout_acc > best_acc:
                best_epoch = t
                best_acc = heldout_acc
                best_logits = logits
            delta = MultiModelBuilding.res(probs,inputY_test[:,0])
            residual = probs - inputY_test[:,0]
            for i, s in enumerate(noharm):
                temp_s = sess_run(noharm[i], inputX_test[:int(inputX_test.shape[0]/2)], sess,net=net)
                temp_s_heldout = sess_run(noharm[i], inputX_test[int(inputX_test.shape[0]/2):inputX_test.shape[0]], sess,net=net)
                samples1 = np.where(temp_s == 1)[0]
                samples2 = np.where(temp_s_heldout == 1)[0]
                clf = Ridge(alpha=1)
                #clf.fit(inputX_test[:800],inputY_test[:800])
                clf.fit(inputX_test[:int(inputX_test.shape[0]/2)],delta[:int(inputX_test.shape[0]/2)])
                pickle.dump(clf, open('model.pkl', 'wb'))
                clf_prediction = clf.predict(inputX_test[int(inputX_test.shape[0]/2):inputX_test.shape[0]])
                #corr = np.mean(clf_prediction[:,0] * residual[800:1600])
                corr = np.mean(clf_prediction * residual[int(inputX_test.shape[0]/2):inputX_test.shape[0]])
                print(corr)
                if corr > 1e-4:
                    coeffs.append(clf.coef_)
                    #h = (tf.matmul(tf.cast(inputX_test,tf.float32), tf.constant(np.expand_dims(clf.coef_,-1),
                     #                                     dtype=tf.float32)) + clf.intercept_)


                    h = (tf.matmul(latent_ph, tf.constant(np.expand_dims(clf.coef_,-1),
                                                          dtype=tf.float32)) + clf.intercept_)
                    h=tf.reshape(h,[-1])
                    logits -= .1 * h * s
                    #logits=tf.reshape(logits,[-1])
                    break
            if i==2:
                break
                
        probs = sess_run(net.y[:,1] - net.y[:,0], X_test, sess,net=net)
        
        groups=['all']
        groups=groups+data[self.group].unique().tolist()
        #groups = ['all', 'F', 'M', 'B', 'N', 'BF', 'BM', 'NF', 'NM']
        errs = []
        idxs = list(range(0,inputX_test.shape[0]))
        
        errs.append(100 * np.mean((probs[idxs]>0.5)!=y_test.iloc[idxs,0]))
        for g in groups[1:]:
            idxs = np.where((X_test[X_test[self.group]==g]))[0]
            errs.append(100 * np.mean((probs[idxs]>0.5)!=y_test.iloc[idxs,0]))

        dict1={}
        metrics1={}
        for grp, err in zip(groups, errs):
            dict1[grp]=str(round(err, 1))
        ma_pred1=(probs<0.5).astype(int)
        actual=inputY_test[:,0]
        metrics1['accuracy'] = round(accuracy_score(actual, ma_pred1), 2)
        metrics1['model_recall'] = round(recall_score(actual, ma_pred1), 2)
        metrics1['model_precision'] = round(precision_score(actual, ma_pred1), 2)
        metrics1['roc_auc_score_model'] = round(roc_auc_score(actual,ma_pred1), 2)
        #print('Original: ', output)
        
        probs = sess_run(tf.nn.sigmoid(best_logits), X_test, sess,net=net)
        groups=['all']
        groups=groups+data[self.group].unique().tolist()
        #groups = ['all', 'F', 'M', 'B', 'N', 'BF', 'BM', 'NF', 'NM']
        errs = []
        idxs = list(range(0,inputX_test.shape[0]))

        errs.append(100 * np.mean((probs[idxs]>0.5)!=y_test.iloc[idxs,0]))
        for g in groups[1:]:
            idxs = np.where((X_test[X_test[self.group]==g]))[0]
            errs.append(100 * np.mean((probs[idxs]>0.5)!=y_test.iloc[idxs,0]))
            
        dict2={}
        metrics2={}
        for grp, err in zip(groups, errs):
            dict2[grp]=str(round(err, 1))
        ma_pred2=(probs<0.5).astype(int)
        metrics2['accuracy'] = round(accuracy_score(actual, ma_pred2), 2)
        metrics2['model_recall'] = round(recall_score(actual, ma_pred2), 2)
        metrics2['model_precision'] = round(precision_score(actual, ma_pred2), 2)
        metrics2['roc_auc_score_model'] = round(roc_auc_score(actual,ma_pred2), 2)


        before_ma = list(dict1.values())
        after_ma = list(dict2.values())
        metrics_before = list(metrics1.values())
        metrics_after = list(metrics2.values())
        for i in range(len(before_ma)):
            before_ma[i] = float(before_ma[i])
        for i in range(len(after_ma)):
            after_ma[i] = float(after_ma[i])
        for i in range(len(metrics_before)):
            metrics_before[i] = float(metrics_before[i]*100)
        for i in range(len(metrics_after)):
            metrics_after[i] = float(metrics_after[i]* 100)


        list_data=[
            {
                'name':'Before MultiAccuracy ',
                'data':dict1,
                'metrics':metrics1
                },
            {
                'name':'After MultiAccuracy',
                'data':dict2,
                'metrics':metrics2
                }
            ]
 
        return list_data

