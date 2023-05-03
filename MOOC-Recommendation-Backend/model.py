#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:59:32 2021

@author: tharuka
"""

import os
import argparse
import time
import logging
import re

import findspark

findspark.init()

# spark imports
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.mllib.recommendation import MatrixFactorizationModel
from pyspark.sql.utils import AnalysisException

from pyspark.sql.types import IntegerType
from pyspark.sql.types import FloatType

logging.basicConfig(filename='logs/recommender.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class AlsRecommender:
    """
    This a collaborative filtering recommender with
    Matrix Factorization, which is implemented by Spark
    """

    def __init__(self, model_dir, users_table, videos_table):

        self.spark = SparkSession.builder.appName("tuning and trainig for recommendation system") \
            .config("spark.driver.extraClassPath",
                    "C:\\Program Files (x86)\\MySQL\\Connector J 8.0\\mysql-connector-j-8.0.33.jar") \
            .getOrCreate()

        self.sc = self.spark.sparkContext
        self.sqlContext = SQLContext(self.sc)
        logging.info('Spark session creation successfull')

        self.model_dir = model_dir

        self.users = self.spark.read \
            .jdbc("jdbc:mysql://localhost:3306/video_recommendation", users_table,
                  properties={"user": "root", "password": "root", "driver": "com.mysql.cj.jdbc.Driver"})

        # self.users = self.sc.parallelize(self.dynamodb.Table(users_table).scan()['Items']).toDF()
        self.users = self.users.withColumn("id", self.users.id.cast(IntegerType()))

        """         
            try:
                for col in  self.items.columns:
                    match = re.search(r'(\S+)_id', col)
                    if match:
                        self.item_id_column = match.group(0)
                        print(self.item_id)
                        break
            except:
                print("id column not found") 
        """

        self.items = self.spark.read \
            .jdbc("jdbc:mysql://localhost:3306/video_recommendation", videos_table,
                  properties={"user": "root", "password": "root", "driver": "com.mysql.cj.jdbc.Driver"})
        self.items = self.items.withColumn("id", self.items.id.cast(IntegerType()))

        logging.info(self.users.show(5))
        logging.info(self.items.show(5))

    def _load_model(self):

        """
        Loading the latest models available at model_dir

        Return:
        -----------

        loaded_model: The loaded ALS models.

        """

        model_list = os.listdir(self.model_dir)

        loaded = False
        loaded_model = latest_model = None

        while not loaded:
            try:
                if len(model_list):
                    latest_model = max(model_list)
                    print(latest_model)
                    latest_model_path = os.path.join(self.model_dir, str(latest_model))
                    loaded_model = MatrixFactorizationModel.load(self.sc, str(latest_model_path))
                    logging.info("%s latest loaded models", latest_model)
                    loaded = True
                else:
                    break
            except AnalysisException as ex:
                model_list = model_list[0:-1]
                print(ex)
            except Exception as ex:
                model_list = model_list[0:-1]
                logging.exception(ex)
                print(ex)

        return loaded_model, latest_model

    def _get_user_index(self, user_id):
        """
        Return user index no associated with given user id.

        Parameters
        ----------

        user_id : str, user id or guest user id.

        """

        value = self.users.where(self.users.id == user_id).select('id').collect()[0]['id']
        return int(value)

    def _get_item(self, video_id):
        """

        """
        item = self.items.where(self.items.id == video_id).select('id').collect()[0][
            'id']
        return item

    def make_recommendations(self, loaded_model, user_id,
                             n_recommendations):

        """
        Return top n  recommendation based on user's input list of favorite items

        Parameters
        ----------
        best_model_params: dict, {'iterations': iter, 'rank': rank, 'lambda_': reg}

        user_id: int, user_id.

        n_recommendations: int, top n recommendations

        Return
        ------
        list of top n movie recommendations
        """

        # inference
        index = self._get_user_index(user_id)
        predictions = loaded_model.recommendProducts(index, n_recommendations)
        # get top n movieId
        recommendations = [item.product for item in predictions]

        for item in recommendations:
            print(self._get_item(item))

        return recommendations


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Movie Recommender",
        description="Run ALS Movie Recommender")
    parser.add_argument('--users_table', nargs='?', default='users',
                        help='table which contains all user ids')
    parser.add_argument('--items_table', nargs='?', default='videos',
                        help='table which contains all item ids')
    parser.add_argument('--top_n', type=int, default=9,
                        help='top n item recommendations'),
    parser.add_argument('--model_dir', nargs='?', default='./models',
                        help='directory path to load models')
    return parser.parse_args()


if __name__ == '__main__':
    start_time = time.time()
    args = parse_args()
    users_table = args.users_table
    items_table = args.items_table

    top_n = args.top_n
    model_dirpath = args.model_dir

    # initial recommender system
    recommender = AlsRecommender(model_dirpath, users_table, items_table)
    loaded_model = recommender._load_model()

    user_index = recommender._get_user_index(1)

    predictions = loaded_model.recommendProducts(user_index, top_n)

    # get top n itemId
    recommendations = [item.product for item in predictions]

    print("--- %s seconds ---" % (time.time() - start_time))
