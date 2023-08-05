#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 17:29:07 2020

@author: charlescrawford
"""
import joblib
import json
import jwt
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import time

from base64 import b64encode
from datetime import datetime as dt
from datetime import timedelta as td
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (f1_score,
                             confusion_matrix,
                             precision_recall_curve,
                             auc,
                             roc_auc_score,
                             accuracy_score,
                             r2_score,
                             mean_squared_error,
                             median_absolute_error)
from sklearn.model_selection import (RandomizedSearchCV,
                                     cross_val_predict,
                                     train_test_split)
from sklearn.utils import resample
from sklearn.ensemble import StackingClassifier, StackingRegressor

class HelperFunctions:
    def __init__(self):
        pass

    def split_data(self, train, target, test_val_percentage=.3, validation_set=False):
        """
        :param train: features for training
        :param target: targets for training
        :param test_val_percentage: total percentage for training and validation, will split evenly between test and val
        :return: returns training, test, and validation split
        """
        x_train, x_test, y_train, y_test = train_test_split(train,
                                                            target,
                                                            test_size=test_val_percentage)
        if validation_set:
            x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=.5)
            return x_train, x_val, x_test, y_train, y_val, y_test
        else:
            return x_train, x_test, y_train, y_test

    def get_label_maps(self, target_df):
        """
        :param target_df: dataframe of string labels
        :return: dictionaries of forwaards and backwards mappings of integer:string class labels
        """
        label_map = {column: idx for idx, column in enumerate(target_df.columns)}
        reverse_map = {idx: column for idx, column in enumerate(target_df.columns)}
        return label_map, reverse_map

    def dummy_column(self, df, col):
        """
        Returns a DataFrame with dummies in place of a columns of labels
        :param df: feature dataframe
        :param col: the column wish to be made into dummies
        :return: pandas dataframe
        """
        df = df.copy()
        df_dummies = pd.get_dummies(df[col], prefix=col)
        df = pd.concat([ df, df_dummies], axis=1)
        del df[col]
        return df

    def map_ordinal_vals(self, df, col, data_map):
        s = pd.Series(df[col], dtype="category")
        s = s.cat.rename_categories(data_map)
        df[col] = s
        return df

    def group_floats(self, df, n_percentiles):
        df = df.copy()
        float_df = df.select_dtypes('float64')
        column_names = float_df.columns
        vals = float_df.values.shape
        n_rows, n_cols = vals
        # remove outliers
        for i in range(n_cols):
            mean = np.mean(vals[:, i])
            std = np.std(vals[:, i])
            upper_limit = mean + 3 * std
            lower_limit = mean - 3 * std
            for j in range(n_rows):
                if vals[j, i] > upper_limit:
                    vals[j, i] = upper_limit
                elif vals[j, i] < lower_limit:
                    vals[j, i] = lower_limit

            cats = pd.qcut(pd.Series(vals[:, i]).rank(method='first'), n_percentiles, labels=False)

            df[column_names[i]] = cats.values

        return df


    def make_heatmap(self, y_test, y_pred, accuracy, model_name):
        sns.set(style="darkgrid", color_codes=True)
        sns.heatmap(confusion_matrix(y_test, y_pred),
                    annot=True,
                    cmap=sns.cubehelix_palette(start=2.8,
                                               rot=.1,
                                               light=1,
                                               dark=.2,
                                               hue=1,
                                               as_cmap=True))
        plt.title('{} Acc: {:.6f}'.format(model_name, accuracy))
        plt.xlabel('True Class')
        plt.ylabel('Predicted Class')
        plt.gca().invert_yaxis()
        plt.show()
        plt.close()

    def iterate_minibatches(self, feature_set, target_set, batch_size, shuffle=True):
        len_feature_set = len(feature_set)
        len_target_set = len(target_set)
        assert (len_feature_set == len_target_set)

        if len_feature_set % batch_size == 0:
            n_batches = len_feature_set // batch_size
        else:
            n_batches = len_feature_set // batch_size + 1

        if shuffle:
            indices = np.arange(len_feature_set)
            np.random.shuffle(indices)
            feature_set = feature_set[indices]
        idxs = [i * batch_size for i in range(n_batches)]
        for idx in idxs:
            yield feature_set[idx:idx + batch_size], target_set[idx:idx + batch_size]

    def get_labels(self, target_df):
        """
        if the targets are given as a one hot vector, this function returns the label as int
        :param target_df: rows of one hot vectors
        :return: representative numpy array of integer labels for the classes
        """
        target_df = target_df.copy()
        zero_action_label = len(target_df.columns)
        labels = np.zeros(len(target_df))

        for idx, row in target_df.iterrows():
            try:
                index = np.where(row.values == 1)[0][0]
                labels[idx] = index
            except:
                labels[idx] = zero_action_label
        return labels.astype('int')


    def balance_classes(self, df, class_imbalances, target_column_name):
        """
        df: (dataframe) of data
        class_imbalances: (list) lidt of classe imbalances from 0 class idx to largest class idx
            i.e. not in order of imbalances
        target_column_name: (str) the column name to be balancing
        """
        for i in range(len(class_imbalances)):
            minority_df = df[df[target_column_name] == i]
            upsampled_data = resample(minority_df, replace=True, n_samples=class_imbalances[i], random_state=123)
            df = pd.concat([df, upsampled_data])
        return df


    def get_class_imbalances(self, data, target_column):
        class_imbalance_counts = data.groupby(target_column).size()
        class_count_max = class_imbalance_counts.max()
        class_imbalances = [class_count_max-class_imbalance_counts[i] for i in range(len(class_imbalance_counts))]
        return class_imbalances


    def default_rf(self, x_train, x_test, y_train, y_test):
        clf = RandomForestClassifier()
        clf.fit(x_train, y_train)
        y_pred = clf.predict(x_test)
        accuracy = round(accuracy_score(y_test, y_pred), 4)
        self.make_heatmap(y_test, y_pred, accuracy, 'Random Forest Default')
        sorted_features = sorted([(i, clf.feature_importances_[i]) for i in range(len(clf.feature_importances_))], key=lambda x:x[1], reverse=True)
        print(sorted_features)
        n_top = len(sorted_features)
        top_cols = [x_test.columns[sorted_features[i][0]] for i in range(n_top)]
        print('Top {} columns: {}'.format(n_top, top_cols))
        return clf, accuracy


    def get_probs(self, model, x_test):
        try:
            y_prob = model.predict_proba(x_test)
            print(y_prob)
        except:
            print("Not probabilistic: returning zeros")
        return y_prob


    def get_predictions(self, model, x_test):
        y_pred = model.predict(x_test)
        y_probs = self.get_probs(model, x_test)
        return y_pred, y_probs


    def load_model(self, classifier, params):
        classifier.set_params(**params)
        return classifier


    def load_model_from_file(self, file_path):
        model = joblib.load(file_path)
        return model

    def load_config(self, config_path):
        with open(config_path) as f:
            config = json.load(f)
        return config

    def encode_auth_token(self, user_id, secret):
        """
        Generates the Auth Token
        :return: string
        Do: set/get secret from env variables or Flask app configs
        """
        try:
            payload = {
                'exp': dt.utcnow() + td(days=10),
                'iat': dt.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                secret,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def decode_auth_token(self, auth_token, secret):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, secret)
            print('payload', payload)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def create_Secret(self, n_chars):
        byte_str = os.urandom(n_chars)
        return b64encode(byte_str).decode('utf-8')


    def get_best_params(self, all_data_split, param_spaces, problem_type, n_iter=10, score_metric='accuracy', search_cv=5):
        """
        Parameters:
            all_data_split : tuple of train-test split tuple for data set,
            repack if scaling needs to be done separately. Needs to be packed
            the same way that sklearn's train_test_split packs them.

            param_spaces : dict that has the form {model_object: parameter_dictionary}
                parameter_dictionary : the parameters wished to be searched
                    need to be iterable distributions from scipy.stats
            problem_type : str classification or regression
            score_metric : str the score metric that is wanted to train the data on

            search_cv : int the number of folds for the grid search

        Returns:
            best_params : dict formatted below with all models input
                {model_name:
                    {best_params: best_params_vals,
                     model : model_object,
                     best_model_test_predictions : best_model_test_predictions_vals,
                     xoos_predictions : xoos_predictions_vals,
                     accuracy : accuracy_val,
                     f1_weighted : f1_weighted_val,
                     f1 : f1_val
                            }
                }

        """
        assert(problem_type in ['classification', 'regression'])
        # x_train, x_val, x_test, y_train, y_val, y_test = all_data_split
        x_train, x_test, y_train, y_test = all_data_split

        df_list = []
        best_params = {}
        for key, val in param_spaces.items():
            start = time.time()
            model_name = type(val['model']).__name__
            print('{}:'.format(model_name))
            search = RandomizedSearchCV(val['model'], val['parameter_distributions'],
                                        scoring=score_metric,
                                        n_jobs=-1,
                                        cv=search_cv,
                                        n_iter=n_iter,
                                        verbose=1,
                                        error_score='raise',
                                        random_state=0)
            search.fit(x_train, y_train)
            best_params[model_name] = {}
            best_params[model_name]['best_params'] = json.dumps(search.best_params_)
            y_pred = search.best_estimator_.predict(x_test)
            y_pred_str = ','.join(map(str, list(y_pred)))
            best_params[model_name]['best_model_test_predictions'] = y_pred_str

            y_pred = y_pred.flatten()
            best_score = search.best_score_
            best_params[model_name]['best_score'] = best_score
            print('Done with parameter search. Model best_score: {:.4}'.format(best_score))
            if problem_type == 'classfication':
                accuracy = accuracy_score(y_test, y_pred)
                best_params[model_name]['accuracy'] = accuracy
    
                f1_weighted = f1_score(y_test, y_pred, average='weighted')
                best_params[model_name]['f1_weighted'] = f1_weighted
    
                f1 = f1_score(y_test, y_pred, average='micro')
                best_params[model_name]['f1_micro'] = f1

                self.make_heatmap(y_test, y_pred, accuracy, model_name)
            
            elif problem_type == 'regression':
                r2 = r2_score(y_test, y_pred)
                best_params[model_name]['r2_score'] = r2
    
                median_absolute_err = median_absolute_error(y_test, y_pred)
                best_params[model_name]['median_absolute_error'] = median_absolute_err
    
                mean_squared_err = mean_squared_error(y_test, y_pred)
                best_params[model_name]['mean_squared_error'] = mean_squared_err
                
                
            print('{} search took {:.4f} mins\n'.format(model_name, (time.time() - start) / 60))
            df = pd.DataFrame.from_dict(search.cv_results_)
            df['algorithm'] = [model_name] * n_iter

            for key in df.keys():
                if key[:6] == 'param_':
                    del df[key]

            df_list.append(df)

        search_results_df = pd.concat(df_list, ignore_index=True)
        best_params_df = pd.DataFrame.from_dict(best_params).T
        return best_params_df, search_results_df


    def stack_models(self, stacking_type, param_spaces, best_params_df, all_data_split, cv=5):
        assert(stacking_type in ['classification', 'regression'])
        x_train, x_test, y_train, y_test = all_data_split
        # build models with best params
        classifiers = [(k, v['model']) for k,v in param_spaces.items()]
        for item in classifiers:
            classifier = item[1]
            classifier_column = type(classifier).__name__
            params_string = best_params_df.loc[classifier_column, 'best_params']
            params = json.loads(params_string)
            
            classifier.set_params(**params)
        if stacking_type == 'classification':
            stacked_model = StackingClassifier(estimators=classifiers, cv=cv, verbose=1)
        else:
            stacked_model = StackingRegressor(estimators=classifiers, cv=cv, verbose=1)
        
        stacked_model.fit(x_train, y_train)
        stacked_score = stacked_model.score(x_test, y_test)
        print('stacked_score: ', stacked_score)
        return stacked_model, stacked_score, classifiers


    def select_features(self, tuned_model, x_train_df, importance_cutoff=.9):
        columns = x_train_df.columns
        feature_importances = tuned_model.feature_importances_
        importances = list(zip(columns, feature_importances))
        importances_sorted = sorted(importances, key=lambda x:x[1], reverse=True)
        pd.Series(feature_importances, index=columns).plot.bar(color='steelblue', figsize=(12, 6))
        importance_sum = 0
        trimmed_features = []
        for item in importances_sorted:
            importance_sum += item[1]
            trimmed_features.append(item[0])
            if importance_sum >= importance_cutoff:
                break
        return trimmed_features


    def stack_from_list(self, stacking_type, classifiers, all_data_split, cv=5):
        """
        Stack models from a list of preloaded classifiers.
        stacking_type: str - either 'classification' or 'regression'
        classifiers: list - a list of classifiers preloaded with optimal params after a grid/random search
        all_data_split: tuple -  x_train, x_test, y_train, y_test
        """
        assert(stacking_type in ['classification', 'regression'])
        x_train, x_test, y_train, y_test = all_data_split
        if stacking_type == 'classification':
            stacked_model = StackingClassifier(estimators=classifiers, cv=cv)
        else:
            stacked_model = StackingRegressor(estimators=classifiers, cv=cv)
        
        stacked_model.fit(x_train, y_train)
        stacked_accuracy = stacked_model.score(x_test, y_test)
        print('stacked_accuracy: ', stacked_accuracy)
        return stacked_model, stacked_accuracy
       
"""
    
