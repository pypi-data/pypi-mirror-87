#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 10:31:42 2020

@author: charles.crawford
"""

import json
import pprint
from numpy import ndarray
from pandas import DataFrame, Series
from joblib import load, dump
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import (RandomizedSearchCV, GridSearchCV)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (OrdinalEncoder, 
                                   PowerTransformer, 
                                   OneHotEncoder,
                                   StandardScaler,
                                   RobustScaler)

from .helper_functions import HelperFunctions
from .outlier_transformer import OutlierTransformer


class DeploymentPipeline:
    def __init__(self, config, pipeline_path=None, classifier=None, data=None):
        """
        Base class for the DeploymentPipeline object
        
        Parameters
        ----------
        config : str or dict
            if str:
                The path to the configuration file: must be in valid JSON format.
            elif dict:
                the dictionary with required configs
            Necessary configuration attributes will be checked on start up.
        
        pipeline_path : str
            The path to load a pickled sklearn pipeline
        
        classifier : sklearn classifier object
            The object will be instatiated and used to fit the pipeline.
        
        Returns
        -------
        None.

        """
        self.config = self.load_config(config)
        self.classifier = classifier
        self.data = data
        self.pipeline_path = pipeline_path
        self.required_configs = ['predictor_columns', 'numeric_features', 
                                 'categorical_features', 'integer_features', 
                                 'boolean_features', 'binary_features', 
                                 'ordinal_features', 'target_column',  
                                 'no_transform_columns']
        
        self.pp = pprint.PrettyPrinter(indent=4, depth=3)
        self.preprocessor = self.construct_preprocessor()
        self.pipeline = self.construct_pipeline()
        self.hf = HelperFunctions()
        self.random_search = None
        self.grid_search = None
        self.check_configs()



    def construct_pipeline(self):
        if self.pipeline_path is not None:
            print('Loading pipeline from: {}'.format(self.pipeline_path))
            self.pipeline = load(self.pipeline_path)
        elif self.classifier is not None:
            print('Building pipeline from classifier: {}'.format(type(self.classifier).__name__))
            steps = [
                        ('preprocessor', self.preprocessor),
                        ('classifier', self.classifier)
                    ]
            pipeline = Pipeline(steps=steps)
            self.pipeline = pipeline
        else:
            print('Please enter a classifier to build a new pipeline or a pickled pipeline to load one.')
            self.pipeline = None
        return self.pipeline    

    def check_configs(self):
        columns_check = self.config['numeric_features'] + \
                self.config['categorical_features'] + \
                self.config['integer_features'] + \
                self.config['boolean_features'] + \
                self.config['ordinal_features'] + \
                self.config['binary_features'] + \
                self.config['no_transform_columns']
        
        if not sorted(columns_check) == sorted(self.config['predictor_columns']):
            print('columns not in predictor_columns:')
            print([item for item in columns_check if item not in self.config['predictor_columns']])
            print('columns not in columns_check:')
            print([item for item in self.config['predictor_columns'] if item not in columns_check])
            print('len columns_check: ', len(columns_check))
            print('len predictor_columns: ', len(self.config['predictor_columns']))
        else:
            print('Configurations are correct')
        
        subset = False
        if( set(self.required_configs).issubset( set( self.config.keys() ) ) ): 
            subset = True
        assert(subset)

    def load_config(self, config):
        if type(config) == str:
            with open(config) as f:
                config = json.load(f)
            return config
        elif type(config) == dict:
            return config
        else:
            print('Please enter a valid path for configs or a valid dict type config object.')

    def print_config(self):
        self.pp.pprint(self.config)
        
    def random_search_cv(self, params, x_train, y_train, score_metric):
        random_search = RandomizedSearchCV(self.pipeline, 
                                           params, 
                                           scoring=score_metric, 
                                           verbose=10, 
                                           error_score='raise')
        random_search.fit(x_train, y_train)
        self.random_search = random_search
        return self.random_search

    def grid_search_cv(self, params, x_train, y_train, score_metric):
        grid_search = GridSearchCV(self.pipeline, 
                                   params, 
                                   scoring=score_metric,                            
                                   verbose=10,
                                   error_score='raise')
        grid_search.fit(x_train, y_train)
        self.grid_search = grid_search
        return self.grid_search
    
    def set_best_model(self, search_type):
        try:
            if search_type == 'random':
                self.classifier(**self.random_search.best_params_)
            elif search_type == 'grid':
                self.classifier(**self.grid_search.best_params_)
            else:
                print('Please enter grid or random.')
                return None
        except:
            print('You need to perform a search first in order to use this function.')

    def construct_preprocessor(self):
        """
        This method creates a generic column transformer object for preprocessing.
        This method can be overwritten if need be for specific functionality.

        Returns
        -------
        preprocessor : ColumnTransformer
            This returns a column transformer object with the transforms and 
            imputators needed to get the data in machine readable format.

        """
        numeric_transform = self.config['numeric_transform']
        if numeric_transform == 'box-cox':
            numeric_transformer = Pipeline(steps=[
                            ('imputer', SimpleImputer(strategy='median')),
                            ('outlier_transformer', OutlierTransformer()),
                            ('numeric_scaler', PowerTransformer(method='box-cox'))
                    ])
        elif numeric_transform == 'yeo-johnson':
            numeric_transformer = Pipeline(steps=[
                            ('imputer', SimpleImputer(strategy='median')),
                            ('outlier_transformer', OutlierTransformer()),
                            ('numeric_scaler', PowerTransformer(method='yeo-johnson'))
                    ])
        elif numeric_transform == 'standard':
            numeric_transformer = Pipeline(steps=[
                            ('imputer', SimpleImputer(strategy='median')),
                            ('outlier_transformer', OutlierTransformer()),
                            ('numeric_scaler', StandardScaler())
                    ])
        elif numeric_transform == 'robust':
            numeric_transformer = Pipeline(steps=[
                            ('imputer', SimpleImputer(strategy='median')),
                            ('outlier_transformer', OutlierTransformer()),
                            ('numeric_scaler', RobustScaler())
                    ])
        else:
            print('The numeric_transform value is not one of: box-cox, yeo-johnson, robust, or standard')
            print('Applying the robust scaler')
            numeric_transformer = Pipeline(steps=[
                            ('imputer', SimpleImputer(strategy='median')),
                            ('outlier_transformer', OutlierTransformer()),
                            ('numeric_scaler', RobustScaler())
                    ])

            
        categorical_transformer = Pipeline(steps=[
                        ('imputer', SimpleImputer(strategy='most_frequent')),
                        ('categorical_encoder', OneHotEncoder())
                ])
        
        ordinal_transformer = Pipeline(steps=[
                        ('imputer', SimpleImputer(strategy='most_frequent')),
                        ('ordinal_encoder', OrdinalEncoder())
                ])
        
        binary_transformer = Pipeline(steps=[
                        ('imputer', SimpleImputer(strategy='most_frequent')),
                        ('binary_encoder', OrdinalEncoder())
                ])
        
        boolean_transformer = Pipeline(steps=[
                        ('boolean_encoder', OneHotEncoder()),
                        ('imputer', SimpleImputer(strategy='most_frequent'))
                        
                ])
                
        integer_transformer = Pipeline(steps=[
                        ('imputer', SimpleImputer(strategy='median'))
                ])
        
        no_transform = Pipeline(steps=[
                        ('imputer', SimpleImputer(strategy='median'))
                ])
                
        transformers = [
                            ('num', numeric_transformer, self.config['numeric_features']),
                            ('cat', categorical_transformer, self.config['categorical_features']),
                            ('bool', boolean_transformer, self.config['boolean_features']),
                            ('integer', integer_transformer, self.config['integer_features']),
                            ('ordinal', ordinal_transformer, self.config['ordinal_features']),
                            ('binary', binary_transformer, self.config['binary_features']),
                            ('no_transform', no_transform, self.config['no_transform_columns'])
                        ]

        preprocessor = ColumnTransformer(transformers=transformers)
        return preprocessor

    def save_model(self, file_path):
        dump(self.pipeline, file_path)

    def process_target(self, target_data, robust_transformer=True):
        target_data_type = type(target_data)
        if target_data_type == DataFrame or target_data_type == Series:
            if len(target_data.values.shape) == 1:
                print('Reshaping target')
                target_data = target_data.values.reshape(-1, 1)
        elif target_data_type == ndarray:
            if len(target_data.shape) == 1:
                print('Reshaping target')
                target_data = target_data.reshape(-1, 1)
        else:
            print('Invalid target type')
            
        transformers = ['box-cox', 'yeo-johnson', 'standard', 'one_hot',
                        'ordinal', 'binary', 'impute', 'robust']

        transform_type = self.config['target_column_transformer']

        if transform_type == 'box-cox':
            steps = [
                            ('imputer', SimpleImputer(strategy='median')),
                            ('transformer', PowerTransformer(method='box-cox'))
                    ]
        elif transform_type == 'yeo-johnson':
            steps = [
                            ('imputer', SimpleImputer(strategy='median')),
                            ('transformer', PowerTransformer(method='yeo-johnson'))
                    ]
        elif transform_type == 'standard':
            steps = [
                            ('imputer', SimpleImputer(strategy='median')),
                            ('transformer', StandardScaler())
                    ]
       
        elif transform_type == 'one_hot':
            steps = [
                            ('imputer', SimpleImputer(strategy='most_frequent')),
                            ('transformer', OneHotEncoder())
                    ]
        
        elif transform_type == 'ordinal':
            steps = [
                            ('imputer', SimpleImputer(strategy='most_frequent')),
                            ('transformer', OrdinalEncoder())
                    ]
        elif transform_type == 'binary':
            steps = [
                            ('imputer', SimpleImputer(strategy='most_frequent')),
                            ('transformer', OrdinalEncoder())
                    ]
                    
        elif transform_type == 'impute':        
            steps = [
                            ('transformer', SimpleImputer(strategy='median'))
                    ]

        elif transform_type == 'robust':
            steps = [
                            ('imputer', SimpleImputer(strategy='most_frequent')),
                            ('transformer', RobustScaler())
                    ]
        else:
            print('Please enter one of the following: {}'.format(', '.join(transformers)))
            print('Applying the standard scaler for this run.')
            steps = [
                            ('imputer', SimpleImputer(strategy='median')),
                            ('transformer', StandardScaler())
                    ]

        transformer = Pipeline(steps=steps)
        transformer.fit(target_data)
        transformed_data = transformer.transform(target_data).flatten()
        return transformed_data, transformer