hf = HelperFunctions()
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import (GradientBoostingClassifier, RandomForestClassifier)
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import scipy.stats as ss
from sklearn.preprocessing import StandardScaler
import pprint
pp = pprint.PrettyPrinter(indent=4)

total_data = load_breast_cancer()
feature_set = total_data.data
target_set = total_data.target
n_features = feature_set.shape[1]

# ############################################################################
# iterate_minibatches(self, feature_set, target_set, batch_size, shuffle=True)

# for batch in hf.iterate_minibatches(feature_set, target_set, 150, shuffle=True):
#     feature_batch = batch[0]
#     target_batch = batch[1]
#     print('features:', feature_batch.shape)
#     print('targets:', target_batch.shape)

# ############################################################################
# # examples
# # get_best_params(self, all_data_split, param_spaces, score_metric='accuracy', search_cv=10, xoos=True,xoos_cv=10)
# # split_data(self, train, target, test_val_percentage=.3)


test_val_percentage = 0.2
x_train, x_val, x_test, y_train, y_val, y_test = hf.split_data(feature_set,
                                                                target_set,
                                                                test_val_percentage=test_val_percentage,
                                                                validation_set=True)

param_spaces = {
    'rf' : {
        
        'model': RandomForestClassifier(),
        'parameter_distributions':
            {'n_estimators': ss.randint(50, 120),
              'max_features': ss.randint(int(n_features / 2), n_features),
              'min_samples_split': ss.randint(2, 15),
              'max_depth': [3, None],
              'min_samples_leaf': ss.randint(2, 10),
              'criterion': ['gini', 'entropy']
              }
    },
    'mlp' :{
    'model': MLPClassifier(),
    'parameter_distributions':
        {'hidden_layer_sizes': ([25, 50, 25], [40, 60, 40], [50, 50]),
          'activation': ['logistic', 'tanh', 'relu'],
          'alpha': ss.uniform(.001, .1),
          'learning_rate': ['invscaling', 'adaptive'],
          'learning_rate_init': ss.uniform(.0001, .01),
          'max_iter': [5000]
          }
    },
    'svc': {
    'model': SVC(),
    'parameter_distributions':
        {'C': ss.uniform(.1, 20),
          'kernel': ['rbf', 'poly', 'linear'],
          'gamma': ['scale']
          }
    },
    'gradient_boost': {
    'model': GradientBoostingClassifier(),
    'parameter_distributions':
        {'n_estimators': ss.randint(50, 120),
          'max_features': ss.randint(int(n_features / 2), n_features),
          'learning_rate': ss.uniform(.0001, 1),
          'max_depth': [3, None],
          'min_samples_split': ss.randint(2, 15),
          'min_samples_leaf': ss.randint(2, 10)
          }
    }
}

scaler_training = StandardScaler().fit(x_train)
x_train = scaler_training.transform(x_train)

scaler_val = StandardScaler().fit(x_val)
x_val = scaler_training.transform(x_val)

scaler_test = StandardScaler().fit(x_test)
x_test = scaler_test.transform(x_test)

all_data_split = (x_train, x_test, x_val, y_train, y_val, y_test)

best_params_df, search_results_df = hf.get_best_params(all_data_split, param_spaces)

stacked_model, stacked_accuracy, classifiers = hf.stack_models('classification', param_spaces, best_params_df, cv=5)

x_train_df = pd.DataFrame(x_train, columns=total_data.feature_names)
clf = classifiers[0][1].fit(x_train, y_train)
features = hf.select_features(clf, x_train_df)
print(features)
"""